import discord
import BotFunctions as GPTBot
from dotenv import load_dotenv
import os

load_dotenv()

# No need for 'global' here as we're in the global scope already
Assistant_Model = os.getenv('Assistant_OpenAI')
user_threads = {}
intents = discord.Intents.default()
intents.message_content = True
Discord_Token = os.getenv('DISCORD_TOKEN')
Discord_Client = discord.Client(intents=intents)

@Discord_Client.event
async def on_ready():
    print(f'We have logged in as {Discord_Client.user}')

@Discord_Client.event
async def on_message(User_Message):
    # Since we're inside a function, we declare Assistant_Model as global if we plan to modify it
    global Assistant_Model

    if User_Message.author == Discord_Client.user:
        return

    if GPTBot.On_Message_Captured(User_Message, '$hello'):
        await GPTBot.Generic_Message(User_Message, "Hello!")

    if GPTBot.On_Message_Captured(User_Message, '$ask'):
        await GPTBot.AI_Message(User_Message, user_threads, Assistant_Model)

    if GPTBot.On_Message_Captured(User_Message, "$createdir"):
        await GPTBot.Create_UserDIR(User_Message)
    if GPTBot.On_Message_Captured(User_Message, "$CreateSave"):
        await GPTBot.Create_Dictonary(User_Message)
    if GPTBot.On_Message_Captured(User_Message, "$nme"):
        await GPTBot.Assign_User_Bot_Name(User_Message)
    if GPTBot.On_Message_Captured(User_Message, "$instruct"):
        await GPTBot.Assign_User_Bot_Instructions(User_Message)
    if GPTBot.On_Message_Captured(User_Message, "$LoadGPT"):
        new_model = await GPTBot.Load_Model(User_Message)
        if new_model is not None:
            Assistant_Model = new_model.id
            await GPTBot.Generic_Message(User_Message, f"Model updated to {Assistant_Model}")

# Run command
if __name__ == '__main__':
    GPTBot.Run(Discord_Token, Discord_Client)
