import matplotlib.pyplot as plt
from graphing import GraphingBrush as gbrush


def main():
    default_brush = gbrush(plt)
    default_brush.one_to_one_aspect()
    default_brush.draw_graph_lines()
    default_brush.circle(3, (1, 2))
    plt.title("Complex Loci Plot")
    plt.show()
    

if __name__ == "__main__":
    main()