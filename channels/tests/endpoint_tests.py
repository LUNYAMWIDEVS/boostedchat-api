# from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from channels.views import * 
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.models import *
from datetime import datetime, date, time, timedelta
from colorama import Fore, Style, init
from setup.utils import *
# from setup.utils import TestUtils
# import base64

class ChannelsViewSetTestCase(TestUtils):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ChannelsViewSet.as_view({'get': 'list'})
        User = get_user_model() 
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.token = AccessToken.for_user(self.user)
        self.header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}


    def test_list_channels(self):
        describe = "Testing endpoint for Listing Channels"
        level = 0

        self.describe(describe,level)

        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
        request = self.factory.get('/channels/', **header)
        response = self.view(request)
        should = "Return status 200"
        self.localTest(
            self.assertEqual,
            response.status_code, 
            status.HTTP_200_OK,
            should=should,
            level=level
            )

class ChannelUserNameViewSetTestCase(TestUtils):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ChannelUserNameViewSet.as_view({'post': 'create', 'get':'list', 'patch':'update', 'delete':'destroy'})
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
    def test_creating_channel_usernames(self):
        level = 0
        describe = "Testing endpoint for Creating Channel UserNames"
        self.describe(describe, level)
        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
        # test invalid channel
        level = 1
        describe = "Testing Creating Without Supplying Channel"
        self.describe(describe, level)
        should = "Return status 400"
        request = self.factory.post('/', self.missing_channel, format='json', **header)
        response = self.view(request)
        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            should=should,
            level=level
            )

        describe = "Testing Creating Using Invalid Channel"
        self.describe(describe, level)
        should = "Return status 400"
        request = self.factory.post('/', self.invalid_channel, format='json', **header)
        response = self.view(request)

        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            should=should,
            level=level
            )
        describe = "Testing Creating Using Empty value for Channel"
        self.describe(describe, level)
        should = "Return status 400"
        request = self.factory.post('/', self.empty_channel, format='json', **header)
        response = self.view(request)
        

        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            should=should,
            level=level
            )
        
        describe = "Testing Creating Using Numerical value for Channel"
        self.describe(describe, level)
        should = "Return status 400"
        request = self.factory.post('/', self.number_channel, format='json', **header)
        response = self.view(request)

        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            should=should,
            level=level
            )

        

        # test upercanse
        # test lowercase
        describe = "Testing Case Insensitivity of channel names"
        self.describe(describe, level)
        should = "Return status 201"
        channels = helpers.channelsList()
        channel = channels[0]

        data = {'channel': channel.lower(), 'username':"lowercase"}
        request = self.factory.post('/', data, format='json', **header)
        response = self.view(request)
        should = f"Return 201 for lowercase({channel.lower()})"

        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_201_CREATED,
            should=should,
            level=level
            )
        data = {'channel': channel.upper(), 'username':"uppercase"}
        request = self.factory.post('/', data, format='json', **header)
        response = self.view(request)
        should = f"Return 201 for UPPERCASE({channel.upper()})"
        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_201_CREATED,
            should=should,
            level=level
            )

        describe = "Testing Creating UserNames for All Valid Channels"
        self.describe(describe, level)

        channels = helpers.channelsList()
        for channel in channels:
            valid_data = {'channel': channel, 'username': f'{channel}-example_username', 'status1': 'active', 'status2': 'inactive', 'status3': 'pending', 'status4': 'completed', 'sandbox': True}
            request = self.factory.post('/', valid_data, format='json', **header)
            response = self.view(request)
            should = f"Return 201 for {channel}"
            self.localTest(
                self.assertEqual,
                response.status_code,
                status.HTTP_201_CREATED,
                should=should,
                level=level
                )
            
        describe = "Test creation with duplicate usernames"
        self.describe(describe, level)
        for channel in channels:
            valid_data = {'channel': channel, 'username': f'{channel}-duplicate-example_username', 'status1': 'active', 'status2': 'inactive', 'status3': 'pending', 'status4': 'completed', 'sandbox': True}
            request = self.factory.post('/', valid_data, format='json', **header)
            response = self.view(request) # create it the first time
            should = f"Return 200 for creating {channel}-duplicate-example_username in {channel}"
            self.localTest(
                self.assertEqual,
                response.status_code,
                status.HTTP_201_CREATED,
                should=should,
                level=level
                )
            request = self.factory.post('/', valid_data, format='json', **header)
            response = self.view(request)
            should = f"Return 400 for duplicate {channel}-duplicate-example_username in {channel}"
            self.localTest(
                self.assertEqual,
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
                should=should,
                level=level
                )
    def test_fetch_function(self):
        level = 0
        describe = "Test endpoint for reading channel usernames"
        self.describe(describe, level)
        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}

        level = 1
        describe = "Fetch using a wrong channel"
        self.describe(describe, level)
        wrong_channel = 'wrongchannel_not_in_list'
        request = self.factory.get('/', **header, data={'channel': wrong_channel})
        response = self.view(request)
        should = "Return 400 for wrong channel"
        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            should=should,
            level=level
        )

        describe = "Fetch without supplying channel"
        self.describe(describe, level)
        request = self.factory.get('/', **header)
        response = self.view(request)
        should = "Return 400 for missing channel"
        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            should=should,
            level=level
        )


        describe = "Fetch for all valid channels"
        self.describe(describe, level)
        channels = helpers.channelsList()

        for channel in channels:
            for i in range(1, 10):
                valid_data = {'channel': channel, 'username': f'{channel}-{i}-example_username', 'status1': 'active', 'status2': 'inactive', 'status3': 'pending', 'status4': 'completed', 'sandbox': True}
                request = self.factory.post('/', valid_data, format='json', **header)
                response = self.view(request)            

            request = self.factory.get(f'/?channel={channel}', **header)
            channelUserNames = helpers_circular.getChannelUserNameModel(channel.lower())
            response = self.view(request)
            # Check if the status code is 200 OK
            should = f"Return 200 for successful fetch in {channel}"
            self.localTest(
                self.assertEqual,
                response.status_code,
                status.HTTP_200_OK,
                should=should,
                level=level
            )
            should = f"Return 9 records for {channel}"
            self.localTest(
                self.assertEqual,
                len(response.data),
                9,
                should=should,
                level=level
            )

            expected_data = channelUserNames.objects.all()
            expected_data = ChannelUserNamesReadSerializer(expected_data, many=True).data
            retrieved_data = response.data

            should = f"Retrieved data should be the same as that which was saved for {channel}"
            self.localTest(
                self.assertEqual,
                retrieved_data,
                expected_data,
                should=should,
                level=level
            )
       


    def test_test_fetch_function_with_filters(self):
