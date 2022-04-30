import matplotlib
from pyparsing import col
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from graphing import GraphingBrush as gbrush, setup_figure
from graphing import GraphingVariables



class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # Overload window deletion so that the program does not hang.
        self.protocol("WM_DELETE_WINDOW", self._quit)

        # Setup tkinter window
        self.title("Complex Loci Plotter")
        self.iconphoto(True, tk.PhotoImage(file=r"./icon.png"))
        self.geometry("960x540")
        self.resizable(False, False)

        # Setup tkinter vars
        entry_text = tk.StringVar()
        self.entry_vars = {1: entry_text}
        colour_select_text = tk.StringVar()
        self.colour_select_vars = {1: colour_select_text}
        self.padding = {"padx" : 10, "pady": 10}
        self.entry_padding = {"padx": 10, "pady": 18}
        self.frame_bg = "#dbdbdb"

        # Matplot lib setup
        # Setup figure
        self.figure, self.axes = plt.subplots()
        setup_figure(plt, self.figure, self.axes)

        # Creating default brush
        self.default_brush = gbrush(plt, fig=self.figure, axs=self.axes, line_colour="green")

        # Set title
        plt.title("Complex Loci Plot")

        # Setup widgets
        self.widget_setup()

        # Setup matplotlib plot
        self.matplotlib_setup()

        # Create {entry# : brush} dict for replacing the correct plot on entry edit.
        self.plotsdict = {1: self.default_brush}

        # Set locus count to 1
        self.locus_count = 1


    def _quit(self):
        self.quit()


    def widget_setup(self):

        # First frame
        self.entry_frame = tk.Frame(self, bg=self.frame_bg, bd=5)
        self.entry_frame.pack(side="left", fill="both")
        title_one = tk.Label(self.entry_frame, justify="center", text="Enter Loci Equations Below:", bg=self.frame_bg)
        title_one.pack(side="top", **self.padding, fill="y")
        entry = ttk.Entry(self.entry_frame, justify="right", validate="all", textvariable=self.entry_vars[1], font=1)
        entry.pack(side="top", **self.entry_padding)
        self.new_entry_button = ttk.Button(self.entry_frame, text="New Locus", command=self.on_new_locus)
        self.new_entry_button.pack(side="top", **self.padding)

        # Second frame for configuring loci.
        self.frame_two = tk.Frame(self, bg=self.frame_bg, bd=5)
        self.frame_two.pack(side="left", fill="both")
        title_two = tk.Label(self.frame_two, justify="center", text="Configure Loci:", bg=self.frame_bg)
        title_two.pack(side="top", **self.padding, fill="y")
        settings_frame = tk.Frame(self.frame_two, bg=self.frame_bg, bd=5, width=200, height=60)
        settings_frame.pack_propagate(False)
        settings_frame.pack(side="top")
        cross_img = tk.PhotoImage(file=r"./cross.png")
        entry_delete = ttk.Button(settings_frame, image=cross_img)
        entry_delete.image = cross_img
        entry_delete.pack(side="left")
        
        colour_select = ttk.OptionMenu(settings_frame, self.colour_select_vars[1], "Select a Colour", *(GraphingVariables.emoji_colour_dict))
        colour_select.pack(side="left", **self.padding)
        self.colour_select_vars[1].set("Select locus colour:")

        self.colour_select_vars[1].trace_add("write", lambda *args: self.change_brush_colour(1))
        self.entry_vars[1].trace_add("write", lambda *args: self.on_entry_change(1))
        

    def on_new_locus(self):
        # Check which is the lowest locus number which can be created
        entry_num = max(self.plotsdict.keys()) + 1

        # Add new entry to entry_vars and new colour select to colour_select_vars
        entry_text = tk.StringVar()
        self.entry_vars[entry_num] = entry_text
        colour_select_text = tk.StringVar()
        self.colour_select_vars[entry_num] = colour_select_text
        self.plotsdict[entry_num] = gbrush(plt, self.figure, self.axes)

        # Frame for configuring loci.
        settings_frame = tk.Frame(self.frame_two, bg=self.frame_bg, bd=5, width=200, height=60)
        settings_frame.pack_propagate(False)
        settings_frame.pack(side="top")
        cross_img = tk.PhotoImage(file=r"./cross.png")
        entry_delete = ttk.Button(settings_frame, image=cross_img)
        entry_delete.image = cross_img
        entry_delete.pack(side="left")
        
        colour_select = ttk.OptionMenu(settings_frame, self.colour_select_vars[entry_num], "Select a Colour", *(GraphingVariables.emoji_colour_dict))
        colour_select.pack(side="left", **self.padding)
        self.colour_select_vars[entry_num].set("Select locus colour:")

        self.colour_select_vars[entry_num].trace_add("write", lambda *args: self.change_brush_colour(entry_num))
        self.entry_vars[entry_num].trace_add("write", lambda *args: self.on_entry_change(entry_num))

        # Remove new entry button, add another entry field, and then add the new entry button back
        self.new_entry_button.destroy()
        entry = ttk.Entry(self.entry_frame, justify="right", validate="all", textvariable=self.entry_vars[entry_num], width=20, font=50)
        entry.pack(side="top", **self.entry_padding)
        self.new_entry_button = ttk.Button(self.entry_frame, text="New Locus", command=self.on_new_locus)
        self.new_entry_button.pack(side="top", **self.padding)

        # Disable button if no more loci can be created
        if len(self.plotsdict.keys()) >= 5:
            self.new_entry_button.configure(state="disabled")


    def change_brush_colour(self, entrynum: int):
        self.plotsdict[entrynum].colour = self.colour_select_vars[entrynum].get()

        # call entry change to force update the plot
        self.on_entry_change(entrynum)


    def matplotlib_setup(self):
        # Matplotlib canvas widget
        # Show plot on canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvaswidget = self.canvas.get_tk_widget()
        self.canvaswidget.pack(side="right")

        # Matplotlib navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side="top", fill="both", expand=True)


    def update_matplotlib(self):
        """
        Updates the matplotlib canvas.
        """
        self.canvaswidget.update()
        self.canvas.draw_idle() 


    def on_entry_change(self, entrynum: int):
        inp = self.default_brush.parse_input(self.entry_vars[entrynum].get(), entrynum)
        self.plotsdict[entrynum].remove_plot(entrynum)
        if inp:   
            self.plotsdict[entrynum].draw_input(inp[0], entrynum, **inp[1])
        else:
            self.plotsdict[entrynum].plotsdict[entrynum] = None
        self.update_matplotlib()


def main():
    # Start tkinter window
    window = Window()
    window.mainloop()
    window.destroy()
    

if __name__ == "__main__":
    main()