#!/bin/bash

cd "$(dirname "$0")"

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

echo "Виртуальное окружение создано и активировано, все зависимости установлены."

read -p "Нажмите любую клавишу для завершения..."