#         # Create channel usernames
        describe = "Test fetching using filters"
        level = 0
        self.describe(describe, level)
        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}

        data = {'channel':'whatsapp','username': 'user1', 'status1': 'active'}
        request = self.factory.post('/', data, format='json', **header)
        response = self.view(request)
        response_data = response.data
        id1 = response_data.get('data', {}).get('id')
        data = {'channel':'whatsapp','username': 'user2', 'status1': 'inactive'}
        request = self.factory.post('/', data, format='json', **header)
        response = self.view(request)
        response_data = response.data
        id2 = response_data.get('data', {}).get('id')
        data = {'channel':'whatsapp','username': 'user3', 'status1': 'active'}
        request = self.factory.post('/', data, format='json', **header)
        response = self.view(request)
        response_data = response.data
        id3 = response_data.get('data', {}).get('id')

        # rest filtering by status
        level = 1
        describe = "Test filtering by status"
        self.describe(describe, level)
        request = self.factory.get('/', **header, data={'channel': 'whatsapp', 'status1': 'active'})
        response = self.view(request)
        should = "Return 200 for status=active"
        self.localTest(
            self.assertEqual,
            response.status_code, 
            status.HTTP_200_OK,
            should=should,
            level=level
        )
        should = "Return 2 values for status=active"
        self.localTest(
            self.assertEqual,
            len(response.data),
            2, 
            should=should,
            level=level
        )
        
        
        request = self.factory.get('/', **header, data={'channel': 'whatsapp', 'status1': 'inactive'})
        response = self.view(request)
        should = "Return 1 value for status=inactive"
        self.localTest(
            self.assertEqual,
            len(response.data),
            1, 
            should=should,
            level=level
        )
        should = "Value of status1 = inactive"
        for username in response.data:
            self.localTest(
                self.assertEqual,
                username['status1'],
               'inactive', 
                should=should,
                level=level
            )
        
        describe = "Test Filtering by Id"
        ids = [id1, id2, id3]
        for id in ids:
            request = self.factory.get('/', **header, data={'channel': 'whatsapp', 'id': id})
            response = self.view(request)
            should = f"Return 1 value for {id}"
            self.localTest(
                self.assertEqual,
                len(response.data),
                1, 
                should=should,
                level=level
            )
            should = f"Return id = {id}"
            for username in response.data:
                self.localTest(
                    self.assertEqual,
                    username['id'],
                    id, 
                    should=should,
                    level=level
                )
            



        # Test filtering by username
        describe = "Test filtering by username"
        self.describe(describe, level)

        request = self.factory.get('/', **header, data={'channel': 'whatsapp', 'username': 'user2'})
        response = self.view(request)
        should = "Return 200 for successful filter by username"
        self.localTest(
            self.assertEqual,
            response.status_code,
            status.HTTP_200_OK,
            should=should,
            level=level
        )

        should = "Return one item when filtering by username"
        self.localTest(
            self.assertEqual,
            len(response.data),
            1,
            should=should,
            level=level
        )

        should = "Return correct username when filtering by username"
        self.localTest(
            self.assertEqual,
            response.data[0]['username'],
            'user2',
            should=should,
            level=level
        )

    def test_test_update_function(self):
        level = 0
        describe = "Testing update function"
        self.describe(describe, level)
        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
        channels = helpers.channelsList()

        level = 1
        describe = "Testing if active status1 is changed to inactive when changed using {status1: 'active'} filter"
        self.describe(describe, level)

        # Update records
        for channel in channels:
            # create 10 inactive records for channel
            for i in range(1, 10):
                valid_data = {'channel': channel, 'username': f'{channel}-{i}-example_username', 'status1': 'active', 'sandbox': True}
                request = self.factory.post('/', valid_data, format='json', **header)
                response = self.view(request)
            
            ## get list of active status1s of channel
            request = self.factory.get('/', **header, data={'channel': channel, 'status1': 'active'})
            response = self.view(request)
            active_status1s = response.data
            for active_status1 in active_status1s:
                active_status1['status1'] = 'inactive'
            

            # update the 10 inactive records to active
            valid_data = {'channel': channel, 'status1': 'inactive', 'sandbox': True, "filters":{"status1":"active"}}
            request = self.factory.patch('/', valid_data, format='json', **header)
            response = self.view(request)

            # Check if the status code is 200 OK
            should = f"Return 200 for successful update in {channel}"
            self.localTest(
                self.assertEqual,
                response.status_code,
                status.HTTP_200_OK,
                should=should,
                level=level
            )

            # Check if the status of the updated record is 'inactive'
            response_data = response.data.get("data", [])

            # The updated_at field will certainly have changed. So remove it from comparison
            for active_status1 in active_status1s:
                del active_status1['updated_at']
            for reponse in response_data:
                del reponse['updated_at']
            
            should = f"Return 'inactive' status for updated records in {channel}"
            self.localTest(
                self.assertEqual,
                active_status1s,
                response_data,
                should=should,
                level=level
            )

            # update sandbox
            describe = "Testing if sandbox status is changed to False when changed using {sandbox: True} filter"
            self.describe(describe, level)
            # update sandbox and check if the update is successful
            true_sandboxes = response_data
            for true_sandbox in true_sandboxes:
                true_sandbox['sandbox'] = False
            valid_data = {'channel': channel, 'status1': 'inactive', 'sandbox': False, "filters":{"sandbox":True}}
            request = self.factory.patch('/', valid_data, format='json', **header)
            response = self.view(request)
            should = f"Return 200 for successful update of sandbox in {channel}"
            self.localTest(
                self.assertEqual,
                response.status_code,
                status.HTTP_200_OK,
                should=should,
                level=level
            )
            response_data = response.data.get("data", [])

            # The updated_at field will certainly have changed. So remove it from comparison
            for true_sandbox in true_sandboxes:
                if 'updated_at' in true_sandbox:
                    del true_sandbox['updated_at']
            for reponse in response_data:
                if 'updated_at' in reponse:
                    del reponse['updated_at']
            should = f"Return False for sandbox in {channel}"
            self.localTest(
                self.assertEqual,
                true_sandboxes,
                response_data,
                should=should,
                level=level
            )




    # write tests for deleting channel usernames
    def test_test_delete_function(self):
        level = 0
        describe = "Testing delete function"
        self.describe(describe, level)
        header = {"HTTP_AUTHORIZATION": f'Bearer {str(self.token)}'}
        channels = helpers.channelsList()

        # create 10 records in each channel
        for channel in channels:
            for i in range(1, 10):
                valid_data = {'channel': channel, 'username': f'{channel}-{i}-example_username', 'status1': 'active', 'sandbox': True}
                request = self.factory.post('/', valid_data, format='json', **header)
                response = self.view(request)

            # loop through the records and delete them one by one using id key
            request = self.factory.get('/', **header, data={'channel': channel})
            response = self.view(request)
            response_data = response.data
            level = 1
            describe = f"Testing if records are deleted one by one for {channel}"
            self.describe(describe, level)
            for response_ in response_data:
                id = response_.get('id')
                valid_data = {'channel': channel, 'id': id}
                url = f'/?channel={channel}&id={id}'
                request = self.factory.delete(url, **header)
                response = self.view(request)
                should = f"Return 200 for successful deletion of {id}"
                self.localTest(
                    self.assertEqual,
                    response.status_code,
                    status.HTTP_200_OK,
                    should=should,
                    level=level
                )
            request = self.factory.get('/', **header, data={'channel': channel})
            response = self.view(request)
            should = f"Return 0 records for {channel}"
            self.localTest(
                self.assertEqual,
                len(response.data),
                0,
                should=should,
                level=level
            )




        ## Update all records where status is 'inactive'
        # valid_data = {'filters': {'status': 'inactive'}, 'status': 'active', 'sandbox': True}
        # request = self.factory.put('/', valid_data, format='json', **header)
        # response = self.view(request)

        # # Check if the status code is 200 OK
        # should = "Return 200 for successful update of all inactive records"
        # self.localTest(
        #     self.assertEqual,
        #     response.status_code,
        #     status.HTTP_200_OK,
        #     should=should,
        #     level=level
        # )

        # # Check if the status of the updated records is 'active'
        # for item in response.data:
        #     should = "Return 'active' status for updated records"
        #     self.localTest(
        #         self.assertEqual,
        #         item['status'],
        #         'active',
        #         should=should,
        #         level=level
        #     )
        
