from importlib.resources import contents

import vertexai
from langchain_google_vertexai import ChatVertexAI, HarmBlockThreshold, HarmCategory
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

vertexai.init(project="rd-ri-genai-dev-2352", location="europe-west4")

def create_llm(
    model_name: str,
    max_retries: int = 1,
    safety_settings: dict[HarmCategory, HarmBlockThreshold] | None = None,
    **kwargs,
):
    if model_name.startswith("gemini"):
        return ChatVertexAI(
            model_name=model_name,
            location="europe-west1",
            max_retries=max_retries,
            max_tokens=8192,
            safety_settings=safety_settings or default_safety_settings,
            **kwargs,
        )


    if model_name.startswith("claude"):
        return ChatAnthropic(
            model=model_name,
            max_tokens=8192,
            timeout=None,
            max_retries=3,
            **kwargs,
        )

    if model_name.startswith("gpt-"):
        return ChatOpenAI(
            model=model_name,
            max_tokens=8192,
            max_retries=2,
            **kwargs
        )

    else:
        raise ValueError(f"No model init strategy for model_name: {model_name}")
    


default_safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
}
