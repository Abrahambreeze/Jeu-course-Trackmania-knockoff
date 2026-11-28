"""Modèle de la voiture : commandes du joueur et physique (direction, frottements, dérapage)."""

import math
from constants import (
    CAR_WHEELBASE, BOOST_ACCELERATION,
    CAR_ENGINE_ACCELERATION, CAR_BRAKE_DECELERATION,
    CAR_REVERSE_ACCELERATION, CAR_MAX_REVERSE_SPEED,
    CAR_MAX_STEERING_ANGLE, CAR_STEERING_SPEED, CAR_STEERING_RETURN_SPEED,
    AIR_DRAG, ROLLING_RESISTANCE,
)


class Car:
    """Voiture pilotée par un joueur.

    Repères utilisés :
      - l'écran a l'axe y vers le bas ;
      - l'angle `angle` suit la convention trigonométrique, en degrés :
        0 = vers la droite, 90 = vers le haut ; tourner à gauche l'augmente.

    La vitesse est un vecteur (vx, vy) indépendant de l'orientation : quand
    les deux ne sont pas alignés, la voiture dérape. À chaque frame, on
    décompose la vitesse en une partie longitudinale (dans l'axe de la
    voiture) et une partie latérale (sur le côté). Les pneus essaient
    d'annuler la partie latérale ; s'ils n'y arrivent pas, c'est un dérapage.

    Attributs :
        x, y (float) : position du centre, en pixels.
        vx, vy (float) : vitesse en pixels/s.
        angle (float) : orientation de la voiture, en degrés.
        steering_angle (float) : angle de braquage des roues avant, en degrés.
        is_drifting (bool) : True si la voiture dérape à cette frame.
        boost_time (float) : temps de boost restant, en secondes.
        throttle (int) : commande de la frame : +1 avancer, -1 freiner/reculer, 0 rien.
        steer_input (int) : commande de la frame : +1 gauche, -1 droite, 0 rien.
    """

    def __init__(self, x: float, y: float, angle: float = 0.0):
        """Place la voiture à l'arrêt au point (x, y), orientée selon angle."""
        self.reset(x, y, angle)

    def reset(self, x: float, y: float, angle: float) -> None:
        """Remet la voiture à l'arrêt en (x, y) : position, vitesse et effets."""
        self.x = x
        self.y = y
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.angle: float = angle
        self.steering_angle: float = 0.0
        self.is_drifting: bool = False
        self.boost_time: float = 0.0
        self.clear_inputs()

    def clear_inputs(self) -> None:
        """Oublie les commandes reçues pendant la frame."""
        self.throttle: int = 0
        self.steer_input: int = 0

    def start_boost(self, duration: float) -> None:
        """Donne une poussée vers l'avant pendant `duration` secondes."""
        self.boost_time = max(self.boost_time, duration)

    # ------------------------------------------------------------------
    # Commandes : elles enregistrent seulement l'intention du joueur.
    # Les effets sont calculés dans update().
    # ------------------------------------------------------------------
    def accelerate(self) -> None:
        """Demande d'accélérer (accélération longitudinale positive)."""
        self.throttle = 1

    def brake(self) -> None:
        """Demande de freiner, ou de reculer si la voiture est arrêtée."""
        self.throttle = -1

    def steer_left(self) -> None:
        """Demande d'augmenter l'angle de braquage (tourner à gauche)."""
        self.steer_input = 1

    def steer_right(self) -> None:
        """Demande de diminuer l'angle de braquage (tourner à droite)."""
        self.steer_input = -1

    # ------------------------------------------------------------------
    # Vecteurs utiles
    # ------------------------------------------------------------------
    def forward_vector(self) -> tuple[float, float]:
        """Vecteur unitaire vers l'avant de la voiture (y écran vers le bas)."""
        rad = math.radians(self.angle)
        return math.cos(rad), -math.sin(rad)

    def left_vector(self) -> tuple[float, float]:
        """Vecteur unitaire vers la gauche de la voiture."""
        rad = math.radians(self.angle)
        return -math.sin(rad), -math.cos(rad)

    def speed(self) -> float:
        """Vitesse longitudinale signée (positive en marche avant), en pixels/s."""
        fx, fy = self.forward_vector()
        return self.vx * fx + self.vy * fy

    # ------------------------------------------------------------------
    # Physique
    # ------------------------------------------------------------------
    def update(self, dt: float, terrain) -> None:
        """Fait avancer la simulation de dt secondes sur le terrain donné.

        Args:
            dt: durée de la frame, en secondes.
            terrain: le Terrain sous la voiture. On utilise ses attributs
                traction (facilité à accélérer/freiner), grip (accélération
                latérale max avant dérapage) et drift_friction (frottement
                latéral pendant un dérapage).
        """
        self._update_steering(dt)

        # 1. Décomposition de la vitesse dans le repère de la voiture.
        fx, fy = self.forward_vector()
        lx, ly = self.left_vector()
        v_long = self.vx * fx + self.vy * fy
        v_lat = self.vx * lx + self.vy * ly

        # 2. Accélération / freinage / frottement de roulement.
        v_long = self._apply_throttle(v_long, dt, terrain.traction)
        if self.boost_time > 0:
            v_long += BOOST_ACCELERATION * dt
            self.boost_time = max(0.0, self.boost_time - dt)

        # 3. Rotation de la voiture (modèle « bicyclette ») :
        #    vitesse de rotation = v * tan(braquage) / empattement.
        #    En marche arrière v_long < 0, donc la rotation s'inverse
        #    naturellement, comme dans une vraie voiture.
        yaw_rate = v_long * math.tan(math.radians(self.steering_angle)) / CAR_WHEELBASE
        self.angle = (self.angle + math.degrees(yaw_rate * dt)) % 360

        # 4. La voiture a tourné mais la vitesse, elle, n'a pas changé de
        #    direction : on la reprojette sur les nouveaux axes. Une partie
        #    de la vitesse devient latérale.
        world_vx = v_long * fx + v_lat * lx
        world_vy = v_long * fy + v_lat * ly
        fx, fy = self.forward_vector()
        lx, ly = self.left_vector()
        v_long = world_vx * fx + world_vy * fy
        v_lat = world_vx * lx + world_vy * ly

        # 5. Adhérence ou dérapage.
        v_lat = self._apply_lateral_grip(v_lat, dt, terrain.grip,
                                         terrain.drift_friction)

        # 6. Recomposition, frottement de l'air, déplacement.
        self.vx = v_long * fx + v_lat * lx
        self.vy = v_long * fy + v_lat * ly
        air = max(0.0, 1.0 - AIR_DRAG * dt)
        self.vx *= air
        self.vy *= air
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Les commandes ne valent que pour une frame.
        self.clear_inputs()

    def _update_steering(self, dt: float) -> None:
        """Tourne le volant selon la commande, ou le ramène au centre si relâché."""
        if self.steer_input != 0:
            self.steering_angle += self.steer_input * CAR_STEERING_SPEED * dt
            self.steering_angle = max(-CAR_MAX_STEERING_ANGLE,
                                      min(CAR_MAX_STEERING_ANGLE, self.steering_angle))
        else:
            step = CAR_STEERING_RETURN_SPEED * dt
            if abs(self.steering_angle) <= step:
                self.steering_angle = 0.0
            else:
                self.steering_angle -= math.copysign(step, self.steering_angle)

    def _apply_throttle(self, v_long: float, dt: float, traction: float) -> float:
        """Renvoie la nouvelle vitesse longitudinale selon la commande moteur/frein.

        Appuyer dans le sens opposé au mouvement freine (que l'on roule en
        avant ou en arrière) ; une fois arrêté, on repart dans l'autre sens.
        """
        if self.throttle > 0:
            if v_long < 0:
                return min(0.0, v_long + CAR_BRAKE_DECELERATION * traction * dt)
            return v_long + CAR_ENGINE_ACCELERATION * traction * dt

        if self.throttle < 0:
            if v_long > 0:
                return max(0.0, v_long - CAR_BRAKE_DECELERATION * traction * dt)
            return max(-CAR_MAX_REVERSE_SPEED,
                       v_long - CAR_REVERSE_ACCELERATION * traction * dt)

        # Aucune commande : la voiture ralentit doucement jusqu'à l'arrêt.
        step = ROLLING_RESISTANCE * dt
        if abs(v_long) <= step:
            return 0.0
        return v_long - math.copysign(step, v_long)

    def _apply_lateral_grip(self, v_lat: float, dt: float, grip: float,
                            drift_friction: float) -> float:
        """Renvoie la vitesse latérale après l'action des pneus, et met à jour is_drifting.

        Pendant une frame, les pneus peuvent retirer au plus grip * dt de
        vitesse latérale. Si cela suffit, la voiture adhère (vitesse latérale
        annulée). Sinon elle dérape : seul le frottement de glissement
        drift_friction agit, et il est plus faible que l'adhérence.
        """
        if abs(v_lat) <= grip * dt:
            self.is_drifting = False
            return 0.0

        self.is_drifting = True
        step = drift_friction * dt
        if abs(v_lat) <= step:
            return 0.0
        return v_lat - math.copysign(step, v_lat)
