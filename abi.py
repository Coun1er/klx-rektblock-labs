import os

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_dir, "data/abi/position_abi.json"), "r") as f:
    POSITION_ABI = f.read()

with open(os.path.join(current_dir, "data/abi/erc20_abi.json"), "r") as f:
    ERC20_ABI = f.read()
