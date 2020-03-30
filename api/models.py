import itertools
import uuid
import random
from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class GameError(Error):
    """Exception raised for Gaming errors.

    Attributes:
        state -- the current state of the game
        message -- explanation of the error
    """

    def __init__(self, state, message):
        self.state = state
        self.message = message


def parse_card_deck(deck_str):
    """
    Takes a string representation of a deck and creates a CardDeck object

    This parser transforms a space separated string to a CardDeck that takes in
    a list of Tuples. Cards are only 2 or 3 chars in length, for example, A♢ or 10♠.
    so we need to handle those two cases separately when creating the tuples.
    """
    cards = deck_str.split(' ')
    return CardDeck([tuple(x) if len(x) == 2 else (x[0:2], x[2]) for x in cards])


class CardDeckField(models.CharField):
    """
    Field that represents the 52 cards in a deck.

    String representation: 'A♠ A♡ A♢ A♣ 2♠ 2♡ 2♢ 2♣ 3♠ 3♡ 3♢ 3♣ ...'
    Object representation: Class CardDeck
    """
    description = "A field to save the representation of the 52 cards in a deck"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return parse_card_deck(value)

    def to_python(self, value):
        if isinstance(value, CardDeck):
            return value

        if value is None:
            return value

        return parse_card_deck(value)

    def get_prep_value(self, value):
        return str(value)


class GameState(Enum):
    NOT_STARTED = 'NOT_STARTED'
    INITIALIZED = 'INITIALIZED'
    USER_CARDS_DEALT = 'USER_CARDS_DEALT'
    FLOP_DEALT = 'FLOP_DEALT'
    TURN_DEALT = 'TURN_DEALT'
    RIVER_DEALT = 'RIVER_DEALT'


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    chips = models.PositiveIntegerField(default=0)
    sit_num = models.PositiveSmallIntegerField(default=0)
    is_admin = models.BooleanField(default=False)


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)
    players = models.ManyToManyField(Player)
    deck = CardDeckField(max_length=160, null=True)
    small_blind = models.PositiveIntegerField(default=0)
    big_blind = models.PositiveIntegerField(default=0)
    starting_chips = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=40, default=GameState.NOT_STARTED,
                             choices=[(tag, tag.value) for tag in GameState])
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def start_game(self, users, small_blind, big_blind, starting_chips):
        if self.state != GameState.NOT_STARTED:
            raise GameError(self.state, "Game has already started")

        self.small_blind = small_blind
        self.big_blind = big_blind
        self.starting_chips = starting_chips
        self.is_active = True
        self.state = GameState.INITIALIZED
        users.append(self.created_by)
        for sit, user in enumerate(users):
            player = Player.objects.create(
                user=user,
                is_admin=True if user == self.created_by else False,
                chips=self.starting_chips,
                sit_num=sit
            )
            player.save()
            self.players.add(player)
        self.deck = CardDeck()
        return self.save()

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

    DENOMINATIONS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, deck=None):
        if deck:
            # TODO: Validate deck
            self.deck = deck
        else:
            self.deck = self.new_deck()

    def shuffle(self):
        random.shuffle(self.deck)

    def new_deck(self):
        return list(itertools.product(
            self.DENOMINATIONS, [self.SUIT_SPADE, self.SUIT_HEART, self.SUIT_DIAMOND, self.SUIT_CLUB]))

    def __str__(self):
        return " ".join(["{0[0]}{0[1]}".format(c) for c in self.deck])
