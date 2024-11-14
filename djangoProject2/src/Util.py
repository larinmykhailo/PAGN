import math

from django.core.cache import cache
from sympy import symbols

from djangoProject2.src.Point import Point



def normalize(x, y, z):

    points = cache.get('points')
    max_x = max(node.x for node in points)
    max_y = max(node.y for node in points)
    max_z = max(node.z for node in points)
    return x / max_x, y / max_y, z / max_z


def format_f(x):
    return float("{0:.2f}".format(x))


# Function to substitute values into the equation
def substitute_values(eq, values):
    # Define the symbols
    x, y, z = symbols('x y z')
    return eq.subs({x: values[0], y: values[1], z: values[2]})


def classify3d(x, y, z):
    equations = cache.get('equations')

    d12 = substitute_values(equations['c12'], [x, y, z])
    d13 = substitute_values(equations['c13'], [x, y, z])
    d14 = substitute_values(equations['c14'], [x, y, z])
    d23 = substitute_values(equations['c23'], [x, y, z])
    d24 = substitute_values(equations['c24'], [x, y, z])
    d34 = substitute_values(equations['c34'], [x, y, z])

    if d12 > 0 and d13 > 0 and d14 > 0:
        return 1
    elif d12 < 0 and d23 > 0 and d24 > 0:
        return 2
    elif d13 < 0 and d23 < 0 and d34 > 0:
        return 3
    elif d14 < 0 and d24 < 0 and d34 < 0:
        return 4
    else:
        return "Cannot classify"


def euclidean_distance(point1: Point, point2: Point) -> float:
    """
    Обчислює евклідову відстань між двома точками в тривимірному просторі.

    :param point1: об'єкт класу Point (x1, y1, z1)
    :param point2: об'єкт класу Point (x2, y2, z2)
    :return: евклідову відстань
    """
    # Обчислення різниць між відповідними координатами
    diff_x = point1.x - point2.x
    diff_y = point1.y - point2.y
    diff_z = point1.z - point2.z

    # Обчислення евклідової відстані
    return math.sqrt(diff_x ** 2 + diff_y ** 2 + diff_z ** 2)


def manhattan_distance(point1: Point, point2: Point) -> float:
    """
    Обчислює відстань за мінімумом за модулів різниць для тривимірного простору.

    :param point1: об'єкт класу Point (x1, y1, z1)
    :param point2: об'єкт класу Point (x2, y2, z2)
    :return: мінімум за модулів різниць
    """
    # Обчислення модулів різниць між відповідними координатами
    diff_x = abs(point1.x - point2.x)
    diff_y = abs(point1.y - point2.y)
    diff_z = abs(point1.z - point2.z)

    # Повертаємо мінімум з модулів різниць
    return min(diff_x, diff_y, diff_z)


def get_farest_etalon(x, y, z, clazz, option1) -> Point:
    points = cache.get('points')
    farest_point = None
    max_distance = 0
    for point in points:
        if point.clazz.label == clazz.label:
            distance = euclidean_distance(Point(x, y, z), point) if option1 == 'o1v1' else manhattan_distance(
                Point(x, y, z), point)
            if distance > max_distance:
                max_distance = distance
                farest_point = point

    return farest_point


def calculate_distance(x, y, z, option1, option2, centroid: Point) -> float:
    point = Point(x, y, z)
    class_point = centroid if option2 == 'o2v1' else get_farest_etalon(x, y, z, centroid.clazz, option1)

    return euclidean_distance(point, class_point) if option1 == 'o1v1' else manhattan_distance(point, class_point)


def get_farest_etalon_after_norm(x, y, z, clazz, option1) -> Point:
    normalized_points = cache.get('normalized_points')
    farest_point = None
    max_distance = 0
    for point in normalized_points:
        if point.clazz.label == clazz.label:
            distance = euclidean_distance(Point(x, y, z), point) if option1 == 'o1v1' else manhattan_distance(
                Point(x, y, z), point)
            if distance > max_distance:
                max_distance = distance
                farest_point = point

    return farest_point


def calculate_distance_after_norm(x, y, z, option1, option2, centroid: Point) -> float:
    point = Point(x, y, z)
    class_point = centroid if option2 == 'o2v1' else get_farest_etalon_after_norm(x, y, z, centroid.clazz, option1)

    return euclidean_distance(point, class_point) if option1 == 'o1v1' else manhattan_distance(point, class_point)
