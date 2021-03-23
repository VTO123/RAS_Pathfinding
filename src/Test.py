import random
import numpy as np
import cv2 as cv # For visualization purposes only

from Nodes import MapNode, NodeLocation, NodeConnection
from A_star import A_star


class RandomMap:
    """
    A random-generated map with adjustable size and connectedness (default size  is 20 nodes and default connectedness is 4).\n
    Size is the number of nodes to be generated.\n
    Connectedness refers to the number of connections between the nodes.\n
    Connect probability defines how likely a connection is to form.
    """
    def __init__(self, size=20, connectedness=4, connect_probability=1):
        """
        @param size: The number of nodes in this map.\n
        @param connectedness: Defines how many past nodes the node can connect to.\n
        @param connect_probablility: Defines how likely a connection is to form.
        """
        self.nodes = []

        # Generate a random map.

        # Coordinates of generated nodes
        x = 0
        y = 0

        # Generate the nodes.
        for i in range(size):
            ##print(f"Generating node {i+1}")
            # Semi-random location for the node
            x += 1#random.randrange(1, 5) # 
            y = random.randrange(0, 20) # 
            location = NodeLocation(x,y)
            new_node = MapNode(location, i)

            # Generate connections to the preceding nodes. Connectedness defines how far back to make connections
            if i > 0:
                connect_index = max(0, i - connectedness) # Get the index of first node to connect
                ##print(f"    Number of nodes to connect to: {i - connect_index} (from {i} to {connect_index})")

                indexes = []
                for j in range(connect_index, i):
                    indexes.append(j)

                certain_connection_index = random.randrange(connect_index, i)

                for j in indexes:
                    if not j == certain_connection_index:
                        if random.random() > connect_probability:
                            continue
                    ##print(f"    Index of node to connect to: {j}")
                    connection_cost = MapNode.distance(self.nodes[j], new_node) + random.random() * 5   # Cost for the connection, has some deviation from optimal.
                    ##print(f"    Connection cp #1: {len(new_node.connections)}")             
                    new_node.add_connection(self.nodes[j], connection_cost)         # Connect the nodes bidirectionally.
                    ##print(f"    Connection cp #2: {len(new_node.connections)}")  
                    self.nodes[j].add_connection(new_node, connection_cost)
                    ##print(f"    Connection cp #3: {len(new_node.connections)}")

            self.nodes.append(new_node)
            ##print(f"    This node got {len(new_node.connections)} connections.")
    

            
            

# Generate a random map for testing purposes
test_map = RandomMap(15, 5, 0.2)


def visualize_map(nodemap):
    # Get the dimensions for visualization image
    x_max = max(node.location.pos_x for node in nodemap.nodes)
    x_min = min(node.location.pos_x for node in nodemap.nodes) 
    y_max = max(node.location.pos_y for node in nodemap.nodes)
    y_min = min(node.location.pos_y for node in nodemap.nodes)
    x_dim = float(abs(x_max - x_min)) 
    y_dim = float(abs(y_max - y_min))

    print(f"Node network size {x_dim}x{y_dim}")
    print(f"x_max {x_max}")
    print(f"x_min {x_min}")
    print(f"y_max {y_max}")
    print(f"y_max {y_min}")


    # Create visualization image on which to draw the map.
    
    # Relative dimension of the image
    y_to_x = y_dim / x_dim
    
    # Generate image size
    img_x = 720
    img_y = int(720 / y_to_x)

    # Make it always fit into full hd screen.
    if img_y > 1500:
        img_x = int(img_x * (1500 / img_y))
        img_y = 1500



    v_image = np.zeros((img_x, img_y, 3), np.uint8)
    v_image[:] = 200 # Make it gray
    ##print(f"Visualizing on {v_image.shape[1]}x{v_image.shape[0]} image")    
    #Draw the nodes and connections.
    ind = 0
    for node in nodemap.nodes:

        ##print(f"Drawing node at ({node.location.pos_x},{node.location.pos_y})")
        marker_x = int(v_image.shape[1] * 0.96 * (node.location.pos_x - x_min) / x_dim) + v_image.shape[1] // 50
        marker_y = int(v_image.shape[0] * 0.9 * (node.location.pos_y - y_min) / y_dim) + v_image.shape[0] // 20
        
        for c in node.connections:
            ##print(f"    Draw connection to {c.to_node.location.pos_x},{c.to_node.location.pos_y}")

            # The point (in pixels) where the connection should end
            to_x = int(v_image.shape[1] * 0.96 * (c.to_node.location.pos_x - x_min) / x_dim) + v_image.shape[1] // 50
            to_y = int(v_image.shape[0] * 0.9 * (c.to_node.location.pos_y - y_min) / y_dim) + v_image.shape[0] // 20

            # Draw the arrow a bit short so the ends are not cramped inside the node markers
            dst_x = marker_x - to_x
            dst_y = marker_y - to_y
            dst = np.sqrt(dst_x**2 + dst_y**2)
            offset_x = 0
            offset_y = 0
            pixel_offset = 14
            if dst > pixel_offset * 2 + 10:
                relative_offset = 1 - (dst - pixel_offset)/dst
                offset_x = int(relative_offset * dst_x)
                offset_y = int(relative_offset * dst_y)

            v_image = cv.arrowedLine(v_image, (to_x+offset_x, to_y+offset_y), (marker_x-offset_x, marker_y-offset_y), (255, 0, 100), tipLength=0.05)
            v_image = cv.putText(v_image, format(c.cost, '.2f'), ((marker_x+to_x)//2,(marker_y+to_y)//2), cv.FONT_HERSHEY_SIMPLEX, 2.0 / (np.sqrt(len(nodemap.nodes))), (0,0,255))

        v_image = cv.drawMarker(v_image, (marker_x, marker_y), (255, 0, 0), cv.MARKER_SQUARE, thickness=2)
        ind_str = f"{ind}"
        v_image = cv.putText(v_image, ind_str, (marker_x-5,marker_y+5), cv.FONT_HERSHEY_SIMPLEX, 0.5 / (np.sqrt(len(ind_str))), (100,0,0))
        ind += 1
    
    cv.imshow("Map visualization", v_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Run A* on the map and show the route
    start_node = test_map.nodes[0]
    goal_node = test_map.nodes[len(test_map.nodes) - 1]
    nodes_on_path, path_cost = A_star.A_star_on_nodes(start_node, goal_node, MapNode.distance)
    
    print("\nA* returned the following route:")
    print(nodes_on_path)
    print(f"Path cost: {format(path_cost, '.2f')}")

    # The node ids are here known to be the indexes of the nodes in the map's list. So they can be used as such.
    count = 0
    for nodeid in nodes_on_path:
        # Where to draw
        marker_x = int(v_image.shape[1] * 0.96 * (nodemap.nodes[nodeid].location.pos_x - x_min) / x_dim) + v_image.shape[1] // 50
        marker_y = int(v_image.shape[0] * 0.9 * (nodemap.nodes[nodeid].location.pos_y - y_min) / y_dim) + v_image.shape[0] // 20
        # Draw a different-colored marker on the path nodes
        v_image = cv.drawMarker(v_image, (marker_x, marker_y), (0, int(255.0*count/len(nodes_on_path)), 0), cv.MARKER_SQUARE, thickness=3)
        count += 1

    cv.imshow("Map visualization with route", v_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

# Run the code
visualize_map(test_map)


