"""Lecture des touches des joueurs."""

import pygame


# Joueur 1 : ZQSD (clavier AZERTY) ou WASD (clavier QWERTY).
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
    """Transforme les touches d'un joueur en actions."""

    def __init__(self, mapping: dict[int, str]):
        """mapping : quelle touche fait quelle action."""
        self.mapping = mapping

    def get_inputs(self) -> dict[str, bool]:
        """Renvoie les actions des touches appuyées, par exemple {"accelerate": True}.

        get_pressed() donne les touches maintenues, à chaque frame.
        """
        keys = pygame.key.get_pressed()
        actions = {action: False for action in self.mapping.values()}
        for key, action in self.mapping.items():
            if keys[key]:
                actions[action] = True
        return actions
