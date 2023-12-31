import asyncio
import OpenAIFunctions as AIAPI
import os
import json


def On_Message_Captured(User_Message, Check):
    return User_Message.content.startswith(Check)

async def Generic_Message(User_Message, response):
    return await User_Message.channel.send(response)

async def Create_UserDIR(User_Message):
        await Generic_Message(User_Message, 'Creating Dir')
        user_id = User_Message.author.id
        directory_path = os.path.join('src', str(user_id))
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        await Generic_Message(User_Message, 'To Start Creating Your GPT Run $CreateSave So You Can Write Save Data To The Bot')

def Run(Discord_Token, Discord_Client):
    Discord_Client.run(Discord_Token)

async def Create_Dictonary(User_Message):
    user_id = User_Message.author.id
    user_data = {
        "user_id": user_id,
        "bot_name": "None",
        "instructions": "None"
    }
    directory_path = os.path.join('src', str(user_id))  # The directory path within 'src'
    if os.path.exists(directory_path) and not os.listdir(directory_path):
        file_path = os.path.join(directory_path, f"{user_id}_data.json")  # Path for the data file
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
        await Generic_Message(User_Message, "Data saved successfully. Run $nme [BOTNAMEHERE] to name your new Assistant")
    else:
        await Generic_Message(User_Message, "You didn't create your directory. Or You Ran This Twice Run $nme [BOTNAMEHERE] to name your new Assistant")

async def Assign_User_Bot_Name(User_Message):
    user_id = User_Message.author.id
    file_path = os.path.join('src', str(user_id), f"{user_id}_data.json")
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            user_data = json.load(file)
        user_data["bot_name"] = User_Message.content[5:]
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
        await Generic_Message(User_Message, "Name Updated")
    else:
        await Generic_Message(User_Message, "Save Data Does Not Exist")

async def Assign_User_Bot_Instructions(User_Message):
    user_id = User_Message.author.id
    file_path = os.path.join('src', str(user_id), f"{user_id}_data.json")
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            user_data = json.load(file)
        user_data["instructions"] = User_Message.content[10:]
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
        await Generic_Message(User_Message, "instructions Updated")
    else:
        await Generic_Message(User_Message, "Save Data Does Not Exist")
async def Load_Model(User_Message):
    await Generic_Message(User_Message, "Loading Attempt 1")
    user_id = User_Message.author.id
    directory_path = os.path.join('src', str(user_id))  # The directory path within 'src'
    if os.path.exists(directory_path) and os.listdir(directory_path):
        file_path = os.path.join('src', str(user_id), f"{user_id}_data.json")
        with open(file_path, 'r') as file:
            user_data = json.load(file)
        if user_data["bot_name"] != None:
            if user_data["instructions"] != None:
                await Generic_Message(User_Message, "LOAD SUCCESS")
                return AIAPI.Create_Assistant(user_data["bot_name"], user_data["instructions"],[{"type": "code_interpreter"}], "gpt-4-1106-preview")
        else:
            await Generic_Message(User_Message, "COULD NOT LOAD SAVE DATA PLEASE CREATE IT IF YOU HAVENT")
            return None





async def AI_Message(User_Message, user_threads, Assistant_Model):
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
