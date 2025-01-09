import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.base import Handoff
from autogen_agentchat.conditions import HandoffTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from shared.executors import create_local_code_executor
from shared.model_client import OpenAIModel, create_model_client

async def main():
    code_executor_agent = CodeExecutorAgent(
        name="code_executor",
        code_executor=create_local_code_executor(),
    )
    assistant_agent = AssistantAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        handoffs=[Handoff(target="user", message="Transfer to user.")],
        system_message="You are a helpful AI assistant. Only hand off to the user if you're stuck after several attempts or have completed the task."
    )

    team = RoundRobinGroupChat(
        participants=[assistant_agent, code_executor_agent],
        termination_condition=HandoffTermination(target="user"),
    )

    task = "Create a chart of META and TESLA stock price changes. Save the chart to an image, and don't open the file."
    while True:
        # Run the conversation and stream messages to console
        await Console(team.run_stream(task=task))
        # Get next user feedback
        task = input("Enter your feedback (type 'exit' to leave): ")
        if task.strip().lower() == "exit":
            break

asyncio.run(main())