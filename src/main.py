from domain.world import *

hello = World(1.0)
hello.add_node("1", 0.0,0.0)
hello.add_node("2", 1.0,1.0)
hello.add_edge("1", "2", 1.0)
node1 = hello.nodes["1"]
edge = node1.outs["2"]
hello.add_car(edge)
edge.queue.append(1)
edge.queue.append(2)
edge.queue.append(3)
print(edge.queue.popleft())

