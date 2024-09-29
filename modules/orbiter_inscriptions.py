import random

from loguru import logger
from config import ORBITER_CHAINS_INFO, LAYERZERO_WRAPED_NETWORKS, ORBITER_INSCRIPTIONS_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class OrbiterInscription(Account):
    def __init__(self, wallet_info, chain: str) -> None:
        super().__init__(wallet_info=wallet_info, chain=chain)

        self.contract_address = ORBITER_INSCRIPTIONS_CONTRACT

        self.name_to_chain_id = {
            "arbitrum": 1,
            "optimism": 31,
            "scroll": 35,
            "base": 7,
            "linea": 22,
            "polygon_zkevm": 34,
            "zksync": 43
        }

    @retry
    @check_gas
    async def mint_orbiter_inscription(self, dest_chains):

        dest_chain = random.choice(dest_chains)
        dest_chain = self.name_to_chain_id[dest_chain]

        to_chain_id = ORBITER_CHAINS_INFO[LAYERZERO_WRAPED_NETWORKS[dest_chain]]['id']
        to_chain_name = ORBITER_CHAINS_INFO[LAYERZERO_WRAPED_NETWORKS[dest_chain]]['name']

        logger.info(f'[{self.account_id}][{self.address}] Start mint inscription on Orbiter. '
                    f'Mint chain: {self.chain}. Dst chain: {to_chain_name}')

        destination_code = 9000 + to_chain_id

        value = int(0.00023 * 10 ** 18 + destination_code)

        tx_data = await self.get_tx_data(value=value)
        tx_data.update({
            'data': '0x' + 'data:,{"p":"layer2-20","op":"claim","tick":"$L2","amt":"1000"}'.encode('utf-8').hex(),
            'to': self.contract_address
        })

        await self.send_tx(tx_data)
