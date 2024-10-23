import numbers
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'lab1/index.html')

@csrf_exempt
def add_point(request):
    if request.method == 'POST':
        x = float(request.POST.get('x'))
        y = float(request.POST.get('y'))
        z = float(request.POST.get('z'))

        if isinstance(x, numbers.Number) & isinstance(y, numbers.Number) & isinstance(z, numbers.Number):
            # detect_class = CLASSES[0] # TODO: detect class
            # TODO add style to new point?
            POINTS.append(Point(x, y, z, Class('V', 's', 'black')))
    return redirect('index')

def plot_view_before(request):
    ax = create_plot('До нормалізації')
    for point in POINTS:
      ax.scatter(point.x, point.y, point.z, marker=point.clazz.marker, color=point.clazz.color)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')

def plot_view_after(request):
    ax = create_plot('Після нормалізації')
    max_x = max(node.x for node in POINTS)
    max_y = max(node.y for node in POINTS)
    max_z = max(node.z for node in POINTS)

    # Print the list of Point objects
    for point in POINTS:
        ax.scatter(point.x / max_x, point.y / max_y, point.z / max_z, marker=point.clazz.marker, color=point.clazz.color)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')

