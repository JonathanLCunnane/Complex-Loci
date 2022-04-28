from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import matplotlib.pyplot as pyplot
from matplotlib import figure, axes, patches
from re import match
from math import tan
from sys import float_info

from interpreting import *


class GraphingVariables:
    ticks_per_axis_check = 5
    xlim_tick = 0
    ylim_tick = 0
    graph_line_colour = "cornflowerblue"
    graph_line_thickness = 3
    prev_y_axis_pos = -2 # -1 means axis are to the left , 0 is in frame, 1 is to the right. (-2 is invalid but forces the program to check axis on the first call.)
    prev_x_axis_pos = -2 # -1 means axis are to the bottom , 0 is in frame, 1 is to the top. (-2 is invalid but forces the program to check axis on the first call.)
    max_matplotlib_dist = float_info.max/2**59


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

        self.axes.add_patch(circle)
        
        # Add circle to plotsdict
        self.plotsdict[entrynum] = ("circle", circle)


    def perpendicular_bisector(self, point_a: tuple[float], point_b: tuple[float], entrynum: int):
        """
        Point A and Point B are the points inbetween which a perpendicular bisector will be drawn.
        """
        # find a point and a slope of the perp bisector
        center = ((point_a[0] + point_b[0])/2, (point_a[1] + point_b[1])/2)

        # if the line is vertical, draw a axvline, else draw a normal axline
        if point_b[1] - point_a[1] == 0:
            perpendicular_bisector = self.axes.axvline(x=center[0], color=self.colour, lw=self.thickness)
        else:
            m = (point_a[0] - point_b[0])/(point_b[1] - point_a[1])
            perpendicular_bisector = self.axes.axline(xy1=center, slope=m, color=self.colour, lw=self.thickness)

        # add to entries dict
        self.plotsdict[entrynum] = ("perpendicular_bisector", perpendicular_bisector)


    def half_line(self, point: tuple[float], theta: float, entrynum: int):
        """
        Point is the point the half line will originate from, and theta is the angle of the half line from the positive horizontal.
        """
        # find the gradient of the point
        m = tan(theta)
        # find x and y coeffs
        if theta >= 0 and theta <= pi/2:
            xcoeff = 1
            ycoeff = 1
        elif theta > pi/2 and theta <= pi:
            xcoeff = -1
            ycoeff = -1
        elif theta < 0 and theta >= -pi/2:
            xcoeff = 1
            ycoeff = 1
        else:
            xcoeff = -1
            ycoeff = -1

        # draw the half line
        dist = GraphingVariables.max_matplotlib_dist
        half_line = self.plot.plot([point[0], point[0]+(xcoeff*dist)], [point[1], point[1]+(ycoeff*m*dist)], color=self.colour, lw=self.thickness)

        # add to entries dict
        self.plotsdict[entrynum] = ("half_line", half_line)
            
        

    def draw_input(self, plottype: str, entry_num: int, **kwargs):
        if plottype == "circle":
            self.circle(kwargs["radius"], kwargs["center"], entry_num)
        elif plottype == "perpendicular_bisector":
            self.perpendicular_bisector(kwargs["point_a"], kwargs["point_b"], entry_num)
        elif plottype == "half_line":
            self.half_line(kwargs["point"], kwargs["theta"], entry_num)

    
    def parse_input(self, input: str, entrynum: int) -> tuple[str, dict[str, float]]:
        number_search = "([-+]?[0-9]*\.?[0-9]+)"
        complex_search = "((?=[iIjJ.\d+-])([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?![iIjJ.\d]))?([+-]?(?:(?:\d+(?:\.\d*)?|\.\d+))?[iIjJ])?)"
        circle_search = f"^(\|(({complex_search}(-|\+)z)|(z(-|\+){complex_search}))\|={number_search})|(\|z\|={number_search})$"
        circle_results = match(circle_search, input)
        if circle_results:
            return circle_locus(circle_results.groups())
        perpendicular_bisector_search = f"^(\|(({complex_search}(-|\+)z)|(z(-|\+){complex_search})|z)\|=\|(({complex_search}(-|\+)z)|(z(-|\+){complex_search})|z)\|)$"
        perpendicular_bisector_results = match(perpendicular_bisector_search, input)
        if perpendicular_bisector_results:
            return perp_bisector_locus(perpendicular_bisector_results.groups())
        half_line_search = f"^(arg\((({complex_search}(-|\+)z)|(z(-|\+){complex_search})|z)\)={number_search})$"
        half_line_results = match(half_line_search, input)
        if half_line_results:
            return half_line_locus(half_line_results.groups())
        return None

    
    def remove_plot(self, entrynum: int):
        if entrynum in self.plotsdict:
            curr = self.plotsdict[entrynum]
            # if None
            if not curr:
                return
            type = curr[0]
            # if the plot is an 'circle' type or a 'perpendicular_bisector' type
            if type == "circle" or type == "perpendicular_bisector":
                curr[1].remove()
            elif type == "half_line":
                half_line = curr[1].pop(0)
                half_line.remove()


def __xlim_change(axis: Axes):
    xlim = axis.get_xlim()
    if xlim[0] > 0:
        currtickpos = -1
    elif xlim[1] < 0:
        currtickpos = 1
    else:
        currtickpos = 0
    if currtickpos != GraphingVariables.prev_y_axis_pos:
        # if the axis is to the left of the screen
        if currtickpos == -1:
            axis.yaxis.tick_left()
            currspine = axis.spines["left"]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        # if the axis is to the right of the screen   
        elif currtickpos == 1:
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
        GraphingVariables.prev_y_axis_pos = currtickpos


def __ylim_change(axis: Axes):
    ylim = axis.get_ylim()
    if ylim[0] > 0:
        currtickpos = -1
    elif ylim[1] < 0:
        currtickpos = 1
    else:
        currtickpos = 0
    if currtickpos != GraphingVariables.prev_x_axis_pos:
    # if the axis is to the bottom of the screen
        if currtickpos == -1:
            axis.xaxis.tick_bottom()
            currspine = axis.spines["bottom"]
            currspine.set_position(("outward", 0))
            currspine.set_color("lightgray")
        # if the axis is to the top of the screen   
        elif currtickpos == 1:
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
        GraphingVariables.prev_x_axis_pos = currtickpos


def setup_figure(plot: pyplot, figure: figure, axes: axes, graph_line_colour: str=GraphingVariables.graph_line_colour):
    """
        ### 1. Grid Lines
        Draws the major and minor grid lines. Defaults to a classic blue graph paper colour.
        Also draws the axis with spines.
        ### 2. Aspect Ratio
        Sets the aspect ratio to 1:1, or 'equal'.
        ### 3. Initial Position
        Sets the initial position of the graph at the origin and with a -10 to 10 view of the axes.
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

    ### 3
    plot.axis([-8, 8, -8, 8])