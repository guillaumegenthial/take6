"""Simple Take 6 Implementation."""


import random

import fire

from classes import Card, Board
from players import BaselinePlayer, InteractivePlayer

def main(name: str = "Me", num_players: int = 3):
    """Launch a new game."""
    play = "y"
    while play == "y":
        # Initialize the game
        deck = [Card(idx + 1) for idx in range(104)]
        random.shuffle(deck)
        board = Board([deck.pop() for _ in range(4)])
        players = [
            BaselinePlayer(name=f"Player {idx}", cards=[deck.pop() for _ in range(10)])
            for idx in range(num_players - 1)
        ]
        players.append(InteractivePlayer(name=name, cards=[deck.pop() for _ in range(10)]))

        # Play the 10 rounds
        for _ in range(10):
            print("=" * 80)
            cards = [player.play(board) for player in players]
            for card, player in sorted(zip(cards, players), key=lambda it: it[0].value):
                print(f"- {player.name} plays {card}")
                player.points += board.step(card)
                print(board)
            print("=" * 80)
            print("Points:")
            for player in players:
                print(f"- {player.name}: {player.points}")

        # Print results
        print("=" * 80)
        for idx, player in enumerate(sorted(players, key=lambda player: player.points)):
            if idx == 0:
                print(f"- {player.name}: {player.points} (WINNER)")
            else:
                print(f"- {player.name}: {player.points}")

        # Want to play another game?
        print("Do you want to play another game? (y/n)")
        answer = None
        while answer is None:
            answer = input()
            if answer not in {"y", "n"}:
                answer = None
                print("Try again, answer must be y/n")
        play = answer


if __name__ == "__main__":
    fire.Fire(main)
