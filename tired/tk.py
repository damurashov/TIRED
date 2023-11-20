"""
Frequently reused Tkinter snippets for building one-off GUI
applications in the most efficient way
"""

# TODO: add interface for easily building simple GUIs with checkboxes, tabs, file selection dialogs, drop-down selections, menus, and buttons

import tkinter


DEFAULT_LABEL_WIDTH = 25

class FileSelectionWidget(tkinter.Frame):

    def __init__(self, parent, title, path_string_variable: tkinter.StringVar, mode_open=True, file_types=("*.*",), *args, **kwargs):
        from tkinter.filedialog import askopenfilename, asksaveasfilename
        # TODO: save value variable in "self"

        tkinter.Frame.__init__(self, parent, *args, **kwargs)

        file_types = tuple([(i,i,) for i in file_types])
        file_dialog_cb = askopenfilename if mode_open else asksaveasfilename

        self.mode_open = mode_open
        self.title_label = tkinter.Label(self, text=title, width=DEFAULT_LABEL_WIDTH, anchor='w')
        self.path_label = tkinter.Label(self, text="", textvariable=path_string_variable)
        self.select_path_btn = tkinter.Button(self, text="...", command=lambda: path_string_variable.set(file_dialog_cb(title=title, filetypes=file_types)))
        self.reset_btn = tkinter.Button(self, text="Reset", command=lambda: path_string_variable.set(""))

        self.title_label.grid(row=0, column=0, sticky='w')
        self.select_path_btn.grid(row=0, column=1)
        self.reset_btn.grid(row=0, column=2)
        self.path_label.grid(row=0, column=3, sticky='wn')


class LabeledSpinbox(tkinter.Frame):
    def __init__(self, parent, title, textvariable, *args, **kwargs):
        # TODO: save value variable in "self"
        tkinter.Frame.__init__(self, parent)
        self.label = tkinter.Label(self, text=title, width=DEFAULT_LABEL_WIDTH, anchor='w')
        self.spinbox = tkinter.Spinbox(self, *args, textvariable=textvariable, **kwargs)
        self.label.grid(row=0, column=0, sticky='nsew')
        self.spinbox.grid(row=0, column=1, sticky='nsew')


class LabeledOptionsMenu(tkinter.Frame):
    def __init__(self, parent, title, targetvar, *args, **kwargs):
        # TODO: save value variable in "self"
        tkinter.Frame.__init__(self, parent)

        self.label = tkinter.Label(self, text=title, width=DEFAULT_LABEL_WIDTH, anchor='w')
        self.option_menu = tkinter.OptionMenu(self, targetvar, *args, **kwargs)
        self.label.grid(row=0, column=0, sticky='nsew')
        self.option_menu.grid(row=0, column=1, sticky='nsew')
