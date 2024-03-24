import json

WALLET_DATA_PATH = 'wallet_data.xlsx'
SHEET_NAME = 'evm'
ENCRYPTED_DATA_PATH = 'encrypted_data.txt'
REALTIME_SETTINGS_PATH = 'realtime_settings.json'

NFTS2ME_CONTRACTS_PATH = 'data/nfts2me_contracts.json'

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open('data/abi/bridge/deposit.json') as file:
    DEPOSIT_ABI = json.load(file)

with open('data/abi/bridge/withdraw.json') as file:
    WITHDRAW_ABI = json.load(file)

with open('data/abi/bridge/oracle.json') as file:
    ORACLE_ABI = json.load(file)

with open('data/abi/scroll/weth.json') as file:
    WETH_ABI = json.load(file)

with open("data/abi/syncswap/router.json", "r") as file:
    SYNCSWAP_ROUTER_ABI = json.load(file)

with open('data/abi/syncswap/classic_pool.json') as file:
    SYNCSWAP_CLASSIC_POOL_ABI = json.load(file)

with open('data/abi/syncswap/classic_pool_data.json') as file:
    SYNCSWAP_CLASSIC_POOL_DATA_ABI = json.load(file)

with open("data/abi/skydrome/abi.json", "r") as file:
    SKYDROME_ROUTER_ABI = json.load(file)

with open("data/abi/zebra/abi.json", "r") as file:
    ZEBRA_ROUTER_ABI = json.load(file)

with open("data/abi/layerbank/abi.json", "r") as file:
    LAYERBANK_ABI = json.load(file)

with open("data/abi/zerius/abi.json", "r") as file:
    ZERIUS_ABI = json.load(file)

with open("data/abi/dmail/abi.json", "r") as file:
    DMAIL_ABI = json.load(file)

with open("data/abi/omnisea/abi.json", "r") as file:
    OMNISEA_ABI = json.load(file)

with open("data/abi/nft2me/abi.json", "r") as file:
    NFTS2ME_ABI = json.load(file)

with open("data/abi/nft2me/abi_main.json", "r") as file:
    NFTS2ME_MAIN_ABI = json.load(file)

with open("data/abi/gnosis/abi.json", "r") as file:
    SAFE_ABI = json.load(file)

with open("data/deploy/abi.json", "r") as file:
    DEPLOYER_ABI = json.load(file)

with open("data/deploy/bytecode.txt", "r") as file:
    DEPLOYER_BYTECODE = file.read()

with open("data/abi/zkstars/abi.json", "r") as file:
    ZKSTARS_ABI = json.load(file)

with open("data/abi/rocketsam/abi.json", "r") as file:
    ROCKETSAM_ABI = json.load(file)

with open("data/abi/nft_origins/abi.json", "r") as file:
    NFT_ORIGINS_ABI = json.load(file)

with open('data/abi/rubyscore/abi.json', 'r') as file:
    RUBYSCORE_ABI = json.load(file)

with open('data/abi/secondlive/abi.json', 'r') as file:
    SECONDLIVE_ABI = json.load(file)

with open('data/orbiter_maker.json', 'r') as file:
    ORBITER_MAKER = json.load(file)

with open("data/abi/owlto/abi.json", "r") as file:
    OWLTO_CHECKIN_ABI = json.load(file)

with open("data/abi/ambient/abi.json", "r") as file:
    AMBIENT_ABI = json.load(file)

with open("data/abi/aave/abi.json", "r") as file:
    AAVE_ABI = json.load(file)

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

BRIDGE_CONTRACTS = {
    "deposit": "0xf8b1378579659d8f7ee5f3c929c2f3e332e41fd6",
    "withdraw": "0x4C0926FF5252A435FD19e10ED15e5a249Ba19d79",
    "oracle": "0x0d7E906BD9cAFa154b048cFa766Cc1E54E39AF9B"
}

ORBITER_CONTRACT = "0x80c67432656d59144ceff962e8faf8926599bcf8"

