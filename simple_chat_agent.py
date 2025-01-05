import os
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

model = "gpt-4o-mini"
llm_config = {
    "model": model,
    "api_key": os.environ.get("OPENAI_API_KEY"),
    "cache_seed": None
}


assistant = AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="TERMINATE",  
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

user_proxy.initiate_chat(
    assistant, message="Create a chart of META and TESLA stock price changes. Save the chart to an image, and don't open the file."
)
