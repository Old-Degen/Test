import tkinter as tk
from tkinter import ttk

from modules.accounts import Accounts
from modules.settings import Settings
from modules.rpc import RPC

class WalletGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Polygon Wallet Generator")

        # Определение размеров окна
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = int(screen_width * 3 / 4)
        window_height = int(screen_height * 3 / 4)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Создание виджетов
        self.left_frame = tk.Frame(master, bg="#f8f8f8")
        self.right_frame = tk.Frame(master)

        # Создание модулей
        self.tasks = Tasks(self.left_frame)
        self.accounts = Accounts(self.left_frame)
        self.settings = Settings(self.left_frame)
        self.rpc = RPC(self.left_frame)

        # Размещение виджетов на экране
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Визуальное отделение левой и правой колонок
        separator = ttk.Separator(self.master, orient="vertical")
        separator.place(relx=0.2, rely=0, relheight=1)
        label = tk.Label(self.master, text="Polygon Wallet Generator", font=("Arial", 16, "bold"))
        label.place(relx=0.25, rely=0.02)


if __name__ == "__main__":
    root = tk.Tk()
    gui = WalletGeneratorGUI(root)
    root.mainloop()
