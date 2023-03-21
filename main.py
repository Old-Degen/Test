import tkinter as tk
from tkinter import messagebox
from web3 import Web3
from gui import WalletGeneratorGUI
from modules.accounts import Accounts
from modules.rpc import RPC
from modules.settings import Settings
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

def main():
    root = tk.Tk()
    gui = WalletGeneratorGUI(root)
    accounts = Accounts(gui.frame1)
    rpc = RPC(gui.frame2)
    settings = Settings(gui.frame3)
    root.mainloop()

if __name__ == "__main__":
    main()
