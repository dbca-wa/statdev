from __future__ import unicode_literals
from datetime import timedelta
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from model_utils import Choices
from django.contrib.auth.models import Group
#from approvals.models import Approval
from ledger.accounts.models import Organisation
#from ledger.payments.models import Invoice


@python_2_unicode_compatible
class Record(models.Model):
    """This model represents a record that needs to be saved for
    future reference. It also records metadata and optional text content to be
    indexed for search.
    """
    DOC_CATEGORY_CHOICES = Choices(
        (1, 'consent', ('Landowner consent')),
        (2, 'deed', ('Deed')),
        (3, 'assessment', ('Assessment report')),
        (4, 'referee_response', ('Referee response')),
        (5, 'lodgement', ('Lodgement document')),
        (6, 'draft', ('Draft document')),
        (7, 'final', ('Final document')),
        (8, 'determination', ('Determination document')),
        (9, 'completion', ('Completed document')),
    )

    upload = models.FileField(max_length=512, upload_to='uploads/%Y/%m/%d')
    name = models.CharField(max_length=256)
    category = models.IntegerField(choices=DOC_CATEGORY_CHOICES, null=True, blank=True)
    metadata = JSONField(null=True, blank=True)
    text_content = models.TextField(null=True, blank=True, editable=False)  # Text for indexing

    def __str__(self):
        if self.category:
            return '{} ({})'.format(self.name, self.get_category_display())
        return self.name


@python_2_unicode_compatible
class Vessel(models.Model):
    """This model represents a vessel/craft that will be used
    in relation to the application
    """
    VESSEL_TYPE_CHOICES = Choices(
        (0, 'vessel', ('Vessel')),
        (1, 'craft', ('Craft')),
    )

    vessel_type = models.SmallIntegerField(choices=VESSEL_TYPE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=256)
    vessel_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Vessel identification')
    registration = models.ManyToManyField(Record, blank=True)
    size = models.PositiveIntegerField(null=True, blank=True, verbose_name='size (m)')
    engine = models.PositiveIntegerField(null=True, blank=True, verbose_name='engine (kW)')
    passenger_capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ApplicationPurpose(models.Model):
    purpose = models.CharField(max_length=256)

    def __str__(self):
        return self.purpose


