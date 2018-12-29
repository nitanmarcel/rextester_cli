import logging
import re

from telethon import events
from telethon.sync import TelegramClient

from api.rextester import CompilerError, Rextester

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


api_id = 12345  # your api id here
api_hash = "abcd1234"  # your api hash here

client = TelegramClient("rextester", api_id, api_hash)


@client.on(events.NewMessage(outgoing=True, pattern="^\$"))
async def rextestercli(event):
    stdin = ""
    message = event.text

    if len(message.split()) > 1:
        language = re.search("\$([\w.#+]+)", message).group(1)
        code = re.search("\s([\s\S]+)", message).group(1)

        if "/stdin" in message:
            code = re.search("\s([\s\S]+)(?=/stdin)", message).group(1)
            stdin = re.search("\/stdin\s*([\s\S]+)", message).group(1)

        try:
            regexter = Rextester(language, code, stdin)
        except CompilerError as exc:
            await event.edit(str(exc))
            return

        output = ""
        output += "**Language:**\n`{}`".format(language)
        output += "**\n\nSource:**\n`{}`".format(code)

        if regexter.result:
            output += "\n\nResult:\n`{}`".format(regexter.result)

        if regexter.warnings:
            output += "\n\n**Warnings:**\n`{}`\n".format(regexter.warnings)

        if regexter.errors:
            output += "\n\n**Errors:**\n'{}`".format(regexter.errors)

        await event.edit(output)


with client:
    client.run_until_disconnected()
