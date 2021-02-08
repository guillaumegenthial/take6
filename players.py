from dataclasses import dataclass
from typing import List
import random

from classes import Card, Board

@dataclass
class Player:
    """Base Player class."""

    name: str
    cards: List[Card]
    points: int = 0

    def __post_init__(self):
        self.cards = sorted(self.cards, key=lambda card: card.value)

    def play(self, board: Board):
        raise NotImplementedError()


class RandomPlayer(Player):
    """Random Player."""

    def play(self, board: Board):
        """Make one move."""
        return self.cards.pop(random.randint(0, len(self.cards) - 1))


class BaselinePlayer(Player):
    """Baseline Player. Plays the lowest possible card."""

    def play(self, board: Board):
        """Make one move."""
        best_idx = 0
        for idx, card in enumerate(self.cards):
            insert_stack_idx = board.get_insert_stack_idx(card)
            if insert_stack_idx is None or len(board.stacks[insert_stack_idx]) >= board.max_len:
                continue
            best_idx = idx
            break
        return self.cards.pop(best_idx)


class InteractivePlayer(Player):
    """Interactive Player."""

    def play(self, board: Board):
        """Make one move."""
        print("Board:")
        print(board)
        print("My cards:")
        for idx, card in enumerate(self.cards):
            print(f"- {idx}: {card}")
        print("Which card do you want to play?")
        best_idx = None
        while best_idx is None:
            try:
                best_idx = int(input())
                if best_idx >= len(self.cards):
                    best_idx = None
                    raise ValueError()
            except ValueError:
                print("Incorrect Value. Please try again")
        return self.cards.pop(best_idx)
