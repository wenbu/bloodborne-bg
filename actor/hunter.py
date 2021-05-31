from board import MapSpace
from actor.actor import Actor


class HunterWeaponDef:
    """Contains hunter weapon information.

    A hunter weapon has two forms, each having three different attacks and a passive ability.
    """
    pass


class HunterGunDef:
    """Contains hunter gun information.

    A hunter gun has one attack and a reload cost.
    """
    pass


class Hunter(Actor):
    """Tracks the current state of a Hunter and has methods for moving, attacking, etc.

    This includes things like current HP, weapon state, board position, etc.
    """
    def __init__(self, position: MapSpace, weapon: HunterWeaponDef, gun: HunterGunDef):
        super().__init__(position, max_hp=6)
        self._hp = 6
        self._weapon = weapon
        self._gun = gun
