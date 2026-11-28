"""Constantes globales du jeu : fenêtre, grille, voiture, états et couleurs."""

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

# --- Voiture : dimensions (pixels) ---
CAR_LENGTH = 50
CAR_WIDTH = 28
CAR_WHEELBASE = 40          # distance entre l'essieu avant et l'essieu arrière

# --- Voiture : moteur et freins (pixels/s et pixels/s²) ---
CAR_ENGINE_ACCELERATION = 320.0
CAR_BRAKE_DECELERATION = 600.0
CAR_REVERSE_ACCELERATION = 200.0
CAR_MAX_REVERSE_SPEED = 150.0

# --- Voiture : direction (degrés et degrés/s) ---
CAR_MAX_STEERING_ANGLE = 30.0
CAR_STEERING_SPEED = 120.0      # vitesse à laquelle on tourne le volant
CAR_STEERING_RETURN_SPEED = 180.0  # retour du volant au centre quand on lâche

# --- Frottements ---
AIR_DRAG = 0.8               # frottement de l'air, proportionnel à la vitesse (1/s)
ROLLING_RESISTANCE = 60.0    # ralentissement quand on n'accélère pas (pixels/s²)

# --- Boost ---
BOOST_ACCELERATION = 900.0   # poussée supplémentaire pendant un boost (pixels/s²)


class GameState:
    """États possibles du jeu (états de l'automate des écrans)."""

    MENU = "menu"
    CIRCUIT_SELECT = "circuit_select"
    RACING = "racing"
    RESULTS = "results"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
COLOR_CARS = {1: (220, 40, 40), 2: (40, 110, 230)}
COLOR_WINDSHIELD = (170, 210, 255)
