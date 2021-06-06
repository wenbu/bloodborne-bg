from board import Direction, MapSpace
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union


class ActionType(Enum):
    # TODO: auto values?
    # TODO: type validation for `arg` on init?
    # --------------------
    # Move-related actions.
    # --------------------
    # Player wants to start a move action.
    MOVE_START = 0

    # A one-space move on the board.
    MOVE = 1

    # A move through a tile exit onto an unknown tile.
    EXIT = 2

    # Player wants to end a move action.
    END_MOVE = 3

    # --------------------
    # TBD not implemented yet!!!
    # --------------------
    INTERACT = 4
    DREAM = 5
    ATTACK = 6
    # TODO Do consumables and rewards need to be different action types or can they be rolled into a single
    # use_card action? We'll see when we implement this.
    USE_CONSUMABLE = 7
    USE_REWARD = 8

    END_TURN = 9


@dataclass
class Action:
    type: ActionType
    """
    In the case of a MOVE action, `arg` is the destination MapSpace.
    In the case of an EXIT action, `arg` is a Direction.
    In the case of an INTERACT action, `arg` is TBD.
    In the case of an ATTACK action, `arg` is the enemy to attack (type TBD).
    In the case of a USE_CONSUMABLE action, `arg` is the card being used (type TBD).
    In the case of a USE_REWARD action, `arg` is the card being used (type TBD).
    MOVE_START, MOVE_END, DREAM, END actions don't have arguments.
    """
    arg: Optional[Union[Direction, MapSpace]] = None

    def __str__(self):
        if self.type == ActionType.MOVE_START:
            return 'Move'
        elif self.type == ActionType.MOVE:
            return 'Move to %s' % self.arg
        elif self.type == ActionType.EXIT:
            return 'Exit %s to an unknown tile' % self.arg
        elif self.type == ActionType.END_MOVE:
            return 'End move'
        elif self.type == ActionType.END_TURN:
            return 'End turn'
        else:
            return 'PLEASE IMPLEMENT ME %s' % self.type
