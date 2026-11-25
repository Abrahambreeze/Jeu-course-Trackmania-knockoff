"""Contrôleur principal : boucle de jeu et gestion des touches selon l'état."""

import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from model.car import Car
from view.game_view import GameView
from controller.input_handler import (
    InputHandler, PLAYER_1_MAPPING, PLAYER_2_MAPPING
)


class GameController:
    """Fait le lien entre le clavier, le modèle et la vue.

    Il possède la boucle principale : à chaque frame, il lit les événements,
    met à jour le modèle puis demande à la vue de dessiner.
    """

    def __init__(self):
        """Ouvre la fenêtre et crée le modèle, la vue et un lecteur de touches par joueur."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handlers = [InputHandler(PLAYER_1_MAPPING),
                               InputHandler(PLAYER_2_MAPPING)]
        self.running = True
        self.dt: float = 0.0

    def run(self) -> None:
        """Boucle principale : une itération correspond à une frame."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            # tick() attend pour ne pas dépasser FPS images/s et renvoie le
            # temps écoulé depuis la frame précédente (en ms). On le limite
            # pour éviter un saut énorme si la fenêtre a été bloquée.
            self.dt = min(self.clock.tick(FPS) / 1000, 0.05)

    def handle_events(self) -> None:
        """Traite les événements ponctuels : fermeture de fenêtre et appuis de touche."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """Envoie la touche pressée au gestionnaire de l'état courant."""
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CIRCUIT_SELECT:
            self.handle_circuit_select_key(key)
        elif state == GameState.RACING:
            self.handle_racing_key(key)
        elif state == GameState.RESULTS:
            self.handle_results_key(key)

    def handle_menu_key(self, key: int) -> None:
        """Menu principal : Entrée -> choix du circuit, Échap -> quitter."""
        if key == pygame.K_RETURN:
            self.model.state = GameState.CIRCUIT_SELECT
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_circuit_select_key(self, key: int) -> None:
        """Choix du circuit : flèches pour changer, Entrée pour lancer, Échap pour revenir."""
        if key == pygame.K_UP:
            self.model.select_previous_circuit()
        elif key == pygame.K_DOWN:
            self.model.select_next_circuit()
        elif key == pygame.K_RETURN:
            self.model.start_race()
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def handle_racing_key(self, key: int) -> None:
        """Pendant la course : Échap ramène au menu principal."""
        if key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def handle_results_key(self, key: int) -> None:
        """Écran de résultats : Entrée ou Échap ramènent au menu principal."""
        if key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.model.state = GameState.MENU

    def update(self) -> None:
        """Pendant la course, applique les touches de chaque joueur puis met à jour le modèle."""
        if self.model.state != GameState.RACING:
            return

        for handler, player in zip(self.input_handlers, self.model.race.players):
            self.apply_input(player.car, handler.get_inputs())
        self.model.update(self.dt)

    def apply_input(self, car: Car, player_input: dict[str, bool]) -> None:
        """Traduit les actions d'un joueur en appels aux méthodes de sa voiture."""
        if player_input["accelerate"]:
            car.accelerate()
        if player_input["brake"]:
            car.brake()
        if player_input["left"]:
            car.steer_left()
        if player_input["right"]:
            car.steer_right()

    def render(self) -> None:
        """Demande à la vue de dessiner l'état actuel du modèle."""
        self.view.draw(self.model)

    def quit(self) -> None:
        """Arrête la boucle, ferme pygame et quitte le programme."""
        self.running = False
        pygame.quit()
        sys.exit()
