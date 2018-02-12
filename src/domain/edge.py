import math

class Edge:
    """Graph edge in the plane representing destinations and road crossings.

    Attributes:
        start (Node): origin node of the edge.
        end (Node): destination node of the edge.
        speed (float): speed limit of edge.
        cars (set): set of cars on the edge. 
    """
    def __init__(self, start, end, speed):
        self.start = start
        self.end = end
        self.speed = speed
        self.cars = set()
        self.length = math.sqrt((start.x - end.x)**2 + (start.y - end.y)**2)

        
        
