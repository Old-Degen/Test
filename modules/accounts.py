class Accounts:
    def __init__(self):
        self.accounts = []

    def add_account(self, group, name, address, private_key):
        self.accounts.append({'Group': group, 'Name': name, 'Address': address, 'Private Key': private_key})