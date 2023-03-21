class Task:
    def __init__(self, private_key, task_manager):
        self.private_key = private_key
        self.task_manager = task_manager

    def run(self):
        public_key = self.taskmanager.Utils.private_to_public_key(self.private_key)
        self.taskmanager.gui.public_key.set(public_key)
        self.taskmanager.gui.input_field.configure(state="normal")
        self.taskmanager.gui.generate_button.configure(state="normal")
        self.taskmanager.gui.output_field.configure(state="readonly")
        self.taskmanager.gui.progress.stop()


class TaskManager:
    def __init__(self, gui):
        from gui import WalletGeneratorGUI
        self.gui = gui
        self.wallet_generator = WalletGeneratorGUI(self.gui.parent)
        self.wallet_manager = WalletManager()

    def create_task(self, group, name, private_key):
        self.gui.public_key.set("")
        self.gui.input_field.configure(state="disabled")
        self.gui.generate_button.configure(state="disabled")
        self.gui.output_field.configure(state="disabled")
        self.gui.progress.start()

        # Создаем кошельки и записываем их в CSV файл
        address, private_key = self.wallet_manager.generate_wallet(group, name)

        # Запускаем задачу
        task = Task(private_key, self)
        task.run()
