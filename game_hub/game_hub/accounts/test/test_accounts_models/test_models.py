from model_bakery import baker
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from game_hub.accounts.models import Profile

GameHubUser = get_user_model()


class TestGameHubUserModel(TestCase):

    def test_create_user_with_valid_email(self):
        user = GameHubUser(
            email='ivo@abv.bg',
            password='123'
        )

        self.assertEqual('ivo@abv.bg', user.email)

    def test_create_user_with_invalid_email_expect_rise_exception(self):
        user = GameHubUser(
            email='ivoabv.bg',
            password='123'
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
            user.save()

        self.assertIsNotNone(context.exception)


class TestProfileModel(TestCase):

    def test_create_profile_with_valid_data(self):
        profile = baker.make(Profile)
        profile.first_name = 'pesho'

        self.assertEqual('pesho', profile.first_name)

    def test_create_profile_with_invalid_first_name_that_contain_sign_percent_expect_raise_exception(self):
        profile = baker.make(Profile)
        profile.first_name = 'pesho%'

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_create_profile_with_invalid_last_name_that_contain_sign_percent_expect_raise_exception(self):
        profile = baker.make(Profile)
        profile.last_name = 'iliev%'

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)
