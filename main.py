from interface import gui

__version__ = "v0.0.3 alpha"
__author__ = "JohnKun136NVCP"


if __name__ == "__main__":
    try:
        gui.showInterface()
    except:
        print("Un error se produjo en la ejecucion")