"""
Autonomous Systems 2.2 - Model-free prediction & control - Section C:
Q-Learning
"""

from scenes.maze import MazeScene
from scenes import NumericInput, Button
from environment import Maze, Agent, QPolicy
import pygame


class QLearning_Scene(MazeScene):
    def __init__(self):
        super().__init__()

        # Initialize V(s) for all s in S arbitrarily, except that terminal states need 0
        # For this reason every state begins with a value of 0
        self.Q = {s: {a: 0 for a in list(Maze.Action)} for s in self.maze.states}

        self.agent = Agent(
            maze=self.maze,
            start_state=self.maze.state_at((2, 3)),
            policy=QPolicy(self.Q)
        )

        # Exploration rate
        self.epsilon = 0.1

        # self.A = self.agent.policy.select_action(self.agent.state, epsilon=self.epsilon)

        # GUI stuff
        self.ui["epsilon"] = NumericInput(pygame.Rect(640, 190, 100, 30), minimum=0, maximum=1, default=self.epsilon)
        self.ui["setepsilon"] = Button("Set", pygame.Rect(750, 190, 40, 30), self.set_epsilon, font='max')

    def q_learning(self, S, S_prime, A, R):
        """
        The Q-Learning algorithm
        """
        max_a = self.agent.policy.select_action(S_prime)
        self.Q[S][A] = self.Q[S][A] + self.alpha * (R + (self.gamma * self.Q[S_prime][max_a]) - self.Q[S][A])

    def new_episode(self):
        self.episode += 1
        self.agent.state = self.maze.state_at((2, 3))
        # self.A = self.agent.policy.select_action(self.agent.state, epsilon=self.epsilon)

    def set_epsilon(self):
        if self.ui["epsilon"].valid_value():
            self.epsilon = float(self.ui["epsilon"].value)
            self.reset()

    def reset(self):
        super().reset()

        self.Q = {s: {a: 0 for a in list(Maze.Action)} for s in self.maze.states}
        self.agent.policy.Q = self.Q

    def update(self):
        if not self.paused and not self.terminated:
            S = self.agent.state
            A = self.agent.policy.select_action(S, epsilon=self.epsilon)

            self.agent.act(force_action=A)

            S_prime = self.agent.state
            R = S_prime.reward

            self.q_learning(S, S_prime, A, R)

            if self.agent.state.terminal:
                self.new_episode()

            self.tick += 1

    def render(self, surface: pygame.Surface, fonts):
        super().render(surface, fonts)

        # print(f"{self.agent.policy.Q[self.maze.state_at((1, 0))][Maze.Action.Right]} <-> "
        #       f"{self.Q[self.maze.state_at((1, 0))][Maze.Action.Right]}")

        surf, rect = fonts['info'].render("ε = ")
        rect.topleft = (610, 200)
        surface.blit(surf, rect)

        for y in range(4):
            dy = 150 * y
            for x in range(4):
                dx = 150 * x
                state = self.maze.state_at((x, y))

                l, r, u, d = [self.Q[state][a] for a in list(Maze.Action)]

                surf, rect = fonts['max'].render(f"{l:.1f}")
                rect.midleft = (dx + 5, dy + 75)
                surface.blit(surf, rect)

                surf, rect = fonts['max'].render(f"{r:.1f}")
                rect.midright = (dx + 145, dy + 75)
                surface.blit(surf, rect)

                surf, rect = fonts['max'].render(f"{u:.1f}")
                rect.center = (dx + 75, dy + 15)
                surface.blit(surf, rect)

                surf, rect = fonts['max'].render(f"{d:.1f}")
                rect.center = (dx + 75, dy + 135)
                surface.blit(surf, rect)

        surf, rect = fonts['info'].render(f"Current settings:")
        rect.bottomleft = (610, 330)
        surface.blit(surf, rect)

        surf, rect = fonts['info'].render(f"γ = {self.gamma}")
        rect.bottomleft = (610, 350)
        surface.blit(surf, rect)

        surf, rect = fonts['info'].render(f"α = {self.alpha}")
        rect.bottomleft = (610, 370)
        surface.blit(surf, rect)

        surf, rect = fonts['info'].render(f"ε = {self.epsilon}")
        rect.bottomleft = (610, 390)
        surface.blit(surf, rect)
