
import tempfile
import os
from dataclasses import dataclass

from autogen_core import SingleThreadedAgentRuntime, DefaultTopicId
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
# from assistant_agent import Assistant, Executor, Message, DefaultTopicId


@dataclass
class Message:
    content: str
    
work_dir = tempfile.mkdtemp()

# Create an local embedded runtime.
runtime = SingleThreadedAgentRuntime()

import asyncio

async def main():
    async with DockerCommandLineCodeExecutor(work_dir=work_dir) as executor:  # type: ignore[syntax]
        # Register the assistant and executor agents by providing
        # their agent types, the factory functions for creating instance and subscriptions.
        await AssistantAgent.register(
            runtime,
            "assistant",
            lambda: AssistantAgent(
                OpenAIChatCompletionClient(
                    model="gpt-4o",
                    api_key= os.environ.get("OPENAI_API_KEY"),
                )
            ),
        )
        await CodeExecutorAgent.register(runtime, "executor", lambda: CodeExecutorAgent(executor))

        # Start the runtime and publish a message to the assistant.
        runtime.start()
        await runtime.publish_message(
            Message("Create a plot of NVIDA vs TSLA stock returns YTD from 2024-01-01. save a screenshot as an image"), DefaultTopicId()
        )
        await runtime.stop_when_idle()

asyncio.run(main())