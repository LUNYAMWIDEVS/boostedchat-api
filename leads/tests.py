from django.test import TestCase
from .models import  LeadsManager
# from instagram.models import Account

class LeadsManagerTestCase(TestCase):
    def setUp(self):
        self.manager = LeadsManager()

    def test_create_lead(self):
        lead_name = "Test Lead"
        lead = self.manager.create_lead(lead_name=lead_name)
        self.assertIsNotNone(lead)
        self.assertEqual(lead.lead_name, lead_name)

        leads = self.manager.get_leads()
        self.assertIsNotNone(leads)
        self.assertTrue(leads.exists())

    # def test_create_lead_for_channel(self):
    #     lead_name = "Test Lead"
    #     channel_name = "Test Channel"
    #     lead = self.manager.create_lead_for_channel(channel_name=channel_name, lead_name=lead_name)
    #     self.assertIsNotNone(lead)
    #     self.assertEqual(lead.lead_name, lead_name)
    #     # Add assertions for channel association if implemented

    # def test_add_channel_to_lead(self):
    #     lead_name = "Test Lead"
    #     channel_name = "Test Channel"
    #     lead = self.manager.add_channel_to_lead(channel_name=channel_name, lead_name=lead_name)
    #     self.assertIsNotNone(lead)
    #     self.assertEqual(lead.lead_name, lead_name)
    #     # Add assertions for channel association if implemented
