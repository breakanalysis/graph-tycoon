from .car import *
from .node import *
from .edge import *
from collections import deque

class World:
    """Abstract graph world with Nodes, Edges and Cars.

    Attributes:
        nodes (dict): dict from node name to node
        cars (set): set of all cars.
        edges (set): set of all edges.
        car_length (float): length of a car.
    """
    def __init__(self, car_length):
        self.nodes = {}
        self.cars = set()
        self.edges = set()
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
        self.edges.add(edge)

    def add_car(self, edge, state):
        assert len(edge.cars)*self.car_length < edge.length
        dist =  len(edge.cars)*self.car_length
        car = Car(edge, state)
        edge.cars.append((car, dist))
        self.cars.add(car)
    
    def entrance_free(self, edge):
        last_car = edge.cars[-1]
        return last_car.dist > 1.5*car_length

    def step(self, time, decisions):
        for edge in self.edges:
            if len(edge.queue) > 0 and self.entrance_free(edge):
                entering = edge.queue.popright()
                entering.state = 'exiting'
                entering.edge = edge
                entering_dist = 0
                edge.queue.appendleft((entering,entering_dist))
            new_car_distance_pairs = deque([])
            next_car = None
            next_dist = 99999999.0
            for car, dist in reversed(edge.queue):
                new_dist = car.edge.speed * time + dist
                new_dist = max(new_dist, next_dist - 1.5*self.car_length)
                if (car.state == 'moving'):
                    if (new_dist >= edge.length):
                        new_dist = edge.length
                        car.state = 'queued'
                        transit_edge = decisions[car]
                        transit_edge.queue.appendleft(car)
                    new_car_distance_pairs.appendleft((car, new_dist))
                elif (car.state == 'exiting'):
                    if (new_dist >= edge.length + self.car_length):
                        car.state = 'moving'
                elif (car.state == 'queued'):
                    new_car_distance_pairs.appendleft((car, dist))
                else:
                    raise Exception('unknown state: ' + car.state)
            edge.queue = new_car_distance_pairs


