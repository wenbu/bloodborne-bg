import unittest
from board import Board, Direction, MapTile
from tiles import BASE, create_tile


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
        cl1, cl2, cl3 = central_lamp_tile.get_spaces()
        board = Board(central_lamp_tile)
        oedon_chapel_tile = board.add_tile(central_lamp_tile, Direction.LEFT, BASE['oedon_chapel'], new_tile_rotation=0)
        oc1, oc2, oc3 = oedon_chapel_tile.get_spaces()
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

    def test_add_tile2(self):
        one_space = [((0, 0), (1, 0), (1, 1), (0, 1))]
        td_straight = create_tile(tile_id='straight', positions=one_space, exits=[0, None, 0, None], adjacency={0: []})
        td_corner1 = create_tile(tile_id='corner1', positions=one_space, exits=[None, None, 0, 0], adjacency={0: []})
        td_corner2 = create_tile(tile_id='corner2', positions=one_space, exits=[None, 0, 0, None], adjacency={0: []})
        td_corner3 = create_tile(tile_id='corner3', positions=one_space, exits=[0, 0, None, None], adjacency={0: []})

        tile_straight = MapTile(td_straight)
        board = Board(tile_straight)
        tile_corner1 = board.add_tile(tile_straight, Direction.UP, td_corner1, new_tile_rotation=0)
        tile_corner2 = board.add_tile(tile_corner1, Direction.LEFT, td_corner2, new_tile_rotation=0)
        tile_corner3 = board.add_tile(tile_corner2, Direction.DOWN, td_corner3, new_tile_rotation=0)

        """
        Map now looks like this:
        
        +---+   +---+
        | 2 E---E 1 |
        +-E-+   +-E-+
          |       |
        +-E-+   +-E-+
        | 3 E   | S |
        +---+   +-E-+
        
        Moving from the space on tile 3 (tile_corner3) to the space on tile S (tile_straight) should not be considered
        a valid move.
        """
        tc3_space = tile_corner3.get_spaces()[0]
        moves = board.get_valid_moves(tc3_space)
        self.assertEqual(1, len(moves))
        self.assertIn(tile_corner2.get_spaces()[0], moves)

        s_space = tile_straight.get_spaces()[0]
        moves = board.get_valid_moves(s_space)
        self.assertEqual(1, len(moves))
        self.assertIn(tile_corner1.get_spaces()[0], moves)


if __name__ == '__main__':
    unittest.main()
