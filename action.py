from board import Direction, MapSpace
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union


class ActionType(Enum):
    MOVE = 0
    INTERACT = 1
    DREAM = 2
    ATTACK = 3
    END = 4
    # TODO Consumables and reward cards should be here too. Same action or different? TBD.


@dataclass
class Action:
    type: ActionType
    """
    In the case of a MOVE action, `arg` is the destination space, or a Direction if exiting the tile.
    In the case of an INTERACT action, `arg` is TBD.
    In the case of an ATTACK action, `arg` is the enemy to attack.
    DREAM and END actions don't have arguments.
    """
    arg: Optional[Union[Direction, MapSpace]] = None

    def __str__(self):
        if self.type == ActionType.MOVE:
            # This is a bit gross. Maybe tile exits should be considered a different ActionType?
            if isinstance(self.arg, MapSpace):
                return 'Move to %s' % self.arg
            elif isinstance(self.arg, Direction):
                return 'Exit %s to an unknown tile' % self.arg
        elif self.type == ActionType.END:
            return 'End turn'
        else:
            return 'PLEASE IMPLEMENT ME'
