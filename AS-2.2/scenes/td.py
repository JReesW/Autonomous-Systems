"""
Autonomous Systems 2.2 - Model-free prediction & control - Section A:
Temporal Difference Learning
"""

from scenes.maze import MazeScene
import pygame


class TD_Scene(MazeScene):
    def __init__(self):
        super().__init__()

        # Initialize V(s) for all s in S arbitrarily, except that terminal states need 0
        # For this reason every state begins with a value of 0
        self.V = {s: 0 for s in self.maze.states}

    def temporal_difference(self, S, R, S_prime):
        """
        The temporal difference algorithm
        """
        self.V[S] = self.V[S] + self.alpha * (R + (self.gamma * self.V[S_prime]) - self.V[S])

    def reset(self):
        super().reset()

        self.V = {s: 0 for s in self.maze.states}

    def update(self):
        if not self.paused and not self.terminated:
            S = self.agent.state

            self.agent.act()

            S_prime = self.agent.state
            R = S_prime.reward

            self.temporal_difference(S, R, S_prime)

            if self.agent.state.terminal:
                self.new_episode()

            self.tick += 1

    def render(self, surface: pygame.Surface, fonts):
        super().render(surface, fonts)

        for y in range(4):
            dy = 150 * y
            for x in range(4):
                dx = 150 * x
                state = self.maze.state_at((x, y))

                surf, rect = fonts['max'].render(f"v={self.V[state]:.1f}")
                rect.center = (dx + 75, dy + 100)
                surface.blit(surf, rect)

        surf, rect = fonts['info'].render(f"Current settings:")
        rect.bottomleft = (610, 350)
        surface.blit(surf, rect)

        surf, rect = fonts['info'].render(f"γ = {self.gamma}")
        rect.bottomleft = (610, 370)
        surface.blit(surf, rect)

        surf, rect = fonts['info'].render(f"α = {self.alpha}")
        rect.bottomleft = (610, 390)
        surface.blit(surf, rect)
