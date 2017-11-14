from __future__ import unicode_literals
from applications.workflow import Flow
from .models import Location, Record, PublicationNewspaper, PublicationWebsite, PublicationFeedback,Referral,Application, Delegate, Compliance
from django.utils.safestring import SafeText
from django.contrib.auth.models import Group
from applications.validationchecks import Attachment_Extension_Check
from ledger.accounts.models import EmailUser, Address, Organisation, Document
from django.db.models import Q
from approvals.models import Approval

class Application_Part5():

    def get(self,app,self_view,context):
        request = self_view.request

        if app.routeid is None:
            app.routeid = 1

        flow = Flow()
        workflowtype = flow.getWorkFlowTypeFromApp(app)
        flow.get(workflowtype)
        context = flow.getAccessRights(request,context,app.routeid,workflowtype)
        context = flow.getCollapse(context,app.routeid,workflowtype)
        context = flow.getHiddenAreas(context,app.routeid,workflowtype)
        context['workflow'] = flow.getAllRouteConf(workflowtype,app.routeid)
        context['workflow_actions'] = flow.getAllRouteActions(app.routeid,workflowtype)
        context['formcomponent'] = flow.getFormComponent(app.routeid,workflowtype)
        context['workflowoptions'] = flow.getWorkflowOptions()

        try:
              LocObj = Location.objects.get(application_id=self_view.object.id)
              context['certificate_of_title_volume'] = LocObj.title_volume
              context['folio'] = LocObj.folio
              context['diagram_plan_deposit_number'] = LocObj.dpd_number
              context['location'] = LocObj.location
              context['reserve_number'] = LocObj.reserve
              context['street_number_and_name'] = LocObj.street_number_name
              context['town_suburb'] = LocObj.suburb
              context['lot'] = LocObj.lot
              context['nearest_road_intersection'] = LocObj.intersection
        except:
              donothing = ''

        context['publication_newspaper'] = PublicationNewspaper.objects.filter(application_id=self_view.object)
        context['publication_website'] = PublicationWebsite.objects.filter(application_id=self_view.object)
        if self_view.object.river_lease_scan_of_application:
            context['river_lease_scan_of_application_short'] = SafeText(self_view.object.river_lease_scan_of_application.upload.name)[19:]

        if self_view.object.document_draft:
            context['document_draft_short'] = SafeText(self_view.object.document_draft.upload.name)[19:]
        if self_view.object.document_final:
            context['document_final_short'] = SafeText(self_view.object.document_final.upload.name)[19:]
        if self_view.object.deed:
            context['deed_short'] = SafeText(self_view.object.deed.upload.name)[19:]


        context['land_owner_consent_list'] = []
        landoc = app.land_owner_consent.all()
        for doc in landoc:
            fileitem = {}
            fileitem['fileid'] = doc.id
            fileitem['path'] = doc.upload.name
            fileitem['path_short'] = SafeText(doc.upload.name)[19:]
            context['land_owner_consent_list'].append(fileitem)


        context['publication_newspaper_list'] = []
        pub_news_obj = []
        pub_news_mod  = PublicationNewspaper.objects.filter(application_id=self_view.object)
        for pubrow in pub_news_mod:
            rowitem = {}
            rowitem['pk'] = pubrow.pk
            rowitem['id'] = pubrow.id
            rowitem['date'] = pubrow.date
            rowitem['newspaper'] = pubrow.newspaper
            rowitem['application'] = pubrow.application
            rowitem['records'] = pubrow.records
            rowitem['documents_short'] = []
            records = pubrow.records.all()
            for doc in records:
                fileitem = {}
                fileitem['fileid'] = doc.id
                fileitem['path'] = doc.upload
                fileitem['path_short'] = SafeText(doc.upload.name)[19:]
                rowitem['documents_short'].append(fileitem)
            context['publication_newspaper_list'].append(rowitem)


        pub_feed_obj = []
        pub_feed_mod = PublicationFeedback.objects.filter(application_id=self_view.object)
        for pubrow in pub_feed_mod:
            rowitem = {}
            rowitem['id'] = pubrow.id
            rowitem['name'] = pubrow.name
            rowitem['address'] = pubrow.address
            rowitem['suburb'] = pubrow.suburb
            rowitem['state'] = pubrow.state
            rowitem['postcode'] = pubrow.postcode
            rowitem['phone'] = pubrow.phone
            rowitem['email'] = pubrow.email
            rowitem['comments'] = pubrow.comments
            rowitem['records'] = pubrow.records
            rowitem['documents_short'] = [] # needed so we can add documents to list
            rowitem['status'] = pubrow.status
            rowitem['application'] = pubrow.application
            records = pubrow.records.all()
            for doc in records:
                fileitem = {}
                fileitem['fileid'] = doc.id
                fileitem['path'] = doc.upload
                fileitem['path_short'] = SafeText(doc.upload.name)[19:]
                rowitem['documents_short'].append(fileitem)
            pub_feed_obj.append(rowitem)

        context['publication_feedback'] = pub_feed_obj

        new_documents_to_publish = {}
        pub_web = PublicationWebsite.objects.filter(application_id=self_view.object.id)
        for pub_doc in pub_web:
            if pub_doc.published_document_id:
                doc = Record.objects.get(id=pub_doc.published_document_id)
                fileitem = {}
                fileitem['fileid'] = doc.id
                fileitem['path'] = doc.upload.name
                new_documents_to_publish[pub_doc.original_document_id] = fileitem

        orignaldoclist = []
        if self_view.object.river_lease_scan_of_application:
            fileitem = {}
            fileitem['fileid'] = self_view.object.river_lease_scan_of_application.id
            fileitem['path'] = self_view.object.river_lease_scan_of_application.upload.name
            fileitem['path_short'] = SafeText(self_view.object.river_lease_scan_of_application.upload.name)[19:]
            fileitem['group_name'] = "River Lease Scan of Application"
            if self_view.object.river_lease_scan_of_application.id in new_documents_to_publish:
                fileitem['publish_doc'] = new_documents_to_publish[self_view.object.river_lease_scan_of_application.id]['path']
                fileitem['publish_doc_short'] = SafeText(new_documents_to_publish[self_view.object.river_lease_scan_of_application.id]['path'])[19:]
            orignaldoclist.append(fileitem)

        if self_view.object.deed:
             fileitem = {}
             fileitem['fileid'] = self_view.object.deed.id
             fileitem['path'] = self_view.object.deed.upload.name
             fileitem['path_short'] = SafeText(self_view.object.deed.upload.name)[19:]
             fileitem['group_name'] = "Deed"
             if self_view.object.deed.id in new_documents_to_publish:
                 fileitem['publish_doc'] = new_documents_to_publish[self_view.object.deed.id]['path']
                 fileitem['publish_doc_short'] = SafeText(new_documents_to_publish[self_view.object.deed.id]['path'])[19:]
             orignaldoclist.append(fileitem)

        landoc = app.land_owner_consent.all()
        for doc in landoc:
            fileitem = {}
            fileitem['fileid'] = doc.id
            fileitem['path'] = doc.upload.name
            fileitem['path_short'] = SafeText(doc.upload.name)[19:]
            fileitem['group_name'] = "Land Owner Consent"
            if doc.id in new_documents_to_publish:
                fileitem['publish_doc'] = new_documents_to_publish[doc.id]['path']
                fileitem['publish_doc_short'] = SafeText(new_documents_to_publish[doc.id]['path'])[19:]
            else:
                fileitem['publish_doc'] = ""
                fileitem['publish_doc_short'] = ""

            orignaldoclist.append(fileitem)

        doclist = app.proposed_development_plans.all()
        for doc in doclist:
            fileitem = {}
            fileitem['fileid'] = doc.id
            fileitem['path'] = doc.upload.name
            fileitem['path_short'] = SafeText(doc.upload.name)[19:]
            fileitem['group_name'] = "Proposed Development Plans"

            if doc.id in new_documents_to_publish:
                fileitem['publish_doc'] = new_documents_to_publish[doc.id]['path']
                fileitem['publish_doc_short'] = SafeText(new_documents_to_publish[doc.id]['path'])[19:]
            else:
                fileitem['publish_doc'] = ""
                fileitem['publish_doc_short'] = ""
            orignaldoclist.append(fileitem)
        context['original_document_list'] = orignaldoclist

        doclist = app.proposed_development_plans.all()
        context['proposed_development_plans_list'] = []
        for doc in doclist:
            fileitem = {}
            fileitem['fileid'] = doc.id
            fileitem['path'] = doc.upload.name
            fileitem['path_short'] = SafeText(doc.upload.name)[19:]
            context['proposed_development_plans_list'].append(fileitem)

        return context


