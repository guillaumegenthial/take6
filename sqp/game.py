"""Game Implementation."""

from typing import List, Union
import random

from tabulate import tabulate


class Card:
    """Card"""

    def __init__(self, value: int, points: int = None):
        self.value = value
        self.points = points if points is not None else 1

    def __repr__(self) -> str:
        return f"Card({self.value})"


class Deck:
    """Deck."""

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __repr__(self):
        return repr(self.cards)

    @property
    def size(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def take(self, k: int = 1) -> Union[List[Card], Card]:
        if self.size < k:
            raise ValueError(f"Cannot take {k} cards from deck of size {self.size}")
        result = self.cards[:k]
        self.cards = self.cards[k:]
        return result if k > 1 else result[0]


class State:
    """State of the game."""

    def __init__(self, cards: List[Card], max_len: int = 5):
        self.stacks: List[List[Card]] = [[card] for card in cards]
        self.max_len = max_len

    def __str__(self) -> str:
        return tabulate({f"Stack {idx}": self.stacks[idx] for idx in range(len(self.stacks))})

    @property
    def heads(self) -> List[Card]:
        return [stack[-1] for stack in self.stacks]

    def add(self, card: Card, stack: int = 0) -> int:
        """Add card and return points lost."""
        # Find which stack the card should go
        best_stack, best_diff = None, None
        for idx, head in enumerate(self.heads):
            diff = card.value - head.value
            if diff > 0 and (best_stack is None or diff < best_diff):
                best_stack, best_diff = idx, diff

        # Handle case where no stack is valid
        if best_stack is None:
            best_stack, best_points = None, None
            for idx, stack in enumerate(self.stacks):
                points = sum(card.points for card in stack)
                if best_points is None or points < best_points:
                    best_stack, best_points = idx, points

            cards = self.stacks[best_stack]
            self.stacks[best_stack] = [card]
            return sum(card.points for card in cards)

        # Insert card in the stack
        cards = self.stacks[best_stack]
        if len(cards) >= self.max_len:
            self.stacks[best_stack] = [card]
            return sum(card.points for card in cards)
        else:
            cards.append(card)

        return 0


class BaselinePlayer:
    """Baseline Player."""

    def __init__(self, cards: List[Card]):
        self.cards = sorted(cards, key=lambda card: card.value)
        self.points = 0

    def __repr__(self):
        return "Baseline"

    def play(self, state):
        """Make one move."""
        best_card_no = None
        for card_no, card in enumerate(self.cards):
            # Find which stack the card should go
            best_stack, best_diff = None, None
            for idx, head in enumerate(state.heads):
                diff = card.value - head.value
                if diff > 0 and (best_stack is None or diff < best_diff):
                    best_stack, best_diff = idx, diff

            # Move to the next card if no stack or full stack
            if best_stack is None or len(state.stacks[best_stack]) >= state.max_len:
                continue

            best_card_no = card_no
            break

        best_card_no = 0 if best_card_no is None else best_card_no
        best_card = self.cards[best_card_no]
        self.cards.pop(best_card_no)
        return best_card


class InteractivePlayer:
    """Interactive Player."""

    def __init__(self, cards: List[Card]):
        self.cards = sorted(cards, key=lambda card: card.value)
        self.points = 0

    def __repr__(self):
        return "Me"

    def play(self, state):
        """Make one move."""
        print("State:")
        print(state)
        print("My cards:")
        for idx, card in enumerate(self.cards):
            print(f"- {idx}: {card}")
        print("Which card do you want to play?")
        best_card_no = None
        while best_card_no is None:
            try:
                best_card_no = int(input())
                if best_card_no >= len(self.cards):
                    best_card_no = None
                    raise ValueError()
            except Exception:
                print("Please try again")
        best_card = self.cards[best_card_no]
        self.cards.pop(best_card_no)
        return best_card


if __name__ == "__main__":
    deck = Deck([Card(idx) for idx in range(103)])
    deck.shuffle()
    state = State(deck.take(4))
    players = [
        BaselinePlayer(deck.take(10)),
        BaselinePlayer(deck.take(10)),
        InteractivePlayer(deck.take(10)),
    ]
    for _ in range(10):
        print("=" * 80)
        cards = [player.play(state) for player in players]
        for card, player in sorted(zip(cards, players), key=lambda it: it[0].value):
            player.points += state.add(card)
        print("Points:")
        for player in players:
            print(f"- {player}: {player.points}")

    print("=" * 80)
    for idx, player in enumerate(sorted(players, key=lambda player: player.points)):
        if idx == 0:
            print(f"- {player}: {player.points} (WINNER)")
        else:
            print(f"- {player}: {player.points}")
