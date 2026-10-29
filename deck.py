from dataclasses import dataclass, field
from collections.abc import Iterable, Iterator
from card import Card, Suit, Rank

def full_deck() -> list[Card]:
    return [Card(r, s) for s in Suit for r in Rank]

@dataclass
class Deck:
    cards: list[Card] = field(default_factory = full_deck)

    def __post_init__(self):
        if len(set(self.cards)) != len(self.cards):
            raise ValueError("Deck contains duplicate cards")

    def remove(self, cards: Iterable[Card]) -> None:
        to_remove = set(cards)
        missing = to_remove.difference(self.cards)
        if missing:
            names = ", ".join(sorted(str(c) for c in missing))
            raise ValueError(f"Not in deck: {names}")
        self.cards = [c for c in self.cards if c not in to_remove]

    def add(self, cards: Iterable[Card]) -> None:
        to_add = list(cards)
        duplicates = set(to_add).intersection(self.cards)
        if duplicates or len(set(to_add)) != len(to_add):
            raise ValueError("Cannot add cards already in the deck")
        self.cards.extend(to_add)

# utilities --------------------------------------------------------------------------------

    def copy(self) -> "Deck":
        return Deck(self.cards.copy())

    def __str__(self) -> str:
        return " ".join(str(c) for c in self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def __contains__(self, card: Card) -> bool:
        return card in self.cards

