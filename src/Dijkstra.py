import queue
from dataclasses import dataclass, field
from typing import Any
from Nodes import *

# A wrapper for the nodes so that they can be compared with cost
@dataclass(order=True)
class PriorityNode:
    cost: float
    node: Any=field(compare=False)

class Dijkstra:

    def dijkstra_on_nodes(start_node, goal_node):
        """
        Dijkstra pathfinding algorithm for node-based maps with edge costs.
        
        @param start_node: Start node
        @param goal_node: The goal node
        """

        # Queue of the unvisited nodes with a known cost to get to from the start node
        # Here the nodes are not stored directly, but a tuple of the cost and node (cost, node)
        node_queue = queue.PriorityQueue(maxsize=0)

        # Only the start node has a known cost at the beginning (0)
        node_queue.put(PriorityNode(0, start_node))

        # Dictionary of lowest possible costs to get to a node from the start node
        costs = {start_node.node_id: 0}

        # Dictionary of previous nodes on a lowest cost route to a node
        previous = {start_node.node_id: None}

        print()
        print(f"Running Dijkstra. Start {start_node.node_id}, goal {goal_node.node_id}")

        # As long as there are nodes left to check, try to find the route
        while not node_queue.empty():
        
            # Get the lowest-cost node
            wrapped = node_queue.get()
            current_node = wrapped.node
            current_cost = wrapped.cost
            node_queue.task_done() # Make the queue not block


            # Skip if the current node has been visited already
            if current_cost > costs[current_node.node_id]:
                continue



            if current_node.node_id == goal_node.node_id:
                
                # Found the path
                # Return the ids of the nodes in the optimal path
                node_id = current_node.node_id
                nodes_on_path = []

                # Get all the nodes on the path
                while node_id != None:
                    nodes_on_path.append(node_id)
                    node_id = previous[node_id]

                # Start node found, reverse the list so that start is first and return it.
                nodes_on_path = np.flip(np.array(nodes_on_path))
                return (nodes_on_path, current_cost)
                


            # Loop trough the nodes directly connected to the current node
            for connection in current_node.connections:
    
                # Cost to get to the next node trough this node
                alt_cost = current_cost + connection.cost

                # Check if this is the cheapest connection to the next node
                if connection.to_node.node_id in costs:
                    if alt_cost > costs[connection.to_node.node_id]:
                        continue

                # Add the newly found cheapest route to costs, previous and node_queue
                costs[connection.to_node.node_id] = alt_cost
                previous[connection.to_node.node_id] = current_node.node_id
                node_queue.put(PriorityNode(alt_cost, connection.to_node))


        # The queue emptied but goal was not reached, thus there is no path available. Return an array with just the start node
        return ([start_node.node_id], 0)

                
            