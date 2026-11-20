class LayerManager:

    def __init__(self):
        self.layers = {}

    def add_layer(self, layer: Layer):
        new_layer_name = layer.get_name()
        if new_layer_name not in self.layers:
            self.layers[new_layer_name] = layer
        else:
            raise ValueError("Error: layer with name \""+new_layer_name+"\" already exists.")

    def get_layer(self, layer_name):
        if layer_name in self.layers:
            return self.layers[layer_name]
        else:
            return None

class Layer:

    def __init__(self, name):
        if self.name[0] == "\"" or self.name[len(self.name)] == "\"":
            raise ValueError("Error: layer name cannot begin or end with quotation marks")
        self.name = name
        self.connections = {}

    def get_name(self):
        return self.name
