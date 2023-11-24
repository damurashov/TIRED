"""
Frequently reused Tkinter snippets for building one-off GUI
applications in the most efficient way
"""

# TODO: add interface for easily building simple GUIs with checkboxes, tabs, file selection dialogs, drop-down selections, menus, and buttons

from tkinter import ttk
import threading
import tired.logging
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
    def __init__(self, parent, title, textvariable, from_=1.0, to=10.0, increment=1.0, *args, **kwargs):
        # TODO: save value variable in "self"
        tkinter.Frame.__init__(self, parent)
        self.label = tkinter.Label(self, text=title, width=DEFAULT_LABEL_WIDTH, anchor='w')
        self.spinbox = tkinter.Spinbox(self, *args, textvariable=textvariable, from_=from_, to=to, increment=increment, **kwargs)
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


class GridPlacementStrategy:
    def place_widget(self, parent: tkinter.Widget, widget: tkinter.Widget):
        nrow = len(parent.grid_slaves())
        tired.logging.debug(f"Adding widget {widget.__class__.__name__} at row {nrow}")
        widget.grid(row=nrow, column=0, sticky='w')


class Frame(tkinter.Frame):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self._tk_variables_map = dict()
        self._file_dialog_map = dict()
        self._checkbox_map = dict()
        self._button_map = dict()
        self._spinbox_map = dict()
        self._tabs_map = dict()
        self._frame_map = dict()

        # Defines how widgets should be arranged on a pane
        self._placement_strategy = GridPlacementStrategy()

    def _is_widget_registered(self, widget_name):
        return widget_name in self._tk_variables_map.keys() or widget_name in self._tabs_map.keys() or widget_name in self._frame_map.keys()

    def add_checkbox(self, string_identifier: str, default_value=False):
        """
        Adds a checkbox onto pane. String identifier is used as title
        """
        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        variable = tkinter.BooleanVar()
        self._tk_variables_map[string_identifier] = variable
        widget = tkinter.Checkbutton(self, text=string_identifier, variable=variable)
        self._checkbox_map[string_identifier] = widget
        self._placement_strategy.place_widget(self, widget)

        return widget

    def set_widget_value(self, widget_string_identifier: str, value: object):
        """
        Sets value to a variable corresponding to a widget selected
        """
        if not self._is_widget_registered(widget_string_identifier):
            raise KeyError(f"A widget with the name \"{widget_string_identifier}\" does not exist")

        self._tk_variables_map[widget_string_identifier].set(value)

    def add_file_selection(self, string_identifier: str, file_types=('*.*', )):
        """
        Adds file dialog onto plane.
        """
        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        variable = tkinter.StringVar()
        self._tk_variables_map[string_identifier] = variable
        widget = FileSelectionWidget(self, string_identifier, variable, True, file_types)
        self._file_dialog_map[string_identifier] = widget
        self._placement_strategy.place_widget(self, widget)

        return widget

    def add_spinbox(self, string_identifier: str, min: float, max: float, step: float = 1.0):
        """
        Adds spinbox onto plane.
        post: The value type for spinbox is `double`
        """
        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        variable = tkinter.DoubleVar()
        self._tk_variables_map[string_identifier] = variable
        widget = LabeledSpinbox(self, string_identifier, variable, min, max, step)
        self._spinbox_map[string_identifier] = widget
        self._placement_strategy.place_widget(self, widget)

        return widget

    def add_button(self, string_identifier, callback=lambda: None):
        """
        Adds a simple button
        """
        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        widget = tkinter.Button(self, text=string_identifier, command=callback)
        self._button_map[string_identifier] = widget
        self._placement_strategy.place_widget(self, widget)

        return widget

    def add_tabs(self, string_identifier):
        from tired.tk import Tabs

        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        widget = Tabs(self)
        self._placement_strategy.place_widget(self, widget)
        self._tabs_map[string_identifier] = widget

        return widget

    def add_frame(self, string_identifier):
        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        widget = Frame(self)
        self._frame_map[string_identifier] = widget
        self._placement_strategy.place_widget(self, widget)

        return widget


class Tabs(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        ttk.Notebook.__init__(self, *args, **kwargs)
        self._frame_map = dict()

    def _is_widget_registered(self, widget_string_identifier: str):
        return widget_string_identifier in self._frame_map.keys()

    def add_frame(self, string_identifier):
        if self._is_widget_registered(string_identifier):
            raise KeyError(f"A widget with the name \"{string_identifier}\" already exists")

        widget = Frame(self)
        self.add(widget, text=string_identifier)

        return widget


class Window(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self._root_frame = Frame(self)
        self._root_frame.pack(expand=True, fill='both')

    def _is_widget_registered(self, widget_string_identifier: str):
        return widget_string_identifier in self._frame_map.keys() or widget_string_identifier in self._tabs_map.keys()

    def add_frame(self, string_identifier: str):
        return self._root_frame.add_frame(string_identifier)

    def add_tabs(self, string_identifier: str):
        return self._root_frame.add_tabs(string_identifier)

    def run(self):
        self.mainloop()
