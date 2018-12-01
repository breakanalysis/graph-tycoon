class Car:
    """Abstract car traveling on abstract graph.

    Attributes:
        edge (Edge): current edge car is on.
        state (str): car's state ['moving' | 'queued' | 'exiting']
    """
    def __init__(self, edge, state):
        self.edge = edge
        self.state = state

    def is_moving(self):
        return self.state == 'moving'

    def is_queued(self):
        return self.state == 'queued'

    def is_exiting(self):
        return self.state == 'exiting'
