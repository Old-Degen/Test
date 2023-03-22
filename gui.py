from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from modules.wallet_manager import WalletManager


class WalletGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wallet Generator")

        # Создание экземпляра класса WalletManager
        self.wallet_manager = WalletManager()

        # Создание переменной StringVar для хранения выбранного кошелька
        self.selected_wallet_var = tk.StringVar()

        # Создание выпадающего списка с именами кошельков
        self.wallet_names = self.wallet_manager.get_wallet()
        self.wallet_menu = tk.OptionMenu(master, self.selected_wallet_var, *self.wallet_names)
        self.wallet_menu.pack()

        self.new_wallet_group_label = ttk.Label(self.wallets_frame, text="Group:")
        self.new_wallet_group_label.grid(row=2, column=0, sticky="w")

        self.new_wallet_group_entry = ttk.Entry(self.wallets_frame, width=30)
        self.new_wallet_group_entry.grid(row=2, column=1, sticky="w")

        self.new_wallet_prefix_label = ttk.Label(self.wallets_frame, text="Prefix:")
        self.new_wallet_prefix_label.grid(row=3, column=0, sticky="w")

        self.new_wallet_prefix_entry = ttk.Entry(self.wallets_frame, width=30)
        self.new_wallet_prefix_entry.grid(row=3, column=1, sticky="w")

        self.new_wallet_count_label = ttk.Label(self.wallets_frame, text="Count:")
        self.new_wallet_count_label.grid(row=4, column=0, sticky="w")

        self.new_wallet_count_entry = ttk.Entry(self.wallets_frame, width=30)
        self.new_wallet_count_entry.grid(row=4, column=1, sticky="w")

    def get_wallet_index(self):
        # Вывод списка кошельков и запрос индекса кошелька
        print("0. Test User")
        print("1. Test User")
        wallet_index = int(input("Select main wallet (by index): "))
        return wallet_index

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

    def select_wallet(wallets):
        print("Select main wallet (by index): ")
        for i, wallet in enumerate(wallets):
            print(f"{i}. {wallet}")
        index = input().strip()
        while not index.isdigit() or int(index) >= len(wallets):
            index = input("Invalid input. Please enter the index of the wallet you want to select: ")
        return index