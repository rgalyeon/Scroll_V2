import asyncio

from modules import *
from utils.progress_checker import Scan


async def deposit_scroll(wallet_info):
    """
    Deposit from official bridge
    ______________________________________________________
    min_amount - the minimum possible amount for sending
    max_amount - maximum possible amount to send
    decimal - to which digit to round the amount to be sent

    all_amount - if True, percentage values will be used for sending (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be sent
    max_percent - the maximum possible percentage of the balance to send

    check_balance_on_dest - if True, it will check the balance in the destination network.
    check_amount - amount to check the balance in the destination network. if the balance is greater than this amount,
                   the bridge will not be executed.
    save_funds - what amount to leave in the outgoing network [min, max], chosen randomly from the range
    min_required_amount - the minimum required balance in the network to make the bridge.
                          if there is no network with the required balance, the bridge will not be made
    """

    min_amount = 0.001
    max_amount = 0.003
    decimal = 6

    all_amount = True

    min_percent = 23
    max_percent = 55

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0

    wait_unlimited_time = False
    sleep_between_attempts = [120, 300]

    scroll_inst = Scroll(wallet_info)
    await scroll_inst.native_bridge_deposit(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent,
        save_funds, check_balance_on_dest, check_amount, min_required_amount,
        wait_unlimited_time, sleep_between_attempts
    )


async def withdraw_scroll(wallet_info):
    """
    Withdraw from official bridge
    ______________________________________________________
    Description: look at deposit_scroll description
    """

    min_amount = 0.0012
    max_amount = 0.0012
    decimal = 4

    all_amount = True

    min_percent = 10
    max_percent = 10

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0

    wait_unlimited_time = False
    sleep_between_attempts = [120, 300]  # min, max

    scroll_inst = Scroll(wallet_info)
    await scroll_inst.withdraw(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent,
        save_funds, check_balance_on_dest, check_amount, min_required_amount, wait_unlimited_time,
        sleep_between_attempts
    )


async def withdraw_okx(wallet_info):
    """
    Withdraw ETH from OKX

    WARNING! OKX DOES NOT SUPPORT SCROLL CHAIN
    ______________________________________________________
    min_amount - min amount (ETH)
    max_amount - max_amount (ETH)
    chains - ['zksync', 'arbitrum', 'linea', 'base', 'optimism']
    terminate - if True - terminate program if money is not withdrawn
    skip_enabled - If True, the skip_threshold check will be applied; otherwise, it will be ignored
    skip_threshold - If skip_enabled is True and the wallet balance is greater than or equal to this threshold,
                     skip the withdrawal
    wait_unlimited_time - the software will wait indefinitely for funds on the OKX
    sleep_between_attempts - minimum-maximum delay between balance checks (if wait_unlimited_time - True)
    """
    token = 'ETH'
    chains = ['arbitrum', 'zksync', 'linea', 'base', 'optimism']

    min_amount = 0.0070
    max_amount = 0.0072

    terminate = False

    skip_enabled = False
    skip_threshold = 0.00327

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    okx_exchange = Okx(wallet_info, chains)
    await okx_exchange.okx_withdraw(
        min_amount, max_amount, token, terminate, skip_enabled, skip_threshold,
        wait_unlimited_time, sleep_between_attempts
    )


async def transfer_to_okx(wallet_info):
    from_chains = ["optimism", "arbitrum"]

    min_amount = 0.0012
    max_amount = 0.0012
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    save_funds = [0.0001, 0.00012]
    min_required_amount = 0.002

    bridge_from_all_chains = True
    sleep_between_transfers = [120, 350]

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    transfer_inst = Transfer(wallet_info, from_chains=from_chains)
    await transfer_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent,
        max_percent, save_funds, False, 0, min_required_amount,
        bridge_from_all_chains=bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers,
        wait_unlimited_time=wait_unlimited_time,
        sleep_between_attempts=sleep_between_attempts
    )


