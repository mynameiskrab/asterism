
#--------------------------------------------------------------------
# Thought class. Holds values & methods for
# name, color, position, and size.
#--------------------------------------------------------------------
class Thought:
    def __init__(self, name, rgb, xpos, ypos, width, height):
        # Name & color
        self.name = name
        self.rgb= rgb

        # Position & size. size might be deprecated or unused.
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
