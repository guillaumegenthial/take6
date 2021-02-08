from dataclasses import dataclass
from typing import List, Optional

from tabulate import tabulate


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


class Board:
    """Board."""

    def __init__(self, cards: List[Card], max_len: int = 5):
        self.stacks: List[List[Card]] = [[card] for card in sorted(cards, key=lambda card: card.value)]
        self.max_len = max_len

    def __str__(self) -> str:
        return tabulate({f"Stack {idx}": self.stacks[idx] for idx in range(len(self.stacks))})

    def get_insert_stack_idx(self, card: Card) -> Optional[int]:
        """Get stack index of insertion."""
        best_idx, best_diff = None, None
        for idx, stack in enumerate(self.stacks):
            diff = card.value - stack[-1].value
            if diff > 0 and (best_diff is None or diff < best_diff):
                best_idx, best_diff = idx, diff
        return best_idx

    def get_best_stack_idx(self) -> int:
        """Get stack index with lowest number of points."""
        best_idx, best_points = None, None
        for idx, stack in enumerate(self.stacks):
            points = sum(card.points for card in stack)
            if best_points is None or points < best_points:
                best_idx, best_points = idx, points
        return best_idx

    def step(self, card: Card) -> int:
        """Add card and return points lost."""
        # Find insertion stack (closest or lowest number of points)
        insert_stack_idx = self.get_insert_stack_idx(card)
        if insert_stack_idx is None:
            insert_stack_idx = self.get_best_stack_idx()
        stack = self.stacks[insert_stack_idx]

        # Add or empty insert stack
        if len(stack) >= self.max_len or stack[-1].value > card.value:
            self.stacks[insert_stack_idx] = [card]
            points = sum(card.points for card in stack)
        else:
            stack.append(card)
            points = 0

        return points
