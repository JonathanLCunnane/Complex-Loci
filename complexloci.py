import matplotlib
from pyparsing import col
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from graphing import GraphingBrush as gbrush, setup_figure



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
        padding = {"padx" : 10, "pady": 10}
        frame_bg = "#dbdbdb"

        # First frame
        frame_one = tk.Frame(self, bg=frame_bg, bd=5)
        frame_one.pack(side="left", fill="both")
        title_one = tk.Label(frame_one, justify="center", text="Enter Loci Equations Below:", bg=frame_bg)
        title_one.pack(side="top", **padding, fill="y")
        entry = ttk.Entry(frame_one, justify="right", validate="all", textvariable=self.entry_vars[1], width=20, font=50)
        entry.pack(side="top", **padding)
        new_entry_button = ttk.Button(frame_one, text="New Locus", command=self.on_new_locus)
        new_entry_button.pack(side="top", **padding)

        # Second frame for configuring loci.
        self.frame_two = tk.Frame(self, bg=frame_bg, bd=5)
        self.frame_two.pack(side="left", fill="both")
        title_two = tk.Label(self.frame_two, justify="center", text="Configure Loci:", bg=frame_bg)
        title_two.pack(side="top", **padding, fill="y")
        settings_frame = tk.Frame(self.frame_two, bg="green", bd=5, width=200, height=50)
        settings_frame.pack_propagate(False)
        settings_frame.pack(side="top")
        cross_img = tk.PhotoImage(file=r"./cross.png")
        entry_delete = ttk.Button(settings_frame, image=cross_img)
        entry_delete.image = cross_img
        entry_delete.pack(side="left")
        
        colour_select = ttk.OptionMenu(settings_frame, self.colour_select_vars[1], "Select a Colour", "green", "blue", "red")
        colour_select.pack(side="left", **padding)
        self.colour_select_vars[1].set("Select locus colour:")

        self.colour_select_vars[1].trace_add("write", lambda *args: self.change_brush_colour(1))
        self.entry_vars[1].trace_add("write", lambda *args: self.on_entry_change(1))
        

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

    
    def on_new_locus(self):
        pass



def main():
    # Start tkinter window
    window = Window()
    window.mainloop()
    window.destroy()
    

if __name__ == "__main__":
    main()