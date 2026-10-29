from dataclasses import dataclass, field
from deck import Deck
from card import Card

VALID_BOARD_SIZES = (0, 3, 4, 5)
BOARD_SIZE = max(VALID_BOARD_SIZES)

@dataclass
class Board:
    deck: Deck = field(default_factory=Deck)
    community_cards: list[Card] = field(default_factory=list)

    def set_community_cards(self, cards:list[Card]):
        if len(cards) not in VALID_BOARD_SIZES:
            raise ValueError("Board must have 0, 3, 4, 5 cards")
        if len((set(cards))) != len(cards):
            raise ValueError("Board cannot have duplicate cards")
        available = set(self.deck) | set(self.community_cards)

        for card in cards:
            if card not in available:
                raise ValueError(f"Card {card} is already in a hand")
        self.deck.add(self.community_cards)
        self.deck.remove(cards)
        self.community_cards = list(cards)

    