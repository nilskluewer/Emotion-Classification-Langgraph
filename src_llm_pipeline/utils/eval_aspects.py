from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langsmith import Client
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import json
from datetime import datetime



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

llm_evaluator_prompt_text = read_prompts("prompt_evaluating_fluency.md")

class Coherence(BaseModel):
        score: int = Field(ge=0, le=100,
            description="Score of zero means 'incoherence' and score of one hundred means 'perfect Coherence'. Note that Coherence measures Incoherence.")


def openai_evaluator(step_1_classification, step_2_classification_summary, aspect = "Coherence"):    
    llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            max_tokens=8192,
            temperature=0.0,
            
        )
    # TODO ersetzten durch enum map 
    ant_aspect = "Incoherence"
    task_ins = "Summary of a in depth classification"
    aspect_inst = "the logical flow and clarity within the passage. Consider whether the passage maintains a logical sequence, clear connections between ideas, and an overall sense of understanding." 
    
    
    llm = llm.with_structured_output(Coherence)
    prompt = PromptTemplate.from_template(llm_evaluator_prompt_text)
    chain = prompt | llm
    
    response = chain.invoke({"task-ins": task_ins,
                             "aspect" : aspect,
                             "ant-aspect" : ant_aspect,
                             "aspect-inst": aspect_inst,
                             "step_1_classification": step_1_classification,
                             "step_2_classification_summary": step_2_classification_summary})
    


    print(response)
    score = response.score
    print(score)
    return score


#openai_evaluator(step_1_classification="The arousal is also variable.  During discussions about Semenya, the arousal level is high, indicated by stronger statements and emotionally charged language.  Comments on other topics like the blackout or the Ibiza scandal show less arousal.   Certain comments contain aggressive and emotionally intense language suggesting a high arousal state. Some comments are emotionally neutral, denoting a low arousal level.",
# step_2_classification_summary="The user's emotional expressions are highly context-dependent.  Strong negative emotions, characterized by high arousal and negative valence, are primarily observed in discussions regarding Caster Semenya, stemming from a rigid, biologically-essentialist view of gender and fairness in sports.  This interpretation significantly shapes their emotional responses.  In other contexts (e.g., power outages, political scandals), emotional responses exhibit lower arousal and fluctuating valence, indicating a more nuanced emotional range outside this specific issue. The user's emotional intensity seems to slightly decrease within the Semenya discussion thread.  Their engagement with various topics reveals awareness of Austrian social and political issues, influencing their emotional responses within those contexts.  The anonymity of the online forum potentially contributes to more direct expression of strong opinions.  Overall, the user's emotional experiences are demonstrably constructed through the interplay of core affect, cognitive appraisals, cultural context, and situational factors.\n")