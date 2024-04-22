import sys

from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    enqueue=True,
    format="<white>{time:YYYY-MM-DD HH:mm:ss}</white> | <level>{message}</level>",
)

head_text = """
 _  ___ _                   _____
| |/ (_) | ___   _____  __ |  ___|_ _ _ __ _ __ ___   ___ _ __
| ' /| | |/ _ \ / _ \ \/ / | |_ / _` | '__| '_ ` _ \ / _ \ '__|
| . \| | | (_) |  __/>  <  |  _| (_| | |  | | | | | |  __/ |
|_|\_\_|_|\___/ \___/_/\_\ |_|  \__,_|_|  |_| |_| |_|\___|_|

 ____  _____ _  _______   ____  _     ___   ____ _  __ 
|  _ \| ____| |/ /_   _| | __ )| |   / _ \ / ___| |/ /
| |_) |  _| | ' /  | |   |  _ \| |  | | | | |   | ' /
|  _ <| |___| . \  | |   | |_) | |__| |_| | |___| . \\
|_| \_\_____|_|\_\ |_|   |____/|_____\___/ \____|_|\_\\

 _        _    ____ ____
| |      / \  | __ ) ___|
| |     / _ \ |  _ \___ \\
| |___ / ___ \| |_) |__) |
|_____/_/   \_\____/____/


"""


bold = "\033[1m"

green = "\033[32m"

yellow = "\033[33m"

red = "\033[31m"

blue = "\033[34m"

grey = "\033[90m"

cyan = "\033[96m"

ml = "\033[95m"

reset = "\033[0m"


def color_position_type(position_type: str):
    color = green if position_type == "LONG" else red

    return f"{color}{position_type}{reset}"


def color_trading_pair(trading_pair: str):
    return f"{blue}{trading_pair}{reset}"


def color_green(text: str):
    return f"{green}{text}{reset}"


def color_cyan(text: str):
    return f"{bold}{cyan}{text}{reset}"


def color_yellow(text: str):
    return f"{yellow}{text}{reset}"


def color_ml(text: str):
    return f"{ml}{text}{reset}"
