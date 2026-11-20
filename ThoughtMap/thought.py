
class Thought:
    def __init__(self, name, x=100, y=100):
        self.thoughtName = name
        self.Links = []

        # Canvas position
        self.x = x
        self.y = y

    def addLink(self, name, link):
        self.Links.append((name, link))

    def removeLink(self, linkIndex):
        if 0 <= linkIndex < len(self.Links):
            self.Links.pop(linkIndex)

    def display(self):
        print(f"{self.thoughtName} - {len(self.Links)} links")

        for link_name, thought in self.Links:
            print(f"   {thought.thoughtName} - {link_name}")

    def displayLinks(self):
        for index, (link_name, thought) in enumerate(self.Links):
            print(
                f"{index + 1}: "
                f"{thought.thoughtName} - {link_name}"
            )

        return len(self.Links)
