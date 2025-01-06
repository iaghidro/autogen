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
        code_block = CodeBlock(code,language="python")
        return await executor.execute_code_blocks([code_block], CancellationToken())
    
    assistant_agent = AssistantAgent(
        name="assistant",
        model_client=create_model_client(OpenAIModel.GPT_4O_MINI),
        description="A helpful and general-purpose AI assistant that has strong language skills, Python skills, and Linux command line skills.",
        system_message="You are a helpful AI assistant.\nSolve tasks using your coding and language skills.\nIn the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.\n    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.\n    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.\nSolve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.\nWhen using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can\'t modify your code. So do not suggest incomplete code which requires users to modify. Don\'t use a code block if it\'s not intended to be executed by the user.\nIf you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don\'t include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use \'print\' function for the output when relevant. Check the execution result returned by the user.\nIf the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can\'t be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.\nWhen you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.\n Only hand off to the user if you're stuck after many attempts or have completed the task.",
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