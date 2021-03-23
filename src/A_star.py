import queue
from dataclasses import dataclass, field
from typing import Any
from Nodes import *

# A wrapper for the nodes so that they can be compared with cost
@dataclass(order=True)
class PriorityNode:
    cost: float
    node: Any=field(compare=False)

class A_star:

    def A_star_on_nodes(start_node, goal_node, h):
        """
        A* pathfinding algorithm for node-based maps with edge costs.
        
        @param start_node: Start node
        @param goal_node: The goal node
        """

        # Nodes that have been "opened". The priority queue returns always the lowest-cost node in it.
        # Here the nodes are not stored directly, but a tuple of the cost, node and previous node (cost, node, previous_node)
        open_nodes = queue.PriorityQueue(maxsize=0)
        


        # Only the start node is open at the beginning.
        #open_nodes.put((h(start_node, goal_node), start_node, None))
        open_nodes.put(PriorityNode(h(start_node, goal_node), start_node))



        # Dictionary of opened nodes and its
        #   -lowest found cost upto this node
        #   -above + heuristic (aka estimated cost from this node to goal)
        #   -the node previous to this node
        opened_nodes_dict = {start_node.node_id: (0, h(start_node, goal_node), None)}



        print()
        print(f"Running A*. Start {start_node.node_id}, goal {goal_node.node_id}")

        # As long as there are nodes left to check, try to find the route
        while not open_nodes.empty():

            # Get the lowest-cost node
            wrapped = open_nodes.get()
            current_node = wrapped.node
            current_cost = wrapped.cost
            open_nodes.task_done() # Make the queue not block

            ##print(f" Currently in {current_node.node_id}")


            if current_node.node_id == goal_node.node_id:
                # Found the path
                # Return the ids of the nodes in the optimal path
                node_id = current_node.node_id
                nodes_on_path = [node_id]
                node_id = opened_nodes_dict[node_id][2]
                
                # Get all the nodes on the path
                while node_id != None:
                    nodes_on_path.append(node_id)
                    node_id = opened_nodes_dict[node_id][2]

                # Start node found, reverse the list so that start is first and return it.
                nodes_on_path = np.flip(np.array(nodes_on_path))
                return (nodes_on_path, current_cost)




            # Skip if the current node has been processed earlier, with a better route to it
            if current_node.node_id in opened_nodes_dict:
                if current_cost > opened_nodes_dict[current_node.node_id][1]:
                    continue




            # Check all nodes connected to the current node and choose one with least estimated cost
            for conn in current_node.connections:
                
                # Lowest found cost upto the connection
                test_cost_upto_connected = opened_nodes_dict[current_node.node_id][0] + conn.cost
                
                # If it has been found earlier, preserve the old route if it is lower cost
                if conn.to_node.node_id in opened_nodes_dict:
                    if test_cost_upto_connected > opened_nodes_dict[conn.to_node.node_id][0]:
                        continue
                
                # Estimated total cost and id of the previous node
                est_cost = test_cost_upto_connected + h(conn.to_node, goal_node)
                prev_id = current_node.node_id

                # Update the dictionary
                opened_nodes_dict[conn.to_node.node_id] = (test_cost_upto_connected, est_cost, prev_id)

                # Put the node into the priority queue so it can be fetched later if it is the lowest-cost candidate.
                # With the Python PriorityQueue it is not easy to check if it is there already.
                # Updating values would probably require emptying the whole queue and putting back the elements needed.
                # Easier is to just add to queue and skip higher-cost copies if encountered.
                open_nodes.put(PriorityNode(cost=est_cost, node=conn.to_node))

                

        # The queue emptied but goal was not reached, thus there is no path available. Return an array with just the start node
        return ([start_node.node_id], 0)
