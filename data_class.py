import typing
import json
from typing import NamedTuple
from dataclasses import dataclass
from collections import namedtuple

# Data Class com NamedTuple
class Coordinate(NamedTuple):
    lat:float
    lon:float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
    
#Data class com @dataclass
@dataclass(frozen=True)    
class Coordinate2:
    lat:float
    lon:float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
    
# Data class com collections namedtuple
City = namedtuple('City','name country population coordinates')

Coordinate3 = namedtuple('Coordinate','lat lon reference', defaults=['WGS84'])

# Classes e metodos para hacking namedtuple injetando um metodo
Card = namedtuple('Card','rank suit')

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank,suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self,position):
        return self._cards[position]
    
def spades_high(card):
    rank_value=FrenchDeck.ranks.index(card.rank)
    suit_value = card.suit_values[card.suit]
    return rank_value*len(card.suit_values) + suit_value

# Hacking a namedtuple to inject a method
Card.suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
Card.overall_rank = spades_high

if __name__=='__main__':
    # Criando uma instancia e printando
    t = Coordinate(55.8000,37.6000)
    print(t)

    # Verificando se Coordinate é subclasse de tuple
    print(issubclass(Coordinate, tuple))

    # Criando uma instancia de Coordinate2 e printando
    t2 = Coordinate2(55.8000,37.6000)
    print(t2)

    # Criando uma instancia de City e printando
    tokyo = City('Tokyo','JP',36.933,(35.689722,139.691667))
    print(tokyo)
    print(tokyo.population)
    print(tokyo.coordinates)
    print(tokyo[1])

    # Verificando os campos de City
    print(City._fields)

    # Verificando os campos padrão de Coordinate3
    print(Coordinate3._field_defaults)

    delhi_data = ('Delhi NCR','IN',21.935,Coordinate3(28.613889,77.208889))
    delhi = City._make(delhi_data)
    print(delhi._asdict())
    print(json.dumps(delhi._asdict()))

    # Testando o hacking para injetar um metodo no data class namedtuple
    lowest_card = Card('2','clubs')
    highest_card = Card('A','spades')
    print(lowest_card.overall_rank())
    print(highest_card.overall_rank())