SCROLL_TOKENS = {
    "ETH": "0x5300000000000000000000000000000000000004",
    "WETH": "0x5300000000000000000000000000000000000004",
    "USDC": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4"
}

SYNCSWAP_CONTRACTS = {
    "router": "0x80e38291e06339d10aab483c65695d004dbd5c69",
    "classic_pool": "0x37BAc764494c8db4e54BDE72f6965beA9fa0AC2d"
}

SKYDROME_CONTRACTS = {
    "router": "0xAA111C62cDEEf205f70E6722D1E22274274ec12F"
}

ZEBRA_CONTRACTS = {
    "router": "0x0122960d6e391478bfe8fb2408ba412d5600f621"
}

LAYERBANK_CONTRACT = "0xec53c830f4444a8a56455c6836b5d2aa794289aa"

LAYERBANK_WETH_CONTRACT = "0x274C3795dadfEbf562932992bF241ae087e0a98C"

ZERIUS_CONTRACT = "0xeb22c3e221080ead305cae5f37f0753970d973cd"

DMAIL_CONTRACT = "0x47fbe95e981c0df9737b6971b451fb15fdc989d9"

OMNISEA_CONTRACT = "0x46ce46951d12710d85bc4fe10bb29c6ea5012077"

SAFE_CONTRACT = "0xa6b71e26c5e0845f74c812102ca7114b6a896ab2"

NFTS2ME_CREATOR_CONTRACT = "0x2269bCeB3f4e0AA53D2FC43B1B7C5C5D13B119a5"

NFT_ORIGINS_CONTRACT = "0x74670A3998d9d6622E32D0847fF5977c37E0eC91"

ORBITER_INSCRIPTIONS_CONTRACT = "0x0a88BC5c32b684D467b43C06D9e0899EfEAF59Df"

RUBYSCORE_CONTRACT = "0xe10Add2ad591A7AC3CA46788a06290De017b9fB4"

SECONDLIVE_CONTRACT = "0xAC1f9Fadc33cC0799Cf7e3051E5f6b28C98966EE"

OWLTO_CHECKIN_CONTRACT = "0xE6FEcA764B7548127672C189D303eb956c3Ba372"

AMBIENT_CONTRACT = "0xaaaaAAAACB71BF2C8CaE522EA5fa455571A74106"

AAVE_CONTRACT = "0xFF75A4B698E3Ec95E608ac0f22A03B8368E05F5D"

SCROLLSCAN_URL = 'https://api.scrollscan.com/api'

SCROLL_API_KEY = ''

CHAINS_OKX = {
    'linea': 'Linea',
    'base': 'Base',
    'arbitrum': 'Arbitrum One',
    'optimism': 'Optimism',
    'zksync': 'zkSync Era'
}

ORBITER_CHAINS_INFO = {
    1: {'name': 'Arbitrum', 'chainId': 42161, 'id': 2},
    2: {'name': 'Arbitrum Nova', 'chainId': 42170, 'id': 16},
    3: {'name': 'Base', 'chainId': 8453, 'id': 21},
    4: {'name': 'Linea', 'chainId': 59144, 'id': 23},
    5: {'name': 'Manta', 'chainId': 169, 'id': 31},
    6: {'name': 'Polygon', 'chainId': 137, 'id': 6},
    7: {'name': 'Optimism', 'chainId': 10, 'id': 7},
    8: {'name': 'Scroll', 'chainId': 534352, 'id': 19},
    9: {'name': 'Starknet', 'chainId': 'SN_MAIN', 'id': 4},
    10: {'name': 'Polygon zkEVM', 'chainId': 1101, 'id': 17},
    11: {'name': 'zkSync Era', 'chainId': 324, 'id': 14},
    12: {'name': 'Zora', 'chainId': 7777777, 'id': 30},
    13: {'name': 'Ethereum', 'chainId': 1, 'id': 1},
    14: {'name': 'BNB Chain', 'chainId': 56, 'id': 15},
    26: {'name': 'Metis', 'chainId': 1088, 'id': 10},
    28: {'name': 'OpBNB', 'chainId': 204, 'id': 25},
    29: {'name': 'Mantle', 'chainId': 5000, 'id': 24},
    45: {'name': 'ZKFair', 'chainId': 42766, 'id': 38}
}

