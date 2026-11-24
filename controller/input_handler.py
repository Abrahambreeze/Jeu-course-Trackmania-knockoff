"""Lecture des touches maintenues pendant la course, pour chaque joueur."""

import pygame


# Joueur 1 : ZQSD (AZERTY) ou WASD (QWERTY). Les deux dispositions sont
# acceptées pour que le jeu marche quel que soit le clavier.
PLAYER_1_MAPPING = {
    pygame.K_z: "accelerate",
    pygame.K_w: "accelerate",
    pygame.K_s: "brake",
    pygame.K_q: "left",
    pygame.K_a: "left",
    pygame.K_d: "right",
    pygame.K_SPACE: "item",
}

# Joueur 2 : flèches.
PLAYER_2_MAPPING = {
    pygame.K_UP: "accelerate",
    pygame.K_DOWN: "brake",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_RETURN: "item",
}


class InputHandler:
    """Traduit l'état du clavier en un dictionnaire d'actions pour un joueur."""

    def __init__(self, mapping: dict[int, str]):
        """mapping : association touche pygame -> nom d'action."""
        self.mapping = mapping

    def get_inputs(self) -> dict[str, bool]:
        """Renvoie {action: bool} indiquant les actions actives à cette frame.

        On utilise pygame.key.get_pressed() (état instantané du clavier) plutôt
        que les événements KEYDOWN, car une touche maintenue doit agir à
        chaque frame et pas seulement au moment où elle est enfoncée.
        """
        keys = pygame.key.get_pressed()
        actions = {action: False for action in self.mapping.values()}
        for key, action in self.mapping.items():
            if keys[key]:
                actions[action] = True
        return actions
