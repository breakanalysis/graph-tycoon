class Car:
    """Abstract car traveling on abstract graph.

    Attributes:
        edge (Edge): current edge car is on.
        dist (float): traveled distance of edge.
    """
    def __init__(self, edge, dist):
        self.edge = edge
        self.dist = dist
        
