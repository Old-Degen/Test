import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Settings:
    def __init__(self):
        self.network = None
        self.provider_uri = None

    def load(self):
        settings_file = os.path.join(BASE_DIR, 'settings.txt')
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                settings = f.read().splitlines()
                if len(settings) == 2:
                    self.network = settings[0]
                    self.provider_uri = settings[1]

    def save(self):
        settings_file = os.path.join(BASE_DIR, 'settings.txt')
        with open(settings_file, 'w') as f:
            f.write(self.network + '\n')
            f.write(self.provider_uri + '\n')
