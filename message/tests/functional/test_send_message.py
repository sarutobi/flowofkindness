# coding: utf-8

from django.core.urlresolvers import reverse

from django_webtest import WebTest

from message.models import Message
from message.factories import MessageFactory
from test.factories import UserFactory


class TestAnonymousMessage(WebTest):
    """ Отправка сообщения незарегистрированным пользователем """

    def setUp(self):
        self.page = self.app.get(reverse('create-request'))
        self.data = MessageFactory.attributes(create=False)

    def test_anonymous_message(self):
        before = Message.objects.count()
        form = self.page.forms['mainForm']
        form['title'] = self.data['title']
        form['message'] = self.data['message']
        form['is_anonymous'] = self.data['is_anonymous']
        form['allow_feedback'] = self.data['allow_feedback']
        form['email'] = 'me@local.host'
        form.submit()
        self.assertEquals(before + 1, Message.objects.count())


class TestSendRequestMessage(WebTest):
    """ Functional test for request creation. """

    def setUp(self):
        self.user = UserFactory()
        self.page = self.app.get(
            reverse('create-request'),
            user=self.user.username)
        self.data = MessageFactory.attributes(create=False)

    def tearDown(self):
        Message.objects.all().delete()

    def test_get_form(self):
        form = self.page.forms['mainForm']
        self.assertIsNotNone(form)

    def test_message_saved(self):
        before = Message.objects.count()
        form = self.page.forms['mainForm']
        form['title'] = self.data['title']
        form['message'] = self.data['message']
        form['is_anonymous'] = self.data['is_anonymous']
        form['allow_feedback'] = self.data['allow_feedback']
        form['email'] = 'me@local.host'
        form.submit()
        self.assertEquals(before + 1, Message.objects.count())


class TestRequestMessageParameters(WebTest):
    """ Tests for new request parameters """
    def setUp(self):
        self.user = UserFactory()
        self.data = MessageFactory.attributes(create=False)
        self.form = self.app.get(
            reverse('create-request'), user=self.user.username
        ).forms['mainForm']

    def send_form(self):
        self.form['title'] = self.data['title']
        self.form['message'] = self.data['message']
        self.form['is_anonymous'] = self.data['is_anonymous']
        self.form['allow_feedback'] = self.data['allow_feedback']
        self.form['email'] = 'me@local.host'
        self.form.submit()

    def test_message_user(self):
        """ Test message author """
        self.send_form()
        msg = Message.objects.get()
        self.assertEquals(msg.user, self.user)

    def test_message_flags(self):
        """ Test default message flags """
        self.send_form()
        msg = Message.objects.get()
        self.assertEquals(Message.NEW, msg.status)
        self.assertFalse(msg.is_removed)
        self.assertTrue(msg.is_anonymous)
        self.assertTrue(msg.allow_feedback)
        self.assertFalse(msg.is_virtual)
        self.assertFalse(msg.is_important)
        self.assertFalse(msg.is_active)

    def test_nonanonymous_message(self):
        """ Send non-anonymous message """
        self.data['is_anonymous'] = False
        self.send_form()
        msg = Message.objects.get()
        self.assertFalse(msg.is_anonymous)

    def test_no_feedback(self):
        """ Send message and do not want feedback """
        self.data['allow_feedback'] = False
        self.send_form()
        msg = Message.objects.get()
        self.assertFalse(msg.allow_feedback)
