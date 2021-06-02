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


class HunterController(Controller):
    def __init__(self, hunter: Hunter):
        super().__init__(hunter)

    def select_action(self, possible_actions: List[Action]) -> Action:
        action = -1
        while not 0 <= action < len(possible_actions):
            prompt_lst = ['Your current space is %s.\n'
                          'Possible actions:\n' % self.actor.position]
            for i, possible_action in enumerate(possible_actions):
                prompt_lst.append('\t%d: %s.' % (i+1, possible_action))
                if possible_action.type == ActionType.MOVE and isinstance(possible_action.arg, MapSpace) and possible_action.arg.has_exit:
                    prompt_lst.append(' This space has an exit to another tile.')
                prompt_lst.append('\n')
            prompt_lst.append('Pick an action: [1-%d] > ' % len(possible_actions))
            try:
                action = int(input(''.join(prompt_lst))) - 1
            except ValueError:
                print('Invalid action.')
                continue
            if not 0 <= action < len(possible_actions):
                print('Invalid action.')
                continue
        return possible_actions[action]


class MonsterController(Controller):
    def select_action(self, possible_actions: List[Action]) -> Action:
        # Just pick a random move.
        return random.choice(possible_actions)
