"""
Implementation of bot telegrams on the tops using the FastApi.

by Lattimerya
"""
import configparser
import os
import time
from typing import Optional
import ipaddress

from fastapi import FastAPI, Request, status
from pydantic import BaseModel
import telebot
import uvicorn

# Creating constants
MAIN_DIRECTORY = os.getcwd()
PATH_TO_CONFIG = MAIN_DIRECTORY + "/config.ini"

CONFIG = configparser.ConfigParser()
CONFIG.read(PATH_TO_CONFIG, encoding="utf-8")

HOST = CONFIG['SERVER']['WEBHOOK_HOST']
PORT = CONFIG['SERVER']['WEBHOOK_PORT']

SSL_CERT = MAIN_DIRECTORY + CONFIG['SSL']['SSL_CERT']
SSL_KEY = MAIN_DIRECTORY + CONFIG['SSL']['SSL_KEY']

WEBHOOK_URL = f"https://{HOST}:{PORT}/bot{CONFIG['BOT']['TOKEN']}"

IPs = []
for el in CONFIG['TELEGRAM']:
    IPs.append(CONFIG['TELEGRAM'][el])
SUBNETs = []
MASKs = []
for ip in IPs:
    SUBNETs.append(ip[:ip.find("/")])
    MASKs.append(ip[ip.find("/"):])

# Creating basic objects
server = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
bot = telebot.TeleBot(CONFIG['BOT']['TOKEN'])

# Setup WebHooks on the server
with open(SSL_CERT, 'r') as certificate:
    bot.delete_webhook()
    time.sleep(0.9)
    bot.set_webhook(url=WEBHOOK_URL, certificate=certificate)


class WebHookUpdate(BaseModel):
    """
    Creating a basic data model that telegram sends as an update.
    """
    update_id: int
    message: Optional[dict] = None
    edited_message: Optional[dict] = None
    inline_query: Optional[dict] = None
    chosen_inline_result: Optional[dict] = None
    callback_query: Optional[dict] = None


# Receiving POST requests from Telegram servers
@server.post("/bot{token}")
def bot_update(update: WebHookUpdate, request: Request):
    """
    Get a POST request using the method specified in the decorator.
    Check the IP of the incoming request.
    Use the :param token: to determine which bot received the update.
    :param message:
    :param request:
    :param token:
    :return:
    """
    for mask in MASKs:
        host = request.client.host + mask
        network = ipaddress.IPv4Network(host, strict=False)
        net_adr = network.network_address
        if str(net_adr) in SUBNETs:
            dictionary = update.dict()
            update = telebot.types.Update.de_json(dictionary)
            bot.process_new_updates([update])
            return status.HTTP_200_OK
    return status.HTTP_403_FORBIDDEN


# A simple example of bot actions
@bot.message_handler(commands='start')
def first_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Ave!")


if __name__ == "__main__":
    uvicorn.run("main:server",
                host=HOST,
                port=int(PORT),
                ssl_keyfile=SSL_KEY,
                ssl_certfile=SSL_CERT
                )
 