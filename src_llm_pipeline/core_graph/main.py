import importlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm

# Load environment variables
load_dotenv()

# Dynamically import the module
models = importlib.import_module("data_models")


def load_system_prompt(filename: str, folder: Path = Path("./prompts")):
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path = Path("./inputs")):
    return (folder / filename).read_text()



# TODO: Prompt mit Langchain bauen für Role play
def create_knowledge_query_translation():
    queries_schema = dereference_refs(models.ClassificationOutput.model_json_schema())
    queries_schema.pop("$defs", None)

    prompt = ChatPromptTemplate(
        [
            ("human", load_system_prompt("LFB_role_setting_prompt.md")),
            ("ai", load_system_prompt("LFB_role_feedback_prompt.md")),
            ("human", load_system_prompt("user_task_prompt.md"))
        ]
    ).partial(context_sphere = "context_sphere")




    # TODO: Create llm müssen wir mit langchain machen da wir mehre modelle nehmen wollen!
    llm = create_llm(
        model_name="gemini-1.5-pro-001",
        temperature=0.5,
        response_mime_type="application/json",
        response_schema=queries_schema,
    )

    chain = prompt | llm | PydanticOutputParser(pydantic_object=models.ClassificationOutput)

    return chain


if __name__ == "__main__":
    chain = create_knowledge_query_translation()
    context_sphere = load_input("user_118399_threads_cleaned.md")
    result = chain.invoke({"context_sphere": context_sphere})
    print("\n ----- \n")
    print(result)



"""
class DimensionalAssessment(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification based on the valence and intensity of the emotion.")
    ]


class CulturalContext(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification of emotion in the context of Austrian cultural factors.")
    ]

class FlexibleInterpretation(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification stating a working hypothesis open to revision.")
    ]
    """
