import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from shared.local_executor import create_local_code_executor
from shared.model_client import OpenAIModel, create_model_client


async def run_group_chat() -> None:
    # create code executor agent
    code_executor_agent = CodeExecutorAgent(
        "code_executor", 
        code_executor=create_local_code_executor()
    )
    
    # create assistant agent (code writer)
    assistantAgent = AssistantAgent(
        name="assistant", 
        model_client=create_model_client(OpenAIModel.O1_MINI), 
        system_message=None # remove this if using the openai o1 series models
    )
    
    # Define a team
    agent_team = SelectorGroupChat(
        participants=[assistantAgent,code_executor_agent], 
        termination_condition=TextMentionTermination("TERMINATE"),
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI), 
        max_turns=30,
    )

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(
        task="Plot a chart of META and TESLA stock price change. save the chart to an image"
    )
    await Console(stream)


asyncio.run(run_group_chat())
