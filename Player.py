from dataclasses import dataclass, field
from card import Card, Rank, Suit

@dataclass
class Player:
    name: str = ""
    hole_cards: list[Card] = field(default_factory=list)


    
