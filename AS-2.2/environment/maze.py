from environment import State

from enum import IntEnum


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
