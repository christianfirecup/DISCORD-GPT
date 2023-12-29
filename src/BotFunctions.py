import asyncio
import OpenAIFunctions as AIAPI
import os


def On_Message_Captured(User_Message, Check):
    return User_Message.content.startswith(Check)

async def Responder_Message(User_Message, response):
    return await User_Message.channel.send(response)

async def Create_UserDIR(User_Message):
        await Responder_Message(User_Message, 'Creating Dir')
        user_id = User_Message.author.id
        if not os.path.exists(str(user_id)):
            os.mkdir(str(user_id))
        await Responder_Message(User_Message, 'To name Your Bot Please Run $nme YOUR BOT NAME HERE. To Stop Creating Your Bot Please type Anything Else')

def Run(Discord_Token, Discord_Client):
    Discord_Client.run(Discord_Token)

async def AI_Sender(User_Message, user_threads, Assistant_Model):
    user_id = User_Message.author.id

    if user_id not in user_threads:
        New_Thread = AIAPI.Create_Thread()
        user_threads[user_id] = New_Thread.id
    try:
        thread_id = user_threads[user_id]
        AIAPI.New_Message(User_Message.content[5:], thread_id)  # Skip the "$ask " part
        New_Run = AIAPI.Create_Run(thread_id, Assistant_Model)
        response = AIAPI.Grab_Result(thread_id, New_Run.id)

        # Split the response into 2000-character chunks
        chunks = [response[i:i + 1900] for i in range(0, len(response), 1900)]

        # Send each chunk in a separate message
        for chunk in chunks:
            await User_Message.channel.send(chunk, reference=User_Message)
            await asyncio.sleep(1)  # Optional: slight delay between messages

    except Exception as e:
        await User_Message.channel.send(f"An error occurred: {e}")
