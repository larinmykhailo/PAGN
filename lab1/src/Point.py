# Define the Point class
import json

from lab1.src.Class import Class


class Point:
    def __init__(self, x, y, z, clazz: Class):
        self.x = x
        self.y = y
        self.z = z
        self.clazz = clazz

class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Point):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