class Craft(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Application(models.Model):
    """This model represents an application by a customer to P&W for a single
    permit, licence/permit, part 5, etc.
    """

    APP_TYPE_CHOICES = Choices(
        (1, 'permit', ('Permit')),
        (2, 'licence', ('Licence/permit')),
        (3, 'part5', ('Part 5')),
        (4, 'emergency', ('Emergency works')),
        (5, 'part5cr', ('Part 5 - Amendment Request')),
        (6, 'part5amend', ('Part 5 - Amendment Application')),
        (7, 'test', ('Test - Application')),
        (8, 'permitamend', ('Amend Permit')),
        (9, 'licenceamend', ('Amend Licence')),
        (10, 'permitrenew', ('Renew Permit')),
        (11, 'licencerenew', ('Renew Licence'))
    )

    APP_APPLY_ON = Choices(
         (1,'yourself', ('On Behalf of yourself')),
         (2,'yourcompany', ('On Behalf of your company')),
         (3, 'somebody_else_individual', ('On Behalf of indivdual as somebody else (as an authorised agent)')),
         (4, 'somebody_else_company', ('On Behalf of a company as somebody else (as an authorised agent)')),
         (5, 'internal', ('Internal'))
    )

    APP_STATE_CHOICES = Choices(
        (0, 'unknown',('Unknown')),
        (1, 'draft', ('Draft')),
        (2, 'with_admin', ('With Admin Officer')),
        (3, 'with_referee', ('With Referrals')),
        (4, 'with_assessor', ('With Assessor')),
        (5, 'with_manager', ('With Manager')),
        (6, 'issued', ('Issued')),
        (7, 'issued_with_admin', ('Issued (with admin)')),
        (8, 'declined', ('Declined')),
        (9, 'new', ('New')),
        (10, 'approved', ('Approved')),
        (11, 'expired', ('Expired')),
        (12, 'with_director', ('With Director')),
        (13, 'with_exec', ('With Executive')),
        (14, 'completed', ('Completed')),
        (15, 'creator', ('Form Creator')),
        (16, 'current', ('Current'))
    )

    APP_LOCATION_CHOICES = Choices(
        (0, 'onland', ('On Land')),
        (1, 'onwater', ('On Water')),
        (2, 'both', ('Both')),
    )

    APP_YESNO = Choices(
        (True, ('Yes')),
        (False, ('No'))
    )

    APP_VESSEL_CRAFT = Choices(
        (1, 'vessel', ('Vessel(s)')),
        (2, 'craft', ('Craft(s)')),
        (0, 'none', ('None'))
    )

    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT, related_name='applicant')
    organisation = models.ForeignKey(Organisation, blank=True, null=True, on_delete=models.PROTECT)
    app_type = models.IntegerField(choices=APP_TYPE_CHOICES, blank=True, null=True)
    apply_on_behalf_of = models.IntegerField(choices=APP_APPLY_ON, blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT, related_name='assignee')
    state = models.IntegerField(choices=APP_STATE_CHOICES, default=APP_STATE_CHOICES.draft, editable=False)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    submit_date = models.DateField()
    expire_date = models.DateField(blank=True, null=True)
    proposed_commence = models.DateField(null=True, blank=True)
    proposed_end = models.DateField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    cost = models.CharField(max_length=256, null=True, blank=True)
    project_no = models.CharField(max_length=256, null=True, blank=True)
    related_permits = models.TextField(null=True, blank=True)
    over_water = models.BooleanField(default=False)
    records = models.ManyToManyField(Record, blank=True, related_name='records')
    vessels = models.ManyToManyField(Vessel, blank=True)
    vessel_or_craft_details = models.IntegerField(null=True, blank=True)
    purpose = models.ForeignKey(ApplicationPurpose, null=True, blank=True)
    max_participants = models.IntegerField(null=True, blank=True)
    proposed_location = models.SmallIntegerField(choices=APP_LOCATION_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location_route_access = models.ForeignKey(Record, null=True, blank=True, related_name='location_route_access')
    jetties = models.TextField(null=True, blank=True)
    jetty_dot_approval = models.NullBooleanField(default=None)
    jetty_dot_approval_expiry = models.DateField(null=True, blank=True)
    drop_off_pick_up = models.TextField(null=True, blank=True)
    food = models.NullBooleanField(default=None)
    beverage = models.NullBooleanField(default=None)
    byo_alcohol = models.NullBooleanField(default=None)
    sullage_disposal = models.TextField(null=True, blank=True)
    waste_disposal = models.TextField(null=True, blank=True)
    refuel_location_method = models.TextField(null=True, blank=True)
    berth_location = models.TextField(null=True, blank=True)
    anchorage = models.TextField(null=True, blank=True)
    operating_details = models.TextField(null=True, blank=True)
    cert_survey = models.ForeignKey(Record, blank=True, null=True, related_name='cert_survey')
    cert_public_liability_insurance = models.ForeignKey(Record, blank=True, null=True, related_name='cert_public_liability_insurace')
    risk_mgmt_plan = models.ForeignKey(Record, blank=True, null=True, related_name='risk_mgmt_plan')
    safety_mgmt_procedures = models.ForeignKey(Record, blank=True, null=True, related_name='safety_mgmt_plan')
    brochures_itineries_adverts = models.ManyToManyField(Record, blank=True, related_name='brochures_itineries_adverts')
    other_relevant_documents = models.ManyToManyField(Record, blank=True, related_name='other_relevant_documents')
    land_owner_consent = models.ManyToManyField(Record, blank=True, related_name='land_owner_consent')
    deed = models.ForeignKey(Record, blank=True, null=True, related_name='deed')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT, related_name='Submitted_by')
    river_lease_require_river_lease = models.NullBooleanField(default=None, null=True, blank=True)
    river_lease_scan_of_application = models.ForeignKey(Record, null=True, blank=True, related_name='river_lease_scan_of_application')
    river_lease_reserve_licence = models.NullBooleanField(default=None, null=True, blank=True)
    river_lease_application_number = models.CharField(max_length=30, null=True, blank=True)
    proposed_development_current_use_of_land = models.TextField(null=True, blank=True)
    proposed_development_plans = models.ManyToManyField(Record, blank=True, related_name='proposed_development_plans')
    proposed_development_description = models.TextField(null=True, blank=True)
    document_draft = models.ForeignKey(Record, null=True, blank=True, related_name='document_draft')
    document_new_draft = models.ForeignKey(Record, null=True, blank=True, related_name='document_newdraft')
    document_new_draft_v3 = models.ForeignKey(Record, null=True, blank=True, related_name='document_newdraftv3')
    document_draft_signed = models.ForeignKey(Record, null=True, blank=True, related_name='document_draft_signed')
    document_final = models.ForeignKey(Record, null=True, blank=True, related_name='document_final')
    document_final_signed = models.ForeignKey(Record, null=True, blank=True, related_name='document_final_signed')
    document_determination = models.ForeignKey(Record, null=True, blank=True, related_name='document_determination')
    document_completion = models.ForeignKey(Record, null=True, blank=True, related_name='document_completion')
    publish_documents = models.DateField(null=True, blank=True)
    publish_draft_report = models.DateField(null=True, blank=True)
    publish_final_report = models.DateField(null=True, blank=True)
    publish_determination_report = models.DateField(null=True, blank=True)
    routeid = models.CharField(null=True, blank=True, default=1, max_length=4)
    assessment_start_date = models.DateField(null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, related_name='application_group_assignment')
    swan_river_trust_board_feedback = models.ForeignKey(Record, null=True, blank=True, related_name='document_swan_river_board_feedback')
    document_memo = models.ForeignKey(Record, null=True, blank=True, related_name='document_memo')
    document_briefing_note = models.ForeignKey(Record, null=True, blank=True, related_name='document_briefing_note')
    document_determination_approved = models.ForeignKey(Record, null=True, blank=True, related_name='document_determination_approved')
    approval_id = models.IntegerField(null=True, blank=True)
    assessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT, related_name='assessed_by')
    supporting_info_demonstrate_compliance_trust_policies = models.ForeignKey(Record, null=True, blank=True, related_name='supporting_info_demonstrate_compliance_trust_policies')
    type_of_crafts = models.ForeignKey(Craft, null=True, blank=True, related_name='craft') 
    number_of_crafts  = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'Application {}: {} - {} ({})'.format(
            self.pk, self.get_app_type_display(), self.title, self.get_state_display())

    def get_absolute_url(self):
        return reverse('application_detail', args=(self.pk,))


