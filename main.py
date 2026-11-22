
import tkinter as tk

from asterism_gui import AsterismGUI


def main():

    root = tk.Tk()

    app = AsterismGUI(root)

    # print("Before removal: ")
    # print("Thoughts: ", len(app.map.bubbles))
    # print("Connections: ", len(app.map.connections))
    #
    # app.map.remove_bubble(app.map.bubbles[0])
    #
    # print("After removal: ")
    # print("Thoughts: ", len(app.map.bubbles))
    # print("Connections: ", len(app.map.connections))

    app.draw_map()

    root.mainloop()


if __name__ == "__main__":
    main()
