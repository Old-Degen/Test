import tkinter as tk
from tkinter import ttk
from modules.wallet_manager import WalletManager


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the window title
        self.title("NFT Wallet Manager")

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
        # Create the wallet module
        self.wallet_module = WalletModule(self.module_frame, "My Wallets")
        self.wallet_module.show()

        # Create the settings module
        self.settings_module = SettingsModule(self.module_frame, "Settings")
        self.settings_module.hide()

        # Create the about module
        self.about_module = AboutModule(self.module_frame, "About")
        self.about_module.hide()

        # Create the content
        self.create_content()

    def create_content(self):
        # Create the wallet manager
        self.wallet_manager = WalletManager(self.content_frame)

        # Add the wallet manager to the content frame
        self.wallet_manager.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_module(self, module):
        # Show a module
        pass

    def hide_module(self, module):
        # Hide a module
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

class WalletModule(Module):
    def __init__(self, parent, title):
        super().__init__(parent, title)

        # Create the add wallet button
        self.add_wallet_button = tk.Button(self.content_frame, text="Add Wallet")
        self.add_wallet_button.pack(pady=10)

        # Create the wallet list
        self.wallet_list = tk.Listbox(self.content_frame)
        self.wallet_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add the wallets to the list
        self.add_wallets_to_list()

    def add_wallets_to_list(self):
        # Add the wallets to the list
        pass

    def on_show(self):
        # Called when the module is shown
        pass

    def on_hide(self):
        # Called when the module is hidden
        pass

class Settings(Module):
    def __init__(self, parent, title):
        super().__init__(parent, title)

    def create_widgets(self):
        # Create a label for the blockchain selection
        blockchain_label = tk.Label(self.content_frame, text="Select a blockchain:")
        blockchain_label.pack(pady=10)

        # Create a dropdown list for the blockchain selection
        self.blockchain_var = tk.StringVar(self)
        blockchain_choices = ["Ethereum", "Binance Smart Chain"]
        self.blockchain_var.set(blockchain_choices[0])
        blockchain_dropdown = tk.OptionMenu(self.content_frame, self.blockchain_var, *blockchain_choices)
        blockchain_dropdown.pack()

        # Create a label for the network selection
        network_label = tk.Label(self.content_frame, text="Select a network:")
        network_label.pack(pady=10)

        # Create a dropdown list for the network selection
        self.network_var = tk.StringVar(self)
        network_choices = ["Mainnet", "Testnet"]
        self.network_var.set(network_choices[0])
        network_dropdown = tk.OptionMenu(self.content_frame, self.network_var, *network_choices)
        network_dropdown.pack()

        # Create a button to save the settings
        save_button = tk.Button(self.content_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        # Get the selected blockchain and network
        blockchain = self.blockchain_var.get()
        network = self.network_var.get()

        # Save the settings to a file
        settings = {"blockchain": blockchain, "network": network}
        with open("settings.json", "w") as f:
            json.dump(settings, f)
