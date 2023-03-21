from modules.wallet_manager import WalletManager
from modules.utils import  Utils

class Task:
    def __init__(self, private_key, task_manager):
        self.private_key = private_key
        self.task_manager = task_manager

    def run(self):
        public_key = self.task_manager.Utils.private_to_public_key(self.private_key)
        self.task_manager.gui.public_key.set(public_key)
        self.task_manager.gui.input_field.configure(state="normal")
        self.task_manager.gui.generate_button.configure(state="normal")
        self.task_manager.gui.output_field.configure(state="readonly")
        self.task_manager.gui.progress.stop()


class TaskManager:
    def __init__(self, gui):
        self.wallet_manager = WalletManager
        self.tasks = []

    def create_task(self, group, name, private_key):
        self.gui.public_key.set("")
        self.gui.input_field.configure(state="disabled")
        self.gui.generate_button.configure(state="disabled")
        self.gui.output_field.configure(state="disabled")
        self.gui.progress.start()

        # Создаем кошельки и записываем их в CSV файл
        address, private_key = self.wallet_manager.generate_wallets(group, name)

        # Запускаем задачу
        task = Task(private_key, self)
        task.run()
