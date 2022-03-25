import matplotlib.pyplot as plt
import tkinter as tk
from graphing import GraphingBrush as gbrush
from graphing import setup_figure

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # Setup tkinter window
        self.title("Complex Loci Plotter")
        self.iconphoto(True, tk.PhotoImage(file=r"./icon.png"))
        self.geometry("960x540")

        # Setup tkinter vars
        self.entrytext = tk.StringVar()

        # Setup widgets
        self.widget_setup()

    def widget_setup(self):
        padding = {"padx" : 10, "pady": 10}
        entry = tk.Entry(self, justify="right", validate="all", textvariable=self.entrytext, width=20, font=50)
        entry.grid(column=0, row=0, **padding)
        self.entrytext.trace_add("write", self.on_entry_change)

    def on_entry_change(self, *args):
        print(self.entrytext.get())



def main():
    # Start tkinter window
    window = Window()
    window.mainloop()

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