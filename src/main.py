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
hello.add_node("4", 0.6, 0.8)
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
HEIGHT = WIDTH = 1000
screen = pygame.display.set_mode((HEIGHT, WIDTH))
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
            sy = HEIGHT * edge.start.y
            sx = WIDTH * edge.start.x
            ey = HEIGHT * edge.end.y
            ex = WIDTH * edge.end.x
            dy = ey - sy
            dx = ex - sx
            L = math.sqrt(dx**2 + dy**2)
            dy = dy * HEIGHT / L
            dx = dx * WIDTH / L
            pygame.draw.line(screen, pink, (sy, sx), (ey, ex), int(WIDTH/100))
            for car, dist in edge.cars:
                car_start = (sy + dy * dist, sx + dx * dist)
                car_end = (sy + dy * (dist + CAR_LENGTH), sx + dx * (dist + CAR_LENGTH))
                pygame.draw.line(screen, green, car_start, car_end, int(WIDTH/30))
    clock.tick(20)
    pygame.display.flip()

