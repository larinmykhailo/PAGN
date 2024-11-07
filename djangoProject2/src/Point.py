# Define the Point class
import json

from djangoProject2.src.Class import Class


class Point:
    def __init__(self, x, y, z, clazz: Class = None):
        self.x = x
        self.y = y
        self.z = z
        self.clazz = clazz

    def __str__(self):
        return f"Point({self.x:.2f}, {self.y:.2f}, {self.z:.2f}, {self.clazz.label})"

class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Point):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
