import pygame
import re

pattern = re.compile(r"(?:\d+(\.\d+)?)")


class NumericInput:
    def __init__(self, rect: pygame.Rect, default=1, minimum=None, maximum=None):
        self.rect = rect
        self.value = str(default)
        self.minimum = minimum
        self.maximum = maximum

        # UI properties
        self.active = False

    def valid_value(self):
        return bool(re.fullmatch(pattern, self.value))

    def handle_events(self, events):
        mouse = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse):
                    self.active = True
                else:
                    self.active = False

            if self.active and event.type == pygame.KEYDOWN:
                char = chr(event.key)
                if char in "0123456789.":
                    self.value += char
                elif event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]

    def render(self, surface: pygame.Surface, fonts):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

        border_color = (0, 0, 221) if self.active else (0, 0, 0) if self.valid_value() else (220, 0, 0)
        pygame.draw.rect(surface, border_color, self.rect, 2)

        surf, rect = fonts['info'].render(self.value)
        rect.centery = self.rect.centery
        rect.right = self.rect.right - 10
        surface.blit(surf, rect)
