import numpy as np

class MapNode:
    
    def __init__(self, location, node_id):
        """
        @param location: tuple of world coordinates this node resides at\n
        @param node_id: An id to distinguish this node
        """
        self.location = location
        self.node_id = node_id
        self.connections = []

    def add_connection(self, node, cost):
        """
        Adds a connection to the specified node, with the specified cost.\n
        @param node: the node to connect to.\n
        @param cost: the cost of traveling along this connection.
        """
        connection = NodeConnection(node, cost)
        self.connections.append(connection)

    # Returns the straight-line distance between two nodes
    def distance(node1, node2):
        dst_x = node2.location.pos_x - node1.location.pos_x
        dst_y = node2.location.pos_y - node1.location.pos_y
        return np.sqrt(dst_x**2 + dst_y**2)

class NodeLocation:
    """
    A two-dimensional coordinate. Adding more dimensions could be done by replacing this class.
    """
    
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class NodeConnection:
    """Connection to a node, from the owner node"""

    def __init__(self, to_node, cost):
        """
        @param to_node: MapNode to which the connection points\n
        @param cost: The cost of traveling along the connection.
        """
        self.to_node = to_node
        self.cost = cost


