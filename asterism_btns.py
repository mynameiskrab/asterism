import tkinter as tk
from tkinter import ttk


# noinspection unbound-local-variable
class AsterismBtns:

    def __init__(self, gui):

        self.gui = gui
        self.canvas = gui.canvas

        self.create_thought_menu()
        self.create_connection_menu()

        self.del_color = "#E3C5BF"

        # Setup style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # -- Standard Button Styling --#
        self.style.configure(
            "TButton",
            font = ("Arial", 10),
            relief = "flat",
            foreground = "#CDD6FE",
            background = "#1E1E2E",
            width = 10,
            padding = 2
        )
        self.style.map(
            'TButton',
            relief = [("pressed", "flat")],
            foreground = [("pressed", "#1E1E2E")],
            background = [("pressed", "#CDD6FE")],
        )

        self.style.configure(
            "ConMenu.TButton",
            width = 15
        )

        #-- Delete Button --#
        self.style.configure(
            "Delete.TButton",
            foreground = self.del_color,
            background = "#AB3318",
        )
        self.style.map(
            'Delete.TButton',
            foreground = [("pressed", "#F5F5F5")],
            background = [("pressed", "#FF4117")],
        )


    # ------------------------------
    # THOUGHT MENU
    # ------------------------------

    def create_thought_menu(self):

        self.thought_menu = tk.Frame(
            self.canvas,
            bg = "#313244",
            highlightbackground = "#CDD6FE",
            highlightcolor = "#CDD6FE",
            highlightthickness = 2,
            width = 0,      # Width simply needs to exist
        )
        self.thought_menu.place_forget()

        # Allows you to rename thought
        self.thought_name_slot = tk.Entry(
            self.thought_menu,
            width = 10,
            font = ("Arial", 10, "bold"),
            relief = "flat",
            justify = "center",
            fg = "#CDD6FE",
            bg = "#1E1E2E",
            insertbackground="#CDD6FE"
        )
        self.thought_name_slot.grid(row=0, column=0, ipadx = 3, ipady = 3,padx = 4, pady = 4, sticky="w")
        self.thought_name_slot.bind("<KeyRelease>", self.gui.update_name)

        # Focus on this thought, revealing all connections splayed out. stub
        focus_btn = ttk.Button(
            self.thought_menu,
            text = "Focus",
            command = self.gui.focus_thought
        )
        focus_btn.grid(row=0, column=1, padx = (0, 4), pady = 4, sticky="w")

        # Allows customization of thought color
        tho_color_btn = ttk.Button(
            self.thought_menu,
            text = "Recolor",
            #command = self.bubble_recolor
        )
        tho_color_btn.grid(row= 1, column= 0, padx = 4, pady = (0, 4), sticky="ew")

        # Deletes this thought, will add a confirmation prompt later
        tho_del_btn = ttk.Button(
            self.thought_menu,
            text = "Delete",
            command = self.gui.delete_thought,
            style = "Delete.TButton"
        )
        tho_del_btn.grid(row=1, column=1, padx = (0, 4), pady = (0, 4), sticky="ew")


        # Text box for a thoughts description/details
        self.description_text = tk.Text(self.thought_menu, width= 20, height=7, wrap="word", takefocus= False)
        self.description_text.grid(row= 2,column= 0, columnspan= 2, pady= (0, 4))

        # Bind key release to save text
        self.description_text.bind("<KeyRelease>", self.gui.update_desc)


    # ------------------------------
    # CONNECTION MENU
    # ------------------------------

    def create_connection_menu(self):

        self.connection_menu = tk.Frame(
            self.canvas,
            bg="#313244",
            highlightbackground="#CDD6FE",
            highlightcolor="#CDD6FE",
            highlightthickness=2,
            width=0,  # Width simply needs to exist
        )
        self.connection_menu.place_forget()

        self.connection_name_slot = tk.Entry(
            self.connection_menu,
            width=15,
            font=("Arial", 10, "bold"),
            relief="flat",
            justify="center",
            fg="#CDD6FE",
            bg="#1E1E2E",
            insertbackground = "#CDD6FE"
        )
        self.connection_name_slot.grid(row=0, column=0, ipadx=3, ipady=3, padx=4, pady=4, sticky="w")
        self.connection_name_slot.bind("<KeyRelease>", self.gui.update_name)

        # Allows customization of thought color
        color_btn = ttk.Button(
            self.connection_menu,
            text="Recolor",
            style = "ConMenu.TButton",
            #command = self.connection_recolor
        )
        color_btn.grid(row=1, column=0, padx=4, pady=(0, 4), sticky="w")

        # Deletes this connection, will add a confirmation prompt later
        con_del_btn = ttk.Button(
            self.connection_menu,
            text = "Delete",
            command = self.gui.delete_connection,
            style = "Delete.TButton",
            width=15
        )
        con_del_btn.grid(row=2, column=0, padx =4, pady =(0, 4), sticky="w")


        # Text box for a connections description/details
        self.con_description_text = tk.Text(self.connection_menu, width= 14, height=3, wrap="word", takefocus= False)
        self.con_description_text.grid(row= 3,column= 0, padx=3, pady= (0, 4), sticky="w")

        # Bind key release to save text
        self.con_description_text.bind("<KeyRelease>", self.gui.update_desc)

    # ------------------------------
    # MENU SHOW AND HIDE
    # ------------------------------
    
    def show_thought_menu(self, bubble):
        
        self.thought_menu.place(x = bubble.x + 65, y = bubble.y - 50)

        # Change name and description to match current bubble
        self.thought_name_slot.delete(0, tk.END)
        self.thought_name_slot.insert(0, bubble.name)

        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", bubble.description)

    def hide_thought_menu(self):

        self.thought_menu.place_forget()

    def show_connection_menu(self, connection):

        self.connection_menu.place(x = connection.x + 65, y = connection.y - 50)

        # Change name and description to match current connection
        self.connection_name_slot.delete(0, tk.END)
        self.connection_name_slot.insert(0, connection.name)

        self.con_description_text.delete("1.0", "end")
        self.con_description_text.insert("1.0", connection.description)

    def hide_connection_menu(self):

        self.connection_menu.place_forget()