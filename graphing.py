from matplotlib.axis import Axis
import matplotlib.pyplot as pyplot
from matplotlib import figure, axes, patches
from re import search
from time import sleep


class GraphingVariables:
    ticks_per_axis_check = 1
    xlim_tick = 0
    ylim_tick = 0
    graph_line_colour = "cornflowerblue"
    graph_line_thickness = 3


class GraphingBrush:

    def __init__(self, plt: pyplot, fig: figure, axs: axes, line_colour: str="black", line_thickness: float=3):
        self.plot = plt
        self.figure = fig
        self.axes = axs
        self.colour = line_colour
        self.thickness = line_thickness
        
        # Create {entry# : plotobj} dict for replacing the correct plot on entry edit.
        self.plotsdict = {}


    def circle(self, radius: float, center: tuple[float], entrynum: int):
        """
        Radius - a float representing the radius of the circle you want to draw.
        Center - a tuple representing the coordinates `(x, y)` of the center of the circle.
        """
        # Create circle 
        circle = patches.Circle(center, radius, fill=False, color=self.colour, lw=self.thickness)

        # Change axes settings and add to axes
        limx = [center[0] - 2*radius, center[0] + 2*radius]
        limy = [center[1] - 2*radius, center[1] + 2*radius]
        self.axes.axis(limx + limy) # Same x and y limits as it is a circle.

        self.axes.add_patch(circle)

        # Add circle to plotsdict
        self.plotsdict[entrynum] = circle


    def draw_input(self, plottype: str, entry_num: int, **kwargs):
        if plottype == "circle":
            self.circle(kwargs["radius"], kwargs["center"], entry_num)

    
    def parse_input(self, input: str, entrynum: int) -> tuple[str, dict[str, float]]:
        number_search = "([-+]?[0-9]*\.?[0-9]+)"
        complex_search = "((?=[iIjJ.\d+-])([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?![iIjJ.\d]))?([+-]?(?:(?:\d+(?:\.\d*)?|\.\d+))?[iIjJ])?)"
        circle_search = search(f"^(\|(({complex_search}(-|\+)z)|(z(-|\+){complex_search}))\|={number_search})$", input)
        if circle_search:
            center = [0, 0]
            radius = 1
            # check if the circle is in the form |* \pm z| or in the form |z \pm *|
            print(circle_search.groups())
            # if in the form |z \pm *|
            if circle_search.group(2).startswith("z"):
                if circle_search.group(11) != None: 
                    center[0] = -float(circle_search.group(11))
                if circle_search.group(12) != None:
                    center[1] = -float(circle_search.group(12)[:-1])
                radius = float(circle_search.group(13))
            # if in the form |* \pm z|
            else:
                # if in the form |* p z|
                if circle_search.group(2)[-2] == "-":
                    coeff = 1
                # if in the form |* m z|
                else:
                    coeff = -1
                if circle_search.group(11) != None: 
                    center[0] = coeff*float(circle_search.group(11))
                if circle_search.group(12) != None:
                    y = circle_search.group(12)[:-1]
                    if y == "":
                        center[1] = 1
                    center[1] = coeff*float(circle_search.group(12)[:-1])
                radius = float(circle_search.group(13))
            return ("circle", {"radius": radius, "center": tuple(center)})
        return None

    
    def remove_plot(self, entrynum: int):
        if entrynum in self.plotsdict:
            # if the plot is an 'circle' type
            if isinstance(self.plotsdict[entrynum], patches.Circle):
                self.plotsdict[entrynum].remove()


def __xlim_change(axis: Axis):
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


def __ylim_change(axis: Axis):
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


def setup_figure(plot: pyplot, figure: figure, axes: axes, graph_line_colour: str=GraphingVariables.graph_line_colour):
    """
        ### 1. Grid Lines
        Draws the major and minor grid lines. Defaults to a classic blue graph paper colour.
        Also draws the axis with spines.
        ### 2. Aspect Ratio
        Sets the aspect ratio to 1:1, or 'equal'.
    """
    ### 1
    # Major grid lines first
    plot.grid(b=True, which="major", axis="both", color=graph_line_colour, linestyle="-", linewidth=(GraphingVariables.graph_line_thickness/4), alpha=0.8)

    # Minor grid lines first
    plot.minorticks_on()
    plot.grid(b=True, which="minor", axis="both", color=graph_line_colour, linestyle="-", linewidth=(GraphingVariables.graph_line_thickness/8), alpha=0.4)

    # Place the grid lines underneath the axis
    axes.set_axisbelow(True)

    # Fixes the x = 0 and y = 0 spines/axes.

    __xlim_change(axes)
    __ylim_change(axes)

    axes.callbacks.connect("xlim_changed", __xlim_change)
    axes.callbacks.connect("ylim_changed", __ylim_change)

    ### 2
    axes.set_aspect("equal")    