class Application_Emergency():

    def get(self,app,self_view,context):
        request = self_view.request
        workflowtype = "emergency"

        if app.routeid is None:
            app.routeid = 1

        flow = Flow()
        flow.get(workflowtype)
        context = flow.getAccessRights(request,context,app.routeid,workflowtype)
        context = flow.getCollapse(context,app.routeid,workflowtype)
        context = flow.getHiddenAreas(context,app.routeid,workflowtype)
        context['workflow_actions'] = flow.getAllRouteActions(app.routeid,workflowtype)
        context['formcomponent'] = flow.getFormComponent(app.routeid,workflowtype)
        context['workflowoptions'] = flow.getWorkflowOptions()

        if app.organisation:
           context['address'] = app.organisation.postal_address
        elif app.applicant:
           context['address'] = app.applicant.postal_address

        return context

class Application_Permit():
    def get(self,app,self_view,context):
        request = self_view.request
        workflowtype = "permit"

        if app.routeid is None:
            app.routeid = 1

        flow = Flow()
        flow.get(workflowtype)
        context = flow.getAccessRights(request,context,app.routeid,workflowtype)
        context = flow.getCollapse(context,app.routeid,workflowtype)
        context = flow.getHiddenAreas(context,app.routeid,workflowtype)
        context['workflow_actions'] = flow.getAllRouteActions(app.routeid,workflowtype)
        context['formcomponent'] = flow.getFormComponent(app.routeid,workflowtype)
        context['workflowoptions'] = flow.getWorkflowOptions()

        return context

