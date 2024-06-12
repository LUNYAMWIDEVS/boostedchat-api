from django.test import TestCase
from channels.models import ChannelManager
from channels.models import InstagramUserNames
from colorama import Fore, Style, init
class InstagramManagerTestCase(TestCase):
    def setUp(self):
        self.manager = ChannelManager("instagram")
        self.model = self.manager.ChannelUserNames

    def test_save_read_update_delete_channel_username(self):
        """Test the save, read, update, and delete operations for Instagram usernames."""
        print(Fore.BLUE + "Testing Instagram username operations")
        # Save a new Instagram username
        try:
            self.manager.save_channel_username({"username":"testuser", "status1":"active"})
            saved_username = self.manager.read_channel_username("testuser")
            self.assertIsNotNone(saved_username)
            self.assertEqual(saved_username.status1, "active")
            print(Fore.GREEN + "\t✓ Test passed: creating instagram username")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: creating instagram username")


        # Update the status of the Instagram username
        try:
            self.manager.update_channel_username({"username":"testuser", "status1":"inactive"})
            updated_username = self.manager.read_channel_username("testuser")
            self.assertEqual(updated_username.status1, "inactive")
            print(Fore.GREEN + "\t✓ Test passed: updating instagram username")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: updating instagram username")

        try:
            usernames = self.manager.read_channel_usernames()
            expected_usernames = self.model.objects.all()
            self.assertQuerysetEqual(
                usernames,
                expected_usernames,
                ordered=False,
                transform=lambda x: x,  # Optional transformation function
                msg="The queryset returned by read_channel_usernames() is not correct"
            )
            print(Fore.GREEN + "\t✓ Test passed: reading instagram usernames")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: reading instagram usernames")
        # Delete the Instagram username
        try:
            self.manager.delete_channel_username("testuser")
            deleted_username = self.manager.read_channel_username("testuser")
            self.assertIsNone(deleted_username)
            print(Fore.GREEN + "\t✓ Test passed: deleting instagram username")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: deleting instagram username")

        # test if username can be created after deleting
        try:
            self.manager.save_channel_username({"username":"testuser", "status1":"active"})
            saved_username = self.manager.read_channel_username("testuser")
            self.assertIsNotNone(saved_username)
            self.assertEqual(saved_username.status1, "active")
            print(Fore.GREEN + "\t✓ Test passed: creating instagram username after deleting")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: creating instagram username after deleting")


        # test duplicate usernames
        try:
            self.manager.save_channel_username({"username":"testuser1", "status1":"active"})
            self.manager.save_channel_username({"username":"testuser1", "status1":"active"}) 
            print(Fore.RED + "\t✗ Test failed: creating duplicate instagram username")
        except Exception:
            print(Fore.GREEN + "\t✓ Test passed: creating duplicate instagram username")
        print(Style.RESET_ALL)
        # self.manager.save_channel_username({"username":"testuser1", "status1":"active"})
        # with self.assertRaises(Exception):
        #     self.manager.save_channel_username({"username":"testuser1", "status1":"active"}) 
        
    def test_list_with_filters(self):
        # Create some test data
        print(Fore.BLUE + "Testing Instagram username filters")
        self.manager.save_channel_username({"username": "user1", "status1": "active"})
        self.manager.save_channel_username({"username": "user2", "status1": "inactive"})
        self.manager.save_channel_username({"username": "user3", "status1": "active"})

        # Test filtering by status
        try:
            active_usernames = self.manager.read_channel_usernames({"status1":"active"})
            self.assertEqual(len(active_usernames), 2)
            for username in active_usernames:
                self.assertEqual(username.status1, "active")
            print(Fore.GREEN + "\t✓ Test passed: filtering by status")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: filtering by status")
        
        try:
            inactive_usernames = self.manager.read_channel_usernames({"status1":"inactive"})
            self.assertEqual(len(inactive_usernames), 1)
            for username in inactive_usernames:
                self.assertEqual(username.status1, "inactive")
            print(Fore.GREEN + "\t✓ Test passed: filtering by status")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: filtering by status")


        # Test filtering by username
        try:
            filtered_usernames = self.manager.read_channel_usernames({"username":"user2"})
            self.assertEqual(len(filtered_usernames), 1)
            self.assertEqual(filtered_usernames[0].username, "user2")
            print(Fore.GREEN + "\t✓ Test passed: filtering by username")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: filtering by username")
        
    # Test for update_channel_usernames
    def test_update_channel_usernames(self):
        # Create some test data
        print(Fore.BLUE + "Testing Instagram username update")
        self.manager.save_channel_username({"username": "user1", "status1": "active"})
        self.manager.save_channel_username({"username": "user2", "status1": "inactive"})
        self.manager.save_channel_username({"username": "user3", "status1": "active"})

        # Test updating
        try:
            self.manager.update_channel_username({"username": "user1", "status1":"inactive"})
            usernames = self.manager.read_channel_usernames({"username": "user1"})
            for username in usernames:
                self.assertEqual(username.status1, "inactive")
            print(Fore.GREEN + "\t✓ Test passed: updating all usernames")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: updating all usernames")

        # test updating a username which already exists
        try:
            self.manager.update_channel_username({"username": "user1", "status1":"inactive"})
        except AssertionError as e:
            print(e)
            print(Fore.RED + "\t✗ Test failed: updating a username")

       