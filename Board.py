from dataclasses import dataclass, field
from deck import Deck
from card import Card

@dataclass
class Board:
    deck: Deck = field(default_factory=Deck)
    community_cards: list[Card] = field(default_factory=list)

    