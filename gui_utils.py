import tkinter as tk


class Selector(tk.Frame):
    def __init__(self, title, choices, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.choice_var = tk.StringVar(self)
        if choices:
            self.choice_var.set(choices[0])
            self.option_command(self.choice_var.get())

        self.title = tk.Label(self, text=title)
        self.title.grid(row=0, sticky=tk.W)

        self.selector = tk.OptionMenu(
            self, self.choice_var, *choices, command=self.option_command
        )
        self.selector.grid(row=1, sticky=tk.W + tk.E)

    def option_command(self, new_value):
        raise NotImplementedError
