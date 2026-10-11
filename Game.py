from dataclasses import dataclass, field
from board import Board
from player import Player
from card import Card

MAX_PLAYERS = 10

@dataclass
class Game:
    board: Board
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

    def set_hole_cards(self, name: str, hole_cards: list[Card]) -> None:
        if len(hole_cards) != 2:
            raise ValueError("Each player must have two starting cards")
        for card in hole_cards:
            if not self.board.deck.__contains__(card):
                raise ValueError(f"Card {card} already exists in another hand")
        found = False
        for p in self.players:
            if p.name == name:
                found = True
        if found:
            p.hole_cards = hole_cards
            self.board.deck.remove(hole_cards)
        else:
            raise ValueError(f"Player with name {name} has not been added")

        

