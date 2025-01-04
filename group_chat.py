import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

from shared.executors import create_docker_executor
from shared.model_client import OpenAIModel, create_model_client

SELECTOR_PROMPT = """
You are the selector. You must choose the next speaker from {participants}.
Current conversation:
{history}

The following roles are available:\n{roles}
Rules:
1. If the last message contains the phrase "REQUEST_USER", select user_proxy.
2. If the last message contains "APPROVE", the conversation is finished. Do not select anyone.
3. Otherwise, if the conversation isn't finished, keep letting the assistant or code_executor speak to each other.
   - Typically, if the assistant needs to run code, it calls code_executor next.
   - If code_executor has responded and there's more to do, choose assistant next.
   - The assistant can speak to itself as well.
4. DO NOT choose code_executor unless there is code to be executed.
5. DO NOT choose user_proxy unless the last message contains "REQUEST_USER".
6. If there are errors thrown related to issues with API calls select user_proxy.
7. Output only the role name of the next speaker, or nothing if we are done.
"""

async def run_group_chat_with_human_intervention() -> None:
    # Create code executor agent
    code_executor_agent = CodeExecutorAgent(
        name="code_executor",
        code_executor= await create_docker_executor(),
    )

    # Create assistant agent
    assistant_agent = AssistantAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        # Advise the assistant to only mention REQUEST_USER if it cannot proceed or needs user approval
        system_message=(
            "You are a helpful assistant especially coding with access to 'code_executor'. Install any necessary libraries using the code_executor."
            "You only mention 'REQUEST_USER' if you are stuck and have attempted a fix at least 30 times. DO NOT request user for library installations"
            "If you're completely finished without user approval, say 'REQUEST_USER'."
            "If you mention 'REQUEST_USER', provide a reason in the following format: REQUEST_USER: <reason>"
        )
    )

    # Create user proxy agent
    user_proxy_agent = UserProxyAgent(
        name="user_proxy",
        input_func=input  # standard console input
    )

    # Define a SelectorGroupChat with a custom prompt
    agent_team = SelectorGroupChat(
        participants=[assistant_agent, code_executor_agent, user_proxy_agent],
        termination_condition=TextMentionTermination("APPROVE"),
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        max_turns=None,
        selector_prompt=SELECTOR_PROMPT,
    )

    # Run the team and stream messages
    stream = agent_team.run_stream(
        task="Create a chart of META and TESLA stock price changes. Save the chart to an image."
    )
    await Console(stream)

# Execute
asyncio.run(run_group_chat_with_human_intervention())
