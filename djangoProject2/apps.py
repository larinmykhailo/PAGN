from django.apps import AppConfig
from django.core.cache import cache

import pandas as pd
from sympy import symbols, simplify
from djangoProject2.src.Class import Class
from djangoProject2.src.Point import Point
from djangoProject2.src.Util import format_f


class MyAppConfig(AppConfig):
    name = 'djangoProject2'

    def ready(self):
        # Ensure the data is calculated and cached on startup
        init_classes()
        init_points()
        init_normalized_points()
        init_centroids()
        init_normalized_centroids()
        init_equations()

def init_normalized_points():
    normalized_points = cache.get('normalized_points')
    if normalized_points is None:
        normalized_points = get_normalized_points()
        cache.set('normalized_points', normalized_points, timeout=None)  # timeout=None means the cache will not expire


def init_classes():
    classes = cache.get('classes')
    if classes is None:
        classes = get_classes()
        cache.set('classes', classes, timeout=None)  # timeout=None means the cache will not expire


def init_points():
    points = cache.get('points')
    if points is None:
        points = get_points()
        cache.set('points', points, timeout=None)  # timeout=None means the cache will not expire

def init_centroids():
    centroids = cache.get('centroids')
    if centroids is None:
        centroids = get_centroids()
        cache.set('centroids', centroids, timeout=None)  # timeout=None means the cache will not expire

def init_normalized_centroids():
    centroids = cache.get('normalized_centroids')
    if centroids is None:
        centroids = get_normalized_centroids()
        cache.set('normalized_centroids', centroids, timeout=None)  # timeout=None means the cache will not expire


def init_equations():
    equations = cache.get('equations')
    if equations is None:
        equations = get_equations()
        cache.set('equations', equations, timeout=None)  # timeout=None means the cache will not expire

def get_classes():
    classes = []
    class1 = Class('1', 'o', 'red')
    classes.append(class1)
    class2 = Class('2', 'x', 'blue')
    classes.append(class2)
    class3 = Class('3', '.', 'green')
    classes.append(class3)
    class4 = Class('4', 's', 'yellow')
    classes.append(class4)
    return classes


def get_points():
    classes = cache.get('classes')
    points = []
    df = pd.read_csv('data.csv')

    for index, row in df.iterrows():
        points.append(Point(row['I-x'], row['I-y'], row['I-z'], classes[0]))
        points.append(Point(row['IV-x'], row['IV-y'], row['IV-z'], classes[1]))
        points.append(Point(row['V-x'], row['V-y'], row['V-z'], classes[2]))
        points.append(Point(row['VI-x'], row['VI-y'], row['VI-z'], classes[3]))

    return points


def get_normalized_points():
    normalized_points = []

    points = cache.get('points')
    max_x = max(node.x for node in points)
    max_y = max(node.y for node in points)
    max_z = max(node.z for node in points)
    for point in points:
        normalized_points.append(Point(point.x / max_x, point.y / max_y, point.z / max_z, point.clazz))
    return normalized_points


def get_centroids():
    classes = cache.get('classes')
    points = cache.get('points')
    c = []
    for CLASS in classes:
        sum_x = 0
        sum_y = 0
        sum_z = 0
        count = 20
        for point in points:
            if point.clazz.label == CLASS.label:
                sum_x = sum_x + point.x
                sum_y = sum_y + point.y
                sum_z = sum_z + point.z
        c.append(Point(format_f(sum_x / count), format_f(sum_y / count), format_f(sum_z / count), CLASS))
    return c

def get_normalized_centroids():
    classes = cache.get('classes')
    normalized_points = cache.get('normalized_points')
    c = []
    for CLASS in classes:
        sum_x = 0
        sum_y = 0
        sum_z = 0
        count = 20
        for point in normalized_points:
            if point.clazz.label == CLASS.label:
                sum_x = sum_x + point.x
                sum_y = sum_y + point.y
                sum_z = sum_z + point.z
        c.append(Point(format_f(sum_x / count), format_f(sum_y / count), format_f(sum_z / count), CLASS))
    return c


def get_equations():
    c = cache.get('normalized_centroids')
    x, y, z = symbols('x y z')

    # Define the centroid points
    # c1 = (0.42, 0.57, 0.25)
    # c2 = (0.56, 0.43, 0.85)
    # c3 = (0.28, 0.45, 0.94)
    # c4 = (0.85, 0.84, 0.51)

    # Function to create and simplify the equation
    def create_equation(c1, c2):
        equation = 2 * (c1.x - c2.x) * (x - (c1.x + c2.x) / 2) + 2 * (c1.y - c2.y) * (
                y - (c1.y + c2.y) / 2) + 2 * (
                           c1.z - c2.z) * (z - (c1.z + c2.z) / 2)

        simplified_equation = simplify(equation)
        return simplified_equation

    # Create and simplify equations for all combinations of centroid points
    equations = {
        'c12': create_equation(c[0], c[1]),
        'c13': create_equation(c[0], c[2]),
        'c14': create_equation(c[0], c[3]),
        'c23': create_equation(c[1], c[2]),
        'c24': create_equation(c[1], c[3]),
        'c34': create_equation(c[2], c[3])
    }

    # Substitute values into the equations
    results = {
        'c12': substitute_values_from_point(equations['c12'], c[0]),
        'c13': substitute_values_from_point(equations['c13'], c[0]),
        'c14': substitute_values_from_point(equations['c14'], c[0]),
        'c23': substitute_values_from_point(equations['c23'], c[1]),
        'c24': substitute_values_from_point(equations['c24'], c[1]),
        'c34': substitute_values_from_point(equations['c34'], c[2])
    }

    for key, result in results.items():
        if result < 0:
            equations[key] = equations[key] * -1
        # print(f"Result for {key} using values from {key[:2]}: {result}")

    # Print the simplified equations and results
    # for key, equation in equations.items():
    #     print(f"Simplified equation for {key}: {equation}")

    return equations

# Function to substitute values into the equation
def substitute_values_from_point(eq, point):
    # Define the symbols
    x, y, z = symbols('x y z')
    return eq.subs({x: point.x, y: point.y, z: point.z})
