from django.test import TestCase
from channels.models import ChannelManager

class WhatsappManagerTestCase(TestCase):
    def setUp(self):
        self.manager = ChannelManager("whatsapp")
        self.model = self.manager.ChannelUserNames

    def test_save_read_update_delete_channel_username(self):
        # Save a new Instagram username
        self.manager.save_channel_username({"username":"testuser", "status1":"active"})
        saved_username = self.manager.read_channel_username("testuser")
        self.assertIsNotNone(saved_username)
        self.assertEqual(saved_username.status1, "active")

        # Update the status of the Instagram username
        self.manager.update_channel_username({"username":"testuser", "status1":"inactive"})
        updated_username = self.manager.read_channel_username("testuser")
        self.assertEqual(updated_username.status1, "inactive")

        usernames = self.manager.read_channel_usernames()
        expected_usernames = self.model.objects.all()
        self.assertQuerysetEqual(
            usernames,
            expected_usernames,
            ordered=False,
            transform=lambda x: x,  # Optional transformation function
            msg="The queryset returned by read_channel_usernames() is not correct"
        )

        # Delete the Instagram username
        self.manager.delete_channel_username("testuser")
        deleted_username = self.manager.read_channel_username("testuser")
        self.assertIsNone(deleted_username)

        # test duplicate usernames
        self.manager.save_channel_username({"username":"testuser1", "status1":"active"})
        with self.assertRaises(Exception):
            self.manager.save_channel_username({"username":"testuser1", "status1":"active"})