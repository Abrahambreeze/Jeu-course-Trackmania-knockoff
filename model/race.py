"""Règles de la course : compte à rebours, tours, points de passage, vainqueur."""

from model.circuit import Circuit
from model.player import Player
from model.block import Checkpoint

COUNTDOWN_DURATION = 3.0


class Race:
    """Une course entre deux joueurs sur un circuit.

    Attributs :
        circuit (Circuit) : le circuit de la course.
        players (list[Player]) : les deux joueurs.
        countdown (float) : temps restant avant le départ, en secondes.
        elapsed (float) : temps écoulé depuis le départ, en secondes.
        winner (Player | None) : premier joueur à avoir fini tous ses tours.
    """

    def __init__(self, circuit: Circuit):
        """Crée les joueurs sur leurs cases de départ et lance le compte à rebours."""
        self.circuit = circuit
        self.players = [Player(number, circuit.start_tiles[number],
                               circuit.start_angle)
                        for number in (1, 2)]
        self.countdown = COUNTDOWN_DURATION
        self.elapsed = 0.0
        self.winner: Player | None = None

    def is_started(self) -> bool:
        """True une fois le compte à rebours terminé."""
        return self.countdown <= 0

    def is_finished(self) -> bool:
        """True dès qu'un joueur a gagné."""
        return self.winner is not None

    def update(self, dt: float) -> None:
        """Fait avancer la course de dt secondes."""
        if self.is_finished():
            return

        if not self.is_started():
            self.countdown -= dt
            for player in self.players:
                player.car.clear_inputs()  # les voitures attendent le départ
            return

        self.elapsed += dt
        for player in self.players:
            self._update_player(player, dt)

    def _update_player(self, player: Player, dt: float) -> None:
        """Déplace la voiture du joueur puis applique les effets de la case atteinte."""
        car = player.car
        terrain = self.circuit.get_terrain_at_pixel(car.x, car.y)
        car.update(dt, terrain)

        if self.circuit.get_terrain_at_pixel(car.x, car.y).is_void:
            player.fall_into_void()
            return

        tile = self.circuit.get_tile_at_pixel(car.x, car.y)
        if tile is not player.current_tile:
            player.current_tile = tile
            if tile.block is not None:
                tile.block.on_enter(player, self)

    def on_checkpoint(self, player: Player, checkpoint: Checkpoint) -> None:
        """Appelé par un Checkpoint : enregistre le passage et le point de réapparition."""
        player.checkpoints_passed.add(checkpoint.index)
        player.set_respawn(player.current_tile)

    def on_finish_line(self, player: Player) -> None:
        """Appelé par la ligne d'arrivée : valide un tour si tous les points sont franchis."""
        if len(player.checkpoints_passed) < self.circuit.checkpoint_count:
            return  # il manque des points de passage : le tour ne compte pas

        player.laps += 1
        player.checkpoints_passed.clear()
        player.set_respawn(player.current_tile)
        if player.laps >= self.circuit.laps and self.winner is None:
            player.finish_time = self.elapsed
            self.winner = player
