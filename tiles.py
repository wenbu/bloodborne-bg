from board import Position, MapSpace, TileDef
from typing import Dict, List


def create_tile(**kwargs) -> TileDef:
    """Convenience function for creating a TileDef.

    # TODO Consider changing the TileDef constructor signature to something like this?
    """
    spaces: List[MapSpace] = []
    for i, position in enumerate(kwargs['positions']):
        space_id = '%s-%d' % (kwargs['tile_id'], i)
        name = ''
        if 'names' in kwargs and i in kwargs['names']:
            name = kwargs['names'][i]
        spaces.append(MapSpace(position, space_id, name=name))
    exits = [spaces[e_idx] if e_idx is not None else None for e_idx in kwargs['exits']]
    print('%s exits = %s' % (kwargs['tile_id'], str(exits)))
    adjacency = {spaces[s_idx]: [spaces[t_idx] for t_idx in kwargs['adjacency'][s_idx]]
                 for s_idx in kwargs['adjacency']}
    return TileDef(spaces, exits, adjacency, kwargs['tile_id'])


TILES = {
    'central_lamp': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----+--E--+-----+
          |     |     |     |
          |     |  N  |     |
          E     |  L  |     E
          |     |     |     |
          |     |     |     |
          +-----+--E--+-----+
        (0, 1)          (1, 1)
    
        Special effect: Interact on Central Lamp space: teleport to any lamp space or inside any fog gate.
        ''',
        tile_id='central_lamp',
        positions=[
            ((0, 0), (0.33, 0), (0.33, 1), (0, 1)),
            ((0.33, 0), (0.67, 0), (0.67, 1), (0.33, 1)),
            ((0.67, 0), (1, 0), (1, 1), (0.67, 1))
        ],
        exits=[1, 2, 1, 0],
        adjacency={0: [1], 1: [0, 2], 2: [1]},
        names={1: 'Central Lamp'}
    ),
    'oedon_chapel': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------E--------+
          |       N L       |
          |                 |
          +--------+--------+
          E        |        E
          |        |        |
          +--------+--------+
        (0, 1)          (1, 1)
    
        Special effect: Enemy attacks suffer -1 speed while on this tile.
        ''',
        tile_id='oedon_chapel',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1)),
            ((0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)),
        ],
        exits=[0, 2, None, 1],
        adjacency={0: [1, 2], 1: [0, 2], 2: [0, 1]},
        names={0: 'Oedon Chapel'}
    ),
    'courtyard_lamp': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----+-----+-----+
          |     |     |     |
          |     |  N  |     |
          E     |  L  |     E
          |     |     |     |
          |     |     |     |
          +-----+--E--+-----+
        (0, 1)          (1, 1)
        ''',
        tile_id='courtyard_lamp',
        positions=[
            ((0, 0), (0.33, 0), (0.33, 1), (0, 1)),
            ((0.33, 0), (0.67, 0), (0.67, 1), (0.33, 1)),
            ((0.67, 0), (1, 0), (1, 1), (0.67, 1))
        ],
        exits=[None, 2, 1, 0],
        adjacency={0: [1], 1: [0, 2], 2: [1]},
        names={1: 'Courtyard Lamp'}
    ),
    'tomb_of_oedon': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----------------+
          |       N C       |
          |                 |
          +-----------------+
          |        L        |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        
        Special effect: Chests are draw-three-select-one. Shuffle others back into deck.
        ''',
        tile_id='tomb_of_oedon',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[None, None, 1, None],
        adjacency={0: [1], 1: [0]},
        names={0: 'Tomb of Oedon'}
    ),
    'alleyway': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------E--------+
          |                 |
          +-----------------+
          |       N 3       |
          +-----------------+
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='alleyway',
        positions=[
            ((0, 0), (1, 0), (1, 0.33), (0, 0.33)),
            ((0, 0.33), (1, 0.33), (1, 0.67), (0, 0.67)),
            ((0, 0.67), (1, 0.67), (1, 1), (0, 1))
        ],
        exits=[0, None, 2, None],
        adjacency={0: [1], 1: [0, 2], 2: [1]},
        names={1: 'Alleyway'}
    ),
    'the_great_bridge': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------E--------+
          |      N C 3      |
          |                 |
          +-----------------+
          |                 |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
    
        Special effect: Hunters may not move out of spaces containing enemies on this tile.
        ''',
        tile_id='great_bridge',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[0, None, 1, None],
        adjacency={0: [1], 1: [0]},
        names={0: 'The Great Bridge'}
    ),
    'ransacked_house': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----------------+
          |     1 C C 3     |
          |        N        |
          +-----------------+
          |                 |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='ransacked_house',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[None, None, 1, None],
        adjacency={0: [1], 1: [0]},
        names={0: 'Ransacked House'}
    ),
    'barred_window': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------+--------+
          |    N   |        |
          |        |        |
          +--------+    C   E
          |    2   |        |
          |        |        |
          +-------E+--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='barred_window',
        positions=[
            ((0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)),
            ((0.5, 0), (1, 0), (1, 1), (0.5, 1)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[None, 1, 2, None],
        adjacency={0: [1, 2], 1: [0, 2], 2: [0, 1]},
        names={0: 'Barred Window'}
    ),
    'church_of_the_good_chalice': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----------------+
          |      N C C      |
          +-----------------+
          |        L        |
          +-----------------+
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        
        Special effect: Interact: Trade one consumable for a blood echo.
        (N.B. unclear if it's one consumable or one chest pickup)
        ''',
        tile_id='good_chalice',
        positions=[
            ((0, 0), (1, 0), (1, 0.33), (0, 0.33)),
            ((0, 0.33), (1, 0.33), (1, 0.67), (0, 0.67)),
            ((0, 0.67), (1, 0.67), (1, 1), (0, 1))
        ],
        exits=[None, None, 2, None],
        adjacency={0: [1], 1: [0, 2], 2: [1]},
        names={1: 'Church of the Good Chalice'}
    ),
    'graveyard': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------E--------+
          |                 |
          +-----------------+
          E       C 2       E
          +-----------------+
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='graveyard',
        positions=[
            ((0, 0), (1, 0), (1, 0.33), (0, 0.33)),
            ((0, 0.33), (1, 0.33), (1, 0.67), (0, 0.67)),
            ((0, 0.67), (1, 0.67), (1, 1), (0, 1))
        ],
        exits=[0, 1, 2, 1],
        adjacency={0: [1], 1: [0, 2], 2: [1]},
        names={1: 'Graveyard'}
    ),
    'occupied_house': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------E--------+
          |        1        |
          E                 E
          +-----------------+
          |        N        |
          |                 |
          +-----------------+
        (0, 1)          (1, 1)
        ''',
        tile_id='occupied_house',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[0, 0, None, 0],
        adjacency={0: [1], 1: [0]},
        names={1: 'Occupied House'}
    ),
    'grand_cathedral': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----------------+
          |        N        |
          +--------+--------+
          |    L   |    C   |
          +--------+--------+
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        
        Special effect: Interact: Heal 2
        ''',
        tile_id='grand_cathedral',
        positions=[
            ((0, 0), (1, 0), (1, 0.33), (0, 0.33)),
            ((0, 0.33), (0.5, 0.33), (0.5, 0.67), (0, 0.67)),
            ((0.5, 0.33), (1, 0.33), (1, 0.67), (0.5, 0.67)),
            ((0, 0.67), (1, 0.67), (1, 1), (0, 1))
        ],
        exits=[None, None, 3, None],
        adjacency={0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2]},
        names={0: 'Grand Cathedral'}
    ),
    'iosefkas_clinic': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----------------+
          |       N L       |
          |                 |
          +-----------------+
          |                 |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        
        Special effect: Once per turn: Take one damage and draw one card
        ''',
        tile_id='iosefkas_clinic',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[None, None, 1, None],
        adjacency={0: [1], 1: [0]},
        names={0: 'Iosefka\'s Clinic'}
    ),
    'unnamed1': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------E--------+
          |                 |
          |                 |
          +-----------------+
          |       C 3       |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='unnamed1',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[0, None, 1, None],
        adjacency={0: [1], 1: [0]}
    ),
    'unnamed2': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------+--------+
          |    1   |    3   |
          E        |        E
          +--------+--------+
          |                 |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='unnamed2',
        positions=[
            ((0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)),
            ((0.5, 0), (1, 0), (1, 0.5), (0.5, 0.5)),
            ((0, 0.5), (1, 0.5), (1, 1), (0, 1)),
        ],
        exits=[None, 1, 2, 0],
        adjacency={0: [1, 2], 1: [0, 2], 2: [0, 1]}
    ),
    'unnamed3': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------+--------+
          |    C   |        |
          |        |        E
          +--------+--------+
          |        1        |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='unnamed3',
        positions=[
            ((0, 0), (0.5, 0), (0.5, 0.5), (0, 0.5)),
            ((0.5, 0), (1, 0), (1, 0.5), (0.5, 0.5)),
            ((0, 0.5), (1, 0.5), (1, 1), (0, 1)),
        ],
        exits=[None, 1, 2, None],
        adjacency={0: [1, 2], 1: [0, 2], 2: [0, 1]}
    ),
    'unnamed4': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----------------+
          |        C        |
          +-----------------+
          E        2        E
          +-----------------+
          |        1        |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='unnamed4',
        positions=[
            ((0, 0), (1, 0), (1, 0.33), (0, 0.33)),
            ((0, 0.33), (1, 0.33), (1, 0.67), (0, 0.67)),
            ((0, 0.67), (1, 0.67), (1, 1), (0, 1))
        ],
        exits=[None, 1, 2, 1],
        adjacency={0: [1], 1: [0, 2], 2: [1]}
    ),
    'unnamed5': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-------E+--------+
          |        |        |
          |        |        |
          E    2   |   C    E
          |        |        |
          |        |        |
          +--------+E-------+
        (0, 1)          (1, 1)
        ''',
        tile_id='unnamed5',
        positions=[
            ((0, 0), (0.5, 0), (0.5, 1), (0, 1)),
            ((0.5, 0), (1, 0), (1, 1), (0.5, 1))
        ],
        exits=[0, 1, 1, 0],
        adjacency={0: [1], 1: [0]}
    ),
    'unnamed6': create_tile(
        help='''
        (0, 0)          (1, 0)
          +--------+--------+
          |        |        |
          |        |        |
          E    2   |   1    E
          |        |        |
          |        |        |
          +--------+--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='unnamed6',
        positions=[
            ((0, 0), (0.5, 0), (0.5, 1), (0, 1)),
            ((0.5, 0), (1, 0), (1, 1), (0.5, 1))
        ],
        exits=[None, 1, None, 0],
        adjacency={0: [1], 1: [0]}
    ),
    'unnamed7': create_tile(
        help='''
        (0, 0)          (1, 0)
          +-----------------+
          |        C        |
          E                 E
          +-----------------+
          |        3        |
          |                 |
          +--------E--------+
        (0, 1)          (1, 1)
        ''',
        tile_id='unnamed7',
        positions=[
            ((0, 0), (1, 0), (1, 0.5), (0, 0.5)),
            ((0, 0.5), (0.5, 0.5), (0.5, 1), (0, 1))
        ],
        exits=[None, 0, 1, 0],
        adjacency={0: [1], 1: [0]}
    ),
}
