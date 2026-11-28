"""Blocs posés sur les cases : départ, point de passage, ligne d'arrivée, boost.

Chaque bloc réagit quand une voiture entre sur sa case, via on_enter().
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # imports utilisés seulement pour les annotations de type
    from model.player import Player
    from model.race import Race


class Block:
    """Classe parente des blocs. Par défaut, entrer sur le bloc ne fait rien."""

    def on_enter(self, player: Player, race: Race) -> None:
        """Effet du bloc quand la voiture de `player` entre sur sa case."""


class StartBlock(Block):
    """Position de départ d'un joueur (aucun effet pendant la course)."""

    def __init__(self, player_number: int):
        """player_number : 1 ou 2, le joueur qui démarre sur cette case."""
        self.player_number = player_number


class Checkpoint(Block):
    """Point de passage. Plusieurs cases voisines peuvent former le même point
    de passage : elles partagent alors le même index."""

    def __init__(self, index: int):
        """index : numéro du point de passage (0, 1, 2…)."""
        self.index = index

    def on_enter(self, player: Player, race: Race) -> None:
        """Signale à la course que le joueur a franchi ce point de passage."""
        race.on_checkpoint(player, self)


class FinishLine(Block):
    """Ligne d'arrivée : compte un tour si tous les points de passage sont franchis."""

    def on_enter(self, player: Player, race: Race) -> None:
        """Signale à la course que le joueur a franchi la ligne."""
        race.on_finish_line(player)


class Boost(Block):
    """Bloc d'accélération : donne une poussée à la voiture pendant un court moment."""

    def __init__(self, duration: float = 0.6):
        """duration : durée de la poussée, en secondes."""
        self.duration = duration

    def on_enter(self, player: Player, race: Race) -> None:
        """Active le boost sur la voiture du joueur."""
        player.car.start_boost(self.duration)
