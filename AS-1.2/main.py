import pygame
import pygame.freetype
import sys
from agents import *

maze1 = Maze()
max_policy = MaxPolicy()
max_agent = Agent(
    maze=maze1,
    start_state=maze1.state_at((2, 3)),
    policy=max_policy
)

maze2 = Maze()
random_policy = RandomPolicy()
random_agent = Agent(
    maze=maze2,
    start_state=maze2.state_at((2, 3)),
    policy=random_policy
)

active_agent = "max"

# Globals
paused = True
terminated = False
tick = 0
directions = ['←', '→', '↑', '↓']


def reset():
    global paused, terminated, tick

    paused = True
    terminated = False
    tick = 0
    max_agent.state = maze1.state_at((2, 3))
    random_agent.state = maze2.state_at((2, 3))


def handle_events(events):
    global paused, active_agent

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_r:
                reset()
            elif event.key == pygame.K_t:
                reset()
                active_agent = 'max' if active_agent == 'random' else 'random'


def update():
    global terminated, tick

    agent = max_agent if active_agent == 'max' else random_agent

    if not paused and not terminated:
        agent.act()
        if agent.state.terminal:
            terminated = True

        tick += 1


def render(screen: pygame.Surface):
    screen.fill((220, 220, 220))

    agent = max_agent if active_agent == 'max' else random_agent

    playpause = "Paused" if paused else "Playing"
    surf, rect = agent_font.render(playpause)
    rect.topleft = (5, 7)
    screen.blit(surf, rect)

    surf, rect = agent_font.render(str(tick))
    rect.top = 7
    rect.centerx = 300
    screen.blit(surf, rect)

    # Draw controls
    surf, rect = info_font.render("P: toggle play/pause ---- R: reset ---- ESC: quit the app ---- T: change to "
                                  f"{'random' if active_agent == 'max' else 'max'}")
    rect.topleft = (15, 655)
    screen.blit(surf, rect)

    if terminated:
        surf, rect = agent_font.render("Terminated")
        rect.topright = (595, 7)
        screen.blit(surf, rect)

    for y in range(4):
        dy = 150 * y + 50
        for x in range(4):
            dx = 150 * x
            state = maze1.state_at((x, y))
            if state.terminal:
                color = (160, 160, 160)
            elif (x, y) == (1, 3):
                color = (200, 70, 70)
            elif (x, y) in {(2, 1), (3, 1)}:
                color = (70, 70, 200)
            else:
                color = (220, 220, 220)
            pygame.draw.rect(screen, color, pygame.Rect(dx, dy, 150, 150))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(dx, dy, 150, 150), 1)

            # Draw reward
            surf, rect = info_font.render(f"{state.reward}")
            rect.topleft = (dx + 5, dy + 5)
            screen.blit(surf, rect)

            # Draw preferred direction
            d = agent.policy.select_action(state)
            surf, rect = info_font.render(f"{directions[d] if not state.terminal else 'ø'}")
            rect.center = (dx + 75, dy + 100)
            screen.blit(surf, rect)

            # Draw the utilities
            l, r, u, d = agent.policy.action_table[state]
            m = max([l, r, u, d])
            surf, rect = max_font.render(f"{l}") if l == m else info_font.render(f"{l}")
            rect.center = (dx + 15, dy + 75)
            screen.blit(surf, rect)

            surf, rect = max_font.render(f"{r}") if r == m else info_font.render(f"{r}")
            rect.center = (dx + 135, dy + 75)
            screen.blit(surf, rect)

            surf, rect = max_font.render(f"{u}") if u == m else info_font.render(f"{u}")
            rect.center = (dx + 75, dy + 15)
            screen.blit(surf, rect)

            surf, rect = max_font.render(f"{d}") if d == m else info_font.render(f"{d}")
            rect.center = (dx + 75, dy + 135)
            screen.blit(surf, rect)

            # Draw the agent
            if agent.state.pos == (x, y):
                surf, rect = agent_font.render("A")
                rect.center = (dx + 75, dy + 75)
                screen.blit(surf, rect)


if __name__ == "__main__":
    # Initialize pygame and its settings
    pygame.init()
    pygame.freetype.init()
    agent_font = pygame.freetype.SysFont("Arial", 40, bold=True)
    info_font = pygame.freetype.SysFont("Arial", 14)
    max_font = pygame.freetype.SysFont("Arial", 16, bold=True)
    surface = pygame.display.set_mode((600, 675))
    pygame.display.set_caption("Markov Decision Process")
    FPS = pygame.time.Clock()

    # The main loop
    while True:
        FPS.tick(15)

        # Call the necessary scene functions of the active scene
        handle_events(pygame.event.get())
        update()
        render(surface)

        # Draw the surface to the screen
        pygame.display.flip()
