from lib2to3.fixes.fix_input import context

from langchain_core.prompts import ChatPromptTemplate
import uuid
from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AnyMessage
from langchain_core.messages.tool import ToolCall
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from model import create_llm
import dotenv


def load_system_prompt(filename: str, folder: Path = Path(__file__).parent):
    return (folder / filename).read_text()

# TODO: Anpassen des Output formats / Structured output langchain
class Classification(BaseModel):
    inner_monologue: Annotated[
        str,
        Field(
            description="Show how you come to conlucsion. Whats in your mind? What is the reason for the given answer"
        ),
    ]
    context_dependent_analysis: Annotated[
        list[str],
        Field(description="""The output should reflect not just the isolated comment, but its place within the broader discussion. For example, "User A's comment expresses frustration, likely in response to the previous comment's dismissive tone towards the article's main argument."""),
    ]
    emotion_granularity: Annotated[
        str,
        Field(description="Assess the user's ability to differentiate emotions. E.g., 'User shows high emotional granularity, distinguishing between frustration and disappointment.'"),
    ]
    emotion_concepts: Annotated[
        list[str],
        Field(description="Identify the emotion concepts the user is drawing upon. E.g., 'User employs complex emotion concepts, blending 'Schadenfreude' with moral indignation.'"),
    ]
    situational_context: Annotated[
        list[str],
        Field(description="Consider broader situational factors influencing the emotional response. E.g., 'User's frustration likely influenced by recent economic downturn affecting job security.'"),
    ]
    emotion_regulation: Annotated[
        str,
        Field(description="Identify any emotion regulation strategies evident in the comment. E.g., 'User appears to be using cognitive reappraisal to manage anger, reframing the situation more positively.'"),
    ]
    dimensional_assessment: Annotated[
        list[str],
        Field(description="""Rather than just labeling emotions, the output should indicate the valence and intensity. For instance, "Comment shows moderate negative valence, with an intensity of 7/10 on the anger dimension."""),
    ]
    probabilistic_classification: Annotated[
        list[str],
        Field(description="""Instead of definitive labels, the output should express probabilities. For example, "70% confidence in primary emotion of disappointment, with 30% possibility of underlying anxiety."""),
    ]
    individual_user_patterns: Annotated[
        list[str],
        Field(description="""The analysis should note how a user's current emotional expression compares to their typical baseline. For instance, 'User B's comment shows unusually high intensity of joy compared to their typical neutral stance in political discussions.'"""),
    ]
    cultural_context: Annotated[
        list[str],
        Field(description="""The output should acknowledge Austrian-specific factors. For example, 'User's sarcasm likely references recent political events in Vienna, suggesting frustration with local governance.'"""),
    ]
    flexible_interpretation: Annotated[
        list[str],
        Field(description="""The analysis should be presented as a working hypothesis, open to revision. For instance, 'Initial assessment suggests anger, but this interpretation may evolve with further context from subsequent comments in the thread.'"""),
    ]


# TODO: Prompt mit Langchain bauen für Role play
def create_knowledge_query_translation():
    queries_schema = Classification.model_json_schema()

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

    chain = prompt | llm | PydanticOutputParser(pydantic_object=Classification)

    return chain


if __name__ == "__main__":
    chain = create_knowledge_query_translation()
    context_sphere = load_system_prompt("user_30537_threads_cleaned.md")
    result = chain.invoke({"context_sphere": context_sphere})
    print("\n ----- \n")
    print(result)
