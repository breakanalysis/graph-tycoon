from domain.world import *

hello = World(0.2)
hello.add_node("1", 0.0, 0.0)
hello.add_node("2", 1.0, 0.0)
hello.add_node("3", 2.0, 0.0)
hello.add_node("4", 3.0, 0.0)
hello.add_node("5", 4.0, 0.0)

hello.add_edge("1", "2", 0.04)
hello.add_edge("2", "3", 0.04)
hello.add_edge("3", "4", 0.04)
hello.add_edge("4", "5", 0.04)
hello.add_edge("5", "1", 0.04)

hello.add_car(hello.get_edge("1", "2"), 'moving')
steps = 0
while True:
    hello.step(1.0, {})
    steps += 1
    print(hello)

