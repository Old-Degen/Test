import tkinter as tk
from gui import WalletGeneratorGUI

class Tasks:
    def __init__(self, master):
        self.master = master

        # Создание виджетов
        self.title_label = tk.Label(master, text="Tasks", font=("Arial", 16, "bold"))
        self.gui_button = tk.Button(master, text="Launch GUI", command=self.launch_gui)

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)
        self.gui_button.pack()

    def launch_gui(self):
        root = tk.Tk()
        gui = WalletGeneratorGUI(root)
        root.mainloop()
