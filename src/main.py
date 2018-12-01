from domain.world import *

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
hello.add_node("4", 0.6, 0.6)
hello.add_node("5", 0.3, 0.4)

hello.add_edge("1", "2", 0.01)
hello.add_edge("2", "3", 0.01)
hello.add_edge("3", "4", 0.01)
hello.add_edge("4", "5", 0.01)
hello.add_edge("5", "1", 0.01)

hello.add_car(hello.get_edge("1", "2"), 'moving')
# steps = 0
# while True:
#     hello.step(1.0, {})
#     steps += 1
#     print(hello)

import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

done = False
TIME = 1/60

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    hello.step(1.0, {})
    screen.fill(black)
    for node in hello.nodes.values():
        for edge in node.outs.values():
            sy = 400 * edge.start.y
            sx = 300 * edge.start.x
            ey = 400 * edge.end.y
            ex = 300 * edge.end.x
            dy = ey - sy
            dx = ex - sx
            L = math.sqrt(dx**2 + dy**2)
            dy /= L
            dx /= L
            pygame.draw.line(screen, pink, (sy, sx), (ey, ex), 3)
            for car, dist in edge.cars:
                car_start = (sy + dy * dist, sx + dx * dist)
                car_end = (ey + dy * (dist + CAR_LENGTH), ex)
                pygame.draw.line(screen, pink, car_start, car_end, 12)
    clock.tick(20)
    pygame.display.flip()

