from board import MapSpace, TileDef


def central_lamp() -> TileDef:
    """Returns the Central Lamp tile def."""
    """
    (0, 0)          (1, 0)
      +-----+--E--+-----+
      |     |     |     |
      |     |     |     |
      E     |     |     E
      |     |     |     |
      |     |     |     |
      +-----+--E--+-----+
    (0, 1)          (1, 1)
    """
    spaces = [MapSpace(((0, 0), (0.33, 0), (0.33, 1), (0, 1)), 'central_lamp1'),
              MapSpace(((0.33, 0), (0.67, 0), (0.67, 1), (0.33, 1)), 'central_lamp2'),
              MapSpace(((0.67, 0), (1, 0), (1, 1), (0.67, 1)), 'central_lamp3')]
    exits = [spaces[1], spaces[2], spaces[1], spaces[0]]
    adjacency = {spaces[0]: [spaces[1]],
                 spaces[1]: [spaces[0], spaces[2]],
                 spaces[2]: [spaces[1]]}
    return TileDef(spaces, exits, adjacency, 'central_lamp')


def oedon_chapel() -> TileDef:
    """Returns the Oedon Chapel tile def."""
    """
    (0, 0)          (1, 0)
      +--------E--------+
      |                 |
      |                 |
      +--------+--------+
      E        |        E
      |        |        |
      +--------+--------+
    (0, 1)          (1, 1)
    """
    spaces = [MapSpace(((0, 0), (1, 0), (1, 0.5), (0, 0.5)), 'oedon_chapel1'),
              MapSpace(((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1)), 'oedon_chapel2'),
              MapSpace(((0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)), 'oedon_chapel3')]
    exits = [spaces[0], spaces[2], None, spaces[1]]
    adjacency = {spaces[0]: [spaces[1], spaces[2]],
                 spaces[1]: [spaces[0], spaces[2]],
                 spaces[2]: [spaces[0], spaces[1]]}
    return TileDef(spaces, exits, adjacency, 'oedon_chapel')
