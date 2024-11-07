import json
import sys
from io import BytesIO

import numpy as np
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from matplotlib import pyplot as plt

from djangoProject2.apps import init_normalized_points, init_normalized_centroids, init_centroids
from djangoProject2.src.Point import Point
from djangoProject2.src.Util import calculate_distance, format_f, calculate_distance_after_norm

new_points = []


def index(request):
    return render(request, 'lab1/index.html')


def add_point1(request):
    points = cache.get('points')

    data = json.loads(request.body)

    # Extract the values from the JSON data
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    option1 = data.get('option1')
    option2 = data.get('option2')

    # Validate or process the data (e.g., convert to float)
    try:
        x = float(x)
        y = float(y)
        z = float(z)
    except ValueError:
        return HttpResponse('Invalid input: Coordinates must be numbers.')

    new_point = classify_by_options(option1, option2, x, y, z)
    new_points.append(new_point)
    points.append(new_point)

    cache.set('points', points)
    cache.delete('normalized_points')
    cache.delete('centroids')
    cache.delete('normalized_centroids')
    init_normalized_points()
    init_centroids()
    init_normalized_centroids()

    return JsonResponse({})


def classify_by_options(option1, option2, x, y, z):
    centroids = cache.get('centroids')
    nearest_class = None
    min_distance = sys.float_info.max
    for centroid in centroids:
        dist = calculate_distance(x, y, z, option1, option2, centroid)
        if dist < min_distance:
            min_distance = dist
            nearest_class = centroid.clazz
    new_point = Point(x, y, z, nearest_class)
    return new_point


def classify_by_options_after_norm(option1, option2, x, y, z):
    centroids = cache.get('normalized_centroids')
    nearest_class = None
    min_distance = sys.float_info.max
    for centroid in centroids:
        dist = calculate_distance_after_norm(x, y, z, option1, option2, centroid)
        if dist < min_distance:
            min_distance = dist
            nearest_class = centroid.clazz
    new_point = Point(x, y, z, nearest_class)
    return new_point


def calculate(request):
    centroids = cache.get('centroids')

    data = json.loads(request.body)

    # Extract the values from the JSON data
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    option1 = data.get('option1')
    option2 = data.get('option2')

    # Validate or process the data (e.g., convert to float)
    try:
        x = float(x)
        y = float(y)
        z = float(z)
    except ValueError:
        return HttpResponse('Invalid input: Coordinates must be numbers.')

    dist_class1 = calculate_distance(x, y, z, option1, option2, centroids[0])
    dist_class2 = calculate_distance(x, y, z, option1, option2, centroids[1])
    dist_class3 = calculate_distance(x, y, z, option1, option2, centroids[2])
    dist_class4 = calculate_distance(x, y, z, option1, option2, centroids[3])

    return_data = {
        'coordinate_x': x,
        'coordinate_y': y,
        'coordinate_z': z,
        'dist_class1': format_f(dist_class1),
        'dist_class2': format_f(dist_class2),
        'dist_class3': format_f(dist_class3),
        'dist_class4': format_f(dist_class4)
    }
    return JsonResponse(return_data)


def plot1(request):
    fig = plt.figure(figsize=(10, 8))

    ax1 = fig.add_subplot(211, projection='3d')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    points = cache.get('points')

    for point in points:
        ax1.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)

    classes = cache.get('classes')

    for clazz in classes:
        ax1.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)

    ax1.legend()

    ax2 = fig.add_subplot(212, projection='3d')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    normalized_points = cache.get('normalized_points')

    for point in normalized_points:
        ax2.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)

    classes = cache.get('classes')

    for clazz in classes:
        ax2.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)

    ax2.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


@csrf_exempt
def compare_results(request):
    classes = cache.get('classes')
    fig = plt.figure(figsize=(10, 10))

    # First plot
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.set_title('1.1')

    # Second plot
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.set_title('1.2')

    # Third plot
    ax3 = fig.add_subplot(223, projection='3d')
    ax3.set_title('2.1')

    # Fourth plot
    ax4 = fig.add_subplot(224, projection='3d')
    ax4.set_title('2.2')

    for clazz in classes:
        ax1.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)
        ax2.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)
        ax3.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)
        ax4.scatter([], [], [], marker=clazz.marker, color=clazz.color, label=clazz.label)

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()

    for i in np.arange(0, 1, 0.1):
        for j in np.arange(0, 1, 0.1):
            for k in np.arange(0, 1, 0.1):
                # new_point = classify_by_options_after_norm('o1v1', 'o2v1', i, j, k)
                # ax1.scatter(new_point.x, new_point.y, new_point.z, marker=new_point.clazz.marker, color=new_point.clazz.color)

                # new_point = classify_by_options_after_norm('o1v1', 'o2v2', i, j, k)
                # ax2.scatter(new_point.x, new_point.y, new_point.z, marker=new_point.clazz.marker, color=new_point.clazz.color)
                #
                # new_point = classify_by_options_after_norm('o1v2', 'o2v1', i, j, k)
                # ax3.scatter(new_point.x, new_point.y, new_point.z, marker=new_point.clazz.marker, color=new_point.clazz.color)

                new_point = classify_by_options_after_norm('o1v2', 'o2v2', i, j, k)
                ax4.scatter(new_point.x, new_point.y, new_point.z, marker=new_point.clazz.marker,
                            color=new_point.clazz.color)

    # Save the figure to a BytesIO object
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return HttpResponse(buf, content_type='image/png')
