# pip install -U autogen-agentchat autogen-ext[openai,web-surfer]
# playwright install
import asyncio
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from shared.model_client import OpenAIModel, create_model_client
from aioconsole import ainput 

from shared.executors import CodingAgent

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    assistant = CodingAgent(
        name="assistant", 
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
    ).get_agent()
    
    web_surfer = MultimodalWebSurfer("web_surfer", model_client, headless=False)
    termination = TextMentionTermination("APPROVE") # Type 'exit' to end the conversation.
    team = RoundRobinGroupChat([web_surfer, assistant], termination_condition=termination)
    task = "Gather every page of the autogen 0.4 documentation and save to a file"
    while True:
        await Console(team.run_stream(task=task))
        task = await ainput("Enter your feedback (type 'exit' to leave): ")
        if task.strip().lower() == "exit":
            break

asyncio.run(main())