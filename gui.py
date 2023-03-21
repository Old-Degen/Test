import tkinter as tk
from tkinter import ttk
from web3 import Web3
import csv
import os.path

class Tasks:
    def __init__(self, master):
        self.master = master

        # Создание виджетов
        self.title_label = tk.Label(master, text="Tasks", font=("Arial", 16, "bold"))

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)

class Accounts:
    def __init__(self, master):
        self.master = master

        # Создание виджетов
        self.title_label = tk.Label(master, text="Accounts", font=("Arial", 16, "bold"))

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)

class Settings:
    def __init__(self, master):
        self.master = master

        # Создание виджетов
        self.title_label = tk.Label(master, text="Settings", font=("Arial", 16, "bold"))

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)

class PolyWalletGenerator:
    def __init__(self, master):
        self.master = master

        # Создание виджетов
        self.title_label = tk.Label(master, text="Poly Wallet Generator", font=("Arial", 16, "bold"))

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)

    def run(self):
        self.master.mainloop()


class PolyTokenManager:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(master, text="PolyTokenManager")
        self.label.pack()


class RPC:
    def __init__(self, master):
        self.master = master

        # Создание виджетов
        self.title_label = tk.Label(master, text="RPC", font=("Arial", 16, "bold"))

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)

class WalletManager:
    def __init__(self, master):
        self.master = master

        # Создание виджетов
        self.title_label = tk.Label(master, text="Wallet Manager", font=("Arial", 16, "bold"))
        self.wallets_button = tk.Button(master, text="Poly Wallet Generator", font=("Arial", 12), command=self.poly_wallet_generator)
        self.tokens_button = tk.Button(master, text="Poly Token Manager", font=("Arial", 12), command=self.poly_token_manager)

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)
        self.wallets_button.pack(pady=10)
        self.tokens_button.pack(pady=10)

    class PolyWalletGenerator:
        def __init__(self, master):
            self.master = master
            self.label = tk.Label(master, text="PolyWalletGenerator")
            self.label.pack()

    def poly_token_manager(self):
        # Создание виджетов
        self.title_label = tk.Label(self.master, text="Poly Token Manager", font=("Arial", 16, "bold"))

        # Размещение виджетов на экране
        self.title_label.pack(pady=20)

