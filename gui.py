import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.title("My NFT Wallet")

        # Set the window size
        self.geometry("800x600")

        # Create a frame to hold the modules
        self.module_frame = tk.Frame(self)
        self.module_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame to hold the content
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the modules
        self.create_modules()

    def create_modules(self):
        # Create the modules
        pass

class Module(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)

        # Set the module title
        self.title = tk.Label(self, text=title, font=("Arial", 16, "bold"))
        self.title.pack(pady=10)

        # Create the content frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def show(self):
        # Show the module
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        # Hide the module
        self.pack_forget()

    def on_show(self):
        # Called when the module is shown
        pass

    def on_hide(self):
        # Called when the module is hidden
        pass

class ButtonBar(tk.Frame):
    def __init__(self, parent, buttons):
        super().__init__(parent)

        # Create the buttons
        for text, command in buttons:
            button = tk.Button(self, text=text, command=command)
            button.pack(side=tk.LEFT, padx=10, pady=10)

    def add_button(self, text, command):
        # Add a new button
        button = tk.Button(self, text=text, command=command)
        button.pack(side=tk.LEFT, padx=10, pady=10)
