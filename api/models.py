import itertools
import uuid
import random

from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, null=True)
    is_active = models.BooleanField(default=False)
    users = models.ManyToManyField(User, related_name='rooms')
    deck = models.CharField(max_length=1000, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class CardDeck:
    deck = None

    def __init__(self):
        self.initialize()

    def shuffle(self):
        random.shuffle(self.deck)

    def initialize(self):
        self.deck = list(itertools.product(
            range(1, 14), ['Spade', 'Heart', 'Diamond', 'Club']))
