from tkinter import Tk
from gui import App
from modules.wallet_manager import WalletManager

if __name__ == "__main__":
    root = Tk()
    root.title("NFT Wallet Manager")
    wallet_manager = WalletManager()
    app = App(root, wallet_manager)
    root.mainloop()