class Application_Licence():
    def get(self,app,self_view,context):
        request = self_view.request
        workflowtype = "licence"

        if app.routeid is None:
            app.routeid = 1

        flow = Flow()
        flow.get(workflowtype)
        context = flow.getAccessRights(request,context,app.routeid,workflowtype)
        context = flow.getCollapse(context,app.routeid,workflowtype)
        context = flow.getHiddenAreas(context,app.routeid,workflowtype)
        context['workflow_actions'] = flow.getAllRouteActions(app.routeid,workflowtype)
        context['formcomponent'] = flow.getFormComponent(app.routeid,workflowtype)
        context['workflowoptions'] = flow.getWorkflowOptions()

        return context


class Referrals_Next_Action_Check():

    def get(self,app):
        app_refs = Referral.objects.filter(application=app)
#       print app_refs
        referralscompleted = True
        for ref in app_refs:
            if ref.status == Referral.REFERRAL_STATUS_CHOICES.referred:
                referralscompleted = False

        return referralscompleted

    def go_next_action(self,app):
        app = Application.objects.get(id=app.id)
        app.status = ''
        flow = Flow()
        workflowtype = flow.getWorkFlowTypeFromApp(app)
        DefaultGroups = flow.groupList()
        flow.get(workflowtype)
        assignee = None
        routes = flow.getAllRouteActions(app.routeid,workflowtype)
        action = routes[0]['routegroup']
        if action in DefaultGroups['grouplink']:
            groupassignment = Group.objects.get(name=DefaultGroups['grouplink'][action])
        else:
            groupassignment = None
        route = flow.getNextRouteObj(action,app.routeid,workflowtype)

        if "route"in route:
            app.routeid = route["route"]
        else:
            app.routeid = None

        if "state" in route:
            app.state = route["state"]
        else:
            app.state = 0 

        app.group = groupassignment
        app.assignee = assignee
        app.save()



class FormsList():

    def get_application(self,self_view,userid,context):

        user = EmailUser.objects.get(id=userid)
        delegate = Delegate.objects.filter(email_user=user).values('organisation__id')

        context['nav_other_applications'] = "active"
        context['app'] = ''

        APP_TYPE_CHOICES = []
        APP_TYPE_CHOICES_IDS = []
        for i in Application.APP_TYPE_CHOICES:
            if i[0] in [4,5,6,7,8,9,10,11]:
                skip = 'yes'
            else:
                APP_TYPE_CHOICES.append(i)
                APP_TYPE_CHOICES_IDS.append(i[0])
        context['app_apptypes'] = APP_TYPE_CHOICES

        context['app_appstatus'] = list(Application.APP_STATE_CHOICES)
        search_filter = Q(applicant=userid) | Q(organisation__in=delegate)
        if 'searchaction' in self_view.request.GET and self_view.request.GET['searchaction']:
            query_str = self_view.request.GET['q']
            if self_view.request.GET['apptype'] != '':
                search_filter &= Q(app_type=int(self_view.request.GET['apptype']))
            else:
                end = ''


            if self_view.request.GET['appstatus'] != '':
                search_filter &= Q(state=int(self_view.request.GET['appstatus']))

            context['query_string'] = self_view.request.GET['q']

            if self_view.request.GET['apptype'] != '':
                context['apptype'] = int(self_view.request.GET['apptype'])
            if 'appstatus' in self_view.request.GET:
                if self_view.request.GET['appstatus'] != '':
                    context['appstatus'] = int(self_view.request.GET['appstatus'])

            if 'q' in self_view.request.GET and self_view.request.GET['q']:
                query_str = self_view.request.GET['q']
                query_str_split = query_str.split()
                for se_wo in query_str_split:
                    search_filter &= Q(Q(pk__icontains=se_wo) | Q(title__icontains=se_wo))

