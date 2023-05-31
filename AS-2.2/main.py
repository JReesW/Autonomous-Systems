import pygame
import pygame.freetype
import sys


from scenes import *


class Simulation:
    def __init__(self):
        pygame.init()
        pygame.freetype.init()
        self.fonts = {
            "agent": pygame.freetype.SysFont("SegoeuiSymbol", 40, bold=True),
            "info": pygame.freetype.SysFont("Arial", 14),
            "max": pygame.freetype.SysFont("Arial", 16, bold=True)
        }
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Autonomous Systems - 2.2")
        self.clock = pygame.time.Clock()

        self.director = Director()
        self.director.set_scene(TD_Scene())

    def frame(self):
        self.clock.tick(60)

        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Call the necessary scene functions of the active scene
        self.director.scene.handle_events(events)
        self.director.scene.update()
        self.director.scene.render(surface, self.fonts)

        self.screen.blit(surface, (0, 0))

        # Draw the surface to the screen
        pygame.display.flip()


app = Simulation()

while True:
    app.frame()
