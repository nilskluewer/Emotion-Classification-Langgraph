from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import json

from langsmith.run_helpers import traceable
from src_llm_pipeline.utils.enums import Aspect

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
    config_path = Path('src_llm_pipeline/config.json')
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
    folder = Path(f"src_llm_pipeline/inputs/prompts/{prompts_version}")
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