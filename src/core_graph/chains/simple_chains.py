from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

_ = load_dotenv()


def grade_emotionality():
    class GradeEmotionality(BaseModel):
        """Reason on how Emotional the given context is. After that give a Score on how you would rate the emotionality"""

        reasoning: str = Field(
            description="Reason on the emotionality of the given context."
        )
        score: str = Field(
            description="Score between 0 and 100 on how Emotional the given context is."
        )


    # LLM with function call
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeEmotionality)

    # Prompt
    system = """You are a grader assessing the extend of emtionality in a given context. \n
    1. You first reason in about 5-10 Sentences why this context, or if the given context is emotional. \n
    2. Give a Score between 0 and 100 how emotional the context is."""
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Context: \n\n <context>{context}</context> \n\n"),
        ]
    )

    emotionality_grader = hallucination_prompt | structured_llm_grader
    return emotionality_grader
