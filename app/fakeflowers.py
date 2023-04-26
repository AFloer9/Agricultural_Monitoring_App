# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

import random
from faker import Faker

fake = Faker()
fake_plant = Faker()
fake_supply = Faker()
fake_user = Faker()
fake_senspr = Faker()

from faker.providers import BaseProvider

class SeedProvider(BaseProvider):
    def seed(self):
        seed = ['sunflower', 'zinnia', 'pansy']
        
        return random.choice(seed)

fake.add_provider(SeedProvider)
fake.seed