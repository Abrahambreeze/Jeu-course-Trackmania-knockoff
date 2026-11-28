"""Joueur : sa voiture et sa progression dans la course."""

from model.car import Car
from model.tile import Tile


class Player:
    """Un participant à la course.

    Attributs :
        number (int) : 1 ou 2.
        car (Car) : la voiture du joueur.
        laps (int) : tours complétés.
        checkpoints_passed (set[int]) : points de passage franchis dans le tour en cours.
        respawn (tuple[float, float, float]) : position (x, y) et angle où la
            voiture réapparaît après une chute dans le vide.
        current_tile (Tile | None) : case sous la voiture à la frame précédente,
            pour ne déclencher un bloc qu'au moment où l'on entre sur sa case.
        finish_time (float | None) : temps de course à l'arrivée, en secondes.
    """

    def __init__(self, number: int, start_tile: Tile, start_angle: float):
        """Place le joueur sur sa case de départ."""
        x, y = start_tile.center()
        self.number = number
        self.car = Car(x, y, start_angle)
        self.laps = 0
        self.checkpoints_passed: set[int] = set()
        self.respawn = (x, y, start_angle)
        self.current_tile: Tile | None = start_tile
        self.finish_time: float | None = None

    def set_respawn(self, tile: Tile) -> None:
        """Retient le centre de `tile` et l'angle actuel comme point de réapparition."""
        x, y = tile.center()
        self.respawn = (x, y, self.car.angle)

    def fall_into_void(self) -> None:
        """Ramène la voiture au dernier point de passage, à l'arrêt."""
        x, y, angle = self.respawn
        self.car.reset(x, y, angle)
        self.current_tile = None
