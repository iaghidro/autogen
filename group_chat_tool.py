import asyncio
from autogen_agentchat.conditions import HandoffTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from shared.model_client import OpenAIModel, create_model_client
from autogen_agentchat.base import Handoff

from shared.executors import CodingAgent

async def main():

    coding_agent = CodingAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        handoffs=[Handoff(target="user", message="Transfer to user.")]
        ).get_agent()

    team = RoundRobinGroupChat(
        participants=[coding_agent],
        termination_condition=HandoffTermination(target="user"),
    )

    task = "Create a chart of META and TESLA stock price changes. Save the chart to an image, and don't open the file."
    while True:
        await Console(team.run_stream(task=task))
        task = input("Enter your feedback (type 'exit' to leave): ")
        if task.strip().lower() == "exit":
            break

asyncio.run(main())
