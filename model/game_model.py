"""Modèle principal : état du jeu, circuit choisi et course en cours."""

from constants import GameState
from model.circuit import Circuit
from model.circuit_library import CIRCUITS
from model.race import Race


class GameModel:
    """Contient tout l'état du jeu, sans rien savoir du clavier ni de l'écran.

    Attributs :
        state (str) : état courant de l'automate (voir GameState).
        circuit_names (list[str]) : noms des circuits proposés dans le menu.
        selected_index (int) : indice du circuit en surbrillance.
        race (Race | None) : course en cours (ou terminée, dans l'état RESULTS).
    """

    def __init__(self):
        """Démarre dans le menu principal, sans course."""
        self.state: str = GameState.MENU
        self.circuit_names: list[str] = list(CIRCUITS.keys())
        self.selected_index: int = 0
        self.race: Race | None = None

    def select_next_circuit(self) -> None:
        """Met en surbrillance le circuit suivant (revient au premier à la fin)."""
        self.selected_index = (self.selected_index + 1) % len(self.circuit_names)

    def select_previous_circuit(self) -> None:
        """Met en surbrillance le circuit précédent (va au dernier au début)."""
        self.selected_index = (self.selected_index - 1) % len(self.circuit_names)

    def start_race(self) -> None:
        """Charge le circuit sélectionné, crée la course et passe en état RACING."""
        name = self.circuit_names[self.selected_index]
        circuit = Circuit.from_description(name, CIRCUITS[name])
        self.race = Race(circuit)
        self.state = GameState.RACING

    def update(self, dt: float) -> None:
        """Fait avancer la course de dt secondes, et passe aux résultats quand elle est finie."""
        if self.state != GameState.RACING or self.race is None:
            return
        self.race.update(dt)
        if self.race.is_finished():
            self.state = GameState.RESULTS
