# Kiloex Farmer
![Title img](https://private-user-images.githubusercontent.com/12481719/324258400-b5db17b8-7763-4792-8504-aae6df4367e6.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTM3MTMzNTgsIm5iZiI6MTcxMzcxMzA1OCwicGF0aCI6Ii8xMjQ4MTcxOS8zMjQyNTg0MDAtYjVkYjE3YjgtNzc2My00NzkyLTg1MDQtYWFlNmRmNDM2N2U2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA0MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNDIxVDE1MjQxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTVhMTE3MTgzOTMyMmE3Yzk4MDZjZTBlOWM5YWUzYzQ4ZTcxYjAwNjRjZjlkMTE0NDYwNmNiNjhhMjI3OTQ1NWUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.GQxL3ZsPYAmtu74IX37LyZZCynpU_ZtdEbF_OyjKC34)

### Быстрый запуск
- качаем себе через `git clone <url>` или просто через `Download ZIP`
- открываем папку со скаченым скриптом
- все настройки проводятся в файле `config.py`, первый раз просто запускаем на дефолтных

![config img](https://private-user-images.githubusercontent.com/12481719/324258433-0ffd7399-d84d-4d3b-9efc-1f9003f97332.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTM3MTMzNTgsIm5iZiI6MTcxMzcxMzA1OCwicGF0aCI6Ii8xMjQ4MTcxOS8zMjQyNTg0MzMtMGZmZDczOTktZDg0ZC00ZDNiLTllZmMtMWY5MDAzZjk3MzMyLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA0MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNDIxVDE1MjQxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTlkZmFiYWUzMjE3ODJhMTBjNDdiYzBjZDA5ZDUxMGU1MDBkZjAwMmQ4OWI3NmE4YWQwODVkYTBhZjFiZTE5NzcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.0t6JSPcPZIgQMBoE4_ctb_cx8IpzB_sRrWrgcDD22nY)

#### Windows(если будут ошибки, смотри видос)
- python 3.11.8 или выше
- ложим в pk.txt свои приватники
- запускаем INSTALL.bat для установки всех зависимостей
- запускаем START.bat для запуска

#### Mac os or Linux (fast)
- python 3.11.8 или выше
- ложим в pk.txt свои приватники
- запускаем `./install.sh` для установки всех зависимостей
- запускаем `./start.sh` для запуска скрипта

#### Mac os or Linux (hard)
- python 3.11.8 или выше
- ложим в pk.txt свои приватники
- создаем виртуальное окружение `python3 -m venv env`
- активируем его `. ./env/bin/activate`
- устанавливаем зависимости `pip install -r requirements.txt`
- запускаем `python main.py`