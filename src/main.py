
import BotFunctions
from dotenv import load_dotenv
import os


load_dotenv()

import discord
Assistant_Model = os.getenv('Assistant')
user_threads = {}
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

    if BotFunctions.MessageContent(message,'$hello'):
        await BotFunctions.sendmessge(message, "Hello!")

    if BotFunctions.MessageContent(message,'$ask'):
        await BotFunctions.AIBotSender(message, user_threads, Assistant_Model)

    if BotFunctions.MessageContent(message, "$createdir"):
        await BotFunctions.BotCreateAssistant("test", None, None, None, message)


Disclient.run(os.getenv('TOKEN'))
