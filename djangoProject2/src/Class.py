
# Define the Class class
class Class:
    def __init__(self, label, marker, color):
        self.label = label
        self.marker = marker
        self.color = color
    points = []

    def __str__(self):
        return f"Class({self.label}, {self.marker}, {self.color})"
