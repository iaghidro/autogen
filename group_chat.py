import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from shared.local_executor import create_local_code_executor

from dotenv import load_dotenv

load_dotenv()

async def run_group_chat() -> None:
    local_executor = create_local_code_executor()
    code_executor_agent = CodeExecutorAgent("code_executor", code_executor=local_executor)
    
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    # The system message is not supported by the o1 series model.
    assistantAgent = AssistantAgent(name="assistant", model_client=model_client, system_message=None)
    
    termination_condition = TextMentionTermination("TERMINATE")
    
    # Define a team
    agent_team = SelectorGroupChat(
        participants=[assistantAgent,code_executor_agent], 
        termination_condition=termination_condition,
        model_client=model_client, # todo: use o1
        max_turns=30
    )

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(task="Plot a chart of META and TESLA stock price change. save the chart to an image")
    await Console(stream)

asyncio.run(run_group_chat())
