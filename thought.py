
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

    # Set name to input name
    def setname(self, name):
        self.thought_name = name

    # Set color to input rgb
    def setrgb(self, rgb):
        self.rgb = rgb

    # Set position to input x&y
    def setpos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    # Set size to input width&height
    def setsize(self, width, height):
        self.width = width
        self.height = height
