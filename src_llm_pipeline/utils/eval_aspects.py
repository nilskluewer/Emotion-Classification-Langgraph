from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
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



@traceable(name="Evaluate Confabulation", run_type="chain")
def hallucination_confabulation_evaluator(question, answer, run_tree_parent_id):
    eval_prompt = read_prompts("prompt_eval_confabulation.md")
    eval_prompt = PromptTemplate.from_template(eval_prompt)
    
    #eval_prompt = eval_prompt.format(question=question, answer=answer)

    
    class ConfabulationEvaluation(BaseModel):
        explanation: str = Field(description="Short explanation if there is confabulation. Based on the given queustion and corresponding answer. Provde the 1:1 text example confabulation is present Keep the initial question given in mind when thinking about confabulation.")
        scale_rating: int =  Field(description="The rating of the confabulation on a scale from 1 to 10. 1 means no confabulation, 10 means high confabulation. The score should ONLY reflect the aspect of confabulation.")
        #confabulated: bool = Field(description="True if the answer is confabulated, False otherwise.")
    
    
    llm_A = ChatOpenAI(
            model_name="gpt-4o",
            max_tokens=2000,
            temperature=0.0,
            
        )
    llm_B = ChatAnthropic(
            model_name="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=0.0,
        )
    
    llm_C = ChatAnthropic(
            model_name="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.0,
        )
    
    llm_D = ChatVertexAI(
            model_name="gemini-1.5-flash-002",
            max_tokens=1000,
            temperature=0.0,
        
    )
    
    
    llm_A_structured = llm_A.with_structured_output(ConfabulationEvaluation)
    llm_B_structured = llm_B.with_structured_output(ConfabulationEvaluation)
    llm_C_structured = llm_C.with_structured_output(ConfabulationEvaluation)
    llm_D_structured = llm_D.with_structured_output(ConfabulationEvaluation)
    
    chain_A = (eval_prompt | llm_A_structured ).with_config({"tags": ["confabulation"]})
    chain_B = (eval_prompt | llm_B_structured).with_config({"tags": ["confabulation"]})
    chain_C = (eval_prompt | llm_C_structured).with_config({"tags": ["confabulation"]})
    chain_D = (eval_prompt | llm_D_structured).with_config({"tags": ["confabulation"]})
    
    response_A = chain_A.invoke({"question": question, "answer": answer})
    response_B = chain_B.invoke({"question": question, "answer": answer})
    response_C = chain_C.invoke({"question": question, "answer": answer})
    response_D = chain_D.invoke({"question": question, "answer": answer})
    
    print(response_A)
    print(response_B)
    print(response_C)
    print(response_D)
    
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_A.explanation,
        score=response_A.scale_rating,
        feedback_source_type="api",
        source_info={"model": "gpt-4o"}
    )
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_B.explanation,
        score=response_B.scale_rating,
        feedback_source_type="api",
        source_info={"model": "claude-3-5-haiku-20241022"}
    )
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_C.explanation,
        score=response_C.scale_rating,
        feedback_source_type="api",
        source_info={"model": "claude-3-5-sonnet-20241022"}
    )
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_D.explanation,
        score=response_D.scale_rating,
        feedback_source_type="api",
        source_info={"model": "gemini-flash-experimental"}
    )

    return True

def aspect_evaluator_all_aspects(step_1_classification, step_2_classification_summary,llm_model_name : str, run_tree_parent_id):    
    for aspect in Aspect:
        aspect_evaluator(step_1_classification, step_2_classification_summary, aspect, llm_model_name, run_tree_parent_id, langsmith_extra={"tags": [f"{aspect}"]})
        
        

if __name__ == "__main__":
    #aspect_evaluator_all_aspects()
    hallucination_confabulation_evaluator("What is the capital of France?", "The capital of France is Paris.") 
