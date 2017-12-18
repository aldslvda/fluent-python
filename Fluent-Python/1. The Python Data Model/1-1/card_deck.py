"""
Pythonic card deck
"""
import collections
import random
Card = collections.namedtuple('Card', ['rank', 'suit'])
class FrenchDeck(object):
    """
    card deck
    """
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    def __len__(self):
        return len(self._cards)
    def __getitem__(self, position):
        return self._cards[position]
    def get_rand_card(self):
        """get a random card from deck"""
        return random.choice(self)

print FrenchDeck
'''
sort by a certain rule
'''
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
deck = FrenchDeck()
for card in sorted(deck, key=spades_high): # doctest: +ELLIPSIS
    print(card)
