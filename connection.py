
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
