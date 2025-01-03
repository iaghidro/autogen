import asyncio
import os
from dotenv import load_dotenv

from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage

load_dotenv()


async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        # model="gpt-4o-mini",
        model="o1-mini",
        api_key= os.environ.get("OPENAI_API_KEY")
    )

    agent = AssistantAgent(name="assistant", model_client=model_client, system_message=None)
    response = await agent.on_messages(
        [TextMessage(content="Plot a chart of META and TESLA stock price change. Install any necessary dependencies", source="user")],
        CancellationToken()
    )
    print(response)

asyncio.run(main())