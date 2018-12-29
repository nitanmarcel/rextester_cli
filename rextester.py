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
        regex = re.search('^\$([\w.#+]+)\s+([\s\S]+?)(?:\s+\/stdin\s+([\s\S]+))?$', message, re.IGNORECASE)
        language = regex.group(1)
        code = regex.group(2)
        stdin = regex.group(3)



        try:
            regexter = Rextester(language, code, stdin)
        except CompilerError as exc:
            await event.edit(str(exc))
            return

        output = ""
        output += "**Language:**\n```{}```".format(language)
        output += "\n\n**Source:** \n```{}```".format(code)

        if regexter.result:
            output += "\n\n**Result:** \n```{}```".format(regexter.result)

        if regexter.warnings:
            output += "\n\n**Warnings:** \n```{}```\n".format(regexter.warnings)

        if regexter.errors:
            output += "\n\n**Errors:** \n'```{}```".format(regexter.errors)

        await event.edit(output)


with client:
    client.run_until_disconnected()
