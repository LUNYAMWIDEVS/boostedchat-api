from rest_framework.test import APIRequestFactory
from rest_framework import status
from channels.views import * 
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.models import *
from datetime import datetime, date, time, timedelta
from colorama import Fore, Style, init
from setup.utils import *
from django.test import TestCase
from sales_rep.models import SalesRep, SalesRepManager

class SalesRepTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        # if user already exists, add to existing user...
        # we want to use the other to create it...
        # self.account = Account.objects.create(name='Test Account')  # Create an Account instance
        self.sales_rep_params = {
            'user': self.user,
            'ig_username': 'test_username',
            'ig_password': 'test_password',
            # 'instagram': [self.account],
            'available': True,
            'country': 'US',
            'city': 'Pasadena',
        }

    def test_save_sales_rep(self):
        # Call the save_sales_rep method with test parameters
        print(Fore.GREEN + "self.sales_rep_params", self.sales_rep_params)
        saved_sales_rep = SalesRepManager().save_sales_rep(self.sales_rep_params)
        print(Fore.GREEN + "saved_sales_rep", saved_sales_rep)

        # Check if the sales rep was saved correctly
        self.assertIsNotNone(saved_sales_rep.id)  # Check if the saved object has an ID

        # Optionally, check other attributes of the saved object
        print(Fore.GREEN + "saved_sales_rep.user", saved_sales_rep)
        self.assertEqual(saved_sales_rep.ig_username, 'test_username')
        self.assertTrue(saved_sales_rep.available)
        self.assertEqual(saved_sales_rep.country, 'US')
        localSerializer = SalesRepManager().getDynamicSerializer('created')
        print(saved_sales_rep, "saved_sales_rep", "localSerializer", localSerializer)
        data = localSerializer(saved_sales_rep).data
        print(Fore.GREEN + "data", data)

    def tearDown(self):
        # Clean up after the test
        SalesRep.objects.filter(user=self.user).delete()  # Delete the created SalesRep instance

# Note: Replace 'myapp' with the actual name of your Django app where models and managers are defined.
