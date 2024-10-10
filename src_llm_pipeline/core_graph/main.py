import importlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm
from save_output_to_csv import main as save_output_to_csv
from langchain_core.tracers.context import collect_runs
from uuid import UUID
from typing import Tuple
from pathlib import Path
from datetime import datetime
from langsmith import Client
from data_models import EmotionAnalysisOutput


path_folder = Path("./inputs/sample_24_09_27__12_58_size_20_tokens_1000_to_3000")

# Load environment variables
load_dotenv()

# Dynamically import the module
models = importlib.import_module("data_models")

def load_system_prompt(filename: str, folder: Path = Path("./prompts")):
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path = path_folder):
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature):
    """
    Create and return the emotion analysis chain.

    Returns:
        Chain: The configured emotion analysis chain.
    """
    queries_schema = dereference_refs(EmotionAnalysisOutput.model_json_schema())
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
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
    )

    return prompt | llm | PydanticOutputParser(pydantic_object=EmotionAnalysisOutput)

def run_emotion_analysis(context_sphere: str, user_id: str) -> Tuple[EmotionAnalysisOutput, UUID]:
    """
    Run the emotion analysis chain and collect the run information.

    Args:
        context_sphere (str): The context sphere containing the text to analyze.
        user_id (str): The user ID for metadata and tracing.

    Returns:
        Tuple[EmotionAnalysisOutput, UUID]: A tuple containing the emotion analysis output
        and the run ID for tracing.
    """
    emotion_analysis_chain = create_emotion_analysis_chain()

    with collect_runs() as runs_collector:
        analysis_result = emotion_analysis_chain.invoke(
            {"context_sphere": context_sphere},
            config={
                "metadata": {"user_id": user_id},
                "run_name": "Emotion_Analysis_Chain"
            }
        )

        run_id = runs_collector.traced_runs[0].id if runs_collector.traced_runs else None

    return analysis_result, run_id


def process_input_file(input_file: Path, client: Client, enable_feedback: bool, enable_csv_output: bool):
    """
    Process a single input file for emotion analysis.

    Args:
        input_file (Path): The path to the input file.
        client (Client): The LangSmith client for feedback.
        enable_feedback (bool): Flag to enable/disable feedback.
        enable_csv_output (bool): Flag to enable/disable CSV output.
    """
    user_id = input_file.stem
    context_sphere = load_input(input_file.name)

    emotion_analysis, run_id = run_emotion_analysis(context_sphere, user_id)

    print(f"Run ID: {run_id}")
    print(f"User ID: {user_id}")
    print(emotion_analysis)

    if enable_feedback and run_id:
        client.create_feedback(
            run_id=run_id,
            key="Valence",
            value=emotion_analysis.core_affect_analysis.valence,
            comment=emotion_analysis.core_affect_analysis.thought
        )
        client.create_feedback(
            run_id=run_id,
            key="Arousal",
            value=emotion_analysis.core_affect_analysis.arousal,
            comment=emotion_analysis.core_affect_analysis.thought
        )

    if enable_csv_output:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_output_to_csv(emotion_analysis, user_id, timestamp)


from typing import List, Dict
from pathlib import Path
from langchain_core.runnables import RunnableConfig
from uuid import uuid4

def process_input_files_batch(
        input_folder: Path,
        client: Client,
        model_temperature: float,
        enable_feedback: bool,
        enable_csv_output: bool,
        batch_size: int,
        max_concurrency: int
) -> None:
    """
    Process multiple input files in batches using LangChain's batch processing.

    Args:
        input_folder (Path): The folder containing input files.
        client (Client): The LangSmith client for feedback.
        enable_feedback (bool): Flag to enable/disable feedback.
        enable_csv_output (bool): Flag to enable/disable CSV output.
        batch_size (int): Number of files to process in each batch.
        max_concurrency (int): Maximum number of concurrent requests.
    """
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature = model_temperature)
    input_files = list(input_folder.glob("*.md"))

    for i in range(0, len(input_files), batch_size):
        batch_files = input_files[i:i+batch_size]
        batch_inputs = []

        for file in batch_files:
            user_id = file.stem
            context_sphere = load_input(file.name, folder=input_folder)
            batch_inputs.append({
                "context_sphere": context_sphere,
                "user_id": user_id
            })

        config = RunnableConfig(
            callbacks=None,
            tags=["emotion_analysis_batch"],
            metadata={"batch_id": str(uuid4()),
                      "run_name": "Batch Run: EA_Chain"},
            max_concurrency=max_concurrency
        )

        with collect_runs() as runs_collector:
            batch_results = emotion_analysis_chain.batch(
                batch_inputs,
                config=config
            )

        for file, result, run in zip(batch_files, batch_results, runs_collector.traced_runs):
            user_id = file.stem
            print(f"Run ID: {run.id}")
            print(f"User ID: {user_id}")
            print(result)

            if enable_feedback and run.id:
                client.create_feedback(
                    run_id=run.id,
                    key="Core Valence",
                    value=result.core_affect_analysis.valence,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Core Arousal",
                    value=result.core_affect_analysis.arousal,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Aspect Extended",
                    value=result.emotional_aspect_extended.nuanced_classification,
                    comment=result.emotional_aspect_extended.thought
                )
                """
                client.create_feedback(
                    run_id=run.id,
                    key="Blends",
                    value=", ".join(result.emotional_blend_analysis.classifications),
                    comment=result.emotional_blend_analysis.thought
                )
                """



            if enable_csv_output:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_output_to_csv(emotion_analysis = result,
                                   model_temperature=model_temperature,
                                   user_id= user_id,
                                   timestamp = timestamp)

if __name__ == "__main__":
    client = Client()
    input_folder = Path("./inputs/sp1")

    # Configure which optional steps to perform
    enable_feedback = True
    enable_csv_output = True
    model_temperature = 1

    #for input_file in input_folder.glob("*.md"):
    #    process_input_file(input_file, client, enable_feedback, enable_csv_output)
    print("---- Start of Batch processing ----")
    process_input_files_batch(
        input_folder=input_folder,
        client=client,
        model_temperature = model_temperature,
        enable_feedback=True,
        enable_csv_output=True,
        batch_size=10,
        max_concurrency=5
    )

def create_dataset_if_enabled(client: Client, dataset_name: str, run_id: UUID, enable_dataset_creation: bool):
    """
    Create a dataset in LangSmith if enabled.

    Args:
        client (Client): The LangSmith client.
        dataset_name (str): The name of the dataset to create.
        run_id (UUID): The run ID to include in the dataset.
        enable_dataset_creation (bool): Flag to enable/disable dataset creation.
    """
    if enable_dataset_creation and run_id:
        # Implement dataset creation logic here
        pass


