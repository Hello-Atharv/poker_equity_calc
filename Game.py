from dataclasses import dataclass, field
from board import Board
from player import Player

@dataclass
class Game:
    num_players: int
    board: Board
    players: list[Player] = [Player() for _ in range(num_players)]

