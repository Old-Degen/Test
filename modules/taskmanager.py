class Task:
    def __init__(self, private_key, task_manager):
        self.private_key = private_key
        self.task_manager = task_manager

    def run(self):
        public_key = self.task_manager.utils.private_to_public_key(self.private_key)
        self.task_manager.gui.public_key.set(public_key)
        self.task_manager.gui.input_field.configure(state="normal")
        self.task_manager.gui.generate_button.configure(state="normal")
        self.task_manager.gui.output_field.configure(state="readonly")
        self.task_manager.gui.progress.stop()


class TaskManager:
    def __init__(self, gui):
        from gui import WalletGeneratorGUI
        self.gui = gui
        self.wallet_generator = WalletGeneratorGUI(self.gui.parent)

    def create_task(self, private_key):
        self.gui.public_key.set("")
        self.gui.input_field.configure(state="disabled")
        self.gui.generate_button.configure(state="disabled")
        self.gui.output_field.configure(state="disabled")
        self.gui.progress.start()
        task = Task(private_key, self)
        task.run()
