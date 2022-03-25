import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
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
    
    axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
    text_box = TextBox(axbox, 'Enter Locus Equation: ', initial=f"|z-({x}+{y}i)|={radius}")

    # Set title
    plt.title("Complex Loci Plot")
    
    # Show plot
    plt.show()
    

if __name__ == "__main__":
    main()