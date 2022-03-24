from turtle import ycor
import matplotlib.pyplot as plt
from graphing import GraphingBrush as gbrush


def main():
    radius = float(input("Enter circle radius: "))
    x, y = [float(i) for i in input("Enter the center coordinates in the form 'x, y': ").split(",")]
    default_brush = gbrush(plt)
    default_brush.one_to_one_aspect()
    default_brush.circle(radius, (x, y))
    default_brush.format_graph()
    plt.title("Complex Loci Plot")
    plt.show()
    

if __name__ == "__main__":
    main()