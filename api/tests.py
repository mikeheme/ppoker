from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Game, GameError
from .factories import GameFactory, UserFactory


class TestGame(TestCase):

    def setUp(self):
        GameFactory(name='mygame')

    def test_start_game_with_all_players(self):
        game = Game.objects.get(name='mygame')
        users = UserFactory.create_batch(6)
        game.start_game(users, 500, 1000, 20000)
        self.assertListEqual([p.user for p in game.players.all()], users)

    def test_start_game_with_too_many_users_fails(self):
        game = Game.objects.get(name='mygame')
        users = UserFactory.create_batch(11)
        with self.assertRaises(GameError):
            game.start_game(users, 500, 1000, 20000)

    def test_start_game_with_max_10_players_succeeds(self):
        game = Game.objects.get(name='mygame')
        users = UserFactory.create_batch(10)
        game.start_game(users, 500, 1000, 20000)
        self.assertEqual(game.state, game.GameState.INITIALIZED)



