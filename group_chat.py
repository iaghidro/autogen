import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

from shared.executors import create_local_code_executor
from shared.model_client import OpenAIModel, create_model_client

async def run_group_chat_with_human_intervention() -> None:
    # Create code executor agent
    code_executor_agent = CodeExecutorAgent(
        name="code_executor",
        code_executor= create_local_code_executor(),
    )

    # Create assistant agent
    assistant_agent = AssistantAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
    )

    # Define a SelectorGroupChat with a custom prompt
    team = RoundRobinGroupChat(
        participants=[assistant_agent, code_executor_agent],
        termination_condition=TextMentionTermination("APPROVE"),
        max_turns=15,
    )

    # Run the team and stream messages
    task = "Create a chart of META and TESLA stock price changes. Save the chart to an image, and don't open the file."
    while True:
        # Run the conversation and stream to the console.
        stream = team.run_stream(task=task)
        # Use asyncio.run(...) when running in a script.
        await Console(stream)
        # Get the user response.
        task = input("Enter your feedback (type 'exit' to leave): ")
        if task.lower().strip() == "exit":
            break

# Execute
asyncio.run(run_group_chat_with_human_intervention())
