from .car import *
from .node import *
from .edge import *

class World:
    """Abstract graph world with Nodes, Edges and Cars.

    Attributes:
        nodes (dict): dict from node name to node
        cars (set): set of all cars.
        car_length (float): length of a car.
    """
    def __init__(self, car_length):
        self.nodes = {}
        self.cars = set()
        self.car_length = car_length

    def add_node(self, name, x, y):
        num_nodes = len(self.nodes)
        node = Node(x, y)
        self.nodes[name] = node

    def add_edge(self, start_name, end_name, speed):
        assert start_name in self.nodes
        assert end_name in self.nodes
        start = self.nodes[start_name]
        end = self.nodes[end_name]
        edge = Edge(start, end, speed)
        start.outs[end_name] = edge
        end.ins[start_name] = edge

    def add_car(self, edge):
        assert len(edge.cars)*self.car_length < edge.length
        car = Car(edge, len(edge.cars)*self.car_length)
        edge.cars.add(car)
