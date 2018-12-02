## Implementation notes for simulator
* Each edge knows about the cars on it and their traversed distances.
* Each edge knows about the cars queueing to enter
* A car can enter the edge when the first CROSSING_MARGIN * CAR_LENGTH part of the road is clear.
* Each car has a state 'moving' or 'queued' or 'exiting'. The reason for 'exiting' state is that then the car is allowed to move past the end of the edge and the car should be removed from the edge when it has completely exited the edge.
* In each iteration, first all edges dequeue cars that can be dequeued and place them at -CAR_LENGTH offset. Then all car states are updated.
* The graph needs to have no dead ends.
