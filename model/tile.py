"""Case du circuit : un terrain et éventuellement un bloc."""

from constants import TILE_SIZE
from model.terrain import Terrain
from model.block import Block


class Tile:
    """Une case de la grille.

    Attributs :
        col, row (int) : position dans la grille.
        terrain (Terrain) : le sol de la case.
        block (Block | None) : le bloc posé sur la case, s'il y en a un.
    """

    def __init__(self, col: int, row: int, terrain: Terrain,
                 block: Block | None = None):
        """Crée une case à la position (col, row)."""
        self.col = col
        self.row = row
        self.terrain = terrain
        self.block = block

    def center(self) -> tuple[float, float]:
        """Coordonnées en pixels du centre de la case."""
        return ((self.col + 0.5) * TILE_SIZE, (self.row + 0.5) * TILE_SIZE)
