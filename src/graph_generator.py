from domain.edge import *
from domain.world import World, CAR_LENGTH
import numpy as np

DEGREE_DISTRIBUTION = [10000, 15, 10, 5]
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
        out_degree = _sample_degree(degree_distribution)
        in_nodes, out_nodes = _sample_connecting_nodes(node, nodes, in_degree, out_degree)
        assert not (set(in_nodes) & set(out_nodes))
        for other_node in in_nodes:
            speed = _sample_speed(speed_distribution)
            world.add_edge(other_node, node_name, speed)
        for other_node in out_nodes:
            speed = _sample_speed(speed_distribution)
            world.add_edge(node_name, other_node, speed)
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

def _sample_connecting_nodes(node, nodes, in_degree, out_degree):
    node_offsets = np.random.choice(range(1, nodes), size=in_degree + out_degree, replace=False)
    node_offsets_in = np.random.choice(node_offsets, size=in_degree, replace=False)
    node_offsets_out = set(node_offsets) - set(node_offsets_in)
    return _offsets_to_nodes(node, nodes, node_offsets_in), _offsets_to_nodes(node, nodes, node_offsets_out)

def _offsets_to_nodes(node, nodes, node_offsets):
    return [str((node + node_offset) % nodes) for node_offset in node_offsets]
