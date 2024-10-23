from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import json

from django.views.decorators.csrf import csrf_exempt
import re


def index(request):
    return render(request, 'lab2/lab2_3/index.html')


@csrf_exempt
def add_point(request):
    data = json.loads(request.body)
    x = float(data.get('x', '0'))
    y = float(data.get('y', '0'))

    classId = classify(x, y)

    if classId == 1:
        color = 'red'
    elif classId == 2:
        color = 'blue'
    elif classId == 3:
        color = 'green'
    else:
        color = 'black'

    fig = get_plot_fig()
    plt.scatter(x, y, color=color)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    response = {
        'decision': classId,
        'image': image_base64
    }
    json_response = json.dumps(response)

    return HttpResponse(json_response, content_type='application/json')

def classify(x, y):
    d1 = 1 * x - 1 * y - 0.3
    d2 = 1 * x + 1 * y - 1.2
    d3 = -3 * x - 1 * y + 1.7
    if d1 > 0 and d2 < 0 and d3 < 0:
        return 1
    elif d1 < 0 and d2 > 0 and d3 < 0:
        return 2
    elif d1 < 0 and d2 < 0 and d3 > 0:
        return 3
    return "Cannot classify"

@csrf_exempt
def plot_2_3(request):
    fig = get_plot_fig()

    for i in np.arange(0, 1.5, 0.05):
        for j in np.arange(0, 1.5, 0.05):
            classId = classify(i, j)

            if classId == 1:
                color = 'red'
            elif classId == 2:
                color = 'blue'
            elif classId == 3:
                color = 'green'
            else:
                color = 'black'

            plt.scatter(i, j, color=color)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return HttpResponse(buf, content_type='image/png')


def get_plot_fig():
    d1 = '1x-1y-0.3'
    d2 = '1x+1y-1.2'
    d3 = '-3x-1y+1.7'
    equations = [d1, d2, d3]
    coefficients = []
    for equation in equations:
        # Извлекаем коэффициенты A, B и C из уравнения
        A, B, C = map(float, re.findall(r'([-+]?\d*\.?\d+)', equation))
        coefficients.append((A, B, C))
    x = np.linspace(-2, 2, 800)
    plt.figure(figsize=(6, 6))
    plt.rc('axes', linewidth=2)
    plt.xlim(-1, 2)
    plt.ylim(-1, 2)
    for i, (A, B, C) in enumerate(coefficients, start=1):
        if B != 0:
            # Уравнение в формате Ax + By + C = 0
            y = (-A * x - C) / B
            plt.plot(x, y, label=f'd{i}(x) = {A}x + {B}y + {C}')
        elif A != 0:
            # Уравнение в формате Ax + C = 0 (вертикальная линия)
            x_val = -C / A
            plt.axvline(x=x_val, label=f'd{i}(x) = {A}x + {C}')
        else:
            # Уравнение в формате C = 0 (не является линией)
            plt.text(0, 0, f'd{i}(x) = {C}', fontsize=12)
    plt.legend()
    plt.grid(True)

    fig = plt.gcf()
    return fig
