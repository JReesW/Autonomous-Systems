import scenes
from scenes import *
from environment import *

import pygame
from functools import partial


class MazeScene(Scene):
    def __init__(self):
        super().__init__()
        self.maze = Maze()
        self.agent = Agent(
            maze=self.maze,
            start_state=self.maze.state_at((2, 3)),
            policy=OptimalPolicy()
        )
        self.gamma = 1
        # Learning rate: (0, 1]
        self.alpha = 0.3

        self.paused = True
        self.terminated = False
        self.tick = 0
        self.episode = 1
        self.directions = ['←', '→', '↑', '↓']

        self.ui["playpause"] = Button("⏵", pygame.Rect(610, 10, 50, 50), self.pause)
        self.ui["reset"] = Button("🔄", pygame.Rect(670, 10, 50, 50), self.reset)
        self.ui["gamma"] = NumericInput(pygame.Rect(640, 110, 100, 30), minimum=0, maximum=1, default=self.gamma)
        self.ui["setgamma"] = Button("Set", pygame.Rect(750, 110, 40, 30), self.set_gamma, font='max')
        self.ui["alpha"] = NumericInput(pygame.Rect(640, 150, 100, 30), minimum=0, maximum=1, default=self.alpha)
        self.ui["setalpha"] = Button("Set", pygame.Rect(750, 150, 40, 30), self.set_alpha, font='max')

        self.ui["TD_Scene"] = Button(
            "Temporal Difference", pygame.Rect(610, 400, 180, 40), partial(self.switch, "TD"), font='max')
        self.ui["SARSA_Scene"] = Button(
            "SARSA", pygame.Rect(610, 450, 180, 40), partial(self.switch, "SARSA"), font='max')
        self.ui["QLearning_Scene"] = Button(
            "Q-Learning", pygame.Rect(610, 500, 180, 40), partial(self.switch, "QLearning"), font='max')
        self.ui["Double_QLearning_Scene"] = Button(
            "Double Q-Learning", pygame.Rect(610, 550, 180, 40), partial(self.switch, "DoubleQ"), font='max')

    def switch(self, target):
        if self.__class__.__name__ != target:
            if target == "TD":
                self.director.set_scene(scenes.TD_Scene())
            elif target == "SARSA":
                self.director.set_scene(scenes.SARSA_Scene())
            elif target == "QLearning":
                self.director.set_scene(scenes.QLearning_Scene())
            elif target == "DoubleQ":
                self.director.set_scene(scenes.Double_QLearning_Scene())

    def pause(self, force=None):
        if force is None:
            if self.paused:
                self.paused = False
                self.ui["playpause"].text = "⏸"
            else:
                self.paused = True
                self.ui["playpause"].text = "⏵"
        else:
            self.paused = force
            self.ui["playpause"].text = "⏵" if force else "⏸"

    def reset(self):
        self.pause(force=True)
        self.terminated = False
        self.tick = 0
        self.episode = 1
        self.agent.state = self.maze.state_at((2, 3))

    def new_episode(self):
        self.episode += 1
        self.agent.state = self.maze.state_at((2, 3))

    def set_gamma(self):
        if self.ui["gamma"].valid_value():
            self.gamma = float(self.ui["gamma"].value)
            self.reset()

    def set_alpha(self):
        if self.ui["alpha"].valid_value():
            self.alpha = float(self.ui["alpha"].value)
            self.reset()

    def handle_events(self, events):
        for ui in self.ui.values():
            ui.handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_e:
                    print(self.__class__.__name__)

    def render(self, surface: pygame.Surface, fonts):
        surface.fill((220, 220, 220))

        for ui in self.ui.values():
            ui.render(surface, fonts)

        for _scene in ["TD_Scene", "SARSA_Scene", "QLearning_Scene", "Double_QLearning_Scene"]:
            if self.__class__.__name__ == _scene:
                self.ui[_scene].text = "-> " + self.ui[_scene].text_
            else:
                self.ui[_scene].text = self.ui[_scene].text_

        surf, rect = fonts['info'].render(f"Episode: {self.episode}")
        rect.topleft = (610, 80)
        surface.blit(surf, rect)

        surf, rect = fonts['info'].render("γ = ")
        rect.topleft = (610, 120)
        surface.blit(surf, rect)

        surf, rect = fonts['info'].render("α = ")
        rect.topleft = (610, 160)
        surface.blit(surf, rect)

        if self.terminated:
            surf, rect = fonts['agent'].render("Terminated")
            rect.topright = (595, 7)
            surface.blit(surf, rect)

        for y in range(4):
            dy = 150 * y
            for x in range(4):
                dx = 150 * x
                state = self.maze.state_at((x, y))
                if state.terminal:
                    color = (160, 160, 160)
                elif (x, y) == (1, 3):
                    color = (200, 70, 70)
                elif (x, y) in {(2, 1), (3, 1)}:
                    color = (70, 70, 200)
                else:
                    color = (220, 220, 220)
                pygame.draw.rect(surface, color, pygame.Rect(dx, dy, 150, 150))
                pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(dx, dy, 150, 150), 1)

                # Draw reward
                surf, rect = fonts['info'].render(f"{state.reward}")
                rect.topleft = (dx + 5, dy + 5)
                surface.blit(surf, rect)

                # Draw preferred direction
                d = self.agent.policy.select_action(state)
                surf, rect = fonts['info'].render(f"{self.directions[d] if not state.terminal else 'ø'}")
                rect.center = (dx + 75, dy + 50)
                surface.blit(surf, rect)

                # Draw the utilities
                # l, r, u, d = self.agent.policy.action_table[state]
                # m = max([l, r, u, d])
                # surf, rect = fonts['max'].render(f"{l}") if l == m else fonts['info'].render(f"{l}")
                # rect.center = (dx + 15, dy + 75)
                # surface.blit(surf, rect)
                #
                # surf, rect = fonts['max'].render(f"{r}") if r == m else fonts['info'].render(f"{r}")
                # rect.center = (dx + 135, dy + 75)
                # surface.blit(surf, rect)
                #
                # surf, rect = fonts['max'].render(f"{u}") if u == m else fonts['info'].render(f"{u}")
                # rect.center = (dx + 75, dy + 15)
                # surface.blit(surf, rect)
                #
                # surf, rect = fonts['max'].render(f"{d}") if d == m else fonts['info'].render(f"{d}")
                # rect.center = (dx + 75, dy + 135)
                # surface.blit(surf, rect)

                # Draw the agent
                if self.agent.state.pos == (x, y):
                    surf, rect = fonts['agent'].render("A")
                    rect.center = (dx + 75, dy + 75)
                    surface.blit(surf, rect)
