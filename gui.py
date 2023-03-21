from tkinter import *
from tkinter import ttk
from modules.task_manager import TaskManager
from modules.utils import Utils


class WalletGeneratorGUI:
    def __init__(self, parent):
        self.parent = parent
        self.task_manager = TaskManager(self.gui)
        self.utils = Utils()

        self.main_frame = ttk.Frame(self.parent, padding="30 15 30 15")
        self.main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.private_key = StringVar()
        self.public_key = StringVar()

        self.create_widgets()

        self.parent.bind("<Return>", self.generate_wallets)

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

    def generate_wallet(self, event=None):
        self.progress.start()
        self.task_manager.create_task(self.input_field.get())
