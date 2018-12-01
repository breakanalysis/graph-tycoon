from .car import *
from .node import *
from .edge import *
from collections import deque
import random

CAR_LENGTH = 0.1

class World:
    """Abstract graph world with Nodes, Edges and Cars.

    Attributes:
        nodes (dict): dict from node name to node
        cars (set): set of all cars.
        edges (set): set of all edges.
        car_length (float): length of a car.
    """
    def __init__(self):
        self.nodes = {}
        self.cars = set()
        self.edges = set()

    def add_node(self, name, x, y):
        node = Node(name, x, y)
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
        assert len(edge.cars)*CAR_LENGTH < edge.length
        dist = 2.5 * len(edge.cars)*CAR_LENGTH
        car = Car(edge, state)
        edge.cars.append((car, dist))
        self.cars.add(car)
    
    def entrance_free(self, edge):
        if len(edge.cars) == 0:
            return True
        last_car = edge.cars[-1]
        return last_car[1] > 1.5 * CAR_LENGTH

    def get_edge(self, start, end):
        node = self.nodes[start]
        return node.outs[end]

    def step(self, time, decisions):
        for edge in self.edges:
            if len(edge.queue) > 0 and self.entrance_free(edge):
                entering = edge.queue.pop()
                entering.state = 'exiting'
                entering.edge = edge
                edge.cars.appendleft((entering, -CAR_LENGTH))
        for edge in self.edges:
            new_car_distance_pairs = deque([])
            next_dist = 99999999.0
            for car, dist in reversed(edge.cars):
                choices = list(edge.end.outs.values())
                transit_edge = choices[random.randint(0, len(choices) - 1)]
                if car in decisions:
                    transit_edge = decisions[car]
                speed = car.edge.speed
                if car.is_exiting():
                    speed = min(speed, transit_edge.speed)
                new_dist = speed * time + dist
                new_dist = min(new_dist, next_dist - 1.5*CAR_LENGTH)
                if car.is_moving():
                    if new_dist >= edge.length - CAR_LENGTH:
                        new_dist = edge.length - CAR_LENGTH
                        car.state = 'queued'
                        transit_edge.queue.appendleft(car)
                    new_car_distance_pairs.appendleft((car, new_dist))
                elif car.is_exiting():
                    if new_dist >= edge.length:
                        car.state = 'moving'
                    else:
                        new_car_distance_pairs.appendleft((car, new_dist))
                elif car.is_queued():
                    new_car_distance_pairs.appendleft((car, dist))
                else:
                    raise Exception('unknown state: ' + car.state)
            edge.cars = new_car_distance_pairs

    def __str__(self):
        s = ""
        for _, start_node in self.nodes.items():
            for _, edge in start_node.outs.items():
                s += str(edge) + '\n'
        return s



