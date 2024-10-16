from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64

from django.views.decorators.csrf import csrf_exempt
import re


def index(request):
    return render(request, 'lab2/lab2_3/index.html')

@csrf_exempt
def add_point(request):


    if request.method == 'POST':
        x = request.POST.get('x', '0')
        y = request.POST.get('y', '0')
        # z = request.POST.get('z', '0')


@csrf_exempt
def plot(request):

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

    plt.figure(figsize=(8, 8))
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
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return HttpResponse(buf, content_type='image/png')