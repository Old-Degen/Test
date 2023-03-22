import csv


class RPC:
    def __init__(self, uri):
        self.uri = self.get_rpc_uri(uri)

    def get_rpc_uri(self, uri):
        with open('private/rpc_list.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] == uri:
                    return row['uri']
        raise ValueError(f"Blockchain '{uri}' is not found in rpc_list.csv")
