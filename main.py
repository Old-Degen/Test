from tkinter import Tk
from gui import App

if __name__ == "__main__":
    root = Tk()
    root.title("NFT Wallet Manager")
    app = App(root)
    root.mainloop()
