from lib2to3.fixes.fix_input import context

from langchain_core.prompts import ChatPromptTemplate
import uuid
from pathlib import Path
from typing import Annotated, TypedDict, List

from dotenv import load_dotenv
from langchain_core.messages import AnyMessage
from langchain_core.messages.tool import ToolCall
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from model import create_llm
import dotenv

load_dotenv()


def load_system_prompt(filename: str, folder: Path = Path("./prompts")):
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path = Path("./inputs")):
    return (folder / filename).read_text()

# TODO: Anpassen des Output formats / Structured output langchain
class EmotionalAspect(BaseModel):
    """Represents a single thought-classification pair for an emotional aspect."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing the emotional aspect.")
    ]
    classification: Annotated[
        str,
        Field(description="Classify the emotional aspect based on the thought process, referencing contextual and theoretical insights.")
    ]
    score: Annotated[
        float,
        Field(description="Score from 0 to 1, low to high", ge=0, le=1)
    ]

class EmotionValence(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for emotion valence.")
    ]

class EmotionIntensity(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for analyzing the intensity of the emotion expressed.")
    ]

class ContextualRelevance(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for evaluating the relevance of the emotion in the given context.")
    ]

class EngagementLevel(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for assessing the level of engagement or involvement of the commenter.")
    ]

class EmotionRegulation(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification of emotion regulation strategies by the user.")
    ]

class Polarization(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for assessing polarization in emotional expressions, considering how extreme or divisive the emotions might be.")
    ]

class ClassificationOutput(BaseModel):
    """Aggregates all emotional aspect classes into a comprehensive schema."""
    emotion_valence: EmotionValence
    emotion_intensity: EmotionIntensity
    contextual_relevance: ContextualRelevance
    engagement_level: EngagementLevel
    emotion_regulation: EmotionRegulation
    polarization: Polarization


# TODO: Prompt mit Langchain bauen für Role play
def create_knowledge_query_translation():
    queries_schema = dereference_refs(ClassificationOutput.model_json_schema())
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

    chain = prompt | llm | PydanticOutputParser(pydantic_object=ClassificationOutput)

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
