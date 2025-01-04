from autogen_ext.models.openai import OpenAIChatCompletionClient
import os

def create_model_client(model: str):
    model_client = OpenAIChatCompletionClient(
        model=model,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    return model_client
