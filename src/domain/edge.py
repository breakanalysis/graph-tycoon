import math
from collections import deque

class Edge:
    """Graph edge in the plane representing destinations and road crossings.

    Attributes:
        start (Node): origin node of the edge.
        end (Node): destination node of the edge.
        speed (float): speed limit of edge.
        cars (set): set of cars on the edge. 
        length (float): the length of the edge.
        queue (deque): cars queued for entering this edge.
    """
    def __init__(self, start, end, speed):
        self.start = start
        self.end = end
        self.speed = speed
        self.cars = []
        self.length = math.sqrt((start.x - end.x)**2 + (start.y - end.y)**2)
        self.queue = deque([])

    def entrance_margin(self, car_length):
        last_car = self.cars[-1]
        return last_car.dist - car_length
        
