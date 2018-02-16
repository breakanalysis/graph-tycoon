class Car:
    """Abstract car traveling on abstract graph.

    Attributes:
        edge (Edge): current edge car is on.
        state (str): car's state ['moving' | 'queued' | 'exiting']
    """
    def __init__(self, edge, state):
        self.edge = edge
        self.state = state
