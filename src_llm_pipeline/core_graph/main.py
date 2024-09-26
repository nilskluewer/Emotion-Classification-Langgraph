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
from data_models import UserNeed, BasicNeed
import csv
from datetime import datetime
import time

path_folder = Path("./inputs/sp0")

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
        model_name="gemini-1.5-flash-002",
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

def save_emotion_analysis_to_csv(emotion_analysis, user_id, timestamp, filename="emotion_analysis.csv"):
    file_exists = os.path.isfile(filename)

    # Extrahiert die Namen der Enums für Basic Needs und User Needs
    basic_needs_labels = [e.name for e in BasicNeed]
    user_needs_labels = [e.name for e in UserNeed]

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            # Überschrift erstellen mit Valence, Engagement, Polarization, User Need Thought und allen Needs als Spalten
            header = [
                "Timestamp", "User ID",
                "Valence Thought", "Valence Classification",
                "Engagement Thought", "Engagement Classification",
                "Polarization Thought", "Polarization Classification",
                "Emotional Blend Thought", "Emotional Blend Classification",
                "User Need Thought"
            ] + basic_needs_labels + user_needs_labels
            writer.writerow(header)
        
        # Datenzeile vorbereiten
        row = [
            timestamp, user_id,
            emotion_analysis.valence.aspect.thought,
            emotion_analysis.valence.aspect.classification,
            emotion_analysis.engagement.aspect.thought,
            emotion_analysis.engagement.aspect.classification,
            emotion_analysis.polarization.aspect.thought,
            emotion_analysis.polarization.aspect.classification,
            emotion_analysis.emotional_blend.aspect.thought,
            emotion_analysis.emotional_blend.aspect.classification,
            emotion_analysis.user_need.thought
        ]
        
        # Flags für Basic Needs
        basic_needs_flags = [(1 if need in emotion_analysis.user_need.basic_needs else 0) for need in BasicNeed]
        row.extend(basic_needs_flags)
        
        # Flags für User Needs
        user_needs_flags = [(1 if need in emotion_analysis.user_need.user_needs else 0) for need in UserNeed]
        row.extend(user_needs_flags)
        
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

        # Provide feedback for each type of analysis with only classification
        provide_feedback(
            client,
            run_id,
            "valence",
            emotion_analysis.valence.aspect.classification,
            emotion_analysis.valence.aspect.thought
        )
        
        provide_feedback(
            client,
            run_id,
            "engagement",
            emotion_analysis.engagement.aspect.classification,
            emotion_analysis.engagement.aspect.thought
        )
        
        provide_feedback(
            client,
            run_id,
            "polarization",
            emotion_analysis.polarization.aspect.classification,
            emotion_analysis.polarization.aspect.thought
        )

        # Save to CSV with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_emotion_analysis_to_csv(emotion_analysis, user_id, timestamp)