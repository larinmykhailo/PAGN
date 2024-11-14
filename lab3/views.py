
import itertools
import json
from io import BytesIO

import numpy as np
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from matplotlib import pyplot as plt

from djangoProject2.apps import init_normalized_points, init_centroids, init_normalized_centroids
from djangoProject2.src.Point import Point
from djangoProject2.src.Util import normalize
from lab3.src.Utils import ho_kashyap_algorithm

new_points = []
d_functions = {}


def index(request):
    return render(request, 'lab3/index.html')


def add_point1(request):
    points = cache.get('points')
    classes = cache.get('classes')
    data = json.loads(request.body)

    # Extract the values from the JSON data
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')

    # Validate or process the data (e.g., convert to float)
    try:
        x = float(x)
        y = float(y)
        z = float(z)
    except ValueError:
        return HttpResponse('Invalid input: Coordinates must be numbers.')

    x, y, z = normalize(x, y, z)
    res = check_class(x, y, z, calculate_d_functions())
    nearest_class = next((obj for obj in classes if obj.label == res), None)
    new_point = Point(x, y, z, nearest_class)

    new_points.append(new_point)

    # points.append(new_point)
    #
    # cache.set('points', points)
    # cache.delete('normalized_points')
    # cache.delete('centroids')
    # cache.delete('normalized_centroids')
    # init_normalized_points()
    # init_centroids()
    # init_normalized_centroids()

    return JsonResponse({})

def calculate_d_functions():

    points = cache.get('normalized_points')
    classes = cache.get('classes')
    d_functions = {}

    for pair in itertools.combinations(classes, 2):

        # Отримання точок першого і другого класу
        first_class_points = [p for p in points if p.clazz.label == pair[0].label]
        second_class_points = [p for p in points if p.clazz.label == pair[1].label]

        # Створення масивів для обох класів (матриця ознак для кожного класу)
        V_first_class = np.array([[p.x, p.y, p.z] for p in first_class_points])
        V_second_class = np.array([[p.x, p.y, p.z] for p in second_class_points])

        # Об'єднання двох масивів
        V = np.concatenate((V_first_class, V_second_class), axis=0)

        w, iter = ho_kashyap_algorithm(V)

        a, b, c, d = w

        d_functions[f"d{pair[0].label}{pair[1].label}"] = lambda x, y, z, a1=a, b1=b, c1=c, d1=d: a1 * x + b1 * y + c1 * z + d1
    return d_functions

def plot1(request):

    # Точки
    fig = plt.figure(figsize=(10, 8))

    ax1 = fig.add_subplot(211, projection='3d')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    points = cache.get('normalized_points')

    for point in points:
        ax1.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)

    for point in new_points:
        ax1.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)

    classes = cache.get('classes')

    for clazz in classes:
        ax1.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)

    ax1.legend()



    # Площини

    ax2 = fig.add_subplot(212, projection='3d')

    # Налаштування міток осей
    ax2.set_xlabel('X1')
    ax2.set_ylabel('X2')
    ax2.set_zlabel('X3')

    for point in new_points:
        ax2.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)


# Створення сітки точок для x1 і x2
    x1_vals = np.linspace(0, 1, 50)  # Діапазон для x1
    x2_vals = np.linspace(0, 1, 50)  # Діапазон для x2
    x1, x2 = np.meshgrid(x1_vals, x2_vals)


    # Генерація всіх комбінацій пар елементів
    # Виведення всіх пар
    for pair in itertools.combinations(classes, 2):

        # Отримання точок першого і другого класу
        first_class_points = [p for p in points if p.clazz.label == pair[0].label]
        second_class_points = [p for p in points if p.clazz.label == pair[1].label]

        # Створення масивів для обох класів (матриця ознак для кожного класу)
        V_first_class = np.array([[p.x, p.y, p.z] for p in first_class_points])
        V_second_class = np.array([[p.x, p.y, p.z] for p in second_class_points])

        # Об'єднання двох масивів
        V = np.concatenate((V_first_class, V_second_class), axis=0)

        w, iter = ho_kashyap_algorithm(V)

        a, b, c, d = w

        # print(f"d{pair[0].label}{pair[1].label}{a:.2f} * x1 + {b:.2f} * x2 + {c:.2f} * x3 + {d:.2f}")

        # Обчислення x3 на основі рівняння площини
        # a * x1 + b * x2 + c * x3 + d = 0
        # x3 = -(a * x1 + b * x2 + d) / c
        x3 = -(a * x1 + b * x2 + d) / c

        d_functions[f"d{pair[0].label}{pair[1].label}"] = lambda x, y, z, a1=a, b1=b, c1=c, d1=d: a1 * x + b1 * y + c1 * z + d1

        # Побудова площини
        ax2.plot_surface(x1, x2, x3, cmap='viridis', alpha=0.1)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


