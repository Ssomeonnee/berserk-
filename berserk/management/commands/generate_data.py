from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from django.contrib.auth import get_user_model
import random

User = get_user_model()

from berserk.models import BerserkCreature, BerserkGeography, BerserkCharacter, BerserkArmy, BerserkArtifact


class Command(BaseCommand):
    def handle(self, *args, **options):

        users = User.objects.all()
        random_user = random.choice(list(users)) 

        fake = Faker(['ru_RU'])
        for _ in range(300):
           
            random_user = random.choice(list(users)) 

            BerserkArtifact.objects.create(
                name = fake.name(),
                description = fake.text(),
                harm_to = BerserkCreature.objects.create(name=fake.name(),description = fake.text()),
                inventor = BerserkCharacter.objects.create(                name = fake.name(),                jap_name = fake.name(),                eng_name = fake.name(),                creature = BerserkCreature.objects.create(name=fake.name(),description = fake.text()),                qoute = fake.text(),                description = fake.text(),                army = BerserkArmy.objects.create(name = fake.name(), description = fake.text(),geography = BerserkGeography.objects.create( name=fake.name(), description = fake.text())),                user = random_user),
                owner = BerserkCharacter.objects.create(                name = fake.name(),                jap_name = fake.name(),                eng_name = fake.name(),                creature = BerserkCreature.objects.create(name=fake.name(),description = fake.text()),                qoute = fake.text(),                description = fake.text(),                army = BerserkArmy.objects.create(name = fake.name(), description = fake.text(),geography = BerserkGeography.objects.create( name=fake.name(), description = fake.text())),                user = random_user))
