from board import MapSpace
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
    In the case of a MOVE action, `arg` is the destination space.
    In the case of an INTERACT action, `arg` is TBD.
    In the case of an ATTACK action, `arg` is the enemy to attack.
    DREAM and END actions don't have arguments.
    """
    arg: Optional[Union[MapSpace]] = None

    def __str__(self):
        if self.type == ActionType.MOVE:
            return 'Move to %s' % self.arg
        elif self.type == ActionType.END:
            return 'End turn'
        else:
            return 'PLEASE IMPLEMENT ME'
