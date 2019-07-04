import tkinter as tk


class Selector(tk.Frame):
    """
    Option menu with a label. Upon making choice function passed as command argument
    is executed. Such function has one parameter - new value.
    """

    def __init__(self, parent, title, choices, command, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.choice_var = tk.StringVar(self)
        if choices:
            self.choice_var.set(choices[0])
            command(self.choice_var.get())

        self.title = tk.Label(self, text=title)
        self.title.grid(row=0, sticky=tk.W)

        self.selector = tk.OptionMenu(self, self.choice_var, *choices, command=command)
        self.selector.grid(row=1, sticky=tk.W + tk.E)
