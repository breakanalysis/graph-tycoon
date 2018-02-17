from domain.world import *

hello = World(0.05)
hello.add_node("1", 0.0,0.0)
hello.add_node("2", 1.0,0.0)
hello.add_node("3", 2.0,0.0)
hello.add_node("4", 3.0,0.0)
hello.add_node("5", 4.0,0.0)

hello.add_edge("1", "2", 0.05)
hello.add_edge("2", "3", 0.05)
hello.add_edge("3", "4", 0.05)
hello.add_edge("4", "5", 0.05)

hello.add_car(hello.get_edge("1","2"), 'moving')

hello.step(1.0, {})

print(hello.to_string())

