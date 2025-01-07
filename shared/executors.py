
import venv
from pathlib import Path
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
from autogen_core.code_executor import CodeBlock

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff
from shared.model_client import OpenAIModel, create_model_client

from typing import List, Optional
def create_local_code_executor():
    work_dir = Path("coding")
    work_dir.mkdir(exist_ok=True)
    venv_dir = work_dir / ".venv"
    venv_builder = venv.EnvBuilder(with_pip=True)
    venv_builder.create(venv_dir)
    venv_context = venv_builder.ensure_directories(venv_dir)
    local_executor = LocalCommandLineCodeExecutor(work_dir=work_dir, virtual_env_context=venv_context)
    return local_executor

async def execute_code(code: str) -> str:
    executor = create_local_code_executor() 
    code_block = CodeBlock(code, language="python")
    return await executor.execute_code_blocks([code_block], CancellationToken())

async def create_docker_executor():
    code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
    await code_executor.start()
    return code_executor

class SoftwareEngineerAgent:
    def __init__(
        self,
        name: str = "assistant",
        model_client=None,
        description: str = "A helpful and general-purpose AI assistant that has strong language skills, Python skills, and Linux command line skills.",
        system_message: str = """
You are a helpful AI assistant. Solve tasks using your coding executor tool.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for execution.
Use shell for system commands such as installing libraries and managing the environment, and python for everything else.
1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, 
print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and 
the task is ready to be solved based on your language skill, you can solve the task by yourself.
2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which 
step uses your language skill.
When using code, you must indicate the script type in the code block. Do not suggest incomplete code which requires modification. 
Don't use a code block if it's not intended to be executed. When you write code to be executed place in a file, put # filename: <filename> inside the code block. 
Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the 
output when relevant. Check the execution result returned.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. 
If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, 
collect additional info you need, and think of a different approach to try. Repeat this problem solving technique several times before giving up.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Hand off to the user only as a last resort—either after multiple failed attempts to fix the issue using different approaches or upon fully completing the task.
        """,
        tools: List = [execute_code],
        handoffs: List = [Handoff(target="user", message="Transfer to user.")],
    ):
        if model_client is None:
            model_client = create_model_client(OpenAIModel.GPT_4O_MINI)
        
        self.agent = AssistantAgent(
            name=name,
            model_client=model_client,
            description=description,
            system_message=system_message,
            tools=tools,
            handoffs=handoffs,
        )

    def get_agent(self):
        return self.agent
