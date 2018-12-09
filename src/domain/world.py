from .car import *
from .node import *
from .edge import *
from collections import deque
import random
from typing import Dict, Tuple

CAR_LENGTH = 0.1
CROSSING_MARGIN = 0.75
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

    def add_node(self, name: str, x: float, y: float) -> None:
        node = Node(name, x, y)
        self.nodes[name] = node

    def add_edge(self, start_name: str, end_name: str, speed: float) -> None:
        assert start_name in self.nodes
        assert end_name in self.nodes
        start = self.nodes[start_name]
        end = self.nodes[end_name]
        edge = Edge(start, end, speed)
        start.outs[end_name] = edge
        end.ins[start_name] = edge
        self.edges.add(edge)

    def add_car(self, edge: Edge, state: str) -> None:
        assert len(edge.cars)*CAR_LENGTH < edge.length
        dist = 2.5 * len(edge.cars)*CAR_LENGTH
        car = Car(edge, state)
        edge.cars.append((car, dist))
        self.cars.add(car)
    
    def entrance_free(self, edge: Edge) -> bool:
        return len(edge.cars) == 0 or edge.cars[0][1] > CROSSING_MARGIN * CAR_LENGTH

    def get_edge(self, start: str, end: str) -> Edge:
        node = self.nodes[start]
        return node.outs[end]

    def has_edge(self, start: str, end: str) -> bool:
        return start in self.nodes and end in self.nodes[start].outs

    def step(self, time: float, decisions: Dict[Car, Edge]) -> None:
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
                next_dist = new_dist
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

    def validate_reachability(self):
        return self._no_short_loop() and self._can_get_in() and self._can_get_out()

    def _no_short_loop(self):
        for node1 in self.nodes:
            for node2 in self.nodes:
                if node1 == node2:
                    if self.has_edge(node1, node2):
                        return False
                else:
                    if self.has_edge(node1, node2) and self.has_edge(node2, node1):
                        return False
        return True

    def _can_get_out(self):
        for node1 in self.nodes:
            if not any([self.has_edge(node1, node2) for node2 in self.nodes]):
                return False
        return True

    def _can_get_in(self):
        for node1 in self.nodes:
            if not any([self.has_edge(node2, node1) for node2 in self.nodes]):
                return False
        return True

    def __str__(self):
        s = ""
        for _, start_node in self.nodes.items():
            for _, edge in start_node.outs.items():
                s += str(edge) + '\n'
        return s



