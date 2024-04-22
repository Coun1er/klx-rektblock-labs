import asyncio
import random

from web3 import AsyncHTTPProvider, AsyncWeb3

from abi import ERC20_ABI
from config import settings
from logs import logger


class Default:
    def __init__(self, private_key: str) -> None:
        self.w3 = AsyncWeb3(AsyncHTTPProvider(settings.rpc))

        self.private_key = private_key

        self.address = self.w3.eth.account.from_key(self.private_key).address

        self.erc20_abi = ERC20_ABI

        self.infinite = 115792089237316195423570985008687907853269984665640564039457584007913129639935

    async def verif_tx(self, tx: str) -> bool:
        try:
            data = await self.w3.eth.wait_for_transaction_receipt(tx, timeout=300)

            if data.get("status") is not None and data.get("status") == 1:
                logger.success(f'{data.get("from")}: Успешно! Tx:{tx.hex()}')
                return True

            else:
                logger.error(
                    f'{data.get("from")}: Произошла ошибка! {data.get("transactionHash").hex()} {tx.hex()}'
                )

                return False

        except Exception as e:
            logger.error(f"{tx.hex()} произошла ошибка! Error: {e}")

            return False

    async def random_sleep(self, sleep_time: list, description: str = ""):
        random_time = random.randint(sleep_time[0], sleep_time[1])

        logger.info(f"{self.address}: Спим {random_time} сек: {description}")

        await asyncio.sleep(random_time)

    async def get_allowance(self, token_address: str, spender: str = None) -> int:
        contract_address = self.w3.to_checksum_address(
            self.w3.to_checksum_address(token_address)
        )

        contract_instance = self.w3.eth.contract(
            address=contract_address, abi=self.erc20_abi
        )

        return await contract_instance.functions.allowance(self.address, spender).call()

    async def approve(self, token_address: str, spender: str) -> bool:
        nonce = await self.w3.eth.get_transaction_count(self.address)

        contract_address = self.w3.to_checksum_address(
            self.w3.to_checksum_address(token_address)
        )

        contract_instance = self.w3.eth.contract(
            address=contract_address, abi=self.erc20_abi
        )

        gas = await contract_instance.functions.approve(
            spender,
            115792089237316195423570985008687907853269984665640564039457584007913129639935,
        ).estimate_gas({"from": self.address, "nonce": nonce, "value": 0})

        tx = {
            "from": self.address,
            "nonce": nonce,
            "gasPrice": int(await self.w3.eth.gas_price * 1.3),
            "value": 0,
            "chainId": await self.w3.eth.chain_id,
            "gas": gas,
        }

        transaction = await contract_instance.functions.approve(
            spender,
            115792089237316195423570985008687907853269984665640564039457584007913129639935,
        ).build_transaction(tx)

        try:
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, private_key=self.private_key
            )

            raw_tx_hash = await self.w3.eth.send_raw_transaction(
                signed_txn.rawTransaction
            )

            status = await self.verif_tx(raw_tx_hash)

            return status

        except Exception as e:
            logger.error(f"{self.address} {e}")

            return False

    async def get_decimals(self, token_address: str) -> int:
        contract_address = self.w3.to_checksum_address(token_address)

        contract_instance = self.w3.eth.contract(
            address=contract_address, abi=self.erc20_abi
        )

        return await contract_instance.functions.decimals().call()

    async def token_conver_from_wei(self, amount: int, token_address: str) -> int:
        decimals = await self.get_decimals(token_address=token_address)

        return amount / (10**decimals)

    async def get_balance(self):
        return await self.w3.eth.get_balance(self.address)

    async def get_token_balance(self, token_address: str) -> int:
        contract_address = self.w3.to_checksum_address(token_address)

        contract_instance = self.w3.eth.contract(
            address=contract_address, abi=self.erc20_abi
        )

        return await contract_instance.functions.balanceOf(self.address).call()
