import itertools
import uuid
import random

from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, null=True)
    is_active = models.BooleanField(default=False)
    viewers = models.ManyToManyField(User, related_name='rooms_viewers')
    players = models.ManyToManyField(User, related_name='rooms_players')
    deck = models.CharField(max_length=1000, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def start_game(self):
        pass

    def add_user(self):
        pass

    def remove_user(self):
        pass

    def sit_user(self):
        pass

    def stand_user(self):
        pass

    def set_game_admin(self):
        pass

    def deal_user_cards(self):
        pass

    def deal_flop(self):
        pass

    def deal_turn(self):
        pass

    def deal_river(self):
        pass


class CardDeck:

    SUIT_SPADE = '\u2660'
    SUIT_CLUB = '\u2663'
    SUIT_HEART = '\u2661'
    SUIT_DIAMOND = '\u2662'

    def __init__(self):
        self.reset()

    def shuffle(self):
        random.shuffle(self.deck)

    def reset(self):
        self.deck = list(itertools.product(
            range(1, 14), [self.SUIT_SPADE, self.SUIT_HEART, self.SUIT_DIAMOND, self.SUIT_CLUB]))

    def __str__(self):
        print(["{0[0]}{0[1]}".format(c) for c in self.deck])
