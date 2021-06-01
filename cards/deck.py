import random
from typing import List, Sequence


class Deck:
    """
    A Deck consists of two piles of cards: the deck and the discard. Cards may be drawn from the deck or added to
    the discard.
    """

    def __init__(self, num_cards: int):
        self._num_cards_available: int = num_cards
        self._deck: List[int] = list(range(num_cards))
        self._discard: List[int] = []

    def current_deck_size(self) -> int:
        return len(self._deck)

    def shuffle(self) -> None:
        """Shuffle the remaining cards in the deck."""
        random.shuffle(self._deck)

    def reset(self) -> None:
        """The discard pile is shuffled and placed on the bottom of the deck."""
        new_deck = self._discard
        random.shuffle(new_deck)
        self._discard = []
        self._deck.extend(new_deck)

    def draw(self, num_cards: int = 1, auto_shuffle_discard: bool = True) -> Sequence[int]:
        """Draw num_cards from the deck, shuffling the discard if necessary."""
        if auto_shuffle_discard:
            num_cards_available = self._num_cards_available
        else:
            num_cards_available = len(self._deck)
        if num_cards > num_cards_available:
            raise ValueError('Number of cards to draw (%d) exceeds number of available cards in deck (%d).' %
                             (num_cards, num_cards_available))
        cards_drawn, self._deck = self._deck[:num_cards], self._deck[num_cards:]
        if len(cards_drawn) < num_cards:
            # It shouldn't be possible to come in here if auto_shuffle_discard is False.
            draw_remainder = num_cards - len(cards_drawn)
            self.reset()
            cards_drawn.extend(self._deck[:draw_remainder])
            self._deck = self._deck[draw_remainder:]
        self._num_cards_available -= num_cards
        return cards_drawn

    def discard(self, cards_to_discard: Sequence[int]):
        """Put cards_to_discard into the discard pile."""
        self._discard.extend(cards_to_discard)
        self._num_cards_available += len(cards_to_discard)

    def shuffle_in(self, cards_to_shuffle: Sequence[int]):
        """Shuffle cards_to_shuffle into the deck."""
        self._deck.extend(cards_to_shuffle)
        self.shuffle()
        self._num_cards_available += len(cards_to_shuffle)
