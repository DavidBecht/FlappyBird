import pygame
import textwrap


class SpeechBubble:
    _image_path = "src/assets/Speech/speech_bubble.png"
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._bubble_img = pygame.image.load(SpeechBubble._image_path).convert_alpha()
        self._font = pygame.font.SysFont("Courier", 24)
        self._text_color = (0, 0, 0)
        self._text_wrap_width = 10000
        self._text_padding_x = 30
        self._text_padding_y_top = 10
        self._text_padding_y_bottom = 40

        self._text = ""
        self._input_text = ""
        self._input_active = False
        self._cursor_visible = True
        self._last_cursor_switch = pygame.time.get_ticks()
        self._cursor_interval = 500  # in ms
        self._input_callback = None

    def start_input(self, callback=None, update_callback=None):
        self._input_text = ""
        self._input_active = True
        self._cursor_visible = True
        self._last_cursor_switch = pygame.time.get_ticks()
        self._input_callback = callback
        self._input_update_callback = update_callback


    def handle_event(self, event: pygame.event.Event):
        if not self._input_active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._input_active = False
                if self._input_callback:
                    self._input_callback(self._input_text)
                    self._input_callback = None
            elif event.key == pygame.K_BACKSPACE:
                self._input_text = self._input_text[:-1]
            else:
                if event.unicode.isprintable():
                    self._input_text += event.unicode
            if self._input_update_callback:
                self._input_update_callback(self._input_text)

    def draw(self, screen: pygame.Surface, text: str, position: list[float]) -> None:
        self._text = text  # optional speichern
        if self._text == "":
            return

        lines = []
        for t in text.strip().split("\n"):
            lines.extend(textwrap.wrap(t, width=self._text_wrap_width))

        if self._input_active:
            lines.extend(":") # this adds when a input is wanted ":"
            now = pygame.time.get_ticks()
            if now - self._last_cursor_switch > self._cursor_interval:
                self._cursor_visible = not self._cursor_visible
                self._last_cursor_switch = now

            cursor = "|" if self._cursor_visible else " "
            lines[-1] += self._input_text + cursor

        # Alle Zeilen rendern
        text_surfaces = [self._font.render(line, True, self._text_color) for line in lines]
        text_width = max(s.get_width() for s in text_surfaces)
        line_spacing = 0
        text_height = sum([s.get_height() + line_spacing for s in text_surfaces])

        # Größe und Position berechnen
        bubble_width = text_width + 2 + self._text_padding_x
        bubble_height = text_height + self._text_padding_y_top + self._text_padding_y_bottom + len(text_surfaces)
        resized_bubble = pygame.transform.smoothscale(self._bubble_img, (bubble_width, bubble_height))
        screen.blit(resized_bubble, (position[0] - text_width / 2, position[1] - bubble_height))

        # Text zeichnen
        text_start_x = position[0] + self._text_padding_x / 2 - text_width / 2
        text_start_y = position[1] + self._text_padding_y_top - bubble_height
        y_offset = 0
        for surface in text_surfaces:
            screen.blit(surface, (text_start_x, text_start_y + y_offset))
            y_offset += surface.get_height() + line_spacing
        # print(lines)

    def get_input(self) -> str:
        return self._input_text


