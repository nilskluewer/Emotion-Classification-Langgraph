import importlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm
from langsmith import Client, traceable
from langsmith.run_helpers import get_current_run_tree
import os
from typing import List
from uuid import UUID
from data_models import EmotionAnalysisOutput, BasicNeed
import csv
from datetime import datetime
import time

path_folder = Path("./inputs/sample_24_09_27__12_58_size_20_tokens_1000_to_3000")

# Load environment variables
load_dotenv()

# Dynamically import the module
models = importlib.import_module("data_models")

def load_system_prompt(filename: str, folder: Path = Path("./prompts")):
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path = path_folder):
    return (folder / filename).read_text()

def run_llm_chain(context_sphere: str, user_id: str):
    @traceable(metadata={"user_id": user_id})
    def invoke_chain():
        llm_chain = LLM_chain()
        result = llm_chain.invoke({"context_sphere": context_sphere})
        time.sleep(20)
        run = get_current_run_tree()
        print(f"run_llm_chain Run Id: {run.id}")
        return result, run.id
    return invoke_chain()

def LLM_chain():
    queries_schema = dereference_refs(models.EmotionAnalysisOutput.model_json_schema())
    queries_schema.pop("$defs", None)

    prompt = ChatPromptTemplate(
        [
            ("human", load_system_prompt("LFB_role_setting_prompt.md")),
            ("ai", load_system_prompt("LFB_role_feedback_prompt.md")),
            ("human", load_system_prompt("user_task_prompt.md"))
        ]
    ).partial(context_sphere="context_sphere")

    llm = create_llm(
        model_name="gemini-1.5-pro-002",
        temperature=1,
        response_mime_type="application/json",
        response_schema=queries_schema,
    )

    chain = prompt | llm | PydanticOutputParser(pydantic_object=models.EmotionAnalysisOutput)

    return chain

def provide_feedback(client: Client, run_id: UUID, analysis_name: str, classification: str, thought: str):
    """
    Simplified feedback mechanism to include only the classification result.
    """
    client.create_feedback(
        run_id=run_id,
        key=f"{analysis_name}_analysis",
        value=f"{classification}",
        comment=f"{thought}"
    )



import csv
import os
from typing import List

def save_emotion_analysis_to_csv(emotion_analysis: EmotionAnalysisOutput, user_id: str, timestamp: str, filename: str = "emotion_analysis.csv"):
    file_exists = os.path.isfile(filename)

    # Get all possible BasicNeed values
    all_basic_needs = [need.value for need in BasicNeed]

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            header = [
                "Timestamp", "User ID",
                "Core Affect Thought", "Valence", "Arousal",
                "Emotional Aspect Thought", "Emotional Aspect Classification", "Context", 
                "Cognitive Appraisal", "Conceptualization", "Cultural Influence",
                "Predictions and Simulations", "Emotional Dynamics",
                "Emotional Blend Thought", "Emotional Blend Classifications",
                "User Need Thought"
            ] + all_basic_needs  # Add all basic needs as separate columns
            writer.writerow(header)
        
        # Prepare the basic needs flags
        basic_needs_flags = [1 if need in emotion_analysis.user_need_analysis.basic_needs else 0 for need in all_basic_needs]

        row = [
            timestamp, user_id,
            emotion_analysis.core_affect_analysis.thought,
            emotion_analysis.core_affect_analysis.valence,
            emotion_analysis.core_affect_analysis.arousal,
            emotion_analysis.emotional_aspect_extended.thought,
            emotion_analysis.emotional_aspect_extended.classification,
            emotion_analysis.emotional_aspect_extended.context,
            emotion_analysis.emotional_aspect_extended.cognitive_appraisal,
            emotion_analysis.emotional_aspect_extended.conceptualization,
            emotion_analysis.emotional_aspect_extended.cultural_influence,
            emotion_analysis.emotional_aspect_extended.predictions_and_simulations,
            emotion_analysis.emotional_aspect_extended.emotional_dynamics,
            emotion_analysis.emotional_blend_analysis.thought,
            ", ".join(emotion_analysis.emotional_blend_analysis.classifications),
            emotion_analysis.user_need_analysis.thought
        ] + basic_needs_flags  # Add the flags to the row
        
        writer.writerow(row)

    print(f"Data has been appended to {filename}")

if __name__ == "__main__":
    client = Client()
    dataset_name = "Emotion Analysis Full Dataset"

    # Directory containing input files
    input_folder = path_folder

    # Process each file in the input folder
    for input_file in input_folder.glob("*.md"):
        user_id = input_file.stem  # Extract user_id from the file name

        # Load input data
        context_sphere = load_input(input_file.name)

        # Get results and run ID from LLM chain
        emotion_analysis, run_id = run_llm_chain(context_sphere, user_id)

        print("RUN:", run_id)
        print("USER ID:", user_id)
        print(emotion_analysis)

        # Save to CSV with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_emotion_analysis_to_csv(emotion_analysis, user_id, timestamp)