async def bridge_orbiter(wallet_info):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chains – source chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one or more
                  If more than one chain is specified, the software will check the balance in each network and
                  select the chain with the highest balance.
    to_chains – destination chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one or more
                If more than one is specified, randomly selected

    min_amount - the minimum possible amount for sending
    max_amount - maximum possible amount to send
    decimal - to which digit to round the amount to be sent

    all_amount - if True, percentage values will be used for sending (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be sent
    max_percent - the maximum possible percentage of the balance to send

    check_balance_on_dest - if True, it will check the balance in the destination network.
    check_amount - amount to check the balance in the destination network. if the balance is greater than this amount,
                   the bridge will not be executed.
    save_funds - what amount to leave in the outgoing network [min, max], chosen randomly from the range
    min_required_amount - the minimum required balance in the network to make the bridge.
                          if there is no network with the required balance, the bridge will not be made
    bridge_from_all_chains - if True, will be produced from all chains specified in the parameter from_chains
    sleep_between_transfers - only if bridge_from_all_chains=True. sleep between few transfers
    wait_unlimited_time - the software will wait indefinitely for funds on the wallet in the source chain
    sleep_between_attempts - minimum-maximum delay between balance checks (if wait_unlimited_time - True)
    """

    from_chains = ["arbitrum", "optimism", "base", "linea"]  # Chain with max balance will be selected
    to_chain = ["scroll"]  # Randomly selected

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 6

    all_amount = True

    min_percent = 98
    max_percent = 100

    check_balance_on_dest = True
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0.005

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    orbiter_inst = Orbiter(wallet_info, from_chains=from_chains)
    await orbiter_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers, wait_unlimited_time=wait_unlimited_time,
        sleep_between_attempts=sleep_between_attempts
    )


async def bridge_layerswap(wallet_info):
    """
    Bridge from Layerswap
    ______________________________________________________
    Description: Look at bridge_orbiter description
    """

    from_chains = ["base"]  # Chain with max balance will be selected
    to_chain = ["scroll"]  # Randomly selected

    min_amount = 0.0002
    max_amount = 0.0003
    decimal = 6

    all_amount = True

    min_percent = 98
    max_percent = 100

    check_balance_on_dest = True
    check_amount = 0.005
    save_funds = [0.0008, 0.001]
    min_required_amount = 0

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    layerswap_inst = LayerSwap(wallet_info=wallet_info, from_chains=from_chains)
    await layerswap_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers, wait_unlimited_time=wait_unlimited_time,
        sleep_between_attempts=sleep_between_attempts
    )


async def bridge_nitro(wallet_info):
    """
    Bridge from Nitro
    ______________________________________________________
    Description: Look at bridge_orbiter description
    """

    from_chains = ["optimism"]  # Chain with max balance will be selected
    to_chain = ["scroll"]  # Randomly selected

    min_amount = 0.0002
    max_amount = 0.0003
    decimal = 6

    all_amount = True

    min_percent = 100
    max_percent = 100

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.0003, 0.0005]
    min_required_amount = 0

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    nitro_inst = Nitro(wallet_info=wallet_info, from_chains=from_chains)
    await nitro_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers, wait_unlimited_time=wait_unlimited_time,
        sleep_between_attempts=sleep_between_attempts
    )


async def bridge_relay(wallet_info):
    """
    Bridge from relay

    Supported chains - 'arbitrum', 'arbitrum_nova', 'base', 'optimism', 'zksync', 'ethereum', 'zora', 'mode', 'blast'
    ______________________________________________________
    Description: Look at bridge_orbiter description
    """

    from_chains = ["optimism"]  # Chain with max balance will be selected
    to_chain = ["ethereum"]  # Randomly selected

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 6

    all_amount = True

    min_percent = 100
    max_percent = 100

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.00005, 0.00003]
    min_required_amount = 0

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    relay_inst = Relay(wallet_info, from_chains=from_chains)
    await relay_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers, wait_unlimited_time=wait_unlimited_time,
        sleep_between_attempts=sleep_between_attempts
    )


async def wrap_eth(wallet_info):
    """
    Wrap ETH
    ______________________________________________________
    min_amount - the minimum possible amount for wrapping
    max_amount - maximum possible amount to wrapping
    decimal - to which digit to round the amount to be wrapped

    all_amount - if True, percentage values will be used for wrapping (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be wrapped
    max_percent - the maximum possible percentage of the balance to wrap
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 5
    max_percent = 10

    scroll_inst = Scroll(wallet_info)
    await scroll_inst.wrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def unwrap_eth(wallet_info):
    """
    Unwrap ETH
    ______________________________________________________
    Description: look at wrap_eth description
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    scroll_inst = Scroll(wallet_info)
    await scroll_inst.unwrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_skydrome(wallet_info):
    """
    Make swap on Skydrome
    You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    min_amount - the minimum possible amount for swap
    max_amount - maximum possible amount for swap
    decimal - to which digit to round the amount to be swapped
    slippage - slippage rate

    all_amount - if True, percentage values will be used for swap (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be swapped
    max_percent - the maximum possible percentage of the balance to swap

    ______________________________________________________
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    skydrome_inst = Skydrome(wallet_info)
    await skydrome_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_zebra(wallet_info):
    """
    Make swap on Zebra
    You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    Description: look at swap_skydrome description
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    zebra_inst = Zebra(wallet_info)
    await zebra_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_syncswap(wallet_info):
    """
    Make swap on SyncSwap
    You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    Description: look at swap_skydrome description
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 1
    max_amount = 2
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    syncswap_inst = SyncSwap(wallet_info)
    await syncswap_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_ambient(wallet_info):
    """
    Make swap on Ambient
    You can swap only ETH to USDC or USDC to ETH!
    ______________________________________________________
    Description: look at swap_skydrome description
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 1
    max_amount = 2
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    ambient_inst = Ambient(wallet_info)
    await ambient_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def deposit_layerbank(wallet_info):
    """
    Make deposit on LayerBank
    ______________________________________________________
    min_amount - the minimum possible amount for deposit
    max_amount - maximum possible amount for deposit
    decimal - to which digit to round the amount to be deposited

    make_withdraw - True, if need withdraw after deposit
    sleep_from, sleep_to - minimum/maximum delay before withdrawal (if make_withdraw = True)

    all_amount - if True, percentage values will be used for deposit (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance for deposit
    max_percent - the maximum possible percentage of the balance for deposit


    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    make_withdraw = True
    sleep_from = 7600
    sleep_to = 15000

    all_amount = True

    min_percent = 5
    max_percent = 35

    layerbank_inst = LayerBank(wallet_info)
    await layerbank_inst.router(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_aave(wallet_info):
    """
    Make deposit on Aave
    ______________________________________________________
    min_amount - the minimum possible amount for deposit
    max_amount - maximum possible amount for deposit
    decimal - to which digit to round the amount to be deposited

    make_withdraw - True, if need withdraw after deposit
    sleep_from, sleep_to - minimum/maximum delay before withdrawal (if make_withdraw = True)

    all_amount - if True, percentage values will be used for deposit (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance for deposit
    max_percent - the maximum possible percentage of the balance for deposit


    all_amount - deposit from min_percent to max_percent
    """

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    make_withdraw = True
    required_amount_for_withdraw = 0.005

    sleep_from = 3650
    sleep_to = 10000

    all_amount = True

    min_percent = 30
    max_percent = 60

    aave_inst = Aave(wallet_info)
    await aave_inst.router(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent,
        required_amount_for_withdraw
    )


async def withdraw_aave(wallet_info):
    required_amount_for_withdraw = 0.005

    aave_inst = Aave(wallet_info)
    await aave_inst.withdraw(required_amount_for_withdraw)


async def deposit_rocketsam(wallet_info):
    """
    Make deposit on RocketSam
    ______________________________________________________
    Description: look at deposit_layerbank description
    """

    contracts = [
        "0x634607B44e21F4b71e7bD5e19d5b8E4dC99Ab9C4",
        "0x1077df51A4059477826549101a30a70b9579A08B",
        "0x802DbB9efE447f8e4f578EB7add3F7e43E89C529",
        "0x0c9Bfb785E6582A15d6523252675abaA7350Bf76",
        "0x288df8088905D71Ff052bf052f3A0ff11A6CDa46",
        "0x2B4a7822F3de8bd6cb0552f562b40a391890E945",
        "0x553a8EFa12d333c864c89CB809D68268C836B70a",
        "0x5ae3cB086887A6FB7662eE58Cf1d5113E69bBA62",
        "0x1feF777Fb93Aa45a6Cefcf5507c665b64b301FB3",
        "0x0557D4C04BB994719b087d2950841BF25cf39899",
    ]

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    make_withdraw = True
    sleep_from = 7600
    sleep_to = 15000

    all_amount = True

    min_percent = 20
    max_percent = 35

    rocketsam_inst = RocketSam(wallet_info)
    await rocketsam_inst.router(
        contracts, min_amount, max_amount, decimal, sleep_from, sleep_to,
        make_withdraw, all_amount, min_percent, max_percent
    )


async def withdraw_rocketsam(wallet_info):
    """
    Make withdraw from RocketSam
    ______________________________________________________
    sleep_from, sleep_to - minimum/maximum delay before withdrawal from contracts
    """
    contracts = [
        "0x634607B44e21F4b71e7bD5e19d5b8E4dC99Ab9C4",
        "0x1077df51A4059477826549101a30a70b9579A08B",
        "0x802DbB9efE447f8e4f578EB7add3F7e43E89C529",
        "0x0c9Bfb785E6582A15d6523252675abaA7350Bf76",
        "0x288df8088905D71Ff052bf052f3A0ff11A6CDa46",
        "0x2B4a7822F3de8bd6cb0552f562b40a391890E945",
        "0x553a8EFa12d333c864c89CB809D68268C836B70a",
        "0x5ae3cB086887A6FB7662eE58Cf1d5113E69bBA62",
        "0x1feF777Fb93Aa45a6Cefcf5507c665b64b301FB3",
        "0x0557D4C04BB994719b087d2950841BF25cf39899",
    ]

    sleep_from = 10
    sleep_to = 30

    rocketsam_inst = RocketSam(wallet_info)
    await rocketsam_inst.withdraw(contracts, sleep_from, sleep_to)


async def bridge_nft_zerius(wallet_info):
    """
    Mint + bridge Zerius NFT
    The Mint function should be called "mint", to make sure of this,
                 look at the name in in explorer
    ______________________________________________________
    chains - list chains for random chain bridge: arbitrum, optimism, polygon, bsc, avalanche
    sleep_from, slip_to - minimum/maximum delay between mint and bridge
    """

    chains = ["arbitrum"]

    sleep_from = 30
    sleep_to = 120

    zerius_inst = Zerius(wallet_info)
    await zerius_inst.mint_and_bridge(chains, sleep_from, sleep_to)


async def mint_nft(wallet_info):
    """
    Mint NFT on NFTS2ME
    ______________________________________________________
    contracts - list NFT contract addresses  (contract_address, method (mint/mintRandomTo))
    """

    contracts = [
        ('0x24178Df853B4Db50B0EC8A8afd7DF51229e3b346', 'mint'),  # potato
        ('0x9E519a8B155C7Cf9ff74D666db079716FFC47318', 'mint'),  # Duality
        ('0xe08c47aeBEaC2d8Ed49AD64d65f6e65877F5716b', 'mint'),  # Architect.l2p
        ('0x1cFe398220E3A76cd05ce98F68e8cB7E5c96A8A0', 'mintRandomTo'),  # LayerZero memes
        ('0x5128ED5C206eBb80068E13f058ba476F27449C26', 'mint'),  # not onchain identity
        ('0xd20F23a8BbBE6e5B63D97b1a94Cc2E111706FB98', 'mint'),  # Autumn zorb
        ('0xE1C60ae5EA9171ABE3FCD3f0Fd8007918e1f961F', 'mint'),  # Not eligible
        ('0xbBa247dCD53af0432511Ae173Ac6e1700B8cC77c', 'mintRandomTo'),  # bull hammer
        ('0x3490e1ecdcbBFBf7f728B65b87199181C5E30c44', 'mint'),  # nastyCat
        ('0x93B99D89AB4F46431cF3D71DD68E431C844A64DC', 'mint'),  # kittyCat
        ('0x1E915a166db76C44ED8FE12F97C4e3b65c2C2629', 'mint'),  # dandy
        ('0xDB9577Ef2Cd8360b3e34aEc7b700AD0894Dc68b7', 'mint'),  # kateVG
        ('0x48BD80a8e60aAa91FD36fb00707590368C9E4468', 'mint'),  # nancyTON1
        ('0x31dCD2726d46550C8162cCB23DA5B9b108906a5f', 'mint'),  # b560
        ('0x28ee739580941e7EbBc3D6e337c3080025A5975E', 'mint'),  # AndyEn2
        ('0xC5c3738Dc94E2395C7afF8a1b5aA322B3465496B', 'mint'),  # alvar1
        ('0x4984E05E77457B9e7c1143D651A2c40Ff6138219', 'mint'),  # ksi2
        ('0x754F3e6E2651e6Cc907B856A6a5592EC6094E4aa', 'mint'),  # ksu002
        ('0xafdEAAd25fB47fBc2151357504292530d89b7A75', 'mint'),  # Anny
        ('0x2a826Ad1a9a7830C25B4988EF444Cd0710B7A61e', 'mint'),  # danny2
        ('0xa8A1876100A5C4f9c1CC18efD3e4acABB8779648', 'mint'),  # howardtens
        ('0x528366eBEc17E348Dcf29Db66422F68ae8a7E310', 'mint'),  # kelly3
        ('0x44CD8b5782d690173010D81eD7fe679A28729b6c', 'mint'),  # bubble3
        ('0x07DEe49894bBDc900eD723556Eabfb0fcbd79A1C', 'mint'),  # Drone
        ('0xe712378C3aeF1D4054c56da020D4eA75Bff76c66', 'mint'),  # Anny
        ('0x6be4b2630da4B5EBeE9C20aD7B996578d0337FbE', 'mint'),  # Marty0
        ('0x90183dFb9dFD684Cd05579787B8A95AE073cbCe2', 'mint'),  # Alex
        ('0x7EdcC98a327178b21CA372156c5fde196a09BE5C', 'mint'),  # Grey
        ('0x2cb36f4D93EE27362A63F99C4E55133b1F56Fe5f', 'mint'),  # Anakin2
        ('0xBf214C36B82d5aFa0Ed52C93DdFf692FFfB147b0', 'mint'),  # Bran2
        ('0xed50b8A648dE7241f39Cf9EEc2d471d6588a7B16', 'mint'),  # Stark00
        ('0xC42706B43168dA0161a8970f99689A2edC10Dd7B', 'mint'),  # Sansa
        ('0xC6bcd4D8c85DC5eA9D78F28D0C69E5128A5e824e', 'mint'),  # Deer
        ('0x67dA10157415ac1f30AE152fEA6DF1366158B551', 'mint'),  # Sticker0
        ('0x9e866bc18604CBFeF6B14A4839dd0883Ac08340f', 'mint'),  # PZ
        ('0x7b1eA7f264eD0c1eeB9AE66a781705b106742C46', 'mint'),  # Hq
        ('0xcd9B72eAE740eE25dF617a4770Ec6d197Bb484b1', 'mint'),  # deer
        ('0x487E0880053e3Ad39C40a7B33eF0d10213ef50e5', 'mint'),  # Moon
        ('0x815E3459dE519b83E3762e73D52f2a41f0Be5fDf', 'mint'),  # Fox2
        ('0xc1Ff98171a47A2b7C307A601fed5Fc119d318795', 'mint'),  # BF
        ('0x2Ed8134a906670613B90C2883Bc7BB05Af2b495a', 'mint'),  # Next
        ('0xE4873F3724b944c0D1dB6893715FA6BFD3b16E93', 'mint'),  # Sun
        ('0x364964a596eA8C30E8a9038491b3e7991C813D83', 'mint')  # Eat
    ]

    minter = Minter(wallet_info)
    await minter.mint_nft(contracts)


async def parse_nfts2me_contracts():
    """
    Parse NFT on NFTS2ME
    ______________________________________________________
    mint_price - price of the sought contracts
    min_total_supply - supply of the sought contracts
    search_limit - among how many recent collections to look for contracts (MAXIMUM 10000)
    """

    mint_price = 0
    min_total_supply = 200
    search_limit = 10000

    await find_and_update_nfts2me_contracts(mint_price, min_total_supply, search_limit)


async def mint_zkstars(wallet_info):
    """
    Mint ZkStars NFT
    ______________________________________________________
    sleep_from, sleep_to - min/max delay between mints
    """

    contracts = [
        "0x609c2f307940b8f52190b6d3d3a41c762136884e",
        "0x16c0baa8a2aa77fab8d0aece9b6947ee1b74b943",
        "0xc5471e35533e887f59df7a31f7c162eb98f367f7",
        "0xf861f5927c87bc7c4781817b08151d638de41036",
        "0x954e8ac11c369ef69636239803a36146bf85e61b",
        "0xa576ac0a158ebdcc0445e3465adf50e93dd2cad8",
        "0x17863384c663c5f95e4e52d3601f2ff1919ac1aa",
        "0x4c2656a6d1c0ecac86f5024e60d4f04dbb3d1623",
        "0x4e86532cedf07c7946e238bd32ba141b4ed10c12",
        "0x6b9db0ffcb840c3d9119b4ff00f0795602c96086",
        "0x10d4749bee6a1576ae5e11227bc7f5031ad351e4",
        "0x373148e566e4c4c14f4ed8334aba3a0da645097a",
        "0xdacbac1c25d63b4b2b8bfdbf21c383e3ccff2281",
        "0x2394b22b3925342f3216360b7b8f43402e6a150b",
        "0xf34f431e3fc0ad0d2beb914637b39f1ecf46c1ee",
        "0x6f1e292302dce99e2a4681be4370d349850ac7c2",
        "0xa21fac8b389f1f3717957a6bb7d5ae658122fc82",
        "0x1b499d45e0cc5e5198b8a440f2d949f70e207a5d",
        "0xec9bef17876d67de1f2ec69f9a0e94de647fcc93",
        "0x5e6c493da06221fed0259a49beac09ef750c3de1"
    ]

    mint_min = 1
    mint_max = 1

    mint_all = False

    sleep_from = 5
    sleep_to = 10

    zkkstars = ZkStars(wallet_info)
    await zkkstars.mint(contracts, mint_min, mint_max, mint_all, sleep_from, sleep_to)


async def swap_tokens(wallet_info):
    """
    SwapTokens module: Automatically swap tokens to ETH
    ______________________________________________________
    use_dex - Choose any dex: syncswap, skydrome, zebra
    sleep_from/sleep_to - min/max delay between swaps
    """

    use_dex = [
        "ambient"
    ]

    use_tokens = ["USDC"]

    sleep_from = 1
    sleep_to = 5

    slippage = 1

    min_percent = 100
    max_percent = 100

    swap_tokens_inst = SwapTokens(wallet_info)
    await swap_tokens_inst.swap(use_dex, use_tokens, sleep_from, sleep_to, slippage, min_percent, max_percent)


async def swap_multiswap(wallet_info):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex: syncswap, skydrome, zebra, ambient
    n_swaps_min, n_swaps_max - Quantity swaps
    ______________________________________________________
    random_swap_token - If True the swap path will be [ETH -> USDC -> USDC -> ETH] (random!)
    If False the swap path will be [ETH -> USDC -> ETH -> USDC]
    """

    use_dex = ["ambient"]

    n_swaps_min = 1
    n_swaps_max = 1

    sleep_from = 200
    sleep_to = 400

    slippage = 1

    random_swap_token = True

    min_percent = 51
    max_percent = 60

    multi = Multiswap(wallet_info)
    await multi.swap(
        use_dex, sleep_from, sleep_to, n_swaps_min, n_swaps_max, slippage, random_swap_token, min_percent, max_percent
    )


async def inscribe_orbiter(wallet_info):
    """
    Mint layer2-20 inscription
    Software picks random chain from dest_chains and makes inscriptions
    ______________________________________________________
    mint_chain - arbitrum, optimism, base, linea, scroll, zksync, polygon_zkevm, choose ONE
    dest_chains - Support arbitrum, optimism, base, linea, scroll, zksync, polygon_zkevm
    """

    mint_chain = "scroll"
    dest_chains = ["scroll"]

    orb_inscriptions = OrbiterInscription(wallet_info, mint_chain)
    await orb_inscriptions.mint_orbiter_inscription(dest_chains)


async def owlto_check_in(wallet_info):
    """
    Owlto daily check in. Send tx and press button on site
    ______________________________________________________

    ref - wallet address of referral
    """

    ref = "0xE022adf1735642DBf8684C05f53Fe0D8339F5663"

    owlto_inst = Owlto(wallet_info)
    await owlto_inst.check_in(ref)


async def custom_routes(wallet_info):
    """
    BRIDGE:
        – deposit_scroll
        – withdraw_scroll
        – bridge_orbiter
        – bridge_layerswap
        - bridge_rhinofi
        - bridge_nitro
        - bridge_relay
    WRAP:
        – wrap_eth
        – unwrap_eth
    DEX:
        – swap_skydrome
        – swap_syncswap
        – swap_zebra
        - swap_ambient
    LANDING:
        – depost_layerbank
        – withdraw_layerbank
        – deposit_rocketsam
        – withdraw_rocketsam
        - deposit_aave
        - withdraw_aave
    NFT/DOMAIN:
        – mint_zerius
        - bridge_nft_zerius
        – mint_zkstars
        – create_omnisea
        – mint_nft
    ANOTHER:
        – swap_multiswap
        – swap_tokens
        – send_mail (Dmail)
        – create_safe
        – deploy_contract
        - vote_rubyscore
        - check_in_secondlive
        - owlto_check_in

    If random_module = True and withdraw_okx in use_modules, withdraw_okx will always be executed first and
                       transfer_to_okx will be executed last
    ______________________________________________________
    Disclaimer - You can add modules to [] to select random ones,
    example [module_1, module_2, [module_3, module_4], module 5]
    The script will start with module 1, 2, then select a random one from module 3 and 4, and end with 5

    You can also specify None in [], and if None is selected by random, this module will be skipped

    You can also specify () to perform the desired action a certain number of times
    example (send_mail, 1, 10) run this module 1 to 10 times
    """

    use_modules = [withdraw_okx, automatic_routes]

    sleep_from = 30
    sleep_to = 60

    random_module = False

    routes_inst = Routes(wallet_info)
    await routes_inst.start(use_modules, sleep_from, sleep_to, random_module)


async def automatic_routes(wallet_info):
    """
    The module automatically generates the paths a wallet will take,
    changing the probabilities of selecting one or another module for each wallet
    ______________________________________________________
    transaction_count - number of transactions (not necessarily all transactions are executed, modules can be skipped)
    cheap_ratio - from 0 to 1, the share of cheap transactions when building a route
    cheap_modules - list of modules to be used as cheap ones
    expensive_modules - list of modules to be used as expensive ones
    use_none - adds probability to skip module execution
    """

    transaction_count = 6
    cheap_ratio = 1

    sleep_from = 1500
    sleep_to = 3600

    use_none = True
    cheap_modules = [send_mail, mint_zkstars, vote_rubyscore, mint_nft, check_in_secondlive]
    expensive_modules = [create_omnisea, create_safe, mint_zerius, deposit_aave]

    routes_inst = Routes(wallet_info)
    await routes_inst.start_automatic(transaction_count, cheap_ratio,
                                      sleep_from, sleep_to,
                                      cheap_modules, expensive_modules,
                                      use_none)


# -------------------------------------------- NO NEED TO SET UP MODULES

async def vote_rubyscore(wallet_info):
    """
    Vote in Scroll at Rubyscore
    """

    rubyscore_inst = Rubyscore(wallet_info)
    await rubyscore_inst.vote()


async def mint_zerius(wallet_info):
    """
    ONLY Mint Zerius NFT
    ______________________________________________________
    The Mint function should be called "mint", please check it
    """

    zerius_inst = Zerius(wallet_info)
    await zerius_inst.mint()


async def withdraw_layerbank(wallet_info):
    layerbank_inst = LayerBank(wallet_info)
    await layerbank_inst.withdraw()


async def send_mail(wallet_info):
    dmail_inst = Dmail(wallet_info)
    await dmail_inst.send_mail()


async def create_omnisea(wallet_info):
    omnisea_inst = Omnisea(wallet_info)
    await omnisea_inst.create()


async def nft_origins(wallet_info):
    nft = NftOrigins(wallet_info)
    await nft.mint()


async def create_safe(wallet_info):
    gnosis_safe = GnosisSafe(wallet_info)
    await gnosis_safe.create_safe()


async def deploy_contract(wallet_info):
    deployer = Deployer(wallet_info)
    await deployer.deploy_token()


async def check_in_secondlive(wallet_info):
    """
    Check-in on second live
    """
    second_live = SecondLive(wallet_info)
    await second_live.sign_in()


def get_tx_count():
    asyncio.run(check_tx())


def progress_check(wallets_data):

    replace = True
    check_eth = True

    Scan(wallets_data).get_wallet_progress(replace, check_eth=check_eth)
