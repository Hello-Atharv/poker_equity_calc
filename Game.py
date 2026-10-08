from Board import Board
from Player import Player

class Game:
    def __init__(self, num_players):
        self.num_players = num_players
        self.board = Board()
        self.players = [Player() for _ in range(num_players)]

        