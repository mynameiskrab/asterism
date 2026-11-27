
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
        self.description = ""
        self.x = (node_one.x + node_two.x) / 2
        self.y = (node_one.y + node_two.y) / 2

    def reset_midpoint(self):
        self.x = (self.node_one.x + self.node_two.x) / 2
        self.y = (self.node_one.y + self.node_two.y) / 2
