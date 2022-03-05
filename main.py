import asyncio
import json
import pprint
import sqlite3 as sq
from sys import exit

import uvicorn
from fastapi import FastAPI, Request
from httpx import AsyncClient
from pyngrok import ngrok
from validations import MessageBodyModel, ResponseToMessage

from COIN_MARKET_CAP import price_of_crypt
from DB import DataBase

TOKEN = "5141013666:AAFDkri_oHLhSxP5fbu0qFEAgm_BDwZ2Hn4"
TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
TELEGRAM_SET_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
HOST_URL = None

# https://github.com/FarukOzderim/Telegram-Bot-Python-FastAPI


app = FastAPI()

conn = sq.connect("messages.db")
conn.row_factory = sq.Row
dbase = DataBase(conn)

if TOKEN == "":
    exit("No secret found, exiting now!")


@app.get("/price")
def get_price(CRYPT: str, CURRENCY: str):
    price = price_of_crypt(CRYPT, CURRENCY)
    my_dict = {"from": f"{CRYPT}", "to": f"{CURRENCY}", "price": f"{price}"}
    return my_dict


async def save(received: dict, sent: dict):
    j1 = json.dumps(received)
    j2 = json.dumps(sent)
    await dbase.add_messages(j1)
    await dbase.add_messages(j2)


@app.post("/webhook/{TOKEN}")
async def post_process_telegram_update(message: MessageBodyModel, request: Request):
    try:
        mes = message.message.text
        crypt, currency = mes.split(" ")
        price = get_price(crypt, currency)["price"]
        my_dict = {"text": f"Цена {crypt} в {currency}: {price}", "chat_id": message.message.chat.id}
        await save(message.dict(), my_dict)
    except Exception as e:
        print(e)
        my_dict = {"text": "Извините, но вы что-то не так ввели!", "chat_id": message.message.chat.id}
    finally:
        js = ResponseToMessage(**my_dict)
        pprint.pprint(js)
        return js


async def request(url: str, payload: dict, debug: bool = False):
    async with AsyncClient() as client:
        request = await client.post(url, json=payload)
        if debug:
            print(request.json())
        return request


# async def send_a_message_to_user(telegram_id: int, message: str) -> bool:
#     message = ResponseToMessage(
#         **{
#             "text": message,
#             "chat_id": telegram_id,
#         }
#     )
#     req = await request(TELEGRAM_SEND_MESSAGE_URL, message.dict())
#     return req.status_code == 200


async def set_telegram_webhook_url() -> bool:
    payload = {"url": f"{HOST_URL}/webhook/{TOKEN}"}
    req = await request(TELEGRAM_SET_WEBHOOK_URL, payload)
    return req.status_code == 200


if __name__ == "__main__":

    PORT = 8000
    http_tunnel = ngrok.connect(PORT, bind_tls=True)
    public_url = http_tunnel.public_url
    HOST_URL = public_url

    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(set_telegram_webhook_url())
    if success:
        uvicorn.run("main:app", host="127.0.0.1", port=PORT, log_level="info")
    else:
        print("Fail, closing the app.")
