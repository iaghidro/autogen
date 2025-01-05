import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import HandoffTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.base import Handoff

from shared.executors import create_local_code_executor
from shared.model_client import OpenAIModel, create_model_client

async def run_group_chat_with_human_intervention() -> None:
    code_executor_agent = CodeExecutorAgent(
        name="code_executor",
        code_executor= create_local_code_executor(),
    )

    assistant_agent = AssistantAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        handoffs=[Handoff(target="user", message="Transfer to user.")],
        system_message=
            "You are a helpful AI assistant with a code executor at your disposal."
             "ONLY transfer to user as a last resort: when you're stuck after several attempts at fixing it or the task is complete"
    )
    
    team = RoundRobinGroupChat(
        participants=[assistant_agent, code_executor_agent],
        termination_condition= HandoffTermination(target="user"),
    )

    # Run the team and stream messages
    task = "Create a chart of META and TESLA stock price changes. Save the chart to an image, and don't open the file."
    while True:
        # Run the conversation and stream to the console.
        await Console(team.run_stream(task=task))
        # Get the user response.
        task = input("Enter your feedback (type 'exit' to leave): ")
        if task.lower().strip() == "exit":
            break

asyncio.run(run_group_chat_with_human_intervention())

            
# "You are a helpful AI assistant capable of many things especially coding, executing code and installing necessary libraries/modules."
# "ONLY transfer to user as a last resort: when you don't know the answer and you're stuck after several tries or the task is complete."