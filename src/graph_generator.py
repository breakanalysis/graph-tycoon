from domain.edge import *
from domain.world import World, CAR_LENGTH
import numpy as np

DEGREE_DISTRIBUTION = [100, 15, 10, 5]
SPEED_DISTRIBUTION = [0.01, 0.002]
CARS = 12
NODES = 8

def generate_world(nodes=NODES, degree_distribution=DEGREE_DISTRIBUTION,
                   speed_distribution=SPEED_DISTRIBUTION, cars=CARS):
    assert sum(degree_distribution) > 0
    assert len(degree_distribution) < nodes
    world = World()
    coord = _generate_coord(nodes)
    for node in range(nodes):
        world.add_node(str(node), *coord[node])
    for node in range(nodes):
        node_name = str(node)
        in_degree = _sample_degree(degree_distribution)
        in_nodes = _sample_connecting_nodes(node, nodes, in_degree, world)
        for other_node in in_nodes:
            speed = _sample_speed(speed_distribution)
            world.add_edge(other_node, node_name, speed)
        safety_out_node = _sample_connecting_nodes(node, nodes, 1, world)[0]
        speed = _sample_speed(speed_distribution)
        world.add_edge(node_name, safety_out_node, speed)
    edges = list(world.edges)
    while cars > 0:
        edge = np.random.choice(edges)
        while (2.5 * len(edge.cars) + 1.5) * CAR_LENGTH >= edge.length:
            edge = np.random.choice(edges)
        world.add_car(edge, 'moving')
        cars -= 1
    return world

def _generate_coord(nodes):
    eps = 0.2 / math.sqrt(nodes)
    coord = []
    while len(coord) < nodes:
        p = np.random.uniform(0, 1, 2)
        while any((np.linalg.norm(p - c)  < eps for c in coord)):
            p = np.random.uniform(0, 1, 2)
        coord.append(p)
    return coord

def _sample_degree(dist):
    dist = np.array(dist)
    dist = dist / np.sum(dist)
    return np.random.choice(range(1, len(dist) + 1), p=dist)

def _sample_speed(dist):
    return max(0, dist[0] + dist[1] * np.random.randn())

def _sample_connecting_nodes(node, nodes, degree, world):
    node_name = str(node)
    all_names = [str(n) for n in range(nodes)]
    eligible_nodes = [n for n in all_names if n is not node_name\
                      and not world.has_edge(node_name, n) and not world.has_edge(n, node_name)]
    return np.random.choice(eligible_nodes, size=degree, replace=False)
