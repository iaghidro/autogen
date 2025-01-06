
import venv
from pathlib import Path
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_core import CancellationToken
from autogen_core.code_executor import CodeBlock

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
