# Описание

Бот для дискорда, умеющий считать словами до определенной цифры.
К примеру на фразу "count to 20", бот начнет считать "one", "two", и так до "twenty". Промежуток между ответами - одна секунда.


# Виртуальное окружение
Рекомендую использовать виртуальное окружение. Создать его можно командой:
```shell
python3 -m venv bot-env
```
Активация происходит командой:

Для Linux:
```shell
source bot-env/bin/activate
```
Для Windows (актвировать лучше в старом CMD, т.к. в PowerShell виртуальное окружение не активируется):
```shell
bot-env\Scripts\activate.bat
```


# Зависимости и запуск
В зависимостях только discord.py и inflect, для их установки выполнить:
```shell
pip3 install -r requirements.txt
```
Перед запуском бота нужно в файле `config.py` у строчки `bot_token = ''` в кавычки вставить токен бота.

Инструкция как получить токен - https://discordpy.readthedocs.io/en/stable/discord.html

Для запуска выполнить:
```shell
python3 main.py
```
