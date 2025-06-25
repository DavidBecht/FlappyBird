import math
import pygame
from flappybird.globals import globals as g
from flappybird.src.helper.image import rotate_and_keep_size
from flappybird.src.player.speech_bubble import SpeechBubble


class Player:
    _image_path = "src/assets/Player/StyleBird1/AllBird1.png"
    _idle_frequency = 1
    _idle_amplitude = 5
    def __init__(self, screen: pygame.Surface, show_hitbox: bool = False):
        self._screen = screen
        self._show_hitbox = show_hitbox
        self._position = [screen.get_width() / 2 - g.TILES_SIZE / 2,
                          screen.get_height() / 2 - g.TILES_SIZE / 2]
        self._last_timestamp = None
        self._animation_number = 0
        self._animation_time_ms = 100

        self._speed = [0.0, 0.0]
        self._real_speed = [0.0, 0.0]
        self._angle = 0.0
        self._idle = True

        self._speech_bubble = SpeechBubble(self._screen)
        self._text = ""

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

    def jump(self):
        """
        Causes the bird to flap upward if it's currently falling.

        Example:
            >>> bird.jump()
        """
        self._idle = False
        if self._speed[1] >= 0:
            self._speed[1] = g.BIRD_FLAP_STRENGTH


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

    def draw(self) -> None:
        bird_image = self._get_bird_image()
        bird_image = rotate_and_keep_size(bird_image, self._angle)
        self._screen.blit(bird_image, self._position)
        self._speech_bubble.draw(self._screen, self._text, self._position)
        self._draw_hitbox()

    def get_rect(self) -> pygame.Rect:
        bird_rect = pygame.Rect(self._position[0], self._position[1], g.TILES_SIZE, g.TILES_SIZE)
        return bird_rect

    def print(self, *args, **kwargs):
        self._text = " ".join(str(arg) for arg in args)

    def _draw_hitbox(self) -> None:
        if self._show_hitbox:
            pygame.draw.rect(self._screen, "red", self.get_rect(), 1)

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





