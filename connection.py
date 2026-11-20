
#--------------------------------------------------------------------
# Connection Class. Each connection links to two thoughts.
# Holds values & methods for each thought, name, color, and layer.
#--------------------------------------------------------------------
class Connection:
    def __init__(self, node_one, node_two, name, rgb, layer):
        # Set connected thoughts
        self.node_one = node_one
        self.node_two = node_two

        # Set connection values
        self.name = name
        self.rgb = rgb
        self.layer = layer

    # Set nodes to input thoughts
    def setnodes(self, node_one, node_two):
        self.node_one = node_one
        self.node_two = node_two

    # Set name to input
    def setname(self, name):
        self.name = name

    # Set color to input rgb
    def setrgb(self, rgb):
        self.rgb = rgb

    # Set layer to input layer
    def setlayer(self, layer):
        self.layer = layer



