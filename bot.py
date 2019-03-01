import logging
import re

from telethon import events
from telethon.sync import TelegramClient

from api.langs import languages
from api.rextester import UnknownLanguage, rexec

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


api_id = 123456  # your api id here
api_hash = "1a2b3cde4f5g7hjk"  # your api hash here

client = TelegramClient("rextester", api_id, api_hash)


@client.on(
    events.NewMessage(
        outgoing=True,
        pattern=r"^\!([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$",
        func=lambda e: e.pattern_match.group(1) in languages))
async def rextestercli(event):
    stdin = ""
    match = event.pattern_match

    group_len = 0
    if len(match.group().split()) > 1:
        language = match.group(1)
        code = match.group(2)
        stdin = match.group(3)

        res = await rexec(language, code, stdin)

        output = "**Language:**\n```{}```".format(language)
        output += "\n\n**Source:**\n```{}```".format(code)

        if res.results:
            output += "\n\n**Result:**\n```{}```".format(res.results)

        elif res.warnings:
            output += "\n\n**Warnings:**\n```{}```\n".format(res.warnings)

        elif res.errors:
            output += "\n\n**Errors:**\n'```{}```".format(res.errors)
        else:
            output += "\n\n **Status:**\n`Success`"

        await event.edit(output)


with client:
    client.run_until_disconnected()
