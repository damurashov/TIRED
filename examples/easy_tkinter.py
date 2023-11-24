import tired.tk
import tkinter
from tkinter import ttk

def main():
	window = tkinter.Tk()
	tabs = ttk.Notebook(window)
	frame = tired.tk.Frame(tabs)
	frame.add_checkbox("Have some rest", True)
	frame.add_file_selection("Select some file")
	frame.add_spinbox("Select value", 0, 100, 20)
	frame.add_button("Apply")
	simple_frame = tired.tk.Frame(tabs)
	simple_frame.add_button("Just run")
	tabs.add(frame, text="Complicated frame")
	tabs.add(simple_frame, text="Simple frame")
	window.title("So TIRED...")
	tabs.pack(expand=True, fill='both')
	window.mainloop()


def even_simpler():
	"""
	window
		tabs
			frame
				checkbox
				selection
				spinbox
				button
			simple_frame
				button
		another_simple_frame
	"""
	window = tired.tk.Window()
	tabs = tired.tk.Tabs(window)
	frame = tired.tk.Frame(tabs)
	frame.add_checkbox("Have some rest", True)
	frame.add_file_selection("Select some file")
	frame.add_spinbox("Select value", 0, 100, 20)
	frame.add_button("Apply")
	simple_frame = tired.tk.Frame(tabs)
	simple_frame.add_button("Just run")
	another_simple_frame = tired.tk.Frame(tabs)
	another_simple_frame.add_button("Just run")
	tabs.add_frame(frame, text="Complicated frame")
	tabs.add_frame(simple_frame, text="Simple frame")
	window.add_tabs(tabs)
	window.add_frame(another_simple_frame)
	window.run()


if __name__ == "__main__":
	main()
