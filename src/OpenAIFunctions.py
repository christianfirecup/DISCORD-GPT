from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI'))
def Create_Assistant(name, instructions, tools, model):
    return client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools,
        model=model

    )
def Create_Thread():
    return client.beta.threads.create()


def New_Message(usermessage, threadID):
    return client.beta.threads.messages.create(
        thread_id=threadID,
        role="user",
        content=usermessage

    )
def Create_Run(threadID, AssistantID):
    return client.beta.threads.runs.create(
        thread_id=threadID,
        assistant_id=AssistantID,

    )
def Grab_Result(threadID, runID):
    received = False
    while not received:

        # Retrieve the latest run status
        results = client.beta.threads.runs.retrieve(
            thread_id=threadID,
            run_id=runID
        )

        # Check if the run is completed
        if results.status == 'completed':

            messages = client.beta.threads.messages.list(thread_id=threadID)
            for message in messages.data:
                role = message.role
                content = message.content[0].text.value
                received = True
                return f"GPTBOT: {content}"


