import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import math

from asterism import Asterism


class AsterismGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Asterism")
        self.root.geometry("1100x700")
        self.root.minsize(600,450)
        self.root.configure(bg="#1e1e2e")

        self.map = Asterism()

        # Connection creation state
        self.selected_bubble = None
        self.last_click = None
        
        # Mouse click variables
        self.click_timer = None
        self.hold_timer = None
        self.is_holding = False
        self.click_count = 0
        # Mouse timings
        self.HOLD_DELAY = 400
        self.DOUBLE_DELAY = 200

        # ------------------------------
        # HEADER
        # ------------------------------

        header = tk.Frame(root, bg="#181825", height=65)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="ThoughtMap",
            font=("Arial", 22, "bold"),
            fg="#cdd6f4",
            bg="#181825"
        )
        title.pack(side="left", padx=20, pady=12)

        self.layer_title = tk.Label(
            header,
            text= self.map.layer_names[self.map.current_layer],
            font = ("Arial", 17, "bold"),
            fg = "#cdd6f4",
            bg = "#181825",
            justify = "center"
        )
        self.layer_title.pack(side="left", padx=20, pady=12)

        # ------------------------------
        # TOOLBAR
        # ------------------------------

        # ToolBar will be respecced to handle Menu/IO Options. Bubble creation should be
        # handled with mouse button presses.

        toolbar = tk.Frame(root, bg="#313244", height=50)
        toolbar.pack(fill="x")

        tk.Button(
            toolbar,
            text="+ Add Thought",
            command=self.add_bubble
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            toolbar,
            text="Display Map",
            command=self.draw_map
        ).pack(side="right", padx=5, pady=8)

        tk.Button(
            toolbar,
            text="Cycle Layer",
            command=self.cycle_layer
        ).pack(side="right", padx=5, pady=8)

        # ------------------------------
        # STATUS BAR
        # ------------------------------

        statusbar = tk.Frame(root, bg="#313244", height=20)
        statusbar.pack(fill="x",side="bottom")

        self.status = tk.Label(
            statusbar,
            text="Ready",
            fg="#cdd6f4",
            bg="#313244"
        )
        self.status.pack(side="left", padx=3)

        self.coordinates = tk.Label(
            statusbar,
            text="400,300",
            fg="#cdd6f4",
            bg="#313244"
        )
        self.coordinates.pack(side="right", padx=3)

        # ------------------------------
        # CANVAS
        # ------------------------------

        self.canvas = tk.Canvas(
            root,
            bg="#11111b",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ------------------------------
        # Button Binds
        # ------------------------------

        # Mouse binds for single, double clicks, & hold for left clicks
        self.canvas.bind("<Button-1>", self.left_click_press)
        self.canvas.bind("<ButtonRelease-1>", self.left_click_release)

        # Mouse binds for single, double clicks, & hold for right clicks
        self.canvas.bind("<Button-3>", self.right_click_press)
        self.canvas.bind("<ButtonRelease-3>", self.right_click_release)

        # Binds mouse movements to check for mouse coordinates
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # ------------------------------
        # Thought Option Menu
        # This menu pulls up when you right click on a thought
        # ------------------------------

        self.thought_menu = tk.Frame(
            self.canvas,
            width = 20,
            height = 10,
        )
        self.thought_menu.place_forget()

        focus_btn = tk.Button(
            self.thought_menu,
            text = "Focus",
            command = self.focus_thought,
        )
        focus_btn.pack(padx = 5, pady = 5)
        del_btn = tk.Button(
            self.thought_menu,
            text="delete",
            command=self.delete_thought,
        )
        del_btn.pack(padx=5)

        # Bind menu buttons to dismiss on middle/right click
        focus_btn.bind("<Button-2>", self.reset_variables(""))
        focus_btn.bind("<Button-3>", self.reset_variables(""))

        # ------------------------------
        # TEST DATA
        # ------------------------------

        self.map.add_bubble("Hello", "#45475a", 200, 150, 50, 50)
        self.map.add_bubble("World", "#45475a", 500, 150, 50, 50)
        self.map.add_bubble("Goodbye", "#45475a", 350, 400, 40, 50)

        self.map.add_connection(self.map.bubbles[0], self.map.bubbles[1], "Winner", "#1C5FC9", 0)
        self.map.add_connection(self.map.bubbles[0], self.map.bubbles[2], "Tied", "#733572", 0)
        self.map.add_connection(self.map.bubbles[1], self.map.bubbles[2], "Lost", "#387A31", 0)
        self.map.add_connection(self.map.bubbles[0], self.map.bubbles[2], "Undecided", "#9C845C", 1)

        self.map.add_layer("tester")

        self.draw_map()

    # ------------------------------
    # ADD BUBBLE
    # ------------------------------

    def add_bubble(self):

        name = simpledialog.askstring(
            "New Thought",
            "Name your new thought:"
        )

        if not name or not name.strip():
            return

        index = len(self.map.bubbles)

        x = 150 + (index % 4) * 200
        y = 150 + (index // 4) * 150

        self.map.add_bubble(name, "#45475A", x, y, 50, 50)

        self.draw_map()

    # ------------------------------
    # FIND BUBBLE UNDER MOUSE
    # ------------------------------

    def find_bubble_at(self, x, y):

        radius = 48

        for bubble in reversed(self.map.bubbles):

            distance = math.hypot(
                x - bubble.xpos,
                y - bubble.ypos
            )

            if distance <= radius:
                return bubble

        return None

    # ------------------------------
    # HANDLE CANVAS CLICK
    # ------------------------------

    # Checks coordinates of mouse
    def on_mouse_move(self, event):
        self.coordinates.config(
            text=f"{event.x}, {event.y}"
        )
        # If creating connection, draw line from selected bubble to cursor
        if(self.last_click == "left_single" and self.selected_bubble):
            # Redraw canvas, then create a line
            self.draw_map()
            self.canvas.create_line(
                self.selected_bubble.xpos,
                self.selected_bubble.ypos,
                event.x,
                event.y,
                fill="#5C5F72",
                width=2
            )

            self.bubble = self.selected_bubble

            # Redraw bubble over line
            self.canvas.create_oval(
                self.bubble.xpos - self.bubble.width,
                self.bubble.ypos - self.bubble.height,
                self.bubble.xpos + self.bubble.width,
                self.bubble.ypos + self.bubble.height,
                fill=self.bubble.rgb,
                outline="#F9E2AF",
                width=5
            )

            # Redraw bubble name
            self.canvas.create_text(
                self.bubble.xpos,
                self.bubble.ypos,
                text=self.bubble.name,
                fill="#CDD6F4",
                font=("Arial", 11, "bold"),
                width=85
            )





    # ------------------------------
    # Left Click Checker
    # ------------------------------
    
    # Left click hold checker - determines click type (single, double, hold)
    def left_click_press(self, event):
        # Reset variables
        self.is_holding = False
        if self.click_timer:
            event.widget.after_cancel(self.click_timer)
            self.click_timer = None
        
        # Start a timer
        self.hold_timer = self.root.after(self.HOLD_DELAY, lambda: self.on_left_hold(event))

    # Left click single double checker - if hold method wasn't called,
    # call single or double method
    def left_click_release(self, event):
        # Reset hold timer
        if self.hold_timer:
            self.root.after_cancel(self.hold_timer)
            self.hold_timer = None

        # If hold was called, return
        if self.is_holding:
            self.click_count = 0
            return

        self.click_count += 1
        if self.click_count == 1:
            self.click_timer = self.root.after(self.DOUBLE_DELAY, lambda: self.on_left_click(event))
        elif self.click_count > 1:
            self.on_double_left_click(event)


    # ------------------------------
    # Left Click Functions
    # ------------------------------

    # Single left click function call
    # Allows for connection making.
    def on_left_click(self, event):

        self.click_count = 0        # reset click counter

        # Resets all values if last click was not a left single click
        if self.last_click != "left_single":
            self.selected_bubble = None
            self.reset_variables("left_single")

        # Check for thought bubble
        clicked = self.find_bubble_at(event.x, event.y)

        if clicked is None:
            return

        # First click: select source
        if self.selected_bubble is None:
            self.selected_bubble = clicked

            self.status.config(
                text=f"Source: {clicked.name}. "
                     "Now select the DESTINATION thought."
            )

            self.draw_map()

            return

        # Second click: select destination
        source = self.selected_bubble
        destination = clicked

        # Prevent self-connections
        if source is destination:
            messagebox.showwarning(
                "Invalid Connection",
                "A thought cannot connect to itself."
            )

            self.cancel_connection()
            return

        # Ask user to name connection
        connection_name = simpledialog.askstring(
            "Name Connection",
            f"How is '{source.name}' related "
            f"to '{destination.name}'?"
        )

        # Check if entered name is empty
        if not connection_name or not connection_name.strip():
            self.cancel_connection()
            return

        # Create connection
        self.map.add_connection(
            source,
            destination,
            connection_name.strip(),
            "#A6ADC8",
            self.map.current_layer)

        # Change status message
        self.status.config(
            text=f"Created: {source.name} → "
                 f"{destination.name}"
        )

        self.selected_bubble = None

        self.draw_map()

    # Double left click function call
    #
    def on_double_left_click(self, event):

        self.click_count = 0  # reset click counter

        self.status.config(
            text="Double left click"
        )

        return

    # Left click & hold function call
    #
    def on_left_hold(self, event):

        # Reset click count, is_holding is set to true to prevent single/double click calls
        self.is_holding = True
        self.click_count = 0

        self.status.config(
            text="Hold left click"
        )
        return


    # ------------------------------
    # Right Click Checker
    # ------------------------------

    # Right click hold checker - determines click type (single, double, hold)
    def right_click_press(self, event):
        # Reset variables
        self.is_holding = False
        if self.click_timer:
            event.widget.after_cancel(self.click_timer)
            self.click_timer = None

        # Start a timer
        self.hold_timer = self.root.after(self.HOLD_DELAY, lambda: self.on_right_hold(event))

    # Right click single double checker - if hold method wasn't called,
    # call single or double method
    def right_click_release(self, event):
        # Reset hold timer
        if self.hold_timer:
            self.root.after_cancel(self.hold_timer)
            self.hold_timer = None

        # If hold was called, return
        if self.is_holding:
            self.click_count = 0
            return

        # Count the amount of click releases within a small time period,
        # then call single/double clicks
        self.click_count += 1
        if self.click_count == 1:
            self.click_timer = self.root.after(self.DOUBLE_DELAY, lambda: self.on_right_click(event))
        elif self.click_count > 1:
            self.on_double_right_click(event)


    # ------------------------------
    # Right Click Functions
    # ------------------------------

    # Single right click function call
    # When you click on a thought, pull up thought menu*            *incomplete
    def on_right_click(self, event):

        self.click_count = 0  # reset click counter

        self.status.config(
            text="Single right click"
        )

        self.reset_variables("right_single")

        # Check for thought bubble
        clicked = self.find_bubble_at(event.x, event.y)
        if clicked is None:
            return

        self.selected_bubble = clicked

        self.draw_map()

        xval = clicked.xpos + 65
        yval = clicked.ypos -50

        self.thought_menu.place(x= xval, y= yval)

        #tester Method
        # self.menu(self.canvas,
        #           xval,
        #           yval,
        #           fill="white",
        #           outline="red",
        #           width=1)
        return

    # Double right click function call
    #
    def on_double_right_click(self, event):

        self.click_count = 0  # reset click counter

        self.status.config(
            text="Double right click"
        )

        return

    # Right click & hold function call
    #
    def on_right_hold(self, event):

        # Reset click count, is_holding is set to true to prevent single/double click calls
        self.is_holding = True
        self.click_count = 0

        self.status.config(
            text="Hold right click"
        )
        return


    # ------------------------------
    # CANCEL CONNECTION MODE
    # ------------------------------

    def cancel_connection(self):

        self.connect_mode = False
        self.selected_bubble = None
        self.draw_map

    # ------------------------------
    # DRAW MAP
    # ------------------------------

    def draw_map(self):

        # Set layer name to current layer
        self.layer_title.config(
            text=self.map.layer_names[self.map.current_layer]
        )

        self.canvas.delete("all")

        # Draw connections first.
        for connection in self.map.connections:
            # Filter out connections not in this layer.
            if connection.layer == self.map.current_layer:

                # Grab Bubble X & Y positions
                start_x = connection.node_one.xpos   # Bubble 1: x & y position
                start_y = connection.node_one.ypos
                end_x = connection.node_two.xpos     # Bubble 2: x & y position
                end_y = connection.node_two.ypos

                # Draw connection line.
                self.canvas.create_line(
                    start_x,
                    start_y,
                    end_x,
                    end_y,
                    fill=connection.rgb,
                    width=2,
                    arrow=tk.LAST
                )

                #write connection type name
                midpoint_x = (start_x + end_x) / 2
                midpoint_y = (start_y + end_y) / 2

                self.canvas.create_text(
                    midpoint_x,
                    midpoint_y,
                    text=connection.name,
                    fill="#a6adc8",
                    font=("Arial", 14)
                )

        # Draw thought bubbles
        for bubble in self.map.bubbles:

            w = bubble.width
            h = bubble.height

            # Highlight selected source
            if bubble is self.selected_bubble:
                outline = "#f9e2af"
                width = 5
            else:
                outline = "#89b4fa"
                width = 3

            # Draw Thought with center at bubble's X & Y position
            self.canvas.create_oval(
                bubble.xpos - w,
                bubble.ypos - h,
                bubble.xpos + w,
                bubble.ypos + h,
                fill=bubble.rgb,
                outline=outline,
                width=width
            )

            self.canvas.create_text(
                bubble.xpos,
                bubble.ypos,
                text=bubble.name,
                fill="#cdd6f4",
                font=("Arial", 11, "bold"),
                width=85
            )

    # ------------------------------
    # Element Removal
    # ------------------------------

    # Deletes the selected bubble. This bubble
    def delete_thought(self):
        self.map.remove_bubble(self.selected_bubble)
        self.selected_bubble = None
        self.reset_variables("")

    # ------------------------------
    # Utility Methods
    # ------------------------------

    # Reset variable values if you use a different function midway
    def reset_variables(self, mode):
        if (mode != "left_single"):
            ...
        if (mode != "left_double"):
            ...
        if (mode != "left_hold"):
            ...
        if(mode != "right_single"):
            self.thought_menu.place_forget()
        if (mode != "right_double"):
            ...
        if (mode != "right_hold"):
            ...
        self.draw_map()
        self.last_click = mode

    # Focus function should show all connections for the selected thought.
    # Other connections should be transparent
    def focus_thought(self):
        #stub
        return

    def cycle_layer(self):
        if self.map.current_layer >= len(self.map.layer_names) - 1:
            self.map.current_layer = 0
            self.draw_map()

        else: self.map.current_layer += 1

        self.draw_map()