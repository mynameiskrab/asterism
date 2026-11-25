
#--------------------------------------------------------------------
# Thought class. Holds values & methods for
# name, color, position, and size.
#--------------------------------------------------------------------
class Thought:
    def __init__(self, name, rgb, description, xpos, ypos, width, height):
        # Name & color
        self.name = name
        self.rgb = rgb
        self.description = description

        # Position & size. size might be deprecated or unused.
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
