import asyncio
from autogen_agentchat.conditions import HandoffTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from shared.executors import CodingAgent

async def main():

    coding_agent = CodingAgent().get_agent()

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
