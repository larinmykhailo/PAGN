# Define the Point class
from lab1.src.Class import Class


class Point:
    def __init__(self, x, y, z, clazz: Class):
        self.x = x
        self.y = y
        self.z = z
        self.clazz = clazz
