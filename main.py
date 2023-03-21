import tkinter as tk
from tkinter import messagebox
from web3 import Web3
from gui import WalletGeneratorGUI
from csv_helper import add_to_csv
dirname = os.path.dirname(__file__)
csv_path = os.path.join(dirname, 'private', 'wallets.csv')
csv_helper_path = os.path.join(dirname, 'csv_helper.py')

def main():
    root = tk.Tk()
    gui = WalletGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
