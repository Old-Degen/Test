import csv
import os

from modules.rpc import get_rpc

# Network settings
NETWORKS = {
    "Polygon": {"rpc_uri": POLYGON_RPC_URI, "provider_uri": "https://rpc-mainnet.maticvigil.com/"}
}

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE_DIR = os.path.join(BASE_DIR, "private")
WALLET_CSV_FILE = os.path.join(PRIVATE_DIR, "wallets.csv")
RPC_LIST_CSV_FILE = os.path.join(PRIVATE_DIR, "rpc_list.csv")

# RPC settings
POLYGON_RPC_URI = get_rpc("polygon")
RPC_URI = POLYGON_RPC_URI

# CSV settings
CSV_HEADERS = ["address", "private_key", "public_key", "mnemonic_phrase", "note"]

# Network settings
NETWORKS = {"Polygon": {"rpc_uri": POLYGON_RPC_URI}}

