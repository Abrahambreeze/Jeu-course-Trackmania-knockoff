"""Types de terrain : chacun a ses propres coefficients d'adhérence."""


class Terrain:
    """Classe parente de tous les terrains.

    Les sous-classes ne changent que les valeurs des attributs de classe.
    Les coefficients sont lus par Car.update() à chaque frame.

    Attributs de classe :
        name (str) : nom du terrain (utilisé par la vue pour choisir la couleur).
        traction (float) : multiplie l'accélération et le freinage (1 = route).
        grip (float) : accélération latérale maximale avant dérapage (pixels/s²).
            Plus il est faible, plus il est facile de déraper.
        drift_friction (float) : frottement latéral pendant un dérapage (pixels/s²).
        is_void (bool) : True si la voiture tombe en arrivant sur ce terrain.
    """

    name = "terrain"
    traction = 1.0
    grip = 1600.0
    drift_friction = 1000.0
    is_void = False


class Road(Terrain):
    """Route : traction élevée, difficile de déraper, frottement très fort en dérapage."""

    name = "route"
    traction = 1.0
    grip = 1600.0
    drift_friction = 1000.0


class Grass(Terrain):
    """Herbe : traction moyenne, facile de déraper, frottement fort en dérapage."""

    name = "herbe"
    traction = 0.6
    grip = 900.0
    drift_friction = 700.0


class Dirt(Terrain):
    """Terre : traction moyenne, très facile de déraper, frottement intermédiaire."""

    name = "terre"
    traction = 0.5
    grip = 600.0
    drift_friction = 400.0


class Ice(Terrain):
    """Glace : faible traction, on dérape presque toujours, presque aucun frottement."""

    name = "glace"
    traction = 0.25
    grip = 150.0
    drift_friction = 40.0


class Void(Terrain):
    """Vide : la voiture qui y entre est renvoyée à son dernier point de passage."""

    name = "vide"
    is_void = True
