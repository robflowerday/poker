from collections import namedtuple
from random import randint

Card = namedtuple('Card', ['suit', 'rank'])


class Deck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def deal_rand_card(self):
        return self._cards.pop(randint(0, len(self._cards) - 1))