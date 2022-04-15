from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

GameUser = get_user_model()


class TestRegisterUserView(TestCase):

    def test_create_user_with_valid_data(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        user = GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        self.client.post(reverse('register'), data=user_data)
        self.assertEqual(user.email, 'sofi@abv.bg')

    # def test_register_view_redirect_to_correct_url(self):
    #     user_data = {
    #         'email': 'sofi@abv.bg',
    #         'password': '123'
    #     }
    #
    #     GameUser.objects.create_user(**user_data)
    #
    #
    #     response = self.client.post(reverse('register'), data=user_data)
    #     expected_url = reverse('catalogue list')
    #
    #     self.assertRedirects(response, expected_url)

    def test_register_user_statuscode(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        response = self.client.post(reverse('register'), data=user_data)

        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        GameUser.objects.create_user(**user_data)

        response = self.client.login(**user_data)
