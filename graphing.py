from matplotlib.axis import Axis
import matplotlib.pyplot as pyplot


class GraphingBrush:
    def __init__(self, plot: pyplot, line_colour: str="black", line_thickness: float=3):
        self.plt = plot
        self.figure, self.axes = plot.subplots()
        self.colour = line_colour
        self.thickness = line_thickness

    def xlim_change(self, axis: Axis):
        xlim = axis.get_xlim()
        # if the axis is to the left of the screen
        if xlim[0] > 0:
            currspine = self.axes.spines[["right", "left"]]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        # if the axis is to the right of the screen   
        elif xlim[1] < 0:
            currspine = self.axes.spines[["right", "left"]]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        else:
            currspine = self.axes.spines[["right", "left"]]
            currspine.set_position("zero")
            currspine.set_color("black")
           


    def ylim_change(self, axis: Axis):
        ylim = axis.get_ylim()
        # if the axis is to the left of the screen
        if ylim[0] > 0:
            currspine = self.axes.spines[["bottom", "top"]]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        # if the axis is to the right of the screen   
        elif ylim[1] < 0:
            currspine = self.axes.spines[["bottom", "top"]]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        else:
            currspine = self.axes.spines[["bottom", "top"]]
            currspine.set_position("zero")
            currspine.set_color("black")
    
    def one_to_one_aspect(self):
        """
        Sets the aspect ratio to 1:1, or 'equal'.
        """
        self.axes.set_aspect("equal")

    def format_graph(self, graph_line_colour: str="cornflowerblue"):
        """
        Draws the major and minor grid lines. Defaults to a classic blue graph paper colour.
        Also draws the axis with spines.
        """
        # Major grid lines first
        self.plt.grid(b=True, which="major", axis="both", color=graph_line_colour, linestyle="-", linewidth=(self.thickness/4), alpha=0.8)

        # Minor grid lines first
        self.plt.minorticks_on()
        self.plt.grid(b=True, which="minor", axis="both", color=graph_line_colour, linestyle="-", linewidth=(self.thickness/8), alpha=0.4)

        # Place the grid lines underneath the axis
        self.axes.set_axisbelow(True)

        # Finally draws the x = 0 and y = 0 axis.

        # Move axes to center
        self.axes.spines["left"].set_position("zero")
        self.axes.spines["bottom"].set_position("zero")

        # Remove right and top axis
        self.axes.spines["right"].set_color("none")
        self.axes.spines["top"].set_color("none")

        self.axes.callbacks.connect("xlim_changed", self.xlim_change)
        self.axes.callbacks.connect("ylim_changed", self.ylim_change)
        


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
