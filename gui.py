from tkinter import *
from tkinter import ttk
from modules.task_manager import TaskManager
from modules.utils import Utils
from modules.wallet_manager import WalletManager
from modules import settings




class WalletGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wallet Generator")

        # Initialize task manager
        self.task_manager = TaskManager()

        # Initialize wallet manager
        self.wallet_manager = WalletManager()

        # Initialize GUI components
        self.chain_var = tk.StringVar(value="Polygon")
        self.group_var = tk.StringVar(value="Mainnet")
        self.wallet_var = tk.StringVar(value="")
        self.wallets = self.wallet_manager.get_wallets(self.chain_var.get(), self.group_var.get())
        self.wallet_options = [wallet["name"] for wallet in self.wallets]

        self.chain_label = tk.Label(master, text="Chain:")
        self.chain_label.pack()

        self.chain_menu = tk.OptionMenu(master, self.chain_var, *self.wallet_manager.get_chains())
        self.chain_menu.pack()

        self.group_label = tk.Label(master, text="Group:")
        self.group_label.pack()

        self.group_menu = tk.OptionMenu(master, self.group_var, *self.wallet_manager.get_groups(self.chain_var.get()))
        self.group_menu.pack()

        self.wallet_label = tk.Label(master, text="Select main wallet:")
        self.wallet_label.pack()

        self.wallet_menu = tk.OptionMenu(master, self.wallet_var, *self.wallet_options)
        self.wallet_menu.pack()

        self.generate_button = tk.Button(master, text="Generate", command=self.generate_wallet)
        self.generate_button.pack()

        self.output_label = tk.Label(master, text="")
        self.output_label.pack()

    def create_widgets(self):
        # Creating input field
        self.input_field = ttk.Entry(
            self.main_frame, width=30, textvariable=self.private_key
        )
        self.input_field.grid(column=1, row=1, sticky=(W, E))

        # Creating the generate button
        self.generate_button = ttk.Button(
            self.main_frame, text="Generate", command=self.generate_wallet
        )
        self.generate_button.grid(column=3, row=1, sticky=W)

        # Creating the labels
        ttk.Label(self.main_frame, text="Private Key:").grid(column=0, row=1, sticky=W)
        ttk.Label(self.main_frame, text="Public Key:").grid(column=0, row=2, sticky=W)

        # Creating the output field
        self.output_field = ttk.Entry(
            self.main_frame, width=30, textvariable=self.public_key, state="readonly"
        )
        self.output_field.grid(column=1, row=2, sticky=(W, E))

        # Add progress bar
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=200, mode="indeterminate")
        self.progress.grid(column=2, row=1, sticky=E)

    def generate_wallet(self):
        # Get the selected wallet
        selected_wallet = self.wallet_listbox.curselection()
        if not selected_wallet:
            messagebox.showerror("Error", "Please select a wallet!")
            return
        selected_wallet = selected_wallet[0]

        # Get the wallets from CSV file
        wallets = []
        with open(settings.WALLET_CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                wallets.append(row)

        # Get the main wallet for Polygon
        main_wallet = None
        for wallet in wallets:
            if wallet["Chain"] == "Polygon" and wallet["Group"] == "Main":
                main_wallet = wallet
                break

        # If main wallet not found, ask the user to select one
        if not main_wallet:
            messagebox.showinfo(
                "Info",
                "No main wallet found for Polygon. Please select one.",
            )
            self.master.destroy()
            main_wallet_gui = Tk()
            WalletManagerGUI(main_wallet_gui)
            return

        # Get the selected wallet
        selected_wallet = wallets[selected_wallet]

        # Set the RPC URI and provider URI
        chain = selected_wallet["Chain"]
        group = selected_wallet["Group"]
        network = settings.NETWORKS.get(chain)
        if network:
            rpc_uri = network.get("rpc_uri")
            provider_uri = network.get("provider_uri")
        else:
            messagebox.showerror("Error", f"No settings for chain {chain}!")
            return

        # Create a wallet manager
        self.wallet_manager = WalletManager(rpc_uri, settings.WALLET_CSV_FILE, provider_uri=provider_uri)

        # Set the account and address
        address = selected_wallet["Address"]
        private_key = selected_wallet["Private Key"]
        account = self.wallet_manager.get_account(private_key)
        self.wallet_manager.set_account(account)

        # Set the main account for Polygon
        main_address = main_wallet["Address"]
        main_private_key = main_wallet["Private Key"]
        main_account = self.wallet_manager.get_account(main_private_key)
        self.wallet_manager.set_main_account(main_account)

        # Display the account address
        self.address_text.delete(0, END)
        self.address_text.insert(0, address)


app.mainloop()