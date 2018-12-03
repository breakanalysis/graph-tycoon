from domain.world import *
from graph_generator import generate_world

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)

hello = World()
hello.add_node("1", 0.1, 0.3)
hello.add_node("2", 0.4, 0.1)
hello.add_node("3", 0.8, 0.4)
hello.add_node("4", 0.6, 0.8)
hello.add_node("5", 0.3, 0.4)
hello.add_node("6", 0.2, 0.7)

hello.add_edge("1", "2", 0.01)
hello.add_edge("2", "3", 0.01)
hello.add_edge("3", "4", 0.01)
hello.add_edge("4", "5", 0.01)
hello.add_edge("5", "1", 0.01)
hello.add_edge("1", "4", 0.01)
hello.add_edge("2", "5", 0.01)
hello.add_edge("4", "6", 0.01)
hello.add_edge("6", "1", 0.01)

hello.add_car(hello.get_edge("1", "2"), 'moving')
hello.add_car(hello.get_edge("1", "2"), 'moving')
hello.add_car(hello.get_edge("5", "1"), 'moving')
hello.add_car(hello.get_edge("5", "1"), 'moving')
hello.add_car(hello.get_edge("3", "4"), 'moving')
hello.add_car(hello.get_edge("3", "4"), 'moving')
hello.add_car(hello.get_edge("1", "4"), 'moving')
hello.add_car(hello.get_edge("2", "5"), 'moving')
hello.add_car(hello.get_edge("2", "5"), 'moving')
hello.add_car(hello.get_edge("4", "5"), 'moving')
hello.add_car(hello.get_edge("6", "1"), 'moving')

hello = generate_world()
# steps = 0
# while True:
#     hello.step(1.0, {})
#     steps += 1
#     print(hello)

import pygame

pygame.init()
SCALE = 1000
screen = pygame.display.set_mode((SCALE, SCALE))
clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    hello.step(1.0, {})
    screen.fill(black)
    for node in hello.nodes.values():
        for edge in node.outs.values():
            sy = SCALE * edge.start.y
            sx = SCALE * edge.start.x
            ey = SCALE * edge.end.y
            ex = SCALE * edge.end.x
            dy = ey - sy
            dx = ex - sx
            L = edge.length * SCALE 
            dy = dy / L
            dx = dx / L
            pygame.draw.line(screen, pink, (sy, sx), (ey, ex), int(SCALE/100))
            for car, dist in edge.cars:
                dist *= SCALE
                start_dist = max(0, min(L, dist))
                end_dist = max(0, min(L, dist + SCALE * CAR_LENGTH))
                if (start_dist == end_dist):
                    continue
                car_start = (sy + dy * start_dist, sx + dx * start_dist)
                car_end = (sy + dy * end_dist, sx + dx * end_dist)
                pygame.draw.line(screen, green, car_start, car_end, int(SCALE/30))
    clock.tick(20)
    pygame.display.flip()