#        applications = Application.objects.filter(Q(app_type__in=APP_TYPE_CHOICES_IDS) & Q(search_filter) ).exclude(state=17)[:200]
        applications = Application.objects.filter(Q(search_filter) ).exclude(state=17)[:200]
        usergroups = self_view.request.user.groups.all()
        context['app_list'] = []

        for app in applications:
             row = {}
             row['may_assign_to_person'] = 'False'
             row['app'] = app

             if app.group is not None:
                 if app.group in usergroups:
                     row['may_assign_to_person'] = 'True'
             context['app_list'].append(row)

        return context

    def get_approvals(self,self_view,userid,context):

        user = EmailUser.objects.get(id=userid)
        delegate = Delegate.objects.filter(email_user=user).values('id')

        search_filter = Q(applicant=userid, status=1 ) | Q(organisation__in=delegate)

        APP_TYPE_CHOICES = []
        APP_TYPE_CHOICES_IDS = []
        for i in Application.APP_TYPE_CHOICES:
            if i[0] in [4,5,6,7,8,9,10,11]:
                skip = 'yes'
            else:
                APP_TYPE_CHOICES.append(i)
                APP_TYPE_CHOICES_IDS.append(i[0])
        context['app_apptypes']= APP_TYPE_CHOICES


        if 'action' in self_view.request.GET and self_view.request.GET['action']:

            if self_view.request.GET['apptype'] != '':
                search_filter &= Q(app_type=int(self_view.request.GET['apptype']))
            else:
                search_filter &= Q(app_type__in=APP_TYPE_CHOICES_IDS)

            if self_view.request.GET['appstatus'] != '':
                search_filter &= Q(status=int(self_view.request.GET['appstatus']))

            context['query_string'] = self_view.request.GET['q']

            if self_view.request.GET['apptype'] != '':
                context['apptype'] = int(self_view.request.GET['apptype'])
            if 'appstatus' in self_view.request.GET:
                if self_view.request.GET['appstatus'] != '':
                    context['appstatus'] = int(self_view.request.GET['appstatus'])

                if 'q' in self_view.request.GET and self_view.request.GET['q']:
                    query_str = self_view.request.GET['q']
                    query_str_split = query_str.split()
                    for se_wo in query_str_split:
                        search_filter= Q(pk__contains=se_wo) | Q(title__contains=se_wo)
        approval = Approval.objects.filter(search_filter)[:200]

        context['app_list'] = []
        context['app_applicants'] = {}
        context['app_applicants_list'] = []
        context['app_appstatus'] = list(Approval.APPROVAL_STATE_CHOICES)

        for app in approval:
            row = {}
            row['app'] = app
            if app.applicant:
                if app.applicant.id in context['app_applicants']:
                    donothing = ''
                else:
                    context['app_applicants'][app.applicant.id] = app.applicant.first_name + ' ' + app.applicant.last_name
                    context['app_applicants_list'].append({"id": app.applicant.id, "name": app.applicant.first_name + ' ' + app.applicant.last_name})

            context['app_list'].append(row)

        return context

    def get_clearance(self,self_view,userid,context):
        context['nav_other_clearance'] = "active"
        if 'q' in self_view.request.GET and self_view.request.GET['q']:
            context['query_string'] = self_view.request.GET['q']

        user = EmailUser.objects.get(id=userid)
        delegate = Delegate.objects.filter(email_user=user).values('id')
        search_filter = Q(applicant=userid) | Q(organisation__in=delegate)

        items = Compliance.objects.filter(applicant=userid).order_by('due_date')

        context['app_applicants'] = {}
        context['app_applicants_list'] = []
        context['app_apptypes'] = list(Application.APP_TYPE_CHOICES)

        APP_STATUS_CHOICES = []
        for i in Application.APP_STATE_CHOICES:
           if i[0] in [1,11,16]:
              APP_STATUS_CHOICES.append(i)

        context['app_appstatus'] = list(APP_STATUS_CHOICES)
        context['compliance'] = items

        return context



