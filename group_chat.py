import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from shared.local_executor import create_local_code_executor
from shared.model_client import OpenAIModel, create_model_client

async def run_group_chat_with_human_intervention() -> None:
    # Create code executor agent
    code_executor_agent = CodeExecutorAgent(
        "code_executor",
        code_executor=create_local_code_executor()
    )

    # Create assistant agent
    assistant_agent = AssistantAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        system_message=None  # Omit system message for o1 models if used
    )

    # Create user proxy agent for human interaction
    user_proxy_agent = UserProxyAgent(
        name="user_proxy",
        input_func=input  # Uses the standard input function for human input
    )

    # Define a SelectorGroupChat
    agent_team = SelectorGroupChat(
        participants=[assistant_agent, code_executor_agent],
        termination_condition=TextMentionTermination("TERMINATE"),
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        max_turns=30,
    )

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(
        task="Create a chart of META and TESLA stock price changes. Save the chart to an image"
    )
    await Console(stream)

# Execute the human-in-the-loop group chat
asyncio.run(run_group_chat_with_human_intervention())
