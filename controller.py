from actor.actor import Actor
from actor.hunter import Hunter
from board import Board
import random


class Controller:
    def __init__(self, actor: Actor):
        self._actor = actor

    def do_action(self, board: Board) -> None:
        raise NotImplemented()


class HunterController(Controller):
    def __init__(self, hunter: Hunter):
        super().__init__(hunter)

    def do_action(self, board: Board) -> None:
        # Only handling moves for now.
        valid_moves = board.get_valid_moves(self._actor.position)
        move = -1
        while not 0 <= move < len(valid_moves):
            prompt_lst = ['Your current space is %s.\n'
                          'Possible moves:\n'
                          '\t0: Don\'t move.\n' % self._actor.position]
            for i, valid_move in enumerate(valid_moves):
                prompt_lst.append('\t%d: Move to %s.\n' % (i+1, valid_move))
            prompt_lst.append('Pick a move: [0-%d] > ' % len(valid_moves))
            try:
                move = int(input(''.join(prompt_lst))) - 1
                if move == -1:
                    # No move.
                    return
            except ValueError:
                print('Invalid move.')
                continue
            if not 0 <= move < len(valid_moves):
                print('Invalid move.')
                continue
            self._actor.move(valid_moves[move])


class MonsterController(Controller):
    def do_action(self, board: Board) -> None:
        # Just pick a random move.
        valid_moves = board.get_valid_moves(self._actor.position)
        move = random.choice(valid_moves)
        self._actor.move(move)
