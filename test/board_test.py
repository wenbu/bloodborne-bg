import unittest
from board import Board, MapTile, UP, LEFT, RIGHT, DOWN
from tiles import BASE


class BoardTest(unittest.TestCase):
    def test_board(self):
        central_lamp_tile = MapTile(BASE['central_lamp'])
        cl1, cl2, cl3 = central_lamp_tile.get_spaces()
        board = Board(central_lamp_tile)

        moves = board.get_valid_moves(cl1)
        self.assertEqual(1, len(moves))
        self.assertIn(cl2, moves)
        moves = board.get_valid_moves(cl2)
        self.assertEqual(2, len(moves))
        self.assertIn(cl1, moves)
        self.assertIn(cl3, moves)
        moves = board.get_valid_moves(cl3)
        self.assertEqual(1, len(moves))
        self.assertIn(cl2, moves)

    def test_add_tile(self):
        central_lamp_tile = MapTile(BASE['central_lamp'])
        oedon_chapel_tile = MapTile(BASE['oedon_chapel'])
        cl1, cl2, cl3 = central_lamp_tile.get_spaces()
        oc1, oc2, oc3 = oedon_chapel_tile.get_spaces()
        board = Board(central_lamp_tile)
        board.add_tile(central_lamp_tile, LEFT, oedon_chapel_tile)
        """
        Board should look like this now:
        +--------E--------+  +-----+--E--+-----+
        |                 |  |     |     |     |
        |                 |  |     |     |     |
        +--------+--------+ /E     |     |     E
        E        |        E/ |     |     |     |
        |        |        |  |     |     |     |
        +--------+--------+  +-----+--E--+-----+
        """
        moves = board.get_valid_moves(cl1)
        self.assertEqual(2, len(moves))
        self.assertIn(cl2, moves)
        self.assertIn(oc3, moves)

        moves = board.get_valid_moves(oc3)
        self.assertEqual(3, len(moves))
        self.assertIn(oc1, moves)
        self.assertIn(oc2, moves)
        self.assertIn(cl1, moves)


if __name__ == '__main__':
    unittest.main()
