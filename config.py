from web3.auto import w3


class Settings:
    # rpc
    rpc: str = "https://opbnb-rpc.publicnode.com"

    position_contract_address = w3.to_checksum_address(
        "0xa02d433868c7ad58c8a2a820d6c3ff8a15536acc"
    )

    usd_token_address = w3.to_checksum_address(
        "0x9e5aac1ba1a2e6aed6b32689dfcf62a509ca96f3"
    )

    # Торговые пары на которых будем торговать. Если пар больше 1, то на каждый трейд пара берется рандомно.
    trading_pairs = ["ETH-USDT", "BTC-USDT"]

    # В какую сторону вставать в позицию, если указаны обе стороны, то каждый раз берется рандомно.
    trading_positions_type = ["LONG", "SHORT"]

    # Сколько спим между трейдами.
    sl_between_trades = [10, 20]

    # Сколько спим внутри трейда между открытием и закрытием позиции.
    sl_inside_trades = [30, 60]

    # Плечё - минимальное = 2, максимальное = 100.
    leverage = 10

    # Процент от баланса который будет использоваться для фарминга.
    margin_percent = 0.2

    # Сумма usdt при которой фарминг остановится, минимум = 10.
    min_balance = 10


settings = Settings()
