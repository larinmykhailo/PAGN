import matplotlib.pyplot as plt
import pandas as pd
from django.apps import AppConfig

from lab1.src.Class import Class
from lab1.src.Point import Point

POINTS = []
CLASSES = []

def initPoints():
    class1 = Class('I', 'o', 'red')
    CLASSES.append(class1)
    class2 = Class('II', 'x', 'blue')
    CLASSES.append(class2)
    class3 = Class('III', '.', 'green')
    CLASSES.append(class3)
    class4 = Class('IV', 's', 'yellow')
    CLASSES.append(class4)

    df = pd.read_csv('data.csv')

    for index, row in df.iterrows():
        POINTS.append(Point(row['I-x'], row['I-y'], row['I-z'], class1))
        POINTS.append(Point(row['IV-x'], row['IV-y'], row['IV-z'], class2))
        POINTS.append(Point(row['V-x'], row['V-y'], row['V-z'], class3))
        POINTS.append(Point(row['VI-x'], row['VI-y'], row['VI-z'], class4))

def create_plot(title):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    return ax
