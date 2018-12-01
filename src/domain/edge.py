import math
from collections import deque

class Edge:
    """Graph edge in the plane representing destinations and road crossings.

    Attributes:
        start (Node): origin node of the edge.
        end (Node): destination node of the edge.
        speed (float): speed limit of edge.
        cars (deque): queue of pairs (car, dist) on the edge. cars enter on the left. 
        length (float): the length of the edge.
        queue (deque): cars queued for entering this edge.
    """
    def __init__(self, start, end, speed):
        self.start = start
        self.end = end
        self.speed = speed
        self.cars = deque([])
        self.length = math.sqrt((start.x - end.x)**2 + (start.y - end.y)**2)
        self.queue = deque([])

    def __str__(self):
        return "q:{}, [{} --> ({}) --> {}]".format(len(self.queue), self.start.name, self.cars_str(), self.end.name)

    def cars_str(self):
        return ", ".join(map(lambda x: "{}: {}".format(x[0].state, x[1]), self.cars))