@csrf_exempt
def compare_results(request):
    classes = cache.get('classes')


    fig = plt.figure(figsize=(15, 20))
    points = cache.get('normalized_points')

    # Площини


    # Генерація всіх комбінацій пар елементів
    # Виведення всіх пар
    i = 1
    for pair in itertools.combinations(classes, 2):

        # Отримання точок першого і другого класу
        first_class_points = [p for p in points if p.clazz.label == pair[0].label]
        second_class_points = [p for p in points if p.clazz.label == pair[1].label]

        # Створення масивів для обох класів (матриця ознак для кожного класу)
        V_first_class = np.array([[p.x, p.y, p.z] for p in first_class_points])
        V_second_class = np.array([[p.x, p.y, p.z] for p in second_class_points])

        # Об'єднання двох масивів
        V = np.concatenate((V_first_class, V_second_class), axis=0)

        w, iter = ho_kashyap_algorithm(V)

        a, b, c, d = w

        d_functions[f"d{pair[0].label}{pair[1].label}"] = lambda x, y, z, a1=a, b1=b, c1=c, d1=d: a1 * x + b1 * y + c1 * z + d1

        plot_id = int(f"23{i}")
        i += 1
        ax = fig.add_subplot(plot_id, projection='3d')
        ax.set_title(f"Клас {pair[0].label} - Клас {pair[1].label}")

        # Налаштування міток осей
        ax.set_xlabel('X1')
        ax.set_ylabel('X2')
        ax.set_zlabel('X3')

        # Створення сітки точок для x1 і x2
        x1_vals = np.linspace(0, 1, 50)  # Діапазон для x1
        x2_vals = np.linspace(0, 1, 50)  # Діапазон для x2
        x1, x2 = np.meshgrid(x1_vals, x2_vals)

        for point in first_class_points:
            ax.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)

        for point in second_class_points:
            ax.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)

        for clazz in classes:
            ax.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)
        ax.legend()


        # Обчислення x3 на основі рівняння площини
        # a * x1 + b * x2 + c * x3 + d = 0
        # x3 = -(a * x1 + b * x2 + d) / c
        x3 = -(a * x1 + b * x2 + d) / c

        # Побудова площини
        ax.plot_surface(x1, x2, x3, cmap='viridis', alpha=1)

        # Змінюємо кут огляду
        def adjust_view(ax, normal):
            # Визначаємо напрямок огляду таким чином, щоб площина була орієнтована як лінія
            azim = np.arctan2(normal[1], normal[0]) * 180 / np.pi  # Кут для azimuth (горизонтальний)
            elev = np.arctan2(normal[2], normal[0]) * 180 / np.pi  # Кут для elevation (вертикальний)

            # Встановлюємо ці кути огляду
            ax.view_init(elev=elev-135, azim=-80)

        # Викликаємо функцію для встановлення кута огляду
        adjust_view(ax, np.array([a, b, c]))

    cache.set('d_functions', d_functions, timeout=None)

    # Save the figure to a BytesIO object
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return HttpResponse(buf, content_type='image/png')
#
# def unclassigied_results(request):
#
#     fig = plt.figure(figsize=(10, 10))
#     # некласифіковіні точки
#     ax_uncl = fig.add_subplot(247, projection='3d')
#     ax_uncl.set_title(f"Некласифікований простір")
#
#     for i in np.arange(0, 1, 0.1):
#         for j in np.arange(0, 1, 0.1):
#             for k in np.arange(0, 1, 0.1):
#                 if check_class(i, j, k, d_functions) is None:
#                     ax_uncl.scatter(i, j, k, color='black', marker='o')
#     ax_uncl.scatter([], [], [], label='unclassified', color='black', marker='o')
#     ax_uncl.legend()
#
#
#
#     # Save the figure to a BytesIO object
#     buf = BytesIO()
#     plt.tight_layout()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     plt.close(fig)
#
#     return HttpResponse(buf, content_type='image/png')
#
#
#
# Функція, яка перевіряє, чи точка задовольняє умови приналежності до кожного класу
def check_class(x, y, z, d_functions):
    # Перевірка першого класу
    if d_functions['d12'](x, y, z) > 0 and d_functions['d13'](x, y, z) > 0 and d_functions['d14'](x, y, z) > 0:
        return '1'
    # Перевірка другого класу
    elif -d_functions['d12'](x, y, z) > 0 and d_functions['d23'](x, y, z) > 0 and d_functions['d24'](x, y, z) > 0:
        return '2'
    # Перевірка третього класу
    elif -d_functions['d13'](x, y, z) > 0 and -d_functions['d23'](x, y, z) > 0 and d_functions['d34'](x, y, z) > 0:
        return '3'
    # Перевірка четвертого класу
    elif -d_functions['d14'](x, y, z) > 0 and -d_functions['d24'](x, y, z) > 0 and -d_functions['d34'](x, y, z) > 0:
        return '4'
    # Якщо жодна система нерівностей не виконується
    else:
        return None