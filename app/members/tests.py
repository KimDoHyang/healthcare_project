from django.contrib.auth import get_user_model
from django.test import TestCase
User = get_user_model()
# Create your tests here.

class RegisterUser(TestCase):
    @classmethod
    def make_dummy_user(self):
        User.objects.create_user(
            username='Tester01',
            email='test01@test.com',
            password='1111',
            name='tester'
        )

    def print_tester_user_email(self):
        test_user = User.objects.get(username='Tester01')
        print(test_user.email)