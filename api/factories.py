import factory
from django.contrib.auth.models import User
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = email = factory.LazyAttribute(lambda a: f'{a.first_name}.{a.last_name}'.lower())
    email = factory.LazyAttribute(lambda a: f'{a.username}@example.com'.lower())
    is_staff = False
    is_active = True
    is_superuser = False


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Game

    name = factory.Sequence(lambda n: 'game%s' % n)
    created_by = factory.SubFactory(UserFactory)



