from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker

from game_hub.accounts.models import GameHubUser
from game_hub.games.models import Game, Comment, LikeGame


class TestGameCreateModel(TestCase):

    def test_game_title_validator_only_letters_numbers_and_underscore_with_valid_data(self):
        game = baker.make(Game)
        game.title = 'Wow'

        self.assertEqual('Wow', game.title)

    def test_game_title_validator_only_letters_numbers_and_underscore_with_invalid_data_contain_sign_percent(self):
        game = baker.make(Game)
        game.title = 'Wow%'

        with self.assertRaises(ValidationError) as context:
            game.full_clean()
            game.save()

        self.assertIsNotNone(context.exception)


class TestCommentModel(TestCase):
    def setUp(self) -> None:
        self.test_user = GameHubUser(
            email='pesho@abv.bg',
            password=123
        )

    def test_create_comment_with_valid_data(self):
        comment = Comment(
            comment='Hello'
        )

        self.assertEqual('Hello', comment.comment)

    def test_create_comment_with_invalid_data_contain_sign_percent(self):
        comment = Comment(
            comment='Hello%',
            user=self.test_user)

        with self.assertRaises(ValidationError) as context:
            comment.full_clean()
            comment.save()

            self.assertIsNotNone(context.exception)


class TestLikeModel(TestCase):

    def setUp(self) -> None:
        self.test_user = GameHubUser(
            email='pesho@abv.bg',
            password=123
        )
        self.test_game = Game(
            title='Wow',
            category='Action',
            max_level=5,
            description='!!!',
        )

    def test_create_like(self):
        like = LikeGame(
            user=self.test_user,

        )

        self.assertIsNotNone(like)
