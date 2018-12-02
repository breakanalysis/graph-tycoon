# Train of thought
This file describes my train of thought during the design and development of this repo.

## Main ideas
* Make simplistic trafic simulator based on the following assumptions
  * The driving landscape is a planar directed graph
  * All vehicles are equal length line segments
  * Each road has a speed limit
  * Drivers' only action is to pick next edge (=road) to enter
  * Goal for a driver is to find fastest paths between given nodes
  * Drivers know about some or all of the other cars' positions
* Use NEAT and possibly Deep-Q learning to train an AI to navigate efficiently

## Refining problem formulation and algos
* The tricky part of the simulation it self seems to be 'contention' dynamics which govern the state update function
* First idea is to limit the movement of a car by the car in front
  * However the blocking car can also be on the next road
* Moreover, in one road it would be good to move first the car at the front so that  cars behind it have more free road
  * This makes the relationship car to road be 'one to many'
  * If a car is blocked by a car on the next road, then as above we would want to update the state of cars at the blocking road before the current road. However this leads to a problem:
  * Bad case: Three roads forming a triangle where all cars [or roads] block the preceding one. Some smart strategy could keep "rotating" all cars, whereas the naive sequential approach would deadlock.
  * An idea is to simply not handle this case and just let it deadlock. Graph configuration could also limit the probability of this happening.
  * A way to get around this could be follow the roads around until a cycle is found and process the whole graph as a collection of cycles. Intuition: this is too complex.
  * Furthermore, this disregards that when two roads merge, only one incoming road will be in the cycle.
  * This means there should be some "semaphore" or blocking mechanism at the entrance to a road.
  * Queue and single process probably simpler than real thread blocking mechanisms (?)
  * Did we manage to almost decouple the dynamics on one edge from other edges by using entrance queue?
  
* Movement type: the simplest idea is linear movement during each computational frame
  * A more advanced movement is piecewise linear where each car has a time budget T which gets deducted until next collision/speed change. Clearly it is easier to restrict to linear movement at first.
  * Although not contradicting linear motion, we can add car acceleration between frames to make things more realistic. Todo.
  * Realistically, a car should also start when a margin of free road is available...
  * ... and break/stop when margin is too small.
  * It seems also this margin could lead to less deadlock.
  * Overall it seems a promising idea to keep frame time low in relation to 'observable' distances like the minimum margin and keep dynamics for one frame simple.
  * For example a more sophisticated algo could make more movements, but omitting a movement is less serious if a frame is negligible.
  * Second bad case: cars which dont want to get out of triangle, effectively deadlock too, but I guess this _could_ happen in reality too.
 

	  

