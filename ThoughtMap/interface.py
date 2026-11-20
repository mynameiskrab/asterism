
import tkinter as tk
from tkinter import simpledialog, messagebox
import math

from thought import Thought


class ThoughtMapGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("ThoughtMap")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1e1e2e")

        self.bubbles = []

        # Connection creation state
        self.connect_mode = False
        self.selected_bubble = None

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

        # ------------------------------
        # TOOLBAR
        # ------------------------------

        toolbar = tk.Frame(root, bg="#313244", height=50)
        toolbar.pack(fill="x")

        tk.Button(
            toolbar,
            text="+ Add Thought",
            command=self.add_bubble
        ).pack(side="left", padx=10, pady=8)

        tk.Button(
            toolbar,
            text="Connect Thoughts",
            command=self.start_connection
        ).pack(side="left", padx=5, pady=8)

        tk.Button(
            toolbar,
            text="Display Map",
            command=self.draw_map
        ).pack(side="left", padx=5, pady=8)

        # ------------------------------
        # STATUS BAR
        # ------------------------------

        self.status = tk.Label(
            root,
            text="Ready",
            bg="#313244",
            fg="#cdd6f4",
            anchor="w",
            padx=12
        )
        self.status.pack(fill="x", side="bottom")

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

        # Listen for mouse clicks
        self.canvas.bind(
            "<Button-1>",
            self.on_canvas_click
        )

        # ------------------------------
        # TEST DATA
        # ------------------------------

        x = Thought("Hello", 200, 150)
        y = Thought("World", 500, 150)
        z = Thought("Goodbye", 350, 400)

        x.addLink("winner", y)
        x.addLink("tied", z)
        y.addLink("lost", z)
        z.addLink("loser", x)

        self.bubbles = [x, y, z]

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

        index = len(self.bubbles)

        x = 150 + (index % 4) * 200
        y = 150 + (index // 4) * 150

        new_bubble = Thought(name.strip(), x, y)

        self.bubbles.append(new_bubble)

        self.draw_map()

    # ------------------------------
    # START CONNECTION MODE
    # ------------------------------

    def start_connection(self):

        self.connect_mode = True
        self.selected_bubble = None

        self.status.config(
            text="Select the SOURCE thought."
        )

        self.draw_map()

    # ------------------------------
    # FIND BUBBLE UNDER MOUSE
    # ------------------------------

    def find_bubble_at(self, x, y):

        radius = 48

        for bubble in reversed(self.bubbles):

            distance = math.hypot(
                x - bubble.x,
                y - bubble.y
            )

            if distance <= radius:
                return bubble

        return None

    # ------------------------------
    # HANDLE CANVAS CLICK
    # ------------------------------

    def on_canvas_click(self, event):

        if not self.connect_mode:
            return

        clicked = self.find_bubble_at(
            event.x,
            event.y
        )

        if clicked is None:
            return

        # First click: select source
        if self.selected_bubble is None:
            self.selected_bubble = clicked

            self.status.config(
                text=f"Source: {clicked.thoughtName}. "
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
        link_name = simpledialog.askstring(
            "Name Connection",
            f"How is '{source.thoughtName}' related "
            f"to '{destination.thoughtName}'?"
        )

        if not link_name or not link_name.strip():
            self.cancel_connection()
            return

        # Create connection
        source.addLink(
            link_name.strip(),
            destination
        )

        self.cancel_connection()

        self.status.config(
            text=f"Created: {source.thoughtName} → "
                 f"{destination.thoughtName}"
        )

        self.draw_map()

    # ------------------------------
    # CANCEL CONNECTION MODE
    # ------------------------------

    def cancel_connection(self):

        self.connect_mode = False
        self.selected_bubble = None

        self.draw_map()

    # ------------------------------
    # DRAW MAP
    # ------------------------------

    def draw_map(self):

        self.canvas.delete("all")

        # Draw connections first
        for bubble in self.bubbles:

            for link_name, target in bubble.Links:

                self.canvas.create_line(
                    bubble.x,
                    bubble.y,
                    target.x,
                    target.y,
                    fill="#89b4fa",
                    width=2,
                    arrow=tk.LAST
                )

                midpoint_x = (bubble.x + target.x) / 2
                midpoint_y = (bubble.y + target.y) / 2

                self.canvas.create_text(
                    midpoint_x,
                    midpoint_y - 12,
                    text=link_name,
                    fill="#a6adc8",
                    font=("Arial", 10)
                )

        # Draw thought bubbles
        for bubble in self.bubbles:

            radius = 48

            # Highlight selected source
            if bubble is self.selected_bubble:
                outline = "#f9e2af"
                width = 5
            else:
                outline = "#89b4fa"
                width = 3

            self.canvas.create_oval(
                bubble.x - radius,
                bubble.y - radius,
                bubble.x + radius,
                bubble.y + radius,
                fill="#45475a",
                outline=outline,
                width=width
            )

            self.canvas.create_text(
                bubble.x,
                bubble.y,
                text=bubble.thoughtName,
                fill="#cdd6f4",
                font=("Arial", 11, "bold"),
                width=85
            )
