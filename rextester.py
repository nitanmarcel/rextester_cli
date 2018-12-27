import asyncio
import logging

import requests
from telethon import TelegramClient, events

from langs import dict

api_id = 12345  # your api id here
api_hash = ""  # your api hash here
client = TelegramClient("rextester", api_id, api_hash)


RUN_URL = "https://rextester.com/rundotnet/api"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


@client.on(events.NewMessage(outgoing=True, pattern="^\$([\w.#+]+)\s+([\s\S]+)"))
async def rextestercli(event):
    lang = event.pattern_match.group(1)
    source = event.pattern_match.group(2)
    if lang in dict:
        langcode = dict[lang]

        data = {"LanguageChoice": langcode, "Program": source}

        request = requests.post(RUN_URL, data=data)
        response = request.json()

        if response["Result"]:
            output = "**Result:**\n\n`{}`".format(response["Result"])
        elif response["Errors"]:
            output = "**Errors:**\n\n`{}`".format(response["Errors"])
        elif response["Warnings"]:
            output = "**Warnings:**\n\n`{}`".format(response["Warnings"])
        else:
            await event.edit("Did you forget to output something?")

        await event.edit(
            "**Language:**\n`{}`\n\n**Source:**\n`{}`\n\n{}".format(lang, source, output)
        )
    else:
        await event.edit("Unknown language")


async def RunClient():
    await client.start()
    await client.get_me()
    await client.run_until_disconnected()


loop = asyncio.get_event_loop()
loop.run_until_complete(RunClient())
