from dataclasses import dataclass, field
from player import Player
from deck import Deck
from card import Card, Rank, Suit

import random
import treys

@dataclass
class calc:

    def calculate_equity(self, players: list[Player], deck: Deck, community_cards: list[Card]) -> dict[str, float]:
        monte_carlo(n = 20000)
        return 

    def monte_carlo(self, )