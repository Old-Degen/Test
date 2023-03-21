from tkinter import *
from gui import WalletGeneratorGUI


if __name__ == "__main__":
    root = Tk()
    root.title("Wallet Generator")

    app = WalletGeneratorGUI(root)
    app.main()

    root.mainloop()
