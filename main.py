# main.py
from board import Board
from player import Player
from game import Game
from card import Card, Rank, Suit

def main():
    game = Game(board=Board())
    game.add_player("Player 1")
    game.add_player("Player 2")
    game.set_hole_cards("Player 1", [Card.from_string("AS"), Card.from_string("KS")])
    game.set_hole_cards("Player 2", [Card.from_string("JS"), Card.from_string("QH")])

if __name__ == "__main__":
    main()