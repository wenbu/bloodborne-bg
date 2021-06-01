import unittest
from cards.deck import Deck


class DeckTest(unittest.TestCase):
    def test_draw(self):
        """Should not be able to draw more cards than the deck has."""
        deck_size = 3
        d = Deck(deck_size)
        for _ in range(deck_size):
            d.draw()
        self.assertRaises(ValueError, d.draw)
        d.shuffle_in([1])
        d.draw()
        self.assertRaises(ValueError, d.draw)

    def test_discard(self):
        """Should be able to draw cards after they have been discarded."""
        deck_size = 3
        d = Deck(deck_size)
        for _ in range(deck_size):
            d.draw()
        d.discard([1, 3])
        drawn = d.draw(2)
        self.assertEqual(len(drawn), 2)
        self.assertIn(1, drawn)
        self.assertIn(3, drawn)


if __name__ == '__main__':
    unittest.main()
