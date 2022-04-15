from django.contrib.auth import get_user_model

from django.test import TestCase
from django.urls import reverse

from game_hub.games.models import Game, Comment

GameUser = get_user_model()


class TestHomePageViews(TestCase):

    def test_home_view_should_be_rendering_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base/home_page.html')


class TestGameListViews(TestCase):

    def test_catalogue_list_view_with_login_user_expect_rendering_template(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        response = self.client.get(reverse('catalogue list'))

        self.assertTemplateUsed(response, 'game_templates/game_catalogue.html')

    def test_catalogue_list_view_listing_all_games(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }
        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        games = (
            Game(title='Wow', category='Action'),
            Game(title='Wow1', category='Action')
        )
        response = self.client.get(reverse('catalogue list'))

        self.assertTemplateUsed(response, 'game_templates/game_catalogue.html')
        self.assertEqual(len(games), 2)


class TestGameCreateView(TestCase):

    def test_game_create_view_rendering_crete_view_template(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        response = self.client.get(reverse('create game'))

        self.assertTemplateUsed(response, 'game_templates/game_create.html')

    def test_game_create_view_post_request(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        game_data = {
            'title': 'Wow',
            'category': 'Action',

        }
        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        self.client.post(reverse('create game'), data=game_data)

        game = Game.objects.get()

        self.assertIsNotNone(game)
        self.assertEqual(game_data['title'], game.title)
        self.assertEqual(game_data['category'], game.category)

    def test_game_create_view_redirect_to_correct_url_after_create_game(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        game_data = {
            'title': 'Wow',
            'category': 'Action',

        }
        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        response = self.client.post(reverse('create game'), data=game_data)

        expect_url = reverse('catalogue list')
        self.assertRedirects(response, expect_url)

    def test_create_view_return_correct_statuscode_after_create(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123',
        }
        game_data = {
            'title': 'Wow',
            'category': 'Action',
        }
        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        response = self.client.post(reverse('create game'), data=game_data)

        self.assertEqual(response.status_code, 302)


class TestGameDetailsView(TestCase):

    def test_rendering_game_details_view_by_pk(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        game_data = {
            'title': 'Wow',
            'category': 'Action',
        }

        user = GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        self.client.post(reverse('create game'), data=game_data)
        game = Game.objects.get()

        response = self.client.get(reverse('game details', kwargs={'pk': game.pk}))

        self.assertTemplateUsed(response, 'game_templates/game_detail.html')
        self.assertEqual(response.context['user'], user)
        self.assertEqual(response.context['game'], game)
        self.assertEqual(response.context['is_owner'], True)


class TestGameEditView(TestCase):

    def test_rendering_game_edit_view_with_valid_data(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        game_data = {
            'title': 'Wow',
            'category': 'Action',
        }

        game_edit_data = {
            'title': 'Woww',
            'category': 'Action',
        }

        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)
        self.client.post(reverse('create game'), data=game_data)
        game = Game.objects.get()
        response = self.client.post(reverse('game edit', kwargs={'pk': game.pk}), data=game_edit_data)
        edit_game = Game.objects.get()
        expected_url = reverse('my games')

        self.assertRedirects(response, expected_url)
        self.assertEqual('Woww', edit_game.title)


class TestGameDeleteView(TestCase):

    def test_game_delete_view_delete_game_by_pk_correct(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123'
        }

        game_data = {
            'title': 'Wow',
            'category': 'Action',
        }

        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        self.client.post(reverse('create game'), data=game_data)

        game = Game.objects.get()
        self.client.delete(reverse('delete game', kwargs={'pk': game.pk}))
        deleted_game = Game.objects.filter(pk=game.pk)
        self.assertQuerysetEqual(deleted_game, [])


class TestMyGamesListView(TestGameDeleteView):

    def test_my_games_view_list_all_games_created_from_user(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123',
        }

        game_data = {
            'title': 'Wow',
            'category': 'Action',
        }
        game_data1 = {
            'title': 'Dota',
            'category': 'Action',
        }

        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        self.client.post(reverse('create game'), data=game_data)
        self.client.post(reverse('create game'), data=game_data1)
        my_games = Game.objects.all()

        self.assertEqual(len(my_games), 2)


class TestCreateCommentView(TestCase):

    def test_create_comment_with_valid_data(self):
        user_data = {
            'email': 'sofi@abv.bg',
            'password': '123',
        }
        comment_data = {
            'comment': 'Hello'
        }
        game_data = {
            'title': 'Wow',
            'category': 'Action',
        }

        GameUser.objects.create_user(**user_data)
        self.client.login(**user_data)

        self.client.post(reverse('create game'), data=game_data)
        game = Game.objects.get()
        response = self.client.post(reverse('create comment', kwargs={'pk': game.pk}), data=comment_data)
        comment = Comment.objects.get()

        self.assertEqual(comment.comment, 'Hello')
        self.assertEqual(response.status_code, 302)
