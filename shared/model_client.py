from autogen_ext.models.openai import OpenAIChatCompletionClient
from enum import Enum
import os

class OpenAIModel(Enum):
    GPT_4 = "gpt-4"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    O1_MINI = "o1-mini"

def create_model_client(model: OpenAIModel):
    model_client = OpenAIChatCompletionClient(
        model=model.value,
        api_key=os.environ.get("OPENAI_API_KEY"),
        cache=False,
        # temperature=0.3,
        max_retries=8,
        retry_delay=2,
        timeout=70,
    )
    return model_client
