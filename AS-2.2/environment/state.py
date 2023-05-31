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
