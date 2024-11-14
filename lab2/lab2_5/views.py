import io
from cProfile import label

import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from djangoProject2.src.Util import classify3d


def index(request):
    return render(request, 'lab2/lab2_5/index.html')


@csrf_exempt
def plot(request):

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


    for i in np.arange(0, 1, 0.1):
        for j in np.arange(0, 1, 0.1):
            for k in np.arange(0, 1, 0.1):
                class_id = classify3d(i, j, k)

                if class_id == 1:
                    ax.scatter(i, j, k, color='red', label='1')
                elif class_id == 2:
                    ax.scatter(i, j, k, color='blue', label='2')
                elif class_id == 3:
                    ax.scatter(i, j, k, color='green', label='3')
                elif class_id == 4:
                    ax.scatter(i, j, k, color='yellow', label='4')
                else:
                    ax.scatter(i, j, k, color='black', label='unknown')


    # ax.legend(title='Classes')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    return HttpResponse(buf, content_type='image/png')
