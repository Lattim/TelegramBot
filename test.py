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



@server.post("/bot{token}")
def bot_update(update: telebot.types.Update.de_json(BaseModel), request: Request, token: str):
    print(update)
