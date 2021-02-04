"""Simple Take 6 Implementation."""

from dataclasses import dataclass
from typing import List, Optional
import random

from tabulate import tabulate
import fire


@dataclass
class Card:
    """Card"""

    value: int
    points: int = None

    def __post_init__(self):
        if self.value == 55:
            self.points = 7
        elif self.value % 11 == 0:
            self.points = 5
        elif self.value % 10 == 0:
            self.points = 3
        elif self.value % 5 == 0:
            self.points = 2
        else:
            self.points = 1

    def __repr__(self):
        return f"Card({self.value}, {'*' * self.points})"


class Table:
    """Table."""

    def __init__(self, cards: List[Card], max_len: int = 5):
        self.stacks: List[List[Card]] = [[card] for card in sorted(cards, key=lambda card: card.value)]
        self.max_len = max_len

    def __str__(self) -> str:
        return tabulate({f"Stack {idx}": self.stacks[idx] for idx in range(len(self.stacks))})

    @property
    def heads(self) -> List[Card]:
        return [stack[-1] for stack in self.stacks]

    def get_insert_stack_idx(self, card: Card) -> Optional[int]:
        """Get stack index of insertion."""
        best_idx, best_diff = None, None
        for idx, stack in enumerate(self.stacks):
            diff = card.value - stack[-1].value
            if diff > 0 and (best_diff is None or diff < best_diff):
                best_idx, best_diff = idx, diff
        return best_idx

    def get_lowest_stack_idx(self) -> int:
        """Get stack index with lowest number of points."""
        best_idx, best_points = None, None
        for idx, stack in enumerate(self.stacks):
            points = sum(card.points for card in stack)
            if best_points is None or points < best_points:
                best_idx, best_points = idx, points
        return best_idx

    def add(self, card: Card) -> int:
        """Add card and return points lost."""
        # Find insertion stack (closest or lowest number of points)
        insert_stack_idx = self.get_insert_stack_idx(card)
        if insert_stack_idx is None:
            insert_stack_idx = self.get_lowest_stack_idx()
        stack = self.stacks[insert_stack_idx]

        # Add or empty insert stack
        if len(stack) >= self.max_len or stack[-1].value > card.value:
            self.stacks[insert_stack_idx] = [card]
            points = sum(card.points for card in stack)
        else:
            stack.append(card)
            points = 0

        return points


@dataclass
class Player:
    """Base Player class."""

    name: str
    cards: List[Card]
    points: int = 0

    def __post_init__(self):
        self.cards = sorted(self.cards, key=lambda card: card.value)

    def play(self, table: Table):
        raise NotImplementedError()


@dataclass
class BaselinePlayer(Player):
    """Baseline Player. Plays the lowest possible card."""

    def play(self, table: Table):
        """Make one move."""
        best_idx = 0
        for idx, card in enumerate(self.cards):
            insert_stack_idx = table.get_insert_stack_idx(card)
            if insert_stack_idx is None or len(table.stacks[insert_stack_idx]) >= table.max_len:
                continue
            best_idx = idx
            break
        return self.cards.pop(best_idx)


class InteractivePlayer(Player):
    """Interactive Player."""

    def play(self, table: Table):
        """Make one move."""
        print("Table:")
        print(table)
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


def main(name: str = "Me", num_players: int = 3):
    """Launch a new game."""
    play = "y"
    while play == "y":
        # Initialize the game
        deck = [Card(idx + 1) for idx in range(104)]
        random.shuffle(deck)
        table = Table([deck.pop() for _ in range(4)])
        players = [
            BaselinePlayer(name=f"Player {idx}", cards=[deck.pop() for _ in range(10)])
            for idx in range(num_players - 1)
        ]
        players.append(InteractivePlayer(name=name, cards=[deck.pop() for _ in range(10)]))

        # Play the 10 rounds
        for _ in range(10):
            print("=" * 80)
            cards = [player.play(table) for player in players]
            for card, player in sorted(zip(cards, players), key=lambda it: it[0].value):
                print(f"- {player.name} plays {card}")
                player.points += table.add(card)
                print(table)
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
