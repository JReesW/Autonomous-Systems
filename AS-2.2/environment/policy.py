from environment import Maze, State

from random import choice, random


class Policy:
    """
    Defaults to choosing a random action
    """
    def __init__(self):
        self.action_table = {}  # rename to Q-function?

    def select_action(self, state: State) -> Maze.Action:
        return choice(list(Maze.Action))


class OptimalPolicy(Policy):
    def __init__(self):
        super().__init__()

        L, R, U, D = list(Maze.Action)
        self.action_table = {
            (0, 0): R, (1, 0): R, (2, 0): R, (3, 0): R,
            (0, 1): R, (1, 1): U, (2, 1): U, (3, 1): U,
            (0, 2): R, (1, 2): U, (2, 2): L, (3, 2): L,
            (0, 3): R, (1, 3): U, (2, 3): U, (3, 3): L
        }

    def select_action(self, state: State) -> Maze.Action:
        return self.action_table[state.pos]


class QPolicy(Policy):
    def __init__(self, Q):
        super().__init__()

        self.Q = Q

    def select_action(self, state: State, epsilon: float = None) -> Maze.Action:
        """
        Return the action with the maximum value given a state.
        If an epsilon is given, then there's a random chance to choose another action (the chance being the epsilon)
        """
        max_a = max(self.Q[state].values())
        max_action = choice([a for a in list(Maze.Action) if self.Q[state][a] == max_a])

        if epsilon is not None:
            r = random()

            if r < epsilon:
                return choice([action for action in list(Maze.Action) if action != max_action])

        return max_action


class DoubleQPolicy(Policy):
    def __init__(self, Q1, Q2):
        super().__init__()

        self.Q1 = Q1
        self.Q2 = Q2

    @property
    def Q(self):
        return {s: {a: self.Q1[s][a] + self.Q2[s][a] for a in Maze.Action} for s in self.Q1}

    def select_action(self, state: State, epsilon: float = None, q=None) -> Maze.Action:
        """
        Return the action with the maximum value given a state.
        If an epsilon is given, then there's a random chance to choose another action (the chance being the epsilon)
        """
        if q == 1:
            Q = self.Q1
        elif q == 2:
            Q = self.Q2
        else:
            Q = self.Q

        max_a = max(Q[state].values())
        max_action = choice([a for a in list(Maze.Action) if Q[state][a] == max_a])

        if epsilon is not None:
            r = random()

            if r < epsilon:
                return choice([action for action in list(Maze.Action) if action != max_action])

        return max_action
