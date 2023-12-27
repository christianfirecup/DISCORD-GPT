import asyncio

from dotenv import load_dotenv
import os
import OpenaiFunctions as AIAPI

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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$ask'):
        user_id = message.author.id
        print(user_id)

        if user_id not in user_threads:
            newthread = AIAPI.CreateThread()
            user_threads[user_id] = newthread.id
        try:
            thread_id = user_threads[user_id]
            AIAPI.NewMessage(message.content[5:], thread_id)  # Skip the "$ask " part
            newrun = AIAPI.CreateRun(thread_id, Assistant_Model)
            response = AIAPI.result(thread_id, newrun.id)

            # Split the response into 2000-character chunks
            chunks = [response[i:i + 1900] for i in range(0, len(response), 1900)]

            # Send each chunk in a separate message
            for chunk in chunks:
                await message.channel.send(chunk)
                await asyncio.sleep(1)  # Optional: slight delay between messages

        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")


Disclient.run(os.getenv('TOKEN'))
