from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI'))


def CreateAssistant(names, instructions1, tools1, model1):
    return client.beta.assistants.create(
        name=names,
        instructions=instructions1,
        tools=tools1,
        model=model1

    )


def CreateThread():
    return client.beta.threads.create()


def NewMessage(usermessage, threadid):
    return client.beta.threads.messages.create(
        thread_id=threadid,
        role="user",
        content=usermessage

    )


def CreateRun(threadID, AssistantID):
    return client.beta.threads.runs.create(
        thread_id=threadID,
        assistant_id=AssistantID,

    )


def result(threadID, runId, ):
    received = False
    while not received:

        # Retrieve the latest run status
        results = client.beta.threads.runs.retrieve(
            thread_id=threadID,
            run_id=runId
        )

        # Check if the run is completed
        if results.status == 'completed':

            messages = client.beta.threads.messages.list(thread_id=threadID)
            for message in messages.data:
                role = message.role
                content = message.content[0].text.value
                received = True
                return f"GPTBOT: {content}"


if __name__ == "__main__":
    newthread = CreateThread()
    NewMessage("What is your objective", newthread.id)
    newrun = CreateRun(newthread.id, "asst_Mv3MzfjZUw4pIUT8jvgWwbMP")
    print(result(newthread.id, newrun.id))
