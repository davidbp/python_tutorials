import random
from collections import namedtuple

Couple = namedtuple('Couple', ['female', 'male'])#, verbose=False)


def create_couples(n_couples:int):
    couples = []

    for n in range(n_couples):
        couple = Couple(random.randint(70_000,200_000),random.randint(70_000,200_000))
        couples.append(couple)
    return couples

couples = create_couples(100_0000)


def py_count_women_earning_more(couples):
    count = 0
    for c in couples:
        count += c.female > c.male
    return count
