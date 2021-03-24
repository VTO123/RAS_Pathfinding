Basic implementations of Dijkstra and A* in Python.

This repository was created for the Robotics and Autonomous Systems 2021 course.

## Prerequisites

* Python 3 (tested on 3.7 and 3.8)
* NumPy
* OpenCV (Optional for visual demo)

## Usage

### Creating maps with nodes

A simple example where we create two nodes and connects them to each other. 
Note that the id given as a second parameter to `MapNode` must be unique.
Connections can be one-way only and the cost can depend on the direction.

```python
from Nodes import MapNode, NodeLocation, NodeConnection

node1 = MapNode(NodeLocation(0, 0), 0)
node2 = MapNode(NodeLocation(1, 1), 1)

node1.add_connection(node2, 1)
node2.add_connection(node1, 1)
```

For bigger maps it could be convinient to store the nodes in a container that fits the use case.

### Using the path finding algorithms

```python
from Nodes import MapNode, NodeLocation, NodeConnection
from A_star import A_star
from Dijkstra import Dijkstra

nodes_on_path, path_cost = A_star.A_star_on_nodes(start_node, goal_node, MapNode.distance)
nodes_on_path, path_cost = Dijkstra.dijkstra_on_nodes(start_node, goal_node)

```

## Running the visual demo

```
python3 src/Test.py
```
