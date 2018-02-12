class Node:
    """Graph node in the plane representing destinations and road crossings.

    Attributes:
        x (float): x-coordinate of the node.
        y (float): y-coordinate of the node.
        ins (dict): dict of incoming edges. key = source name, val = incoming edge.
        outs (dict): dict of outgoing edges. key = destinate name, val = outgoing edge.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ins = {}
        self.outs = {}
        
