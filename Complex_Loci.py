import matplotlib.pyplot as plt
from graphing import GraphingBrush as gbrush
from graphing import setup_figure


def main():
    # Temporary Inputs for testing purposes
    radius = float(input("Enter circle radius: "))
    x, y = [float(i) for i in input("Enter the center coordinates in the form 'x, y': ").split(",")]

    # Setup figure
    figure, axes = plt.subplots()
    setup_figure(plt, figure, axes)

    # Creating and using brush
    default_brush = gbrush(plt, figure, axes)
    default_brush.circle(radius, (x, y))
    
    # Set title
    plt.title("Complex Loci Plot")
    
    # Show plot
    plt.show()
    

if __name__ == "__main__":
    main()