@python_2_unicode_compatible
class PublicationFeedback(models.Model):
    PUB_STATES_CHOICES = Choices(
        (1, 'Western Australia', ('Western Australia')),
        (2, 'New South Wales', ('New South Wales')),
        (3, 'Victoria', ('Victoria')),
        (4, 'South Australia', ('South Australia')),
        (5, 'Northern Territory', ('Northern Territory')),
        (6, 'Queensland', ('Queensland')),
        (7, 'Australian Capital Territory', ('Australian Capital Territory')),
        (8, 'Tasmania', ('Tasmania')),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    suburb = models.CharField(max_length=100)
    state = models.IntegerField(choices=PUB_STATES_CHOICES)
    postcode = models.CharField(max_length=4)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    comments = models.TextField(null=True, blank=True)
    records = models.ManyToManyField(Record, blank=True, related_name='feedback')
    status = models.CharField(max_length=20)

    def __str__(self):
        return 'PublicationFeedback {} ({})'.format(self.pk, self.application)


@python_2_unicode_compatible
class PublicationNewspaper(models.Model):
    """This model represents Application Published in newspapert
    """

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    newspaper = models.CharField(max_length=150)
    records = models.ManyToManyField(Record, blank=True, related_name='newspaper')

    def __str__(self):
        return 'PublicationNewspaper {} ({})'.format(self.pk, self.application)


@python_2_unicode_compatible
class PublicationWebsite(models.Model):
    """This model represents Application Published in Website
    """

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    original_document = models.ForeignKey(Record, blank=True, null=True, related_name='original_document')
    published_document = models.ForeignKey(Record, blank=True, null=True, related_name='published_document')

    def __str__(self):
        return 'PublicationWebsite {} ({})'.format(self.pk, self.application)


@python_2_unicode_compatible
class Location(models.Model):
    """This model represents a single spatial location associated with an
    application.
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    lot = models.CharField(max_length=256, null=True, blank=True)
    reserve = models.CharField(max_length=256, null=True, blank=True)
    suburb = models.CharField(max_length=256, null=True, blank=True)
    intersection = models.CharField(max_length=256, null=True, blank=True)
    # TODO: validation related to LGA name (possible FK).
    lga = models.CharField(max_length=256, null=True, blank=True)
    poly = models.PolygonField(null=True, blank=True)
    records = models.ManyToManyField(Record, blank=True)
    # TODO: certificate of title fields (ref. screen 30)
    title_volume = models.CharField(max_length=256, null=True, blank=True)
    folio = models.CharField(max_length=30, null=True, blank=True)
    dpd_number = models.CharField(max_length=30, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)  # this seem like it different from street address based on the example form.
    street_number_name = models.CharField(max_length=256, null=True, blank=True)
    local_government_authority = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return 'Location {} ({})'.format(self.pk, self.application)


@python_2_unicode_compatible
class Referral(models.Model):
    """This model represents a referral of an application to a referee
    (external or internal) for comment/conditions.
    """
    REFERRAL_STATUS_CHOICES = Choices(
        (1, 'referred', ('Referred')),
        (2, 'responded', ('Responded')),
        (3, 'recalled', ('Recalled')),
        (4, 'expired', ('Expired')),
    )
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    details = models.TextField(blank=True, null=True)
    sent_date = models.DateField()
    period = models.PositiveIntegerField(verbose_name='period (days)')
    expire_date = models.DateField(blank=True, null=True, editable=False)
    response_date = models.DateField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    records = models.ManyToManyField(Record, blank=True)
    status = models.IntegerField(choices=REFERRAL_STATUS_CHOICES, default=REFERRAL_STATUS_CHOICES.referred)

    class Meta:
        unique_together = ('application', 'referee')

    def __str__(self):
        return 'Referral {} to {} ({})'.format(self.pk, self.referee, self.application)

    def save(self, *args, **kwargs):
        """Override save to set the expire_date field.
        """
        self.expire_date = self.sent_date + timedelta(days=self.period)
        super(Referral, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Condition(models.Model):
    """This model represents a condition of approval for an application
    (either proposed by a referee or applied by P&W).
    """
    CONDITION_STATUS_CHOICES = Choices(
        (1, 'proposed', ('Proposed')),
        (2, 'applied', ('Applied')),
        (3, 'rejected', ('Rejected')),
        (4, 'cancelled', ('Cancelled')),
    )
    CONDITION_RECUR_CHOICES = Choices(
        (1, 'weekly', ('Weekly')),
        (2, 'monthly', ('Monthly')),
        (3, 'annually', ('Annually')),
    )

    application = models.ForeignKey(Application, on_delete=models.PROTECT)
    condition = models.TextField(blank=True, null=True)
    referral = models.ForeignKey(Referral, null=True, blank=True, on_delete=models.PROTECT)
    status = models.IntegerField(choices=CONDITION_STATUS_CHOICES, default=CONDITION_STATUS_CHOICES.proposed)
    records = models.ManyToManyField(Record, blank=True)
    due_date = models.DateField(blank=True, null=True)
    # Rule: recurrence patterns (if present) begin on the due date.
    recur_pattern = models.IntegerField(choices=CONDITION_RECUR_CHOICES, null=True, blank=True)
    recur_freq = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='recurrence frequency',
        help_text='How frequently is the recurrence pattern applied (e.g. every 2 months)')

    def __str__(self):
        return 'Condition {}: {}'.format(self.pk, self.condition)


@python_2_unicode_compatible
class Compliance(models.Model):
    """This model represents a request for confirmation of fulfilment of the
    requirements for a single condition, based upon supplied evidence.
    """
    COMPLIANCE_STATUS_CHOICES = Choices(
        (1, 'current', ('Current')),
        (2, 'due',('Due')),
        (3, 'future', ('Future')),
        (4, 'approved', ('Approved')),
        (5, 'with_assessor', ('With Assessor')),
        (6, 'with_manager', ('With Manager')),
        (7, 'with_holder', ('With Licence Holder')),
        (8, 'expired', ('Expired'))
    )

    approval_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True) 
    app_type = models.IntegerField(choices=Application.APP_TYPE_CHOICES, blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT, related_name='compliance_applicant')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT, related_name='compliance_assignee')
    assessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT, related_name='compliance_assigned_by')
    assessed_date = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=COMPLIANCE_STATUS_CHOICES, default=COMPLIANCE_STATUS_CHOICES.future)
    submit_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    compliance = models.TextField(blank=True, null=True, help_text='Information to fulfil requirement of condition.')
    comments = models.TextField(blank=True, null=True)
    approve_date = models.DateField(blank=True, null=True)
    records = models.ManyToManyField(Record, blank=True)

    def __str__(self):
        return 'Compliance {} ({})'.format(self.pk, self.condition)


class Communication(models.Model):
    """This model represents the communication model
    """
    COMM_TYPE = Choices(
        (0, 'none', ('None')),
        (1, 'phone', ('Phone')),
        (2, 'email', ('Email')),
        (3, 'mail', ('Mail')),
    )

    application = models.ForeignKey(Application, on_delete=models.PROTECT)
    comms_to = models.CharField(max_length=256, null=True, blank=True)
    comms_from = models.CharField(max_length=256, null=True, blank=True)
    subject = models.CharField(max_length=256, null=True, blank=True)
    comms_type = models.IntegerField(choices=COMM_TYPE, default=COMM_TYPE.none )
    details = models.TextField(blank=True, null=True)
    records = models.ManyToManyField(Record, blank=True, related_name='communication_docs')
    state = models.IntegerField(blank=True, null=True)  # move to foreign key once APP_STATE_CHOICES becomes a model
    created = models.DateTimeField(auto_now_add=True)


@python_2_unicode_compatible
class Delegate(models.Model):
    """This model represents the delegation of authority for an EmailUser to
    submit applications on behalf of an Organisation, within the Statutory
    Development application.
    """
    email_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.PROTECT)
    organisation = models.ForeignKey(Organisation, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return '{}: {}'. format(self.email_user.email, self.organisation.name)

    class Meta:
        unique_together = ('email_user', 'organisation')


class OrganisationContact(models.Model):
    """This model represents the contact people within the organisation for this application.
    """
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=128, blank=True, verbose_name='Given name(s)')
    last_name = models.CharField(max_length=128, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True)
    fax_number = models.CharField(max_length=50, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, blank=False, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return '{}: {}'. format(self.first_name, self.last_name, self.email)


@python_2_unicode_compatible
class ApplicationInvoice(models.Model):
    """This model represents a reference to an invoice for payment raised against
    an application.
    """
    application = models.ForeignKey(Application)
    invoice_reference = models.CharField(max_length=64)

    def __str__(self):
        return 'Application {} invoice {}'.format(self.application, self.invoice_reference)
