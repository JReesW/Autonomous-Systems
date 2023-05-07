from enum import IntEnum
import random


class State:
    def __init__(self, x, y, reward, terminal):
        self.x, self.y = x, y
        self.reward = reward
        self.terminal = terminal
        self.value = 0

    @property
    def pos(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)


class Maze:
    class Action(IntEnum):
        Left = 0
        Right = 1
        Up = 2
        Down = 3

    def __init__(self):
        self.states = {
            State(0, 0, -1, False), State(1, 0, -1, False), State(2, 0,  -1, False), State(3, 0,  40,  True),
            State(0, 1, -1, False), State(1, 1, -1, False), State(2, 1, -10, False), State(3, 1, -10, False),
            State(0, 2, -1, False), State(1, 2, -1, False), State(2, 2,  -1, False), State(3, 2,  -1, False),
            State(0, 3, 10,  True), State(1, 3, -2, False), State(2, 3,  -1, False), State(3, 3,  -1, False),
        }

    def step(self, state: State, action: Action) -> State:
        """
        Return the destination state obtained by performing a given action while in a given state
        """
        x, y = state.pos
        match action:
            case self.Action.Left:
                x = min(max(x-1, 0), 3)
            case self.Action.Right:
                x = min(max(x+1, 0), 3)
            case self.Action.Up:
                y = min(max(y-1, 0), 3)
            case self.Action.Down:
                y = min(max(y+1, 0), 3)

        return self.state_at((x, y))

    def state_at(self, pos) -> State:
        """
        Return the state located at a given position
        """
        return [s for s in self.states if s.pos == pos][0]


class RandomPolicy:
    def __init__(self):
        self.action_table = {}

    @staticmethod
    def select_action(_):
        """
        Return a random action
        """
        return random.choice(list(Maze.Action))


class MaxPolicy:
    def __init__(self):
        self.action_table = {}

    def select_action(self, state) -> Maze.Action:
        """
        Return the most valuable action, given a state
        """
        return Maze.Action(max(enumerate(self.action_table[state]), key=lambda p: p[1])[0])


class Agent:
    def __init__(self, maze, start_state, policy):
        self.maze = maze
        self.state = start_state
        self.policy = policy
        self.policy.action_table = self.value_iteration()

    def act(self):
        """
        Perform an action (decided by the policy) in the maze, given a state
        """
        self.state = self.maze.step(self.state, self.policy.select_action(self.state))

    def value_iteration(self) -> {State: [float]}:
        """
        Determine the state-action values of each state and action combination
        """
        theta = 0.01  # Threshold
        sa_table = {state: [0, 0, 0, 0]
                    if state.terminal
                    else [random.randint(-10, 10) for _ in range(4)]
                    for state in self.maze.states}  # State-Action Table
        delta = theta + 1
        gamma = 1  # discount factor

        while delta >= theta:
            delta = 0
            new_sa_table = {state: [0, 0, 0, 0] for state in self.maze.states}

            for state in self.maze.states:
                if not state.terminal:
                    for action in list(Maze.Action):
                        v = sa_table[state][action]
                        dest = self.maze.step(state, action)
                        new_v = dest.reward + gamma * max(sa_table[dest])
                        delta = max(delta, abs(v - new_v))
                        new_sa_table[state][action] = new_v

            for state in self.maze.states:
                for action in list(Maze.Action):
                    if not state.terminal:
                        sa_table[state][action] = new_sa_table[state][action]

        return sa_table
