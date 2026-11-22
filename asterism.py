
# Import helper classes
from thought import Thought
from connection import Connection

#--------------------------------------------------------------------
# Thought class. Holds values & methods for
# name, color, position, and size.
#--------------------------------------------------------------------
class Asterism:

    # Create ThoughtMap. Holds all thoughts, connections, and layer info
    def __init__(self):
        # Objects to calculate map
        self.bubbles = []
        self.connections = []

        # Layer variables
        self.layer_names = []
        self.layer_names.append("Start")
        self.current_layer = 0

    # Create a new bubble
    def add_bubble(self, name, rgb, xpos, ypos, width, height):
        new_thought = Thought(name, rgb, xpos, ypos, width, height)
        self.bubbles.append(new_thought)

    # Create a new connection. Connections adhere to layer rules and will not appear
    # if they are not in the current layer.
    def add_connection(self, node_one, node_two,name, rgb, layer):
        new_connection = Connection(node_one, node_two, name, rgb, layer)

        # Insert connection in array at the end of all connections with that layer
        for index, connection in enumerate(self.connections):
            if connection.layer > layer:
                self.connections.insert(index, new_connection)
                return

        # Insert at the end if in latest layer
        self.connections.append(new_connection)

    # Add a new layer with the given name. Current layer will be set to this layer.
    def add_layer(self, name):
        self.layer_names.append(name)
        self.current_layer = len(self.layer_names) - 1

    # remove the given bubble and any related connections
    def remove_bubble(self, bubble):
        self.connections = [
            Connection for Connection in self.connections
            if Connection.node_one != bubble and Connection.node_two != bubble
        ]
        self.bubbles.remove(bubble)


    def remove_connection(self, connection):
        self.connections.remove(connection)