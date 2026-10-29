# main.py
from board import Board
from player import Player
from game import Game
from card import Card, Rank, Suit
from calc import Calc
from rich.console import Console
from rich.table import Table

def print_equity_table(game: Game, equities: dict) -> None:
    board = " ".join(str(c) for c in game.board.community_cards) or "Pre-flop"
    table = Table(title=f"Board: {board}")
    table.add_column("Player")
    table.add_column("Hand")
    table.add_column("Win", justify="right")
    table.add_column("Tie", justify="right")
    table.add_column("Equity", justify="right")
    for player in game.players:
        eq = equities[player.name]
        hand = " ".join(str(c) for c in player.hole_cards)
        table.add_row(player.name, hand, f"{eq.win:.1%}", f"{eq.tie:.1%}", f"{eq.equity:.1%}")
    Console().print(table)

def main():
    game = Game(board=Board(), calc=Calc())
    game.add_player("Player 1")
    game.add_player("Player 2")
    game.set_hole_cards("Player 1", [Card.from_string(i) for i in ["AS", "KS"]])
    game.set_hole_cards("Player 2", [Card.from_string(i) for i in ["JS", "QH"]])
    game.set_community_cards([Card.from_string(i) for i in ["QS", "7C", "4H"]])
    equities = game.calculate_equity()
    print_equity_table(game, equities)

if __name__ == "__main__":
    main()