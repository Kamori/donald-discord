import os

import discord

from util.brain import Brain

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    channel = client.get_channel(os.environ["DONALD_DEFAULT_CHANNEL"])
    brain = Brain("brain.brain")
    brain["general"] = str(dir(channel))
    # await channel.send('Should I even exist?')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


client.run(os.environ["DONALD_BOT_KEY"])
