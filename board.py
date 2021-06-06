import random
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Tuple, NewType, Dict, Iterable

Position = NewType('Position', Tuple[int, int])


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def reverse(self) -> 'Direction':
        return Direction((self.value + 2) % 4)


def move(position: Position, direction: Direction) -> Position:
    """Return the position that is one space in the provided direction from the provided position."""
    # I'm sure there's a more elegant way to do this but I'm not clever enough to think of it right now.
    if direction == Direction.UP:
        return Position((position[0], position[1]+1))
    elif direction == Direction.RIGHT:
        return Position((position[0]+1, position[1]))
    elif direction == Direction.DOWN:
        return Position((position[0], position[1]-1))
    elif direction == Direction.LEFT:
        return Position((position[0]-1, position[1]))
    else:
        raise ValueError('Invalid direction %d' % direction)


@dataclass(eq=True, frozen=True)
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
    id: str
    bounds: Tuple[Tuple[float, float], ...]
    name: str = ''
    has_exit: bool = False

    def __str__(self):
        return self.id


class TileDef:
    """Contains information about a map tile's spaces, exits and connectivity."""
    def __init__(self, spaces: List[MapSpace], exits: List[Optional[MapSpace]],
                 adjacency: Dict[MapSpace, List[MapSpace]], name: str):
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
        # TODO probably tile effects, lamps, chest/monster spawns, etc. will go here too


class MapTile:
    """Represents one map tile as it exists on the board.

    Currently this means it tracks its own rotation in addition to the TileDef. This may change in the future.
    """
    def __init__(self, tile_def: TileDef, rotation: int = 0):
        """
        Args:
            tile_def: This MapTile's TileDef.
            rotation: Number of clockwise 90 degree rotations from the TileDef orientation.
        """
        self._tile_def = tile_def
        self._rotation = rotation % 4

    def _rotate(self, lst: List[Any]) -> List[Any]:
        return lst[-self._rotation:] + lst[:-self._rotation]

    def get_exit_directions(self) -> List[Direction]:
        """Return a list of Directions in which one can exit this tile."""
        rotated_exits = self._rotate(self._tile_def.exits)
        return [Direction(i) for i, e in enumerate(rotated_exits) if e is not None]

    def get_exit_space(self, direction: Direction) -> Optional[MapSpace]:
        """Return the MapSpace with the exit in the specified direction, or None."""
        rotated_exits = self._rotate(self._tile_def.exits)
        return rotated_exits[direction.value]

    def get_space_exits(self, space: MapSpace) -> List[Direction]:
        """Return the Directions in which the specified space have exit(s), or an empty list."""
        if space not in self._tile_def.spaces:
            raise ValueError('Specified space is not on this tile.')
        return [Direction((i + self._rotation) % 4) for i, e in enumerate(self._tile_def.exits) if space == e]

    def get_spaces(self) -> List[MapSpace]:
        return self._tile_def.spaces

    def get_space_neighbors(self, space: MapSpace) -> List[MapSpace]:
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
        # Here Positions are used to describe where a given MapTiles are located
        # relative to the board origin.
        # TODO some of the physical tiles are larger than the standard ones, do we need special
        # handling for those?
        origin = Position((0, 0))
        # Graph structure representing tile network.
        self._board_root = self._BoardNode(first_tile, origin)
        # MapTile -> Position lookup dict.
        self._tile_positions = {first_tile: origin}
        # Position -> BoardNode lookup dict.
        self._positions = {origin: self._board_root}
        # MapSpace -> MapTile lookup dict.
        self._spaces: Dict[MapSpace, MapTile] = {}
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

    def get_current_tiles(self) -> Iterable[MapTile]:
        return self._tile_positions.keys()

    def add_tile(self, tile: MapTile, direction: Direction, new_tile_def: TileDef,
                 new_tile_rotation: Optional[int] = None) -> MapTile:
        """Add `new_tile` to the board in the position one space from `tile` in `direction`.
        `new_tile` will be rotated appropriately to connect the exits. Return the added tile.

        If new_tile_rotation is not specified (default), then the rotation of the new tile will be randomly chosen.
        new_tile_rotation is primarily intended to simplify testing, but there is still some uncertainty about whether
        players are intended to determine tile rotation or if it's supposed to be randomly chosen.
        """
        if tile not in self._tile_positions:
            raise ValueError('Specified base tile is not on the board.')
        # Validate tile orientation.
        tile_exits = tile.get_exit_directions()
        if direction not in tile_exits:
            raise ValueError('Tile not in valid orientation.')
        if new_tile_rotation is None:
            tile_exits = new_tile_def.exits
            # Pick a rotation at random to line up the exits.
            exit_directions = [Direction(i) for i, exit_space in enumerate(tile_exits) if exit_space is not None]
            chosen_exit_direction = random.choice(exit_directions)
            new_tile_rotation = Direction(direction).reverse().value - chosen_exit_direction.value
        new_tile = MapTile(new_tile_def, new_tile_rotation)
        if new_tile_rotation is not None:
            # Validate provided rotation.
            if direction.reverse() not in new_tile.get_exit_directions():
                raise ValueError('Provided rotation is not valid.')

        # Create new position and BoardNode.
        src_position = self._tile_positions[tile]
        dst_position = move(src_position, direction)
        dst_node = self._BoardNode(new_tile, dst_position)

        # Hook up new node to graph.
        src_node = self._positions[src_position]
        src_node.neighbors[direction.value] = dst_node
        dst_node.neighbors[direction.reverse().value] = src_node

        # Update lookup dicts.
        self._positions[dst_position] = dst_node
        self._tile_positions[new_tile] = dst_position
        self._register_spaces(new_tile)

        return new_tile

    def get_tile(self, space: MapSpace) -> MapTile:
        """Return the tile on which the specified space exists."""
        return self._spaces[space]

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
        moves: List[MapSpace] = tile.get_space_neighbors(space)
        exit_directions = tile.get_space_exits(space)
        if exit_directions:
            for direction in exit_directions:
                exit_tile = self.get_tile_in_direction(tile, direction)
                if exit_tile:
                    # Check that the tile on the other side of the exit actually has an exit itself in the
                    # opposite direction.
                    exit_space = exit_tile.get_exit_space(direction.reverse())
                    if exit_space:
                        moves.append(exit_space)
        return moves
