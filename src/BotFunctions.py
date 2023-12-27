import asyncio
import OpenaiFunctions as AIAPI
import os


async def BotCreateAssistant(names, instructions1, tools1, model1, message):
    user_id = message.author.id
    os.mkdir("/"+user_id)

async def AIBotSender(message, user_threads, Assistant_Model):
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
            await message.channel.send(chunk, reference=message)
            await asyncio.sleep(1)  # Optional: slight delay between messages

    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")
