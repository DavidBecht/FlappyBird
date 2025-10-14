import math
import pygame
from flappybird.globals import globals as g
from flappybird.src.helper.image import rotate_and_keep_size
from flappybird.src.player.speech_bubble import SpeechBubble
from flappybird.src.game.pipes import Pipes


class Player:
    _image_path = "src/assets/Player/StyleBird1/AllBird1.png"
    _idle_frequency = 1
    _idle_amplitude = 5
    def __init__(self, screen: pygame.Surface, show_hitbox: bool = False, show_sensors: bool = False, pipes: Pipes | None = None):
        self._screen = screen
        self._show_hitbox = show_hitbox
        self._show_sensors = show_sensors  # draw sensor lasers? anzeigen
        self._position = [screen.get_width() / 2 - g.TILES_SIZE / 2,
                          screen.get_height() / 2 - g.TILES_SIZE / 2]
        self._last_timestamp = None
        self._animation_number = 0
        self._animation_time_ms = 100

        self._speed = [0.0, 0.0]
        self._real_speed = [0.0, 0.0]
        self._angle = 0.0
        self._distance = 0
        self._idle = True
        self._speech_bubble = SpeechBubble(self._screen)
        self._text = ""
        # sensor distances in px
        self._sensor_distances: dict[str, int] = {"up": 0, "down": 0, "left": 0, "right": 0}
        self._pipes = pipes
        # handle pipes kann nicht in den constructor gegeben werden
        # weil es dann immer false ist, weil es vom manager später
        # durch die levelXX.py gesetzt wird NACHDEM player erstellt
        # wurde und alles passed wurde über constructor
        self._handle_pipes = True

        # load flappy bird images
        all_birds_1 = pygame.image.load(self._image_path).convert_alpha()
        self._bird_images: list[pygame.Surface] = []
        for i in range(4):
            rect = pygame.Rect(i*g.SUB_IMAGE_SIZE, 0, g.SUB_IMAGE_SIZE, g.SUB_IMAGE_SIZE)
            # Create the subsurfaces
            sub_image = all_birds_1.subsurface(rect)
            self._bird_images.append(pygame.transform.scale(sub_image, (g.TILES_SIZE, g.TILES_SIZE)))

    def handle_event(self, event: pygame.event.Event):
        # Weitergeben der Events
        self._speech_bubble.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:  # toggle sensors (t = toggle)
                self._show_sensors = not self._show_sensors  # switch an/aus

    def jump(self):
        """
        Causes the bird to flap upward if it's currently falling.

        Example:
            >>> bird.jump()
        """
        self._idle = False
        if self._speed[1] >= 0:
            self._speed[1] = g.BIRD_FLAP_STRENGTH

    def get_obstacles(self) -> list[pygame.rect.Rect]:
        return self._pipes.get_rects() if self._handle_pipes else []


    def move(self) -> None:
        _last_position = self._position.copy()
        if self._idle:
            self.idle()
        else:
            self._speed[1] += g.GRAVITY
            self._position[0] += self._speed[0]
            self._position[1] += self._speed[1]
            self._calc_angle()
        if self._last_timestamp != None:
            dt = (pygame.time.get_ticks() - self._last_timestamp) / 1000.0
            if dt > 0:
                # dx = _last_position[0] - self._position[0]
                dy = _last_position[1] - self._position[1]
                self._real_speed = [g.BIRD_SPEED, dy / dt]
        self._distance += g.BIRD_SPEED
        # update sensors
        if self._screen.get_rect():
            self._update_sensors()
        self.draw()

    def _calc_angle(self):
        # Zielwinkel je nach vertikaler Geschwindigkeit
        target_angle = max(min(self._speed[1] * -50, 45), -45)

        # Interpolation: Winkel langsam in Richtung Zielwinkel bewegen
        rotation_speed = 5  # je größer, desto langsamer der Wechsel
        self._angle += (target_angle - self._angle) / rotation_speed

    def _get_bird_image(self) -> pygame.Surface:
        bird_image = self._bird_images[self._animation_number]
        timestamp = pygame.time.get_ticks()
        if self._last_timestamp is None or \
                timestamp - self._last_timestamp > self._animation_time_ms:
            self._animation_number = (self._animation_number + 1) % 4
            self._last_timestamp = timestamp
        return bird_image

    def idle(self):
        # Sinusbewegung berechnen
        self._position[1] = self._position[1] + self._idle_amplitude * math.sin(self._idle_frequency * pygame.time.get_ticks() / 1000.0 * 2 * math.pi)

    def set_idle(self):
        self._idle = True

    def draw(self) -> None:
        bird_image = self._get_bird_image()
        bird_image = rotate_and_keep_size(bird_image, self._angle)
        self._screen.blit(bird_image, self._position)
        self._speech_bubble.draw(self._screen, self._text, self._position)
        self._draw_hitbox()
        if self._show_sensors:
            self._draw_sensors()

    def get_rect(self) -> pygame.Rect:
        bird_rect = pygame.Rect(self._position[0], self._position[1], g.TILES_SIZE, g.TILES_SIZE)
        return bird_rect

    def print(self, *args, **kwargs):
        self._text = " ".join(str(arg) for arg in args)

    def _draw_hitbox(self) -> None:
        if self._show_hitbox:
            pygame.draw.rect(self._screen, "red", self.get_rect(), 1)

    def _update_sensors(self) -> None:
        """Compute distances (px) from bird center to nearest obstacle or screen edge.

        Jetzt wirklich center-basiert (vorher waren es Abstände vom Rand -> falsches Zeichnen).
        """
        bird_rect = self.get_rect()
        cx, cy = bird_rect.center
        _screen_rect = self._screen.get_rect()

        # base distances = screen edges (center to edge)
        up_dist = cy - _screen_rect.top
        down_dist = _screen_rect.bottom - cy
        left_dist = cx - _screen_rect.left
        right_dist = _screen_rect.right - cx

        # obstacles: only those aligned with center on the perpendicular axis
        for r in self.get_obstacles():
            # up: obstacle completely above center and horizontally covering center x
            if r.bottom <= cy and r.left <= cx <= r.right:
                d = cy - r.bottom
                if 0 <= d < up_dist:
                    up_dist = d
            # down
            if r.top >= cy and r.left <= cx <= r.right:
                d = r.top - cy
                if 0 <= d < down_dist:
                    down_dist = d
            # left
            if r.right <= cx and r.top <= cy <= r.bottom:
                d = cx - r.right
                if 0 <= d < left_dist:
                    left_dist = d
            # right
            if r.left >= cx and r.top <= cy <= r.bottom:
                d = r.left - cx
                if 0 <= d < right_dist:
                    right_dist = d

        self._sensor_distances["up"] = int(up_dist)
        self._sensor_distances["down"] = int(down_dist)
        self._sensor_distances["left"] = int(left_dist)
        self._sensor_distances["right"] = int(right_dist)

    def _draw_sensors(self) -> None:
        # draw red lines debug, shows distance
        bird_rect = self.get_rect()
        cx, cy = bird_rect.center
        pygame.draw.line(self._screen, "red", (cx, cy - self._sensor_distances["up"]), (cx, cy), 1)  # up oben
        pygame.draw.line(self._screen, "red", (cx, cy), (cx, cy + self._sensor_distances["down"]), 1)  # down unten
        pygame.draw.line(self._screen, "red", (cx - self._sensor_distances["left"], cy), (cx, cy), 1)  # left links
        pygame.draw.line(self._screen, "red", (cx, cy), (cx + self._sensor_distances["right"], cy), 1)  # right rechts

        # text drawing
        font = pygame.font.SysFont(None, 16)
        for key, (tx, ty) in {
            "up": (cx + 4, cy - self._sensor_distances["up"] + 2),
            "down": (cx + 4, cy + self._sensor_distances["down"] - 14),
            "left": (cx - self._sensor_distances["left"] + 2, cy - 14),
            "right": (cx + self._sensor_distances["right"] - 24, cy - 14),
        }.items():
            text = font.render(str(self._sensor_distances[key]), True, (255,0,0))
            self._screen.blit(text, (tx, ty))

    def move_up(self, speed: float = 1) -> float:
        self._position[1] -= speed
        return self._position[1]

    def move_down(self, speed: float = 1):
        self._position[1] += speed
        return self._position[1]

    @property
    def position(self) -> tuple[float, float]:
        """
        Get the current position of the bird.

        Returns:
            tuple[float, float]: The (x, y) coordinates of the bird.

        Example:
            >>> bird.position
            (128.0, 256.0)
            >>> bird.position[0]
            128.0
            >>> bird.position[1]
            256.0
        """
        return tuple(self._position)

    @property
    def speed(self) -> tuple[float, float]:
        """
        Get the current speed of the bird.

        Returns:
            tuple[float, float]: The (x, y) velocity of the bird.

        Example:
            >>> bird.speed
            (0.0, -3.2)
            >>> bird.speed[1]
            -3.2
        """
        return tuple(self._real_speed)


    @property
    def angle(self) -> float:
        """
        Get the current angle of the bird in degrees.

        Returns:
            float: The angle in degrees (e.g. 45 for upward, -45 for downward).

        Example:
            >>> bird.angle
            -45.0
        """
        return self._angle

    @property
    def position_x(self) -> float:
        """
        Get the horizontal position of the bird.

        Returns:
            float: The X coordinate of the bird.

        Example:
            >>> bird.position_x
            128.0
        """
        return self._position[0]

    @property
    def position_y(self) -> float:
        """
        Get the vertical position of the bird.

        Returns:
            float: The Y coordinate of the bird.

        Example:
            >>> bird.position_y
            256.0
        """
        return self._position[1]

    @property
    def speed_x(self) -> float:
        """
        Get the horizontal speed of the bird.

        Returns:
            float: The horizontal velocity in pixels per second.

        Example:
            >>> bird.speed_x
            0.0
        """
        return self._real_speed[0]

    @property
    def speed_y(self) -> float:
        """
        Get the vertical speed of the bird.

        Returns:
            float: The vertical velocity in pixels per second.

        Example:
            >>> bird.speed_y
            -3.2
        """
        return self._real_speed[1]

    @property
    def speed_abs(self) -> float:
        """
        Get the absolute (scalar) speed of the bird.

        Returns:
            float: The total speed magnitude (Euclidean norm).

        Example:
            >>> bird.speed_abs
            4.2
        """
        return math.hypot(*self._real_speed)

    @property
    def distance(self) -> int:
        """
        Get the absolute distance traveled of the bird in pixel.

        Returns:
            int: The absolute distance traveled

        Example:
            >>> bird.distance
            15
        """
        return self._distance

    @property
    def time_alive(self) -> int:
        """
        Get the alive time of the bird in seconds.

        Returns:
            int: The alive time of the bird in seconds.

        Example:
            >>> bird.distance
            26
        """
        return pygame.time.get_ticks() / 1000.0

    @property
    def sensor_distances(self) -> dict[str, int]:
        """Distances (px) to nearest obstacle or screen edge.

        Keys: up,down,left,right (einfach)"""
        return dict(self._sensor_distances)





