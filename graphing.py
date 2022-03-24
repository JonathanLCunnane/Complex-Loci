from matplotlib.axis import Axis
import matplotlib.pyplot as pyplot
from matplotlib import figure, axes


class GraphingVariables:
    ticks_per_axis_check = 1
    xlim_tick = 0
    ylim_tick = 0
    graph_line_colour = "cornflowerblue"
    graph_line_thickness = 3


class GraphingBrush:

    def __init__(self, plt: pyplot,fig: figure, axs: axes, line_colour: str="black", line_thickness: float=3):
        self.plot = plt
        self.figure = fig
        self.axes = axs
        self.colour = line_colour
        self.thickness = line_thickness
    
    def one_to_one_aspect(self):
        """
        Sets the aspect ratio to 1:1, or 'equal'.
        """
        self.axes.set_aspect("equal")

    def format_graph(self):
        """
        Draws the major and minor grid lines. Defaults to a classic blue graph paper colour.
        Also draws the axis with spines.
        """
        return
        


    def circle(self, radius: float, center: tuple):
        """
        Radius - a float representing the radius of the circle you want to draw.
        Center - a tuple representing the coordinates `(x, y)` of the center of the circle.
        """
        # Create circle 
        circle = self.plot.Circle(center, radius, fill=False, color=self.colour, lw=self.thickness)

        # Change axes settings and add to axes
        limx = [center[0] - 2*radius, center[0] + 2*radius]
        limy = [center[1] - 2*radius, center[1] + 2*radius]
        self.axes.axis(limx + limy) # Same x and y limits as it is a circle.

        self.axes.add_artist(circle)


def xlim_change(axis: Axis):
    if GraphingVariables.xlim_tick % GraphingVariables.ticks_per_axis_check == 0:
        GraphingVariables.xlim_tick = 0
        xlim = axis.get_xlim()
        # if the axis is to the left of the screen
        if xlim[0] > 0:
            axis.yaxis.tick_left()
            currspine = axis.spines["left"]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        # if the axis is to the right of the screen   
        elif xlim[1] < 0:
            axis.yaxis.tick_right()
            currspine = axis.spines["right"]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
            currspine = axis.spines["left"]
            currspine.set_color("none")
        else:
            axis.yaxis.tick_left()
            currspine = axis.spines["left"]
            currspine.set_position("zero")
            currspine.set_color("black")
            currspine = axis.spines["right"]
            currspine.set_color("none")
    GraphingVariables.xlim_tick += 1

def ylim_change(axis: Axis):
    if GraphingVariables.ylim_tick % GraphingVariables.ticks_per_axis_check == 0:
        GraphingVariables.ylim_tick = 0
        ylim = axis.get_ylim()
        # if the axis is to the left of the screen
        if ylim[0] > 0:
            axis.xaxis.tick_bottom()
            currspine = axis.spines["bottom"]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        # if the axis is to the right of the screen   
        elif ylim[1] < 0:
            axis.xaxis.tick_top()
            currspine = axis.spines["top"]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
            currspine = axis.spines["bottom"]
            currspine.set_color("none")
        else:
            axis.xaxis.tick_bottom()
            currspine = axis.spines["bottom"]
            currspine.set_position("zero")
            currspine.set_color("black")
            currspine = axis.spines["top"]
            currspine.set_color("none")
    GraphingVariables.ylim_tick += 1


def setup_figure(plot: pyplot, figure: figure, axes: axes):
    ### 1
    # Major grid lines first
    plot.grid(b=True, which="major", axis="both", color=GraphingVariables.graph_line_colour, linestyle="-", linewidth=(GraphingVariables.graph_line_thickness/4), alpha=0.8)

    # Minor grid lines first
    plot.minorticks_on()
    plot.grid(b=True, which="minor", axis="both", color=GraphingVariables.graph_line_colour, linestyle="-", linewidth=(GraphingVariables.graph_line_thickness/8), alpha=0.4)

    # Place the grid lines underneath the axis
    axes.set_axisbelow(True)

    # Finally draws and fixes the x = 0 and y = 0 axis.

    xlim_change(axes)
    ylim_change(axes)

    # Fixing spines on scrolling

    axes.callbacks.connect("xlim_changed", xlim_change)
    axes.callbacks.connect("ylim_changed", ylim_change)