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
            # Really need some way to visualize the board for this to make any sense.
            try:
                move = int(input('Pick a move: [0-%d] > ' % (len(valid_moves)-1)))
            except ValueError:
                print('Invalid move.')
                continue
            if not 0 <= move < len(valid_moves):
                print('Invalid move.')
                continue
            self._actor.move(valid_moves[move])
        print('Hunter moved.')


class MonsterController(Controller):
    def do_action(self, board: Board) -> None:
        # Just pick a random move.
        valid_moves = board.get_valid_moves(self._actor.position)
        move = random.choice(valid_moves)
        self._actor.move(move)
