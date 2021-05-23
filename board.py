from __future__ import annotations
from typing import Any, List, Optional, Tuple, NamedTuple, NewType, Dict

Position = NewType('Position', Tuple[int, int])
Direction = NewType('Direction', int)
UP = Direction(0)
RIGHT = Direction(1)
DOWN = Direction(2)
LEFT = Direction(3)


def reverse(direction: Direction) -> Direction:
    """Return the direction that is the opposite of the one provided."""
    return Direction((direction + 2) % 4)


def move(position: Position, direction: Direction) -> Position:
    """Return the position that is one space in the provided direction from the provided position."""
    # I'm sure there's a more elegant way to do this but I'm not clever enough to think of it right now.
    if direction == UP:
        return Position((position[0], position[1]+1))
    elif direction == RIGHT:
        return Position((position[0]+1, position[1]))
    elif direction == DOWN:
        return Position((position[0], position[1]-1))
    elif direction == LEFT:
        return Position((position[0]-1, position[1]))
    else:
        raise ValueError('Invalid direction %d' % direction)


class MapSpace:
    """Contains information about a space's physical boundaries on a tile."""
    """
    The coordinate system used here is as follows:
    (0, 0)          (1, 0)
      +---------------+
      |               |
      |               |
      |     Tile      |
      |               |
      |               |
      +---------------+
    (0, 1)          (1, 1)
    
    Coordinates will be stored in a list in clockwise order.
    """
    def __init__(self, bounds: Tuple[Tuple[float, float], ...], space_id: str, name: str = ''):
        self.bounds = bounds
        self.id = space_id
        self.name = name

    def __hash__(self):
        return hash((self.bounds, self.name))

    def __eq__(self, other):
        if isinstance(other, MapSpace):
            return (self.bounds, self.name) == (other.bounds, other.name)
        return NotImplemented

    def __repr__(self):
        return self.id

    def __str__(self):
        return self.__repr__()


class TileDef:
    def __init__(self, spaces: List[MapSpace], exits: List[Optional[MapSpace]],
                 adjacency: Dict[MapSpace: List[MapSpace]], name: str):
        """
        Args:
            spaces: a list of MapSpaces in this tile.
            exits: List of length 4. Entries in this list correspond to directions, starting with UP and proceeding
                clockwise. Each entry in this list is either the MapSpace connected to the exit, or None if there is no
                such exit.
            adjacency: For each MapSpace, a list of MapSpaces that it is adjacent to.
        """
        if len(exits) != 4:
            raise ValueError('exits list must have length 4')

        self.spaces = spaces
        self.exits = exits
        self.adjacency = adjacency
        self.name = name
        # TODO probably tile effects will go here too
    """Contains information about a map tile's spaces, exits and connectivity."""


class MapTile:
    """A single MapTile can contain multiple MapSpaces."""
    """     
    Orientation is stored as number of of clockwise 90-degree rotations from some canonical orientation.
    """
    def __init__(self, tile_def: TileDef, rotation: int = 0):
        self._tile_def = tile_def
        self._rotation = rotation

    def _rotate(self, lst: List[Any]) -> List[Any]:
        return lst[-self._rotation:] + lst[:-self._rotation]

    def get_exit_directions(self) -> List[Direction]:
        """Return a list of Directions in which one can exit this tile."""
        rotated_exits = self._rotate(self._tile_def.exits)
        return [Direction(i) for i, e in enumerate(rotated_exits) if e is not None]

    def get_exit_space(self, direction: Direction) -> Optional[MapSpace]:
        """Return the MapSpace with the exit in the specified direction, or None."""
        rotated_exits = self._rotate(self._tile_def.exits)
        return rotated_exits[direction]

    def get_exit(self, space: MapSpace) -> List[Direction]:
        """Return the Directions in which the specified space have exit(s), or None."""
        if space not in self._tile_def.spaces:
            raise ValueError('Specified space is not on this tile.')
        return [Direction((i + self._rotation) % 4) for i, e in enumerate(self._tile_def.exits)]

    def get_spaces(self) -> List[MapSpace]:
        return self._tile_def.spaces

    def get_neighbors(self, space: MapSpace) -> List[MapSpace]:
        if space not in self._tile_def.spaces:
            raise ValueError('Specified space is not on this tile.')

        return list(self._tile_def.adjacency[space])

    def __repr__(self):
        return '%s, rotation=%d' % (self._tile_def.name, self._rotation)

    def __str__(self):
        return self.__repr__()


class Board:
    """Represents the entirety of the playing board."""
    def __init__(self, first_tile: MapTile):
        origin = Position((0, 0))
        # Graph structure representing tile network.
        self._board_root = self._BoardNode(first_tile, origin)
        # MapTile -> position lookup dict.
        self._tile_positions = {first_tile: origin}
        # Tile position -> BoardNode lookup dict.
        self._positions = {origin: self._board_root}
        # MapSpace -> MapTile lookup dict.
        self._spaces: Dict[MapSpace: MapTile] = {}
        self._register_spaces(first_tile)

    class _BoardNode:
        """This is pretty much a bidirectional 2d linked list node."""
        def __init__(self, tile: MapTile, position: Position):
            self.tile = tile
            self.position = position
            # clockwise, starting with top
            self.neighbors: List[Optional[Board._BoardNode]] = [None, None, None, None]

    def _register_spaces(self, tile: MapTile) -> None:
        for space in tile.get_spaces():
            self._spaces[space] = tile

    def add_tile(self, tile: MapTile, direction: Direction, new_tile: MapTile) -> None:
        """Add `new_tile` to the board in the position one space from `tile` in `direction`."""
        if tile not in self._tile_positions:
            raise ValueError('Specified base tile is not on the board.')
        # Validate tile orientation.
        tile_exits = tile.get_exit_directions()
        if direction not in tile_exits:
            raise ValueError('Tile not in valid orientation.')
        tile_exits = new_tile.get_exit_directions()
        if reverse(direction) not in tile_exits:
            raise ValueError('New tile not in valid orientation.')

        # Create new position and BoardNode.
        src_position = self._tile_positions[tile]
        dst_position = move(src_position, direction)
        dst_node = self._BoardNode(new_tile, dst_position)

        # Hook up new node to graph.
        src_node = self._positions[src_position]
        src_node.neighbors[direction] = dst_node
        dst_node.neighbors[reverse(direction)] = src_node

        # Update lookup dicts.
        self._positions[dst_position] = dst_node
        self._tile_positions[new_tile] = dst_position
        self._register_spaces(new_tile)

    def get_tile_in_direction(self, tile: MapTile, direction: Direction) -> Optional[MapTile]:
        """Return the tile in the specified direction from the specified tile, or None."""
        position = self._tile_positions[tile]
        dst_position = move(position, direction)
        return self._positions[dst_position].tile if dst_position in self._positions else None

    def get_valid_moves(self, space: MapSpace) -> List[MapSpace]:
        """Return a list of valid moves from `space`."""
        # Valid moves from a given space include all of its neighbors on the tile, plus whatever spaces are through
        # any exits.
        tile = self._spaces[space]
        moves: List[MapSpace] = tile.get_neighbors(space)
        exit_directions = tile.get_exit(space)
        if exit_directions:
            for direction in exit_directions:
                exit_tile = self.get_tile_in_direction(tile, direction)
                if exit_tile:
                    exit_space = exit_tile.get_exit_space(reverse(direction))
                    if exit_space:
                        moves.append(exit_space)
        return moves
