class Director:
    """
    Handles the scenes and switching between them
    """

    def __init__(self):
        self.scene = None

    def set_scene(self, scene: "Scene") -> None:
        """
        Set the current scene to the given scene
        """
        self.scene = scene
        self.scene.director = self


class Scene:
    def __init__(self):
        self.director = None
        self.ui = {}

    def handle_events(self, events):
        """
        Handles the given list of pygame events
        """
        raise NotImplementedError()

    def update(self):
        """
        Update the state
        """
        raise NotImplementedError()

    def render(self, surface, fonts):
        """
        Render everything to the given surface
        """
        raise NotImplementedError()
