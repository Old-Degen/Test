import csv
import os
from modules.rpc import get_rpc


# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE_DIR = os.path.join(BASE_DIR, "private")
WALLET_CSV_FILE = os.path.join(PRIVATE_DIR, "wallets.csv")
RPC_LIST_CSV_FILE = os.path.join(PRIVATE_DIR, "rpc_list.csv")

# RPC settings
POLYGON_RPC_URI = get_rpc("polygon")
RPC_URI = POLYGON_RPC_URI

# CSV settings
CSV_HEADERS = ["Chain", "Group", "Name", "Address", "Private_Key"]

# Network settings
POLYGON_NETWORKS = {}

def get_wallets():
    wallets = []
    with open(WALLET_CSV_FILE, "r") as f:
        reader = csv.DictReader(f, fieldnames=CSV_HEADERS)
        next(reader)  # skip header row
        for row in reader:
            wallets.append(row)
    return wallets

def get_main_wallet():
    wallets = get_wallets()
    for i, wallet in enumerate(wallets):
        print(f"{i}. {wallet['Name']}")
    selection = input("Select main wallet (by index): ")
    try:
        index = int(selection)
        return wallets[index]
    except:
        print("Invalid selection")
        return None

MAIN_WALLET = get_main_wallet()

if MAIN_WALLET:
    NETWORKS = {
        MAIN_WALLET["Chain"]: {
            "rpc_uri": POLYGON_RPC_URI,
            "provider_uri": "https://rpc-mainnet.maticvigil.com/",
            "wallet_address": MAIN_WALLET["Address"],
            "wallet_private_key": MAIN_WALLET["Private_Key"]
        }
    }
else:
    NETWORKS = {}

