import json

WALLET_DATA_PATH = 'wallet_data.xlsx'
SHEET_NAME = 'evm'
ENCRYPTED_DATA_PATH = 'encrypted_data.txt'
REALTIME_SETTINGS_PATH = 'realtime_settings.json'
BADGES_PATH = 'badges.xlsx'
MARKS_PATH = 'marks.xlsx'

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

with open("data/abi/canvas/abi.json", "r") as file:
    CANVAS_ABI = json.load(file)

with open("data/abi/omnihub/abi.json", "r") as file:
    OMNIHUB_ABI = json.load(file)

with open("data/abi/pumpscroll/abi.json", "r") as file:
    PUMPSCROLL_ABI = json.load(file)

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

BRIDGE_CONTRACTS = {
    "deposit": "0x6774Bcbd5ceCeF1336b5300fb5186a12DDD8b367",
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

CANVAS_CONTRACT = "0xB23AF8707c442f59BDfC368612Bd8DbCca8a7a5a"

OMNIHUB_CONTRACT = "0xD6238AD2887166031567616d9a54B21eb70e4dFd"

PUMPSCROLL_CONTRACT = "0xCe64dA1992Cc2409E0f0CdCAAd64f8dd2dBe0093"


ETH_BADGE = ("https://canvas.scroll.cat/badge/check?badge=0x3dacAd961e5e2de850F5E027c70b56b5Afa5DfeD", "ETH Year")
AMBIENT_SWAPOOOR = ("https://ambient-scroll-badge.liquidity.tools/api/check?badge=0xDaf958ec36dB494e82709a3AaB9FA6981EfC4Dad", "Ambient Swapooor")
AMBIENT_PROVIDOOR = ("https://ambient-scroll-badge.liquidity.tools/api/check?badge=0xC634b718618729df70331D79fcd6E889a547fbEB", "Ambient Providoor")
AMBIENT_FILLOOR = ("https://ambient-scroll-badge.liquidity.tools/api/check?badge=0x21C5E85eBCbd924BA633D4A7A5F2718f25C713D8", "Ambient Filloor")
AMBIENT_YEET = ("https://ambient-scroll-badge.liquidity.tools/api/check?badge=0x7bD1AEADCc59EedaF4775E4D3197Ce9a7031BD01", "Ambient Yeet")
ZEBRA_BADGE = ("https://zebra.xyz/api/badge/check?badge=0x09E14E520eec3583681Fe225a4B506743EC3cc78", "Zebra")
SCROLLY_BADGE = ("https://api.scrolly.xyz/api/badge/check?badge=0x79b4f7492328D0Cc4ED0Ddaee08Cd42f0F36A4CC", "Scrolly")
PENCIL_S_BADGE = ("https://pencilsprotocol.io/api/scroll/canvas/badge/pencil/check?badge=0x766e3f1EE86439DE0597F6e917F980A4e5d187A3", "Pencil S")
PENCIL_P_BADGE = ("https://pencilsprotocol.io/api/scroll/canvas/badge/pencil/check?badge=0x2d8E67c1427a1ebb9ddB5c4D38143140B0c19aC8", "Pensil P")
SCROLLER_AGENT_BADGE = ("https://vwb06c8e7h.execute-api.us-east-1.amazonaws.com/dev/check?badge=0x9aD600bDD45Cc30242fd905872962dc415F68530", "Scroller Agent")
PASSPORT_XYZ_BADGE = ("https://passport-iam.gitcoin.co/scroll/check?badge=0xa623f348A12cFdC6B64a8c9e883dD9B243438E79", "Passport XYZ")
SYMBIOSIS_PROFESSIONAL = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0xB936740f00FFA90a55C362C33840913eaCFDcE25", "Symbiosis Professional")
TRUSTA_MEDIA_BADGE = ("https://mp.trustalabs.ai/attestations/media_badge/check?badge=0x47FF789Da49686C6cC38998F76F78A12A5939082", "Trusta MEDIA")
SYMBIOSIS_WHALE = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0xaE98FC0e46977DaF650B180041dB20155ac66277", "Symbiosis Whale")
SYMBIOSIS_SWAPPER = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x3c1A82D5877AB970Be9d80AB8185C5F9F1505C49", "Symbiosis Swapper")
SYMBIOSIS_BEGINNER = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x66703cd7eBA1b114cA652b1C2DE268858cBedEc8", "Symbiosis Beginner")
XHS_BADGE = ("https://scroll-canvas-api.xname.app/api/check?badge=0x7C0deB6aBf29cC829186933720af67da8B1EF633", "XHS")
SCROLL_BOOSTER = ("https://scroll-canvas-api.xname.app/api/domain/check?badge=0xed269A526ad793CcB671Ef55A7AF6E45F300d462", "Scroll Booster")
OMNIHUB_BADGE = ("https://api.omnihub.xyz/api/integration/scroll/check?badge=0xdd8CCDad022999afD61DFda146e4C40F47dE4Eec", "Omnihub")
TRUSTA_POH_BADGE = ("https://mp.trustalabs.ai/attestations/poh_badge/check?badge=0x26B97C832C04C06cAd34dCE23c701beDC3555a5c", "Trusta POH")
RETRO_BRIDGE_BADGE = ("https://backend.retrobridge.io/api/quest/check?badge=0x59700c6Ed282eD7611943129f226914ACBB3982b", "Retro Bridge")
SYMBIOSIS_PRO_SWAPPER = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x0a584c042133aF17f3e522F09A77Ee1496f3a567", "Symbiosis Pro Swapper")
SMILECOBRA_BADGE = ("https://api.smilecobra.io/tripartite/scroll/badge/check?badge=0x7ecf596Ed5fE6957158cD626b6bE2A667267424f", "Smilecobra")
SCROLL_EXPLORER = ("https://publicapi.xenobunny.xyz/canvas/lands/check?badge=0x7188B352C818f291432CDe8E4B1f0576c188F9e4", "Scroll Explorer")
SYMBIOSIS_BRIDGE_1 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0xB69cF3247b60F72ba560B3C1e0F53DAF9e9D5201", "Symbiosis Bridge 1")
SYMBIOSIS_BRIDGE_2 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x35CB802ede5f970AE6d7B8E7b7b82C82Fea273C7", "Symbiosis Bridge 2")
SYMBIOSIS_BRIDGE_3 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x4445BE64c03154052bd661fD1B0d01FC625Df06E", "Symbiosis Bridge 3")
SYMBIOSIS_BRIDGE_4 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x475d1E9Be98B7B7b97D7ED9695541A0209e982dE", "Symbiosis Bridge 4")
SYMBIOSIS_BRIDGE_5 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0xCA5d53f143822dd8b9789b1A12d2a10A39a499e4", "Symbiosis Bridge 5")
SYMBIOSIS_BRIDGE_6 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x9765B7B7926Cb27b84f5F48EA0758Fa99da3C7d6", "Symbiosis Bridge 6")
SYMBIOSIS_BRIDGE_7 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x6d352E2987C0AC7D896B74453f400477dE7446F0", "Symbiosis Bridge 7")
SYMBIOSIS_BRIDGE_8 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x5bA1cC19C89BeD7d4660316D1eB41B6A581B98c7", "Symbiosis Bridge 8")
SYMBIOSIS_BRIDGE_9 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0xCd223ce0Cc6C05c1604f8f83A50e98202E600bD6", "Symbiosis Bridge 9")
SYMBIOSIS_BRIDGE_10 = ("https://api.symbiosis.finance/crosschain/v1/scroll-badge/check?badge=0x3573335B5128F50F79617f1218f2A7aA0EE68703", "Symbiosis Bridge 10")

SCROLLSCAN_URL = 'https://api.scrollscan.com/api'
SCROLL_API_KEYS = ['']  # api from https://scrollscan.com/ ['api_key1', 'api_key2']
ETHERSCAN_API_KEYS = ['']  # api from https://etherscan.io/ ['api_key1', 'api_key2']

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