LAYERZERO_WRAPED_NETWORKS = {
    1: 1,
    2: 2,
    3: 27,
    4: 34,
    5: 14,
    6: 15,
    7: 3,
    8: 35,
    9: 19,
    10: 23,
    11: 21,
    12: 36,
    13: 13,
    14: 33,
    15: 37,
    16: 38,
    17: 20,
    18: 17,
    19: 25,
    20: 32,
    21: 31,
    22: 4,
    23: 44,
    24: 5,
    25: 29,
    26: 39,
    27: 26,
    28: 16,
    29: 30,
    30: 40,
    31: 7,
    32: 24,
    33: 6,
    34: 10,
    35: 8,
    36: 41,
    37: 18,
    38: 22,
    39: 42,
    40: 43,
    41: 12,
    42: 28,
    43: 11,
    44: 46
}

RHINO_CHAIN_INFO = {
    1: 'ARBITRUM',
    2: 'ARBITRUMNOVA',
    3: 'BASE',
    4: 'LINEA',
    5: 'MANTA',
    6: 'MATIC_POS',
    7: 'OPTIMISM',
    8: 'SCROLL',
    9: 'STARKNET',
    10: 'ZKEVM',
    11: 'ZKSYNC',
}

COINGECKO_TOKEN_API_NAMES = {
     'ETH': 'ethereum',
     'ASTR': 'astar',
     'AVAX': 'avalanche-2',
     'BNB': 'binancecoin',
     'CANTO': 'canto',
     'CELO': 'celo',
     'CFX': 'conflux-token',
     'COREDAO': 'coredaoorg',
     'JEWEL': 'defi-kingdoms',
     'FTM': 'fantom',
     'FUSE': 'fuse-network-token',
     'GETH': 'goerli-eth',
     'xDAI': 'xdai',
     'ONE': 'harmony',
     'ZEN': 'zencash',
     'KAVA': 'kava',
     'KLAY': 'klay-token',
     'AGLD': 'adventure-gold',
     'MNT': 'mantle',
     'MTR': 'meter-stable',
     'METIS': 'metis-token',
     'GLMR': 'moonbeam',
     'MOVR': 'moonriver',
     'OKT': 'oec-token',
     'MATIC': 'matic-network',
     'SMR': 'shimmer',
     'TLOS': 'telos',
     'TOMOE': 'tomoe',
     'TENET': 'tenet-1b000f7b-59cb-4e06-89ce-d62b32d362b9',
     'XPLA': 'xpla',
     'BEAM': 'beam-2',
     'INJ': 'injective-protocol',
     'DAI': 'dai',
     'USDT': 'tether',
     'USDC': 'usd-coin',
     'USDC.e': 'bridged-usdc-polygon-pos-bridge',
     'BUSD': 'binance-usd',
     'WETH': 'ethereum',
     'USDbC': 'bridged-usd-coin-base',
     'STG': 'stargate-finance'
}

HEADER = """███████╗ ██████╗██████╗  ██████╗ ██╗     ██╗         ██╗   ██╗██████╗ 
██╔════╝██╔════╝██╔══██╗██╔═══██╗██║     ██║         ██║   ██║╚════██╗
███████╗██║     ██████╔╝██║   ██║██║     ██║         ██║   ██║ █████╔╝
╚════██║██║     ██╔══██╗██║   ██║██║     ██║         ╚██╗ ██╔╝██╔═══╝ 
███████║╚██████╗██║  ██║╚██████╔╝███████╗███████╗     ╚████╔╝ ███████╗
╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝      ╚═══╝  ╚══════╝                                                                      
"""
