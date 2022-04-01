import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import tkinter as tk
from graphing import GraphingBrush as gbrush, setup_figure


def tokenise(inp: str, delimeters: dict) -> list:
    """
    Takes in anput string inp and a dict of delimeters.\n
    An example is as follows.\n
    inp = "|z-i^i|"\n
    delimeters = {
        "|": "ABS",
        "z": "COMPLEX_VARIABLE",
        "+": "ADD",
        "-": "SUB",
        "^": "POW",
        "i": "IMAGINARY_UNIT"
    }\n
    Would return:\n
    [
        "ABS",
        "COMPLEX_VARIABLE",
        "SUB",
        "IMAGINARY_UNIT",
        "POW",
        "IMAGINARY_UNIT"
    ]
    """
    out = {}
    for char in delimeters:
        return


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
        self.entrytext = tk.StringVar()

        # Matplot lib setup
        # Setup figure
        self.figure, self.axes = plt.subplots()
        setup_figure(plt, self.figure, self.axes)

        # Creating and using brush
        default_brush = gbrush(plt, fig=self.figure, axs=self.axes, line_colour="green")
        default_brush.circle(1, (1, 2))

        # Set title
        plt.title("Complex Loci Plot")

        # Setup widgets
        self.widget_setup()

        # Setup matplotlib plot
        self.matplotlib_setup()


    def _quit(self):
        self.quit()


    def widget_setup(self):
        padding = {"padx" : 10, "pady": 10}
        frame_one_bg = "#dbdbdb"
        frame_two_bg = ""

        # First frame
        frame_one = tk.Frame(self, bg=frame_one_bg, bd=5)
        frame_one.pack(side="left", fill="both")
        title_one = tk.Label(frame_one, justify="center", text="Enter Loci Equations Below:", bg=frame_one_bg)
        title_one.pack(side="top", **padding, fill="y")
        entry = tk.Entry(frame_one, justify="right", validate="all", textvariable=self.entrytext, width=20, font=50)
        entry.pack(side="top", **padding)
        #submit_locus_button = tk.Button(frame_one, text="Draw Locus", anchor="center") This could be used if parsing the input each time is too time consuming
        #submit_locus_button.grid(column=1, row=1, **padding)
        new_entry_button = tk.Button(frame_one, text="New Locus", anchor="center")
        new_entry_button.pack(side="top", **padding)

        # Second frame for settings, to be implemented later.
        """
        frame_two = tk.Frame(self, bg="yellow", bd=5)
        frame_two.grid(column=1, row=0 , **padding)
        entry = tk.Entry(frame_two, justify="right", validate="all", textvariable=self.entrytext, width=20, font=50)
        title_two = tk.Label(frame_two, justify="center", text="Set Loci Settings:", bg=frame_one_bg)
        title_two.grid(column=0, row=0, **padding)
        entry.grid(column=0, row=1, **padding, ipady=20)
        """

        self.entrytext.trace_add("write", self.on_entry_change)
        
    def matplotlib_setup(self):
        # Matplotlib canvas widget
        # Show plot on canvas
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.get_tk_widget().pack(side="right")

        # Matplotlib navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side="top", fill="both", expand=True)


    def on_entry_change(self, *args):
        print(self.entrytext.get())



def main():
    # Start tkinter window
    window = Window()
    print("hi")
    window.mainloop()
    print("hi")
    window.destroy()

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