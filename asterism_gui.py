import time
import math
import tkinter as tk
from tkinter import simpledialog, messagebox

from asterism import Asterism
from asterism_btns import AsterismBtns


class AsterismGUI:

    def __init__(self, root):

        # Window attributes
        self.root = root
        self.root.title("Asterism")
        self.root.geometry("1100x700")
        self.root.minsize(600,450)
        self.root.configure(bg="#1e1e2e")

        # Asterism Object
        self.map = Asterism()

        # Draw Loop variables
        self.running = True
        self.last_frame = 0
        self.frame_interval = 16        # 1000/interval = fps

        # Bubble and connection ID
        self.bubble_id = {}
        self.connection_id = {}

        # variables for temp line and placement ring
        self.connection_line = None
        self.placement_guide = {}

        # Selected bubble for various use applications
        self.selected_bubble = None
        self.selected_connection = None
        self.last_click = None
        
        # Mouse click variables
        self.left_click_timer = None
        self.left_hold_timer = None
        self.left_is_holding = False
        self.left_click_count = 0

        self.right_click_timer = None
        self.right_hold_timer = None
        self.right_is_holding = False
        self.right_click_count = 0


        # Mouse timings
        self.HOLD_DELAY = 250
        self.DOUBLE_DELAY = 200
        # Mouse coordinates
        self.mouse_x = 0
        self.mouse_y = 0

        self.color = "#CDD6FE"


        # ------------------------------
        # HEADER
        # ------------------------------

        header = tk.Frame(root, bg="#181825", height=65)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Concept Asterism",
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
        self.layer_title.pack(side="left", padx=250, pady=12)

        # ------------------------------
        # TOOLBAR
        # ------------------------------

        # ToolBar will be respecced to handle Menu/IO Options. Bubble creation should be
        # handled with mouse button presses.

        toolbar = tk.Frame(root, bg="#313244", height=50)
        toolbar.pack(fill="x")

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
            text="0,0",
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
        # MENUS
        # ------------------------------

        # Creates button layouts when modifying either a bubble or connection
        self.menus = AsterismBtns(self)

        # ------------------------------
        # Temporary canvas objects
        # ------------------------------

        self.connection_line = self.canvas.create_line(
            0,0,0,0,
            fill = "#5C5F72",
            width = 2,
            state = "hidden"
        )


        placement_ring = self.canvas.create_oval(
            0, 0, 0, 0,
            fill = "#799ED9",
            state = "hidden"
        )
        inner_bubble = self.canvas.create_oval(
            0, 0, 0, 0,
            fill = "#9DA4B0",
            outline = "#89B4FA",
            width = 3,
            state = "hidden"
        )

        self.placement_guide = {
            "pr": placement_ring,
            "inner": inner_bubble
        }



        # ------------------------------
        # Button Binds
        # ------------------------------

        # Mouse binds for single, double clicks, & hold for left clicks
        self.canvas.bind("<Button-1>", self.left_click_press)
        self.canvas.bind("<ButtonRelease-1>", self.left_click_release)
        self.canvas.bind("<B1-Motion>", self.on_left_hold)

        # Mouse binds for single, double clicks, & hold for right clicks
        self.canvas.bind("<Button-3>", self.right_click_press)
        self.canvas.bind("<ButtonRelease-3>", self.right_click_release)
        self.canvas.bind("<B3-Motion>", self.on_right_hold)

        # Binds mouse movements to check for mouse coordinates
        self.canvas.bind("<Motion>", self.on_mouse_move)


        # ------------------------------
        # TEST DATA
        # ------------------------------

        self.map.add_bubble("Hello", "#45475a", "wow", 200, 150, 48)
        self.map.add_bubble("World", "#45475a", "bop", 500, 150, 48)
        self.map.add_bubble("Goodbye", "#45475a", "sick", 350, 400, 48)

        self.map.add_connection(self.map.bubbles[0], self.map.bubbles[1], "Winner", "#1C5FC9", 0)
        self.map.add_connection(self.map.bubbles[0], self.map.bubbles[2], "Tied", "#733572", 0)
        self.map.add_connection(self.map.bubbles[1], self.map.bubbles[2], "Lost", "#387A31", 0)
        self.map.add_connection(self.map.bubbles[0], self.map.bubbles[2], "Undecided", "#9C845C", 1)

        self.map.connections[0].x = 300
        self.map.connections[0].y = 200

        self.map.add_layer("Tester")

        self.start_cycle()
        
    # ------------------------------
    # HANDLE CANVAS CLICK
    # ------------------------------

    # Checks coordinates of mouse
    def on_mouse_move(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.coordinates.config(
            text=f"{self.mouse_x}, {self.mouse_y}"
        )


    # ------------------------------
    # Left Click Checker
    # ------------------------------
    
    # Left click hold checker - determines click type (single, double, hold)
    def left_click_press(self, event):
        # Reset variables
        self.left_is_holding = False
        if self.left_click_timer:
            event.widget.after_cancel(self.left_click_timer)
            self.left_click_timer = None
        
        # Start a timer
        self.left_hold_timer = self.root.after(self.HOLD_DELAY, lambda: self.set_left_holding(event, True))

    # Set left_is_holding to True, allowing left click motions
    def set_left_holding(self, event, hold):
        self.status.config(
            text="Hold left click"
        )
        self.reset_variables("left_hold")

        clicked = self.find_bubble_at(event.x, event.y, 48, True)
        if clicked:
            self.selected_bubble = clicked
            self.left_is_holding = hold


    # Left click single double checker - if hold method wasn't called,
    # call single or double method
    def left_click_release(self, event):
        # Reset hold timer
        if self.left_hold_timer:
            self.root.after_cancel(self.left_hold_timer)
            self.left_hold_timer = None

        # If hold was called: place bubble, then return
        if self.left_is_holding:

            # Check drop location
            clicked = self.find_bubble_at(event.x, event.y, 192, False)

            # Set bubble location if drop location is not too close to another bubble
            # Change status if drop fails
            if clicked is None or clicked is self.selected_bubble:
                self.selected_bubble.x = event.x
                self.selected_bubble.y = event.y

                # Reset the midpoint of all connections linked to this thought
                for connection in self.map.connections:
                    if connection.node_one == self.selected_bubble or connection.node_two == self.selected_bubble:
                        connection.reset_midpoint()

                self.status.config(
                    text=f"Movement of {self.selected_bubble.name} completed."
                )
            else:
                self.status.config(
                    text=f"Movement of {self.selected_bubble.name} canceled: too close to {clicked.name}."
                )
            # Reset Variables
            self.selected_bubble = None
            self.left_click_count = 0
            self.left_is_holding = False

            return

        self.left_click_count += 1
        if self.left_click_count == 1:
            self.left_click_timer = self.root.after(self.DOUBLE_DELAY, lambda: self.on_left_click(event))
        elif self.left_click_count > 1:
            self.on_double_left_click(event)


    # ------------------------------
    # Left Click Functions
    # ------------------------------

    # Single left click function call
    # Allows for connection making.
    def on_left_click(self, event):

        self.left_click_count = 0        # reset click counter

        # Resets all values if last click was not a left single click
        if self.last_click != "left_single":
            self.selected_bubble = None
            self.reset_variables("left_single")

        # Check for thought bubble
        clicked = self.find_bubble_at(event.x, event.y, 48, True)

        if clicked is None:
            self.reset_variables("left_single")
            return

        # First click: select source
        if self.selected_bubble is None:
            self.selected_bubble = clicked

            self.status.config(
                text=f"Source: {clicked.name}. "
                     "Now select the DESTINATION thought."
            )

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

            self.reset_variables("")
            return

        # Ask user to name connection
        connection_name = simpledialog.askstring(
            "Name Connection",
            f"How is '{source.name}' related "
            f"to '{destination.name}'?"
        )

        # Check if entered name is empty
        if not connection_name or not connection_name.strip():
            self.reset_variables("")
            return

        # Create connection
        self.map.add_connection(
            source,
            destination,
            connection_name.strip().capitalize(),
            "#A6ADC8",
            self.map.current_layer)

        # Change status message
        self.status.config(
            text=f"Created: {source.name} → "
                 f"{destination.name}"
        )

        self.selected_bubble = None

    # Double left click function call
    # Create bubble at that location. Will cancel if too close to another thought.
    def on_double_left_click(self, event):

        self.left_click_count = 0  # reset click counter

        self.status.config(
            text="Double left click"
        )
        self.reset_variables("left_double")


        # Check if spot is empty -> not too near other bubbles
        clicked = self.find_bubble_at(event.x, event.y, 192, True)
        if clicked:
            self.status.config(
                text=f"Could not create thought: Too close to {clicked.name}."
            )
            return

        # Prompt bubble name
        name = simpledialog.askstring(
            "New Thought",
            "Name your new thought:"
        )

        if not name or not name.strip():
            return

        # Draw bubble
        self.map.add_bubble(name.capitalize(), "#45475A", "Base Thought", event.x, event.y, 48)

        return

    # Left click & hold function call
    # Uses its own button bind. Allows moving thoughts.
    def on_left_hold(self, event):

        self.mouse_x = event.x
        self.mouse_y = event.y
        self.coordinates.config(
            text=f"{self.mouse_x}, {self.mouse_y}"
        )

        return


    # ------------------------------
    # Right Click Checker
    # ------------------------------

    # Right click hold checker - determines click type (single, double, hold)
    def right_click_press(self, event):
        # Reset variables
        self.right_is_holding = False
        if self.right_click_timer:
            event.widget.after_cancel(self.right_click_timer)
            self.right_click_timer = None

        # Start a timer
        self.right_hold_timer = self.root.after(self.HOLD_DELAY, lambda: self.set_right_holding(event, True))

    # Set right_is_holding to True, allowing right click motions
    def set_right_holding(self, event, hold):
        self.status.config(
            text="Hold right click"
        )
        self.reset_variables("right_hold")

        clicked = self.find_bubble_at(event.x, event.y, 48, True)
        if clicked:
            self.selected_bubble = clicked
            self.right_is_holding = hold

    # Right click single double checker - if hold method wasn't called,
    # call single or double method
    def right_click_release(self, event):
        # Reset hold timer
        if self.right_hold_timer:
            self.root.after_cancel(self.right_hold_timer)
            self.right_hold_timer = None

        # If hold was called, return
        if self.right_is_holding:
            self.right_click_count = 0
            return

        # Count the amount of click releases within a small time period,
        # then call single/double clicks
        self.right_click_count += 1
        if self.right_click_count == 1:
            self.right_click_timer = self.root.after(self.DOUBLE_DELAY, lambda: self.on_right_click(event))
        elif self.right_click_count > 1:
            self.on_double_right_click(event)


    # ------------------------------
    # Right Click Functions
    # ------------------------------

    # Single right click function call
    # When you click on a thought, pull up thought menu*            *incomplete
    def on_right_click(self, event):

        self.right_click_count = 0  # reset click counter

        self.status.config(
            text="Single right click"
        )

        self.reset_variables("right_single")

        # Check for thought bubble
        clicked = self.find_bubble_at(event.x, event.y, 48, True)
        if clicked is None:
            return

        self.selected_bubble = clicked

        # Open thought menu near thought
        self.menus.show_thought_menu(clicked)

    # Double right click function call
    # Brings up the menu for the selected connection
    def on_double_right_click(self, event):

        self.right_click_count = 0  # reset click counter

        self.status.config(
            text="Double right click"
        )

        self.reset_variables("right_double")

        # Check for connection
        clicked = self.find_connection_at(event.x, event.y)
        if clicked is None:
            return

        self.selected_connection = clicked

        self.menus.show_connection_menu(clicked)

        return

    # Right click & hold function call
    #
    def on_right_hold(self, event):

        # Reset click count, left_is_holding is set to true to prevent single/double click calls
        self.right_is_holding = True
        self.right_click_count = 0

        self.status.config(
            text="Hold right click"
        )
        return

    # ------------------------------
    # FIND BUBBLE OR CONNECTION UNDER MOUSE
    # ------------------------------

    # Find the bubble nearest the mouse within a given radius
    #
    def find_bubble_at(self, x, y, radius, check_self):

        # Radius standard is 48, though it may be increased if you want to avoid being too close
        greatest_distance = radius + 1
        closest_bubble = None

        # Will allow checking your own node
        if check_self:
            for bubble in reversed(self.map.bubbles):

                # Get distance
                distance = math.hypot(
                    x - bubble.x, y - bubble.y
                )

                # Find the shortest distance within the radius
                if distance <= radius and distance < greatest_distance:
                    greatest_distance = distance
                    closest_bubble = bubble

        # Will only check other non-selected thoughts
        else:
            for bubble in reversed(self.map.bubbles):

                if bubble is not self.selected_bubble:
                    # Get distance
                    distance = math.hypot(
                        x - bubble.x, y - bubble.y
                    )

                    # Find the shortest distance within the radius
                    if distance <= radius and distance < greatest_distance:
                        greatest_distance = distance
                        closest_bubble = bubble

        return closest_bubble

    def find_connection_at(self, x, y):

        greatest_distance = 41
        closest_connection = None

        for connection in reversed(self.map.connections):
            distance = math.hypot(
                x - connection.x, y - connection.y
            )

            # Find the shortest distance within the radius
            if distance <= 40 and distance < greatest_distance and connection.layer == self.map.current_layer:
                greatest_distance = distance
                closest_connection = connection

        return closest_connection

    # ------------------------------
    # Element Removal
    # ------------------------------

    # Deletes the selected bubble.
    def delete_thought(self):
        # Check for selected bubble
        if self.selected_bubble is None:
            return

        # Delete bubble ids
        ids = self.bubble_id.pop(self.selected_bubble)
        self.canvas.delete(ids["oval"])
        self.canvas.delete(ids["text"])

        # Delete bubble from map, reset variables
        for connection in reversed(self.map.connections):
            if connection.node_one == self.selected_bubble or connection.node_two == self.selected_bubble:
                ids = self.connection_id.pop(connection)
                self.canvas.delete(ids["line"])
                self.canvas.delete(ids["text"])

        self.map.remove_bubble(self.selected_bubble)
        self.reset_variables("")

    # Deletes the selected connection
    def delete_connection(self):

        if self.selected_connection is None:
            return

        # Delete connection ids
        ids = self.connection_id.pop(self.selected_connection)
        self.canvas.delete(ids["line"])
        self.canvas.delete(ids["text"])

        self.map.remove_connection(self.selected_connection)
        self.reset_variables("")

    # ------------------------------
    # Utility Methods
    # ------------------------------

    # Change description of a given thought on keystroke
    def update_desc(self, event):
        if self.selected_bubble:
            self.selected_bubble.description = self.menus.description_text.get("1.0", "end-1c")
        elif self.selected_connection:
            self.selected_connection.description = self.menus.con_description_text.get("1.0", "end-1c")

    # Change the selected thought name on keystroke
    def update_name(self, event):
        if self.selected_bubble:
            self.selected_bubble.name = self.menus.thought_name_slot.get().capitalize()
        elif self.selected_connection:
            self.selected_connection.name = self.menus.connection_name_slot.get().capitalize()

    # Reset variable values if you use a different function midway
    # This function needs a bit of a rework. Don't mind it yet.
    def reset_variables(self, mode: str):
        if mode != "left_hold":
            self.selected_bubble = None
        if mode != "right_hold":
            self.selected_connection = None
        self.menus.hide_thought_menu()
        self.menus.hide_connection_menu()
        self.last_click = mode

    #def connection_recolor

    # Focus function should show all connections for the selected thought.
    # Other connections should be transparent
    def focus_thought(self):
        #stub
        return

    def cycle_layer(self):
        if self.map.current_layer >= len(self.map.layer_names) - 1:
            self.map.current_layer = 0

        else: self.map.current_layer += 1

    # ------------------------------
    # DRAW FUNCTIONS
    # ------------------------------

    def draw_map(self):

        # Set layer name to current layer
        self.layer_title.config(
            text=self.map.layer_names[self.map.current_layer]
        )

        #self.canvas.delete("all")

        # Draw thought connection line
        if self.last_click == "left_single" and self.selected_bubble:
            # Update temp line
            self.canvas.coords(
                self.connection_line,
                self.selected_bubble.x,
                self.selected_bubble.y,
                self.mouse_x,
                self.mouse_y
            )

            self.canvas.itemconfigure(
                self.connection_line,
                state="normal"
            )
        else:
            self.canvas.itemconfigure(
                self.connection_line,
                state="hidden"
            )

        ids = self.placement_guide

        # Draw bubble placement and minimum distance ring
        if self.left_is_holding:

            # Placement Ring - How close a bubble can be placed to another
            self.canvas.coords(
                ids["pr"],
                self.mouse_x - 144, self.mouse_y - 144,
                self.mouse_x + 144, self.mouse_y + 144
            )
            self.canvas.itemconfigure(
                ids["pr"],
                state="normal"
            )

            self.canvas.coords(
                ids["inner"],
                self.mouse_x - 48, self.mouse_y - 48,
                self.mouse_x + 48, self.mouse_y + 48
            )
            self.canvas.itemconfigure(
                ids["inner"],
                state="normal"
            )
        else:
            self.canvas.itemconfigure(
                ids["pr"],
                state="hidden"
            )
            self.canvas.itemconfigure(
                ids["inner"],
                state="hidden"
            )


        # Draw connections first.
        for connection in self.map.connections:
            # Filter out connections not in this layer.
            if connection.layer == self.map.current_layer:
                # If connection does not have a set of IDs, create them
                if connection not in self.connection_id:
                    self.create_connection(connection)

                # Update connection IDs, then use them
                self.update_connection(connection)
                ids = self.connection_id[connection]

                # Reveal connections in current layer
                self.canvas.itemconfigure(ids["line"], state = "normal")
                self.canvas.itemconfigure(ids["text"], state = "normal")

            elif connection in self.connection_id:

                ids = self.connection_id[connection]

                # Hide connections outside of current layer
                self.canvas.itemconfigure(ids["line"], state="hidden")
                self.canvas.itemconfigure(ids["text"], state="hidden")

        for bubble in self.map.bubbles:

            if bubble not in self.bubble_id:
                self.create_bubble(bubble)

            self.update_bubble(bubble)



    # Adds rendered objects for new bubble
    def create_bubble(self, bubble):

        # Create oval object
        oval = self.canvas.create_oval(
            bubble.x - bubble.radius,
            bubble.y - bubble.radius,
            bubble.x - bubble.radius,
            bubble.y - bubble.radius,
            fill = bubble.rgb,
            outline = "#89B4FA",
            width = 3
        )

        # Create text object
        text = self.canvas.create_text(
            bubble.x,
            bubble.y,
            text = bubble.name,
            fill = "#CDD6F4",
            font = ("Arial", 11, "bold"),
            width = 85
        )

        # Set bubble ids
        self.bubble_id[bubble] = {
            "oval": oval,
            "text": text
        }

    # Update existing bubble rendering object
    def update_bubble(self, bubble):

        ids = self.bubble_id[bubble]

        # Update oval position
        self.canvas.coords(
            ids["oval"],
            bubble.x - bubble.radius,
            bubble.y - bubble.radius,
            bubble.x + bubble.radius,
            bubble.y + bubble.radius,
        )

        # Update text position
        self.canvas.coords(
            ids["text"],
            bubble.x,
            bubble.y
        )

        # Change outline if selected
        if bubble is self.selected_bubble:
            outline = "#F9E2AF"
            width = 5
        else:
            outline = "#89B4FA"
            width = 3

        # Update oval color
        self.canvas.itemconfigure(
            ids["oval"],
            fill = bubble.rgb,
            outline = outline,
            width = width
        )

        # Update text
        self.canvas.itemconfigure(
            ids["text"],
            text = bubble.name
        )

    # Adds rendered objects for new connection
    def create_connection(self, connection):

        x1 = connection.node_one.x
        y1 = connection.node_one.y
        x2 = connection.node_two.x
        y2 = connection.node_two.y

        # Get the midpoints
        midpoint_x = int((x1 + x2) / 2)
        midpoint_y = int((y1 + y2) / 2)

        points = [x1, y1, midpoint_x, midpoint_y, x2, y2]
        # Create line object
        line = self.canvas.create_line(
            points,
            fill = connection.rgb,
            width = 2,
            arrow = tk.LAST,
            splinesteps= 60,
            smooth = True,
        )



        # Create text object at midpoints
        text = self.canvas.create_text(
            midpoint_x,
            midpoint_y,
            text = connection.name,
            fill = "#A6ADC8",
            font = ("Arial", 11, "bold"),
        )

        self.connection_id[connection] = {
            "line": line,
            "text": text
        }

    # Changes connections based on coordinates of the original in the map
    def update_connection(self, connection):

        ids = self.connection_id[connection]

        # Gather x-y coords of each node.
        # adding midpoints 1 and 3 makes the curve less smooth so the names stay close to the line.
        x1 = connection.node_one.x
        y1 = connection.node_one.y
        mid_x1 = (connection.x + connection.x + connection.node_one.x) / 3
        mid_y1 = (connection.y + connection.y + connection.node_one.y) / 3
        mid_x2 = connection.x
        mid_y2 = connection.y
        mid_x3 = (connection.x + connection.x + connection.node_two.x) / 3
        mid_y3 = (connection.y + connection.y + connection.node_two.y) / 3
        x2 = connection.node_two.x
        y2 = connection.node_two.y

        # Update line position
        self.canvas.coords(
            ids["line"],
            x1, y1, mid_x1, mid_y1, mid_x2, mid_y2, mid_x3, mid_y3, x2, y2
        )

        # Update text position
        self.canvas.coords(
            ids["text"],
            mid_x2,
            mid_y2
        )

        # Update line
        self.canvas.itemconfigure(
            ids["line"],
            fill = connection.rgb
        )

        # Update text
        self.canvas.itemconfigure(
            ids["text"],
            text = connection.name
        )

        # This prevents it from laying on top of thoughts
        self.canvas.tag_lower(ids["line"])

    # ------------------------------
    # DRAW CYCLE FUNCTIONS
    # ------------------------------

    # Starts animation cycle
    def start_cycle(self):
        self.last_frame = time.perf_counter()
        self.draw_cycle()

    # Starts an animation cycle currently 60 fps
    def draw_cycle(self):
        if not self.running:
            return

        current_time = time.perf_counter()

        dt = current_time - self.last_frame
        self.last_frame = current_time

        #self.update(dt)
        self.update_cycle(dt)

        # Draws canvas
        self.draw_map()
        self.root.after(self.frame_interval, self.draw_cycle)

    # Updates objects for animation logic
    def update_cycle(self, dt):
        pass
