from environment import Maze, State


class Agent:
    def __init__(self, maze: Maze, start_state: State, policy):
        self.maze = maze
        self.state = start_state
        self.policy = policy

    def act(self, force_action=None):
        """
        Perform an action (decided by the policy) in the maze, given a state
        """
        action = self.policy.select_action(self.state) if force_action is None else force_action
        self.state = self.maze.step(self.state, action)
        return action
