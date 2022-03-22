import matplotlib.pyplot as pyplot


class GraphingBrush:
    def __init__(self, plot: pyplot, line_colour: str="black", line_thickness: float=3):
        self.plt = plot
        self.figure, self.axes = plot.subplots()
        self.colour = line_colour
        self.thickness = line_thickness
    
    def one_to_one_aspect(self):
        """
        Sets the aspect ratio to 1:1, or 'equal'.
        """
        self.axes.set_aspect("equal")

    def draw_graph_lines(self, graph_line_colour: str="cornflowerblue"):
        """
        Draws the major and minor grid lines. Defaults to a classic blue graph paper colour.
        """
        # Major grid lines first
        self.plt.grid(b=True, which="major", axis="both", color=graph_line_colour, linestyle="-", linewidth=(self.thickness/4), alpha=0.8)

        # Minor grid lines first
        self.plt.minorticks_on()
        self.plt.grid(b=True, which="minor", axis="both", color=graph_line_colour, linestyle="-", linewidth=(self.thickness/8), alpha=0.4)

    def circle(self, radius: float, center: tuple):
        """
        Radius - a float representing the radius of the circle you want to draw.
        Center - a tuple representing the coordinates `(x, y)` of the center of the circle.
        """
        # Create circle 
        circle = self.plt.Circle(center, radius, fill=False, color=self.colour, lw=self.thickness)

        # Change axes settings and add to axes
        limx = [center[0] - 2*radius, center[0] + 2*radius]
        limy = [center[1] - 2*radius, center[1] + 2*radius]
        self.axes.axis(limx + limy) # Same x and y limits as it is a circle.

        self.axes.add_artist(circle)
