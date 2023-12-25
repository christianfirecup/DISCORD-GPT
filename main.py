from dotenv import load_dotenv
import os
load_dotenv()

import discord

intents = discord.Intents.default()
intents.message_content = True
Disclient = discord.Client(intents=intents)

@Disclient.event
async def on_ready():
    print(f'We have logged in as {Disclient.user}')

@Disclient.event
async def on_message(message):
    if message.author == Disclient.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$ask'):
        await message.channel.send("Processing Request")


Disclient.run(os.getenv('TOKEN'))