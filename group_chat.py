import tempfile
import os
import asyncio
import venv

from pathlib import Path
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from dotenv import load_dotenv

async def run_group_chat() -> None:
    # Create a code executor agent that executes locally
    work_dir = Path("coding")
    work_dir.mkdir(exist_ok=True)
    venv_dir = work_dir / ".venv"
    venv_builder = venv.EnvBuilder(with_pip=True)
    venv_builder.create(venv_dir)
    venv_context = venv_builder.ensure_directories(venv_dir)
    local_executor = LocalCommandLineCodeExecutor(work_dir=work_dir, virtual_env_context=venv_context)
    code_executor_agent = CodeExecutorAgent("code_executor", code_executor=local_executor)
    
    model_client = OpenAIChatCompletionClient(
        model="o1-mini",
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    # The system message is not supported by the o1 series model.
    assistantAgent = AssistantAgent(name="assistant", model_client=model_client, system_message=None)
    
    # Define termination condition
    termination = TextMentionTermination("TERMINATE")
    
    # Define a team
    agent_team = RoundRobinGroupChat([code_executor_agent,assistantAgent], termination_condition=termination, max_turns=30)

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(task="Plot a chart of META and TESLA stock price change. Install any necessary dependencies")
    await Console(stream)

asyncio.run(run_group_chat())