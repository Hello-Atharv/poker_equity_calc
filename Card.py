from dataclasses import dataclass
from enum import Enum

class Suit(Enum):
    CLUBS = "C"
    DIAMONDS = "D"
    HEARTS = "H"
    SPADES = "S"

class Rank(Enum):
    TWO = 2; THREE = 3; FOUR = 4; FIVE = 5; SIX = 6; SEVEN = 7; EIGHT = 8; NINE = 9; TEN = 10; JACK = 11; QUEEN = 12; KING = 13; ACE = 14

RANK_CHARS = {c: Rank(v) for c, v in zip("23456789TJQKA", range(2, 15))}

@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def __post_init__(self):
        if not isinstance(self.rank, Rank) or not isinstance(self.suit, Suit):
            raise TypeError("Card needs valid rank or suit")

    @classmethod
    def from_string(cls, input:str) -> "Card":
        input = input.strip().upper().replace("10", "T")
        if len(input) != 2:
            raise ValueError(f"{input} should be two characters")
        r = input[0]
        s = input[1]
        if r not in RANK_CHARS:
            raise ValueError("Invalid rank")
        try:
            suit = Suit(s)
        except ValueError:
            raise ValueError("Invalid suit") from None
        return cls(RANK_CHARS[r], suit)

    def __str__(self):
        return f"{'23456789TJQKA'[self.rank.value-2]}{self.suit.value}"

    