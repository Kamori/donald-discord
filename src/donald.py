import os

import discord

from util.brain import Brain
from util.person import Person
import logging
import signal
import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO)
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
donald = Person('./conf/donald.yml')
brain = Brain("./brain.brain")
channel = lambda: client.get_channel(int(os.environ["DONALD_DEFAULT_CHANNEL"]))
should_be_running = True

def signal_handler(sig, frame):
    global should_be_running
    print('You pressed Ctrl+C!')
    should_be_running = False

signal.signal(signal.SIGINT, signal_handler)


async def departure():
    await channel().send(donald.random_outro())
    await client.close()
  
async def arrival():
    await client.start(os.environ["DONALD_BOT_KEY"])

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print(channel())
    brain["general"] = str(channel().id)
    await channel().send(donald.random_greeting())

    while should_be_running:
        # time.sleep(2)
        await asyncio.sleep(2)

    await departure()
    await client.close()
    



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        await message.channel.send(donald.random_tagged_response())

    if 'reload' in message.content:
        donald.reload()


loop = asyncio.get_event_loop()
try:
  loop.run_until_complete(client.start(os.environ["DONALD_BOT_KEY"]))
finally:
    loop.close()