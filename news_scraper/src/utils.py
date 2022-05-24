import os


def clear_screen():
    if os.name == "nt":
        clear = "cls"
    else:
        clear = "clear"
    os.system(clear)

class clear_terminal:
    def __enter__(self):
        clear_screen()
    def __exit__(self, type, value, traceback):
        clear_screen()