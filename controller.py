from action import Action, ActionType
from actor.actor import Actor
from actor.hunter import Hunter
from board import Board, MapSpace
from dataclasses import dataclass
from enum import Enum
from typing import List
import random


class Controller:
    def __init__(self, actor: Actor):
        self.actor = actor

    def select_action(self, possible_actions: List[Action]) -> Action:
        raise NotImplemented()

    def new_round(self) -> None:
        raise NotImplemented()


class HunterController(Controller):
    def __init__(self, hunter: Hunter):
        super().__init__(hunter)
        # TODO replace this with stat cards when those are implemented.
        self._num_actions = 3

    def new_round(self) -> None:
        # TODO draw three new stat cards; discard as needed to get down to three
        self._num_actions = 3

    def has_action(self) -> bool:
        return self._num_actions > 0

    def discard_stat_card(self) -> None:
        # TODO prompt player for stat card to discard.
        # TODO return discarded stat card
        self._num_actions -= 1

    def select_action(self, possible_actions: List[Action]) -> Action:
        return self._action_prompt(possible_actions,
                                   'Your current space is %s.\nPossible actions:\n' % self.actor.position)

    def select_move(self, possible_moves: List[Action], num_moves: int) -> Action:
        return self._action_prompt(possible_moves, '%d moves remaining. Possible moves:\n' % num_moves)

    def _action_prompt(self, action_list: List[Action], initial_prompt: str) -> Action:
        action = -1
        while not 0 <= action < len(action_list):
            prompt_lst = [initial_prompt]
            for i, possible_action in enumerate(action_list):
                prompt_lst.append('\t%d: %s.' % (i + 1, possible_action))
                if possible_action.type == ActionType.MOVE and isinstance(possible_action.arg,
                                                                          MapSpace) and possible_action.arg.has_exit:
                    prompt_lst.append(' This space has an exit to another tile.')
                prompt_lst.append('\n')
            prompt_lst.append('Pick an action: [1-%d] > ' % len(action_list))
            try:
                action = int(input(''.join(prompt_lst))) - 1
            except ValueError:
                print('Invalid selection.')
                continue
            if not 0 <= action < len(action_list):
                print('Invalid selection.')
                continue
        return action_list[action]


class MonsterController(Controller):
    def select_action(self, possible_actions: List[Action]) -> Action:
        # Just pick a random move.
        return random.choice(possible_actions)

    def new_round(self) -> None:
        # Do nothing. Maybe some boss monsters care about new rounds?
        pass
