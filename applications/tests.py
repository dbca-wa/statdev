from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from mixer.backend.django import mixer
from unittest import skip

from accounts.utils import random_dpaw_email
from .models import Application, Task

User = get_user_model()


class ApplicationTest(TestCase):

    def setUp(self):
        # TODO: authorisation groups below are WiP.
        # Note that we have to instantiate groups in setUp().
        PROCESSOR = Group.objects.get_or_create(name='Processor')[0]
        self.client = Client()
        # Set up some non-superuser internal users.
        self.user1 = mixer.blend(User, email=random_dpaw_email, is_superuser=False, is_staff=True)
        self.user1.set_password('pass')
        self.user1.save()
        self.user1.groups.add(PROCESSOR)
        self.superuser = mixer.blend(User, email=random_dpaw_email, is_superuser=True, is_staff=True)
        self.superuser.set_password('pass')
        self.superuser.save()
        self.customer = mixer.blend(User, is_superuser=False, is_staff=False)
        self.customer.set_password('pass')
        self.customer.save()
        # Log in user1, by default.
        self.client.login(email=self.user1.email, password='pass')
        # Generate test fixtures..
        self.app1 = mixer.blend(Application)
        self.task1 = mixer.blend(Task)

    def test_get_absolute_url(self):
        """Test that Application.get_absolute_url works
        """
        self.assertTrue(self.app1.get_absolute_url())

    def test_list_application_view_get(self):
        """Test the application list view renders
        """
        url = reverse('application_list')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

    def test_create_application_view_get_redirect(self):
        """Test the application create view redirects unauthorised users
        """
        self.client.logout()
        self.client.login(email=self.customer.email, password='pass')
        url = reverse('application_create')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 302)

    def test_create_application_view_get(self):
        """Test the application create view renders for an authorised user
        """
        url = reverse('application_create')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        # Test for a superuser.
        self.client.logout()
        self.client.login(email=self.superuser.email, password='pass')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

    def test_create_application_view_post(self):
        """Test the application create view accepts a valid POST
        """
        count = Application.objects.count()
        url = reverse('application_create')
        resp = self.client.post(url, {'app_type': 1, 'title': 'foo', 'submit_date': '1/1/2017'})
        # Create view will redirect to the detail view.
        self.assertEquals(resp.status_code, 302)
        # Test that a new object has been created.
        self.assertTrue(Application.objects.count() > count)

    def test_detail_application_view_get(self):
        """Test the application detail view renders
        """
        url = reverse('application_detail', args=(self.app1.pk,))
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

    def test_update_application_view_get(self):
        """Test the application update view renders
        """
        self.app1.state = Application.APP_STATE_CHOICES.draft
        self.app1.save()
        url = reverse('application_update', args=(self.app1.pk,))
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

    def test_update_application_view_redirect(self):
        """Test the application update view redirect business rules
        """
        self.app1.state = Application.APP_STATE_CHOICES.with_admin
        self.app1.save()
        url = reverse('application_update', args=(self.app1.pk,))
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 302)

    def test_update_application_view_post(self):
        """Test the application update view accepts a valid POST
        """
        self.app1.state = Application.APP_STATE_CHOICES.draft
        self.app1.save()
        url = reverse('application_update', args=(self.app1.pk,))
        resp = self.client.post(url, {
            'app_type': 1, 'title': 'foo', 'submit_date': '1/1/2017'})
        # Create view will redirect to the detail view.
        self.assertEquals(resp.status_code, 302)
        a = Application.objects.get(pk=self.app1.pk)
        self.assertEquals(a.title, 'foo')

    @skip('Test stub')
    def test_update_application_lodge_get(self):
        pass

    @skip('Test stub')
    def test_update_application_lodge_post(self):
        pass

    @skip('Test stub')
    def test_update_application_refer_get(self):
        pass

    @skip('Test stub')
    def test_update_application_refer_post(self):
        pass

    def test_reassign_task_view_get(self):
        """Test the reassign task view renders
        """
        url = reverse('task_reassign', args=(self.task1.pk,))
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

    def test_reassign_task_view_post(self):
        """Test the reassign task view accepts a valid POST
        """
        url = reverse('task_reassign', args=(self.task1.pk,))
        resp = self.client.post(url, {'assignee': self.user1.pk})
        # Create view will redirect to the parent application detail view.
        self.assertEquals(resp.status_code, 302)
        t = Task.objects.get(pk=self.task1.pk)  # Reinstantiate the object.
        # Test that the task is assigned to user1.
        self.assertEquals(t.assignee, self.user1)
