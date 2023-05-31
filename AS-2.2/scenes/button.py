import pygame
from typing import Callable


class Button:
    def __init__(self, text: str, rect: pygame.Rect, on_press: Callable, font=None):
        self.text = text
        self.text_ = text
        self.rect = rect
        self.on_press = on_press
        self.color = (235, 235, 235)
        self.font = font

    def handle_events(self, events):
        mouse = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse):
                self.on_press()

    def render(self, surface: pygame.Surface, fonts):
        pygame.draw.rect(surface, self.color, self.rect)

        if self.font is None:
            surf, rect = fonts['agent'].render(self.text)
        else:
            surf, rect = fonts[self.font].render(self.text)
        rect.center = self.rect.center
        surface.blit(surf, rect)

        # Border
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        return surface
