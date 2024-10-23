from django.core.cache import cache

import matplotlib.pyplot as plt
from sympy import symbols

from djangoProject2.apps import MyAppConfig


def create_plot(title):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    return ax


def format_f(x):
    return float("{0:.2f}".format(x))



# Function to substitute values into the equation
def substitute_values(eq, values):
    # Define the symbols
    x, y, z = symbols('x y z')
    return eq.subs({x: values[0], y: values[1], z: values[2]})



def classify3d(x, y, z):
    equations = cache.get('equations')

    d12 = substitute_values(equations['c12'], [x, y ,z])
    d13 = substitute_values(equations['c13'], [x, y ,z])
    d14 = substitute_values(equations['c14'], [x, y ,z])
    d23 = substitute_values(equations['c23'], [x, y ,z])
    d24 = substitute_values(equations['c24'], [x, y ,z])
    d34 = substitute_values(equations['c34'], [x, y ,z])

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
