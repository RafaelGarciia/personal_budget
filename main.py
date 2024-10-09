from Source import window, frames


def application():
    app = window.Window()
    app.main_frame = frames.BudGet_screen(app)
    app.show_frame()
    app.mainloop()


application()
