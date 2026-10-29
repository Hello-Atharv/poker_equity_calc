from dataclasses import dataclass, field
from player import Player
from deck import Deck
from card import Card, Rank, Suit
from board import BOARD_SIZE

import random
from treys import Card as TreysCard, Evaluator

DEFAULT_SIMULATIONS = 20000
_evaluator = Evaluator()

@dataclass(frozen=True)
class PlayerEquity:
    win: float     # share of runs won outright
    tie: float     # share of runs tied for the best hand
    equity: float  # win plus each tied pot split between its winners

@dataclass
class Calc:
    n: int = DEFAULT_SIMULATIONS
    seed: int | None = None

    def __post_init__(self):
        if self.n<1:
            raise ValueError("n must be at least 1")
        
    def calculate_equity(self, players: list[Player], deck: Deck, community_cards: list[Card]) -> dict[str, PlayerEquity]:
        """Monte Carlo win, tie and equity (ties split) per player, each 0.0 to 1.0."""
        self.validate(players, community_cards)

        # Board.set_community_cards already takes board cards out of the deck;
        # this keeps the result correct even if they were set by hand
        known = [c for p in players for c in p.hole_cards] + list(community_cards)
        seen = set(known)
        pool = [self.to_treys(c) for c in deck if c not in seen]
        board = [self.to_treys(c) for c in community_cards]
        hands = [[self.to_treys(c) for c in p.hole_cards] for p in players]

        if BOARD_SIZE - len(board) > len(pool):
            raise ValueError("Not enough cards left in the deck to finish the board")

        results = self.monte_carlo(hands, board, pool)
        return {p.name: result for p, result in zip(players, results)}

    def monte_carlo(self, hands: list[list[int]], board: list[int], pool: list[int]) -> list[PlayerEquity]:
        needed = BOARD_SIZE - len(board)
        n = self.n if needed > 0 else 1  # a full board has nothing left to randomise
        rng = random.Random(self.seed)
        wins = [0] * len(hands)
        ties = [0] * len(hands)
        shares = [0.0] * len(hands)
        for _ in range(n):
            full_board = board + rng.sample(pool, needed)
            scores = [_evaluator.evaluate(full_board, hand) for hand in hands]
            best = min(scores)  # treys: lower score is a better hand
            winners = [i for i, s in enumerate(scores) if s == best]
            for i in winners:
                shares[i] += 1 / len(winners)
                if len(winners) == 1:
                    wins[i] += 1
                else:
                    ties[i] += 1
        return [PlayerEquity(wins[i] / n, ties[i] / n, shares[i] / n) for i in range(len(hands))]

    @staticmethod
    def validate(players:list[Player], community_cards: list[Card])-> None:
        if len(players)<2:
            raise ValueError("Need at least two players for equity calculation")
        for p in players:
            if len(p.hole_cards) != 2:
                raise ValueError(f"{p.name} does not have two hole cards")
        if len(community_cards) > BOARD_SIZE:
            raise ValueError(f"Board cannot have more than {BOARD_SIZE} cards")
        known = [c for p in players for c in p.hole_cards] + list(community_cards)
        if len(set(known)) != len(known):
            raise ValueError("Duplicate cards across hands or board")
    
    @staticmethod
    def to_treys(card: Card) -> int:
        text = str(card)
        return TreysCard.new(text[0] + text[1].lower())
