# Django imports
from django.core import mail
from django.contrib.auth.models import User
from django.conf import settings

# Piston imports
from test import TestCase
from models import Consumer

class ConsumerTest(TestCase):
    fixtures = ['models.json']

    def setUp(self):
        self.consumer = Consumer()
        self.consumer.name = "Piston Test Consumer"
        self.consumer.description = "A test consumer for Piston."
        self.consumer.user = User.objects.get(pk=3)
        self.consumer.generate_random_codes()

    def test_create_pending(self):
        """ Ensure creating a pending Consumer sends proper emails """
        # If it's pending we should have two messages in the outbox; one 
        # to the consumer and one to the site admins.
        if len(settings.ADMINS):
            self.assertEquals(len(mail.outbox), 2)
        else:
            self.assertEquals(len(mail.outbox), 1)

        expected = "Your API Consumer for example.com is awaiting approval."
        self.assertEquals(mail.outbox[0].subject, expected)

    def test_delete_consumer(self):
        """ Ensure deleting a Consumer sends a cancel email """

        # Clear out the outbox before we test for the cancel email.
        mail.outbox = []

        # Delete the consumer, which should fire off the cancel email.
        self.consumer.delete() 
        
        self.assertEquals(len(mail.outbox), 1)
        expected = "Your API Consumer for example.com has been canceled."
        self.assertEquals(mail.outbox[0].subject, expected)

