import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_dir, "data/product_list.json"), "r") as f:
    PRODUCT_LIST = json.loads(f.read())

with open(os.path.join(current_dir, "data/trading_pairs.json"), "r") as f:
    TRADING_PAIRS = json.loads(f.read())
