from action import Action, ActionType
from actor.hunter import Hunter, HunterGunDef, HunterWeaponDef
from board import Board, Direction, MapTile, MapSpace
from controller import HunterController, MonsterController
from enum import Enum
import random
from tiles import BASE, TileDeck
from typing import List


class Game:
    def __init__(self, num_players: int):
        # TODO hunter types will need to be specified
        self._num_players = num_players
        self._current_round = 0
        self._init_tiles()
        self._init_board()
        self._init_players()
        self._init_monsters()

    def _init_tiles(self):
        # TODO tile deck is campaign-dependent
        all_tiles = dict(BASE)
        del all_tiles['central_lamp']
        self._tiles = TileDeck(list(all_tiles.values()))

    def _init_board(self):
        # TODO starting board is campaign-dependent
        self._board = Board(MapTile(BASE['central_lamp'], 0))

    def _init_players(self):
        self._players: List[HunterController] = []
        # TODO hunters should have choice of starting space as applicable
        starting_spaces = [space for tile in self._board.get_current_tiles() for space in tile.get_spaces()]
        starting_space = random.choice(starting_spaces)
        for _ in range(self._num_players):
            hunter = Hunter(starting_space, HunterWeaponDef(), HunterGunDef())
            controller = HunterController(hunter)
            self._players.append(controller)

    def _init_monsters(self):
        # TODO This should loop through all spaces on the board, find the spawns, and set up monsters accordingly.
        # But monster spawns aren't implemented yet :)
        self._monsters: List[MonsterController] = []

    def round(self):
        for player in self._players:
            # TODO: Action card implementation. For now players get one action per turn.
            possible_actions = self.get_player_actions(player)
            player_action = player.select_action(possible_actions)
            if player_action.type == ActionType.MOVE:
                if isinstance(player_action.arg, MapSpace):
                    player.actor.move(player_action.arg)
                elif isinstance(player_action.arg, Direction):
                    # Player is exiting the tile.
                    exit_direction = player_action.arg
                    current_tile = self._board.get_tile(player.actor.position)
                    new_tile_def = self._tiles.draw()
                    new_tile = self._board.add_tile(current_tile, exit_direction, new_tile_def)
                    print('Added new tile %s.' % new_tile)
                    # TODO need to handle case where adding this tile would lead to no open exits on board (redraw tile)
                    destination_space = new_tile.get_exit_space(exit_direction.reverse())
                    player.actor.move(destination_space)
                # TODO: Player should get a second move here (and possibly a third, depending on action card)
                # TODO: Handle monster pursuit.
            elif player_action.type == ActionType.END:
                pass

            # Enemy activation
            for monster in self._monsters:
                # TODO: Keep track of player moves for monster move.
                monster.select_action([])

        # End of round stuff goes here, e.g. increment hunt track
        self._current_round += 1

    def get_player_actions(self, player: HunterController) -> List[Action]:
        possible_actions = []
        current_position = player.actor.position
        current_tile = self._board.get_tile(current_position)
        valid_moves = self._board.get_valid_moves(current_position)
        for move in valid_moves:
            possible_actions.append(Action(type=ActionType.MOVE, arg=move))
        if current_position.has_exit:
            all_exits = self._board.get_tile(current_position).get_space_exits(current_position)
            for exit_direction in all_exits:
                if not self._board.get_tile_in_direction(current_tile, exit_direction):
                    possible_actions.append(Action(type=ActionType.MOVE, arg=exit_direction))
        possible_actions.append(Action(type=ActionType.END))
        return possible_actions

    def is_game_over(self) -> bool:
        # TODO this is completely arbitrary
        return self._current_round > 4
