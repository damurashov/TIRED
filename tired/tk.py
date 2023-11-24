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
    def __init__(self, parent, title, textvariable, *args, from_=1, to=10, **kwargs):
        # TODO: save value variable in "self"
        tkinter.Frame.__init__(self, parent)
        self.label = tkinter.Label(self, text=title, width=DEFAULT_LABEL_WIDTH, anchor='w')
        self.spinbox = tkinter.Spinbox(self, *args, textvariable=textvariable, from_=from_, to=to, **kwargs)
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


class Frame(tkinter.Frame):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self._tk_variables_map = dict()
        self._file_dialog_map = dict()
        self._checkbox_map = dict()
        self._button_map = dict()

    def _count_widgets(self):
        return len(self.grid_slaves())

    def _is_widget_registered(self, widget_name):
        return widget_name in self._tk_variables_map.keys()

    def _autoplace_widget(self, widget: tkinter.Widget):
        """
        pre: widget's parent should be assigned to self
        """
        nrow = self._count_widgets()
        widget.grid(row=nrow, column=0)

    def add_checkbox(self, string_identifier: str, default_value=False):
        """
        Adds a checkbox onto pane. String identifier is used as title
        """
        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        variable = tkinter.BooleanVar()
        self._tk_variables_map[string_identifier] = variable
        widget = tkinter.CheckButton(self, text=string_identifier, variable=variable)
        self._checkbox_map[string_identifier] = widget

    def set_widget_value(self, widget_string_identifier: str, value: object):
        """
        Sets value to a variable corresponding to a widget selected
        """
        if not self._is_widget_registered(widget_string_identifier):
            raise KeyError(f"A widget with the name \"{widget_string_identifier}\" does not exist")

        self._tk_variables_map[widget_string_identifier].set(value)

    def add_file_dialog(self, string_identifier: str):
        """
        Adds file dialog onto plane.
        """
        pass

    def add_spinbox(self, string_identifier: str, file_types, min: float, max: float, step: float = 1.0):
        """
        Adds spinbox onto plane
        """
        pass

    def add_button(self, string_identifier: str):
        pass
