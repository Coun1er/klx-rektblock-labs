#!/bin/bash

 cd "$(dirname "$0")"

source ./env/bin/activate

python main.py

read -p "Нажмите любую клавишу для завершения..."
