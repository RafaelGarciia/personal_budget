import tkinter as tk
from tkinter import font


class Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.width = 640
        self.height = 480

        self.defaultFont = font.nametofont('TkDefaultFont')
        self.defaultFont.configure(family='DejaVu Sans Mono')

        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)
        self.title('Personal Budget')

        self.main_frame: tk.Frame = None

    def clear_frame(self):
        if self.main_frame == None:
            return
        else:
            self.main_frame.place_forget()

    def show_frame(self):
        if self.main_frame != None:
            self.main_frame.place(x=0, y=0)
