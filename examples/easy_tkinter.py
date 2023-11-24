import tired.tk
import tkinter

def main():
	window = tkinter.Tk()
	frame = tired.tk.Frame(window)
	frame.add_checkbox("Have some rest", True)
	frame.add_file_selection("Select some file")
	frame.add_spinbox("Select value", 0, 100, 20)
	window.title("So TIRED...")
	frame.pack(expand=True, fill='x')
	window.mainloop()


if __name__ == "__main__":
	main()
