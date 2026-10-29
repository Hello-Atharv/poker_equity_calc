from dataclasses import dataclass, field
from board import Board
from player import Player
from card import Card
from calc import Calc, PlayerEquity

MAX_PLAYERS = 10

@dataclass
class Game:
    board: Board
    calc: Calc
    players: list[Player] = field(default_factory=list)

    def add_player(self, name:str) -> Player:
        name = name.strip()
        if not name:
            raise ValueError("Player name cannot be empty")
        if any(p.name.lower() == name.lower() for p in self.players):
            raise ValueError(f"Player named {name} already exists")
        if len(self.players) >= MAX_PLAYERS:
            raise ValueError(f"Table is full ({MAX_PLAYERS} max capacity)")

        player = Player(name = name)
        self.players.append(player)
        return player

    def get_player(self, name: str) -> Player:
        for p in self.players:
            if p.name.lower() == name.strip().lower():
                return p
        raise ValueError(f"Player with name {name} has not been added")

    def set_hole_cards(self, name: str, hole_cards: list[Card]) -> None:
        if len(hole_cards) != 2:
            raise ValueError("Each player must have two starting cards")
        if len(set(hole_cards)) != 2:
            raise ValueError("Hole cards must be two different cards")
        player = self.get_player(name)
        # a player's current cards are free to be re-dealt to them
        available = set(self.board.deck) | set(player.hole_cards)
        for card in hole_cards:
            if card not in available:
                raise ValueError(f"Card {card} is already in another hand or on the board")
        self.board.deck.add(player.hole_cards)
        self.board.deck.remove(hole_cards)
        player.hole_cards = hole_cards

    def set_community_cards(self, cards: list[Card]) -> None:
        self.board.set_community_cards(cards)

    def calculate_equity(self) -> dict[str, PlayerEquity]:
        return self.calc.calculate_equity(players = self.players, deck = self.board.deck, community_cards = self.board.community_cards)
