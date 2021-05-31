from board import MapSpace


class Actor:
    """Represents an entity that can move around on the board and has HP, etc."""
    def __init__(self, position: MapSpace, max_hp: int):
        self.position = position
        self._max_hp = max_hp
        self._current_hp = max_hp

    def move(self, new_position: MapSpace) -> None:
        """Update this Actor's current position. Does not make any checks about the validity of the move."""
        self.position = new_position

    def set_hp(self, new_hp: int) -> None:
        """Set this Actor's current hp."""
        self._current_hp = new_hp

