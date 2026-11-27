
#--------------------------------------------------------------------
# Thought class. Holds values & methods for
# name, color, position, and size.
#--------------------------------------------------------------------
class Thought:
    def __init__(self, name, rgb, description, x, y, radius):
        # Name & color
        self.name = name
        self.rgb = rgb
        self.description = description

        # Position & size. size might be deprecated or unused.
        self.x = x
        self.y = y
        self.radius = radius
