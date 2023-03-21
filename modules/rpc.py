from web3.auto import w3
from web3.providers import HTTPProvider
from web3.middleware import geth_poa_middleware
from settings import NETWORKS

def get_provider_uri(network):
    return NETWORKS[network]['rpc']

def get_rpc(network):
    provider_uri = get_provider_uri(network)
    w3 = Web3(HTTPProvider(provider_uri))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3
