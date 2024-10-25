import importlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm
from save_output_to_csv import main as save_output_to_csv
from langchain_core.tracers.context import collect_runs
from uuid import uuid4
from typing import Dict
from datetime import datetime
from langsmith import Client
from data_models import EmotionAnalysisOutput
from langchain_core.callbacks import StdOutCallbackHandler
from langchain_core.runnables import RunnableConfig
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate



# Load environment variables
load_dotenv()

# Dynamically import the module
models = importlib.import_module("data_models")

def load_system_prompt(filename: str, folder: Path) -> Dict[str, str]:
    folder = Path(f"./prompts/{prompts_version}")
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path):
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature):
    queries_schema = dereference_refs(EmotionAnalysisOutput.model_json_schema())
    queries_schema.pop("$defs", None)

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_setting_prompt.md"))),
            AIMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_feedback_prompt.md"))),
            HumanMessagePromptTemplate.from_template(str(load_system_prompt("user_task_prompt.md")))
        ]
    ).partial(context_sphere="context_sphere")

    llm = create_llm(
        model_name=model_name,
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
        top_p=top_p
    )

    parser = PydanticOutputParser(pydantic_object=EmotionAnalysisOutput)


    return prompt | llm | parser

def process_input_files_batch(
        input_folder: Path,
        client: Client,
        model_temperature: float,
        top_p:float,
        enable_feedback: bool,
        enable_csv_output: bool,
        batch_size: int,
        max_concurrency: int
) -> None:
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature=model_temperature)
    input_files = list(input_folder.glob("*.md"))

    # Create a callback handler
    callback_handler = StdOutCallbackHandler()

    for i in range(0, len(input_files), batch_size):
        batch_files = input_files[i:i+batch_size]
        batch_inputs = []

        for file in batch_files:
            user_id = file.name.split('_')[1]
            context_sphere = load_input(file.name, folder=input_folder)
            batch_inputs.append({
                "context_sphere": context_sphere,
                "user_id": user_id
            })
        batch_id = str(uuid4())
        tag_str = "batch: " + batch_id + " , temp: " + str(model_temperature)

        config = RunnableConfig(
            callbacks=None,
            tags=["EA_Batch_"],
            metadata={"batch_id": batch_id,
                      "temperature": model_temperature,
                      "top_p":top_p,
                      "model_name": model_name,
                      "prompt_template_version": prompts_version},
            max_concurrency=max_concurrency,
            run_name="Batch Run: EA_Chain",
        )

        with collect_runs() as runs_collector:
            batch_results = emotion_analysis_chain.batch(
                batch_inputs,
                config=config
            )

        for file, result, run in zip(batch_files, batch_results, runs_collector.traced_runs):
            user_id = file.name.split('_')[1]
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

            if enable_csv_output:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_output_to_csv(emotion_analysis=result,
                                   model_temperature=model_temperature,
                                   top_p=top_p,
                                   batch_id=batch_id,
                                   user_id=user_id,
                                   run_id=run.id,
                                   timestamp=timestamp,
                                   model_name=model_name,
                                   prompt_template_version=prompts_version)

if __name__ == "__main__":
    client = Client()
    input_folder = Path("./inputs/sp0")

    # Configure which optional steps to perform
    enable_feedback = True
    enable_csv_output = True
    # Metadata variables maybe to externalize?
    # model name
    # model temperature
    # batch run
    # model configuration top_n etc.
    # prompt folder v1 / v2 / v3 / ...

    prompts_version = "v3"
    model_name = "gemini-1.5-pro-002"
    top_p = 0
    model_temperature = 0
    test_set = ""

    print("---- Start of Batch processing ----")
    process_input_files_batch(
        input_folder=input_folder,
        client=client,
        model_temperature=model_temperature,
        top_p=top_p,
        enable_feedback=True,
        enable_csv_output=True,
        batch_size=1,
        max_concurrency=1
    )