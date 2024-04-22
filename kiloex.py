import binascii
import random

import aiohttp

from abi import POSITION_ABI
from config import settings
from data import PRODUCT_LIST, TRADING_PAIRS
from default import Default
from helper import retry
from logs import (
    color_cyan,
    color_green,
    color_position_type,
    color_trading_pair,
    color_yellow,
    logger,
)


class Kiloex(Default):
    def __init__(self, private_key: str) -> None:
        super().__init__(private_key)
        self.position_abi = POSITION_ABI

    async def get_current_token_price(self, tiker: str):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={tiker}USDT"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return float(data["price"])

    def conver_to_kilo(self, amount: int):
        return amount * (10**8)

    def convert_to_hex(self, input_string):
        hex_string = binascii.hexlify(input_string.encode()).decode()

        padded_hex_string = hex_string.ljust(64, "0")

        return padded_hex_string

    def get_kiloex_data(self, id: int):
        for bath in PRODUCT_LIST["productList"]:
            if bath["productId"] == id:
                if not bath["isActive"]:
                    raise Exception("Пара с текущим id не активна.")

                return bath

        raise Exception(
            "Не получилось найти нужный id. Проверьте правильность id и повторите запрос."
        )

    def get_tradig_pairs_id(self, trading_pair: str):
        for item in TRADING_PAIRS:
            if item["ticker_id"] == trading_pair:
                return item["contract_index"], item["base_currency"]

        raise ValueError(f"Переданная торговая пара '{trading_pair}' не найдена.")

    @retry
    async def create_position(
        self, amount_for_trading, position_type_str, product_id, first_tiker_trade
    ):
        amount = self.w3.to_wei(0.000007, "ether")

        contract_instance = self.w3.eth.contract(
            address=settings.position_contract_address, abi=self.position_abi
        )

        if position_type_str == "LONG":
            acceptable_price = (
                await self.get_current_token_price(tiker=first_tiker_trade) * 1.01
            )

        else:
            acceptable_price = (
                await self.get_current_token_price(tiker=first_tiker_trade) * 0.99
            )

        data = contract_instance.encodeABI(
            "createIncreasePosition",
            args=[
                product_id,
                self.conver_to_kilo(amount_for_trading),
                self.conver_to_kilo(settings.leverage),
                True if position_type_str == "LONG" else False,
                int(self.conver_to_kilo(acceptable_price)),
                amount,
                self.w3.to_bytes(
                    hexstr="73706c6179657200000000000000000000000000000000000000000000000000"
                ),
            ],
        )

        tx = {
            "chainId": await self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "gasPrice": await self.w3.eth.gas_price,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "to": settings.position_contract_address,
            "value": amount,
        }

        tx.update({"gas": await self.w3.eth.estimate_gas(tx)})

        try:
            signed_txn = self.w3.eth.account.sign_transaction(
                tx, private_key=self.private_key
            )

            raw_tx_hash = await self.w3.eth.send_raw_transaction(
                signed_txn.rawTransaction
            )

            status = await self.verif_tx(raw_tx_hash)

            return status

        except Exception as e:
            logger.error(e)

    @retry
    async def close_position(
        self, amount_for_trading, position_type_str, product_id, first_tiker_trade
    ):
        amount = self.w3.to_wei(0.000007, "ether")

        contract_instance = self.w3.eth.contract(
            address=settings.position_contract_address, abi=self.position_abi
        )
        if position_type_str == "LONG":
            acceptable_price = (
                await self.get_current_token_price(tiker=first_tiker_trade) * 0.99
            )
        else:
            acceptable_price = (
                await self.get_current_token_price(tiker=first_tiker_trade) * 1.01
            )

        data = contract_instance.encodeABI(
            "createDecreasePosition",
            args=[
                product_id,
                self.conver_to_kilo(amount_for_trading),
                True if position_type_str == "LONG" else False,
                int(self.conver_to_kilo(acceptable_price)),
                amount,
            ],
        )

        tx = {
            "chainId": await self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "gasPrice": await self.w3.eth.gas_price,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "to": settings.position_contract_address,
            "value": amount,
        }

        tx.update({"gas": await self.w3.eth.estimate_gas(tx)})

        try:
            signed_txn = self.w3.eth.account.sign_transaction(
                tx, private_key=self.private_key
            )

            raw_tx_hash = await self.w3.eth.send_raw_transaction(
                signed_txn.rawTransaction
            )

            status = await self.verif_tx(raw_tx_hash)

            return status

        except Exception as e:
            logger.error(e)

    async def run(self):
        balance_opBNB = self.w3.from_wei(await self.get_balance(), "ether")

        balance_usdt_raw = await self.get_token_balance(
            token_address=settings.usd_token_address
        )

        balance_usdt = await self.token_conver_from_wei(
            amount=balance_usdt_raw, token_address=settings.usd_token_address
        )

        logger.info(
            f"{self.address}: {color_yellow(f'{balance_opBNB} opBNB')} | {color_green(f'{balance_usdt} USDT')}"
        )

        allowance = await self.get_allowance(
            token_address=settings.usd_token_address,
            spender=settings.position_contract_address,
        )

        if allowance < self.infinite:
            logger.info(f"{self.address}: Апрувим токен перед стартом.")

            await self.approve(
                token_address=settings.usd_token_address,
                spender=settings.position_contract_address,
            )

        volume, iter = 0, 0

        while True:
            balance_raw = await self.get_token_balance(
                token_address=settings.usd_token_address
            )

            balance = await self.token_conver_from_wei(
                amount=balance_raw, token_address=settings.usd_token_address
            )

            if balance < settings.min_balance:
                logger.error(
                    f"{self.address}: На кошельке баланс {balance} USD - это меньше минимально установленого баланса {settings.min_balance} USD"
                )

                break

            trading_pair = random.choice(settings.trading_pairs)

            position_type_str = random.choice(settings.trading_positions_type)

            amount_for_trading_raw = (
                int(balance_raw * settings.margin_percent)
                if int(balance_raw * settings.margin_percent) > 1000000000
                else 1000000000
            )

            amount_for_trading = int(
                await self.token_conver_from_wei(
                    amount=amount_for_trading_raw,
                    token_address=settings.usd_token_address,
                )
            )

            product_id, first_tiker_trade = self.get_tradig_pairs_id(
                trading_pair=trading_pair
            )

            logger.info(
                f"{self.address}: Открываем {color_position_type(position_type_str)} на {color_trading_pair(trading_pair)} {amount_for_trading} USD с {settings.leverage} плечëм ({amount_for_trading * settings.leverage} usd позиция)"
            )

            await self.create_position(
                amount_for_trading=amount_for_trading,
                position_type_str=position_type_str,
                product_id=product_id,
                first_tiker_trade=first_tiker_trade,
            )

            await self.random_sleep(
                sleep_time=settings.sl_inside_trades,
                description=f"внутри {color_position_type(position_type_str)} на {color_trading_pair(trading_pair)} {amount_for_trading} USD с {settings.leverage} плечëм ({amount_for_trading * settings.leverage} usd позиция).",
            )

            logger.info(
                f"{self.address}: Закрываем {color_position_type(position_type_str)} на {color_trading_pair(trading_pair)} {amount_for_trading} USD с {settings.leverage} плечëм ({amount_for_trading * settings.leverage} usd позиция)."
            )

            await self.close_position(
                amount_for_trading=amount_for_trading,
                position_type_str=position_type_str,
                product_id=product_id,
                first_tiker_trade=first_tiker_trade,
            )

            volume += amount_for_trading * settings.leverage
            iter += 1

            logger.info(
                f"{self.address}: {color_green(f'Успешно закончили {iter} круг.')} {color_cyan(f'Всего накручено объема: {volume} USD.')}"
            )

            await self.random_sleep(
                sleep_time=settings.sl_between_trades, description="между трейдами."
            )
