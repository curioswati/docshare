from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase

from .viewsets import DocumentViewSet


class TestDocument(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DocumentViewSet.as_view({'get': 'list'})
        self.uri = '/documents/'

        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_list_unauthenticated(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 401,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_list_authenticated(self):
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
