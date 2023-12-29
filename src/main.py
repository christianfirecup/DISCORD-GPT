import discord
import BotFunctions as GPTBot
from dotenv import load_dotenv
import os

load_dotenv()
Assistant_Model = os.getenv('Assistant_OpenAI')
user_threads = {}
intents = discord.Intents.default()
intents.message_content = True
Discord_Client = discord.Client(intents=intents)

@Discord_Client.event
async def on_ready():
    print(f'We have logged in as {Discord_Client.user}')

@Discord_Client.event
async def on_message(User_Message):
    if User_Message.author == Discord_Client.user:
        return

    if GPTBot.On_Message_Captured(User_Message, '$hello'):
        await GPTBot.Responder_Message(User_Message, "Hello!")

    if GPTBot.On_Message_Captured(User_Message, '$ask'):
        await GPTBot.AI_Sender(User_Message, user_threads, Assistant_Model)

    if GPTBot.On_Message_Captured(User_Message, "$createdir"):
        await GPTBot.Create_UserDIR(User_Message)
    if GPTBot.On_Message_Captured(User_Message, "$nme"):
        await GPTBot.Responder_Message(User_Message, "Name Saved")

GPTBot.Run(os.getenv('DISCORD_TOKEN'), Discord_Client)
