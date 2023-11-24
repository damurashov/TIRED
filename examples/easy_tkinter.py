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


if __name__ == "__main__":
	main()
