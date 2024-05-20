from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from setup.app_api_generator import APIRouterGenerator
router = APIRouterGenerator().router

class TestAPIEndpoints(APITestCase):
    def setUp(self):
        # Setup any necessary data or configurations before each test
        self.router_generator = APIRouterGenerator()
        self.router = self.router_generator.create_router()

    def test_api_endpoints_exist(self):
        # Iterate through the registered routes and test that each endpoint returns a 200 OK response
        for urlpattern in self.router.urls:
            response = self.client.get(urlpattern._regex)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    # You can add more specific tests for each endpoint if needed
    # For example:
    # def test_create_object(self):
    #     response = self.client.post('/api/endpoint/', data={...})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # Add assertions to verify the created object

    # def test_retrieve_object(self):
    #     response = self.client.get('/api/endpoint/<id>/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Add assertions to verify the retrieved object
