from tkinter import Tk
from Test import Test
import GUI

test = Test('test.json')
window = Tk()
window.title("Multiple Choice Test Generator")

GUI.Init_Frame(window, test)

window.mainloop()
