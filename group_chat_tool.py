import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_core import CancellationToken
from autogen_agentchat.conditions import HandoffTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.code_executor import CodeBlock
from autogen_agentchat.base import Handoff

from shared.executors import create_local_code_executor
from shared.model_client import OpenAIModel, create_model_client

async def main():
    
    async def execute_code(code: str) -> str:
        executor = create_local_code_executor() 
        cancellation_token = CancellationToken()  # Create a cancellation token
        code_block = CodeBlock(code,language="python")
        result = await executor.execute_code_blocks([code_block], cancellation_token)
        return result
    
    assistant_agent = AssistantAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        system_message="You are a helpful AI assistant capable of writing, executing code and installing necessary libraries/packages. Solve tasks using your tools. Only hand off to the user if you're stuck after many attempts or have completed the task.",
        tools=[execute_code],
        handoffs=[Handoff(target="user", message="Transfer to user.")],
    )

    team = RoundRobinGroupChat(
        participants=[assistant_agent],
        termination_condition=HandoffTermination(target="user"),
    )

    task = "Create a chart of META and TESLA stock price changes. Save the chart to an image, and don't open the file."
    # task = "generate a pdf for the autogen documentation. Crawl all pages under this base url: https://microsoft.github.io/autogen/0.4.0.dev13"
    while True:
        # Run the conversation and stream messages to console
        await Console(team.run_stream(task=task))
        # Get next user feedback
        task = input("Enter your feedback (type 'exit' to leave): ")
        if task.strip().lower() == "exit":
            break

asyncio.run(main())