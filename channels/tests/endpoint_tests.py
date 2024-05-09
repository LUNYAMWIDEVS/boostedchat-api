from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from channels.views import * 
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.models import *
from datetime import datetime, date, time, timedelta
from colorama import Fore, Style, init

# import base64

class ChannelsViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ChannelsViewSet.as_view({'get': 'list'})
        User = get_user_model() 
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.token = AccessToken.for_user(self.user)
        self.header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}


    def test_list_channels(self):
        print(Fore.BLUE + "Testing list channels")
        try:
            header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
            request = self.factory.get('/channels/', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print(Fore.GREEN + "\t✓ Test passed: list channels")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: list channels")

class ChannelUserNameViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ChannelUserNameViewSet.as_view({'post': 'create', 'get':'list'})  # Assuming 'create' is the action name in your viewset
        channels = helpers.channelsList()
        channels_string = ','.join(channels)
        self.missing_channel = {}
        self.invalid_channel = {'channel': channels_string}
        self.empty_channel = {'channel': ''}
        self.number_channel = {'channel': ''}

        User = get_user_model() 
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.token = AccessToken.for_user(self.user)

    # POST
    def test_create_valid_data(self):
        # test invalid channel
        print(Fore.BLUE + "Testing create channel usernames")
        try:
            header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
            request = self.factory.post('/', self.missing_channel, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print(Fore.GREEN + "\t✓ Test passed: invalid channel")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: invalid channel")
        try:
            request = self.factory.post('/', self.invalid_channel, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print(Fore.GREEN + "\t✓ Test passed: invalid channel")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: invalid channel")
        try:
            request = self.factory.post('/', self.empty_channel, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print(Fore.GREEN + "\t✓ Test passed: empty channel")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: empty channel")
        try:
            request = self.factory.post('/', self.number_channel, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print(Fore.GREEN + "\t✓ Test passed: number channel")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: number channel")
        # test all valid channels
        channels = helpers.channelsList()
        for channel in channels:
            channel = channel.upper()
        
            valid_data = {'channel': channel, 'username': f'{channel}-example_username', 'status1': 'active', 'status2': 'inactive', 'status3': 'pending', 'status4': 'completed', 'sandbox': True}
            request = self.factory.post('/', valid_data, format='json', **header)
            response = self.view(request)
            try:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                print(Fore.GREEN + f"\t✓ Test passed: valid data: {channel}-example_username")
            except AssertionError:
                print(Fore.RED + f"\t✗ Test failed: valid data: {channel}-example_username")

        # test duplicate usernames
        try:
            valid_data = {'channel': 'whatsapp', 'username': 'whatsapp-duplicate-example_username', 'status1': 'active', 'status2': 'inactive', 'status3': 'pending', 'status4': 'completed', 'sandbox': True}
            request = self.factory.post('/', valid_data, format='json', **header)
            response = self.view(request)
            valid_data = {'channel': 'whatsapp', 'username': 'whatsapp-duplicate-example_username', 'status1': 'active', 'status2': 'inactive', 'status3': 'pending', 'status4': 'completed', 'sandbox': True}
            request = self.factory.post('/', valid_data, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print(Fore.GREEN + "\t✓ Test passed: duplicate usernames")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: duplicate usernames")

    # list
    def test_list_function(self):
        print(Fore.BLUE + "Testing list channel usernames")
        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
        # test with missing channel
        try:
            request = self.factory.get('/', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print(Fore.GREEN + "\t✓ Test passed: missing channel")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: missing channel")
        
        # test with wrong channel
        try:
            wrong_channel = 'wrongchannel_not_in_list'
            request = self.factory.get('/', **header, data={'channel': wrong_channel})
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print(Fore.GREEN + "\t✓ Test passed: wrong channel")
        except AssertionError:
            print(Fore.RED + "\t✗ Test failed: wrong channel")
        
        # test with correct channels
        channels = helpers.channelsList()
        for channel in channels:
            # create usernames
            for i in range(1, 10):
                valid_data = {'channel': channel, 'username': f'{channel}-{i}-example_username', 'status1': 'active', 'status2': 'inactive', 'status3': 'pending', 'status4': 'completed', 'sandbox': True}
                request = self.factory.post('/', valid_data, format='json', **header)
                response = self.view(request)            

            request = self.factory.get(f'/?channel={channel}', **header)
            channelUserNames = helpers_circular.getChannelUserNameModel(channel.lower())
            response = self.view(request)
            try:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 9)
                print(Fore.GREEN + f"\t✓ Test passed: correct channel: {channel}")
            except AssertionError:
                print(Fore.RED + f"\t✗ Test failed: correct channel: {channel}")

            expected_data = channelUserNames.objects.all()
            expected_data = ChannelUserNamesReadSerializer(expected_data, many=True).data

            retrieved_data = response.data
            try:
                self.assertEqual(retrieved_data, expected_data)
                print(Fore.GREEN + f"\t✓ Test passed: Created correct data for: {channel}")
            except AssertionError:
                print(Fore.RED + f"\t✗ Test failed: Created correct data for: {channel}")

    def test_create_and_filter_channel_usernames(self):
        print(Fore.BLUE + "Testing create and filter channel usernames")
        # Create channel usernames
        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
        try:
            data = {'channel':'whatsapp','username': 'user1', 'status1': 'active'}
            request = self.factory.post('/', data, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print(Fore.GREEN + f"\t✓ Test passed: create channel usernames user1")
        except AssertionError:
            print(Fore.RED + f"\t✗ Test failed: create channel usernames user1")
        
        try:
            data = {'channel':'whatsapp','username': 'user2', 'status1': 'inactive'}
            request = self.factory.post('/', data, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print(Fore.GREEN + f"\t✓ Test passed: create channel usernames user2")
        except AssertionError:
            print(Fore.RED + f"\t✗ Test failed: create channel usernames user2")

        try:
            data = {'channel':'whatsapp','username': 'user3', 'status1': 'active'}
            request = self.factory.post('/', data, format='json', **header)
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print(Fore.GREEN + f"\t✓ Test passed: create channel usernames user3")
        except AssertionError:
            print(Fore.RED + f"\t✗ Test failed: create channel usernames user3")

            

        # # Test filtering by status
        try:
            request = self.factory.get('/', **header, data={'channel': 'whatsapp', 'status1': 'active'})
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)
            for username in response.data:
                self.assertEqual(username['status1'], 'active')
            print(Fore.GREEN + f"\t✓ Test passed: filter by status1 active")
        except AssertionError:
            print(Fore.RED + f"\t✗ Test failed: filter by status1 active")

        try:
            request = self.factory.get('/', **header, data={'channel': 'whatsapp', 'status1': 'inactive'})
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            for username in response.data:
                self.assertEqual(username['status1'], 'inactive')
            print(Fore.GREEN + f"\t✓ Test passed: filter by status1 inactive")
        except AssertionError:
            print(Fore.RED + f"\t✗ Test failed: filter by status1 inactive")


        # Test filtering by username
        try:
            request = self.factory.get('/', **header, data={'channel': 'whatsapp', 'username': 'user2'})
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['username'], 'user2')
            print(Fore.GREEN + f"\t✓ Test passed: filter by username user2")
        except AssertionError:
            print(Fore.RED + f"\t✗ Test failed: filter by username user2")
    
        
