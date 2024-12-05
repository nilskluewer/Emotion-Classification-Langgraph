from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langsmith import Client
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import json
from datetime import datetime
from langsmith.run_helpers import traceable
from enum import Enum

from enum import Enum

class Aspect(Enum):
    COHERENCE = (
        "Coherence",
        "Incoherence",
        "the logical flow and clarity within the passage. Consider whether the passage maintains a logical sequence, clear connections between ideas, and an overall sense of understanding."
    )
    RELEVANCE = (
        "Relevance",
        "Irrelevance",
        "how well the summarized emotion classification relates to the original in-depth classification. Does the summary accurately reflect the key emotional categories and their relationships identified in the classification?"
    )
    CONSISTENCY = (
        "Consistency",
        "Inconsistency",
        "whether the emotional categories and their assigned probabilities in the summary are consistent with the findings of the original in-depth classification. Are there any contradictions or inconsistencies between the two?"
    )
    HELPFULNESS = (
        "Helpfulness",
        "Unhelpfulness",
        "how useful the summarized emotion classification is for understanding the overall emotional tone of the text. Does it provide a clear and concise representation of the key emotions and their intensities?"
    )
    COMPREHENSIVENESS = (
        "Comprehensiveness",
        "Incompleteness",
        "whether the summary captures all the significant emotional categories and nuances identified in the original in-depth classification. Are there any important emotions or details missing from the summary?"
    )
    # Potentially add more aspects like:
    #  -  Bias (Fairness/Neutrality of the emotion classification)
    #  -  Confidence (Certainty expressed by the LLM in its classification)
    #  -  Specificity/Granularity (Level of detail in the emotion classification)


# TODO ander aspect typen adden
# TODO maybe critique einfügen das man auch weiß was laut model hätte besser sein können

class EvaluationResult(BaseModel):
    aspect: str
    score: bool = Field()
    reasoning: str = Field(description="The reasoning for the score. Max three sentences!")
    critique: str = Field(description="Suggested improvements to the summary. Short precise key points! Max. 3 points.")

class CoherenceEvaluation(EvaluationResult):
    aspect: str = "coherence" # fixed value

class RelevanceEvaluation(EvaluationResult):
    aspect: str = "relevance" # fixed value

class ConsistencyEvaluation(EvaluationResult):
    aspect: str = "consistency" # fixed value

class HelpfulnessEvaluation(EvaluationResult):
    aspect: str = "helpfulness" # fixed value

class ComprehensivenessEvaluation(EvaluationResult):
    aspect: str = "comprehensiveness" # fixed value

def load_config():
    config_path = './config.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

load_dotenv()
client = Client()

config = load_config()

client = Client()

dataset_tag = config["dataset_tag"]
delete_dataset = config["delete_dataset"]
model_name_eval = config["model_name_eval"]
prompts_version = config["prompt_version"]

dataset_tag = "default_dataset_2024-11-28:13:03:39"




def read_prompts(filename: str) -> str:
    """Load system prompt from file."""
    folder = Path(f"./inputs/prompts/{prompts_version}")
    return (folder / filename).read_text()

llm_evaluator_prompt_text = read_prompts("prompt_eval_aspects.md")
instructions_summary = read_prompts("step_2_summary_prompt.md")


@traceable(name="Evaluate Aspects", run_type="chain")
def aspect_evaluator(step_1_classification, step_2_classification_summary, aspect: Aspect,llm_model_name : str, run_tree_parent_id):    
    aspect, ant_aspect, aspect_inst = aspect.value
    task_ins = "summary of an in-depth classification"
    
    # Select the appropriate Pydantic model based on the aspect
    print("ASPECT:", aspect)
    if aspect == "Coherence":
        pydantic_model = CoherenceEvaluation
    elif aspect == "Relevance":
        pydantic_model = RelevanceEvaluation
    elif aspect == "Consistency":
        pydantic_model = ConsistencyEvaluation
    elif aspect == "Helpfulness":
        pydantic_model = HelpfulnessEvaluation
    elif aspect == "Comprehensiveness":
        pydantic_model = ComprehensivenessEvaluation
    else:
        raise ValueError(f"Aspect {aspect} not supported")
    
    # TODO: if model string start with gpt string then use the model name and use ChatOpenAi
    
    if llm_model_name.startswith("gpt"):
        llm = ChatOpenAI(
                model_name=llm_model_name,
                max_tokens=2000,
                temperature=0.0,
                
            )
    elif llm_model_name.startswith("claude"):
        llm = ChatAnthropic(
                model_name=llm_model_name,
                max_tokens=1000,
                temperature=0.0,
            )

    llm = llm.with_structured_output(pydantic_model)
    prompt = PromptTemplate.from_template(llm_evaluator_prompt_text)
    chain = (prompt | llm).with_config({"tags": [f"{aspect}"]})
    
    response = chain.invoke({"task-ins": task_ins,
                             "aspect" : aspect,
                             "ant-aspect" : ant_aspect,
                             "aspect-inst": aspect_inst,
                             "step_1_classification": step_1_classification,
                             "step_2_classification_summary": step_2_classification_summary,
                            "instructions_summary": instructions_summary})
    #print(response)
    print("The Score from OpenAi is:", response.score)
    print("The Reasoning from OpenAi is:", response.reasoning)
    print("The Critique from OpenAi is:", response.critique)
    
    client.create_feedback(
        run_id=run_tree_parent_id,
        key=aspect,
        value=response.critique,
        score=response.score,
        comment=response.reasoning,
        feedback_source_type="api",
        source_info={"model": llm_model_name}
    )
    return response

def aspect_evaluator_all_aspects(step_1_classification, step_2_classification_summary,llm_model_name : str, run_tree_parent_id):    
    for aspect in Aspect:
        aspect_evaluator(step_1_classification, step_2_classification_summary, aspect, llm_model_name, run_tree_parent_id, langsmith_extra={"tags": [f"{aspect}"]})