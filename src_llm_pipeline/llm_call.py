import json
import uuid
from pathlib import Path
from typing import List, Tuple, Any
from uuid import UUID

import vertexai
from dotenv import load_dotenv
from langchain_core.utils.json_schema import dereference_refs
from langsmith import Client
from langsmith import RunTree
from langsmith.run_helpers import traceable
from vertexai.generative_models import GenerativeModel, SafetySetting, Part, Content, GenerationConfig, \
    GenerationResponse

from utils.data_models import *
from utils.langsmith_dataset import create_langsmith_dataset
from utils.model import default_safety_settings
from utils.langsmith_feedback import send_feedback_to_trace
from utils.output_parser import parse_emotion_analysis, print_emotion_analysis, check_property_ordering

# Load environment variables
load_dotenv()

client = Client()

model_name = "gemini-1.5-flash-002"

vertexai.init(project="rd-ri-genai-dev-2352", location="europe-west1")

prompts_version = "v6"


def read_prompts(filename: str) -> str:
    """Load system prompt from file."""
    folder = Path(f"./inputs/prompts/{prompts_version}")
    return (folder / filename).read_text()


def insert_context_sphere_into_prompt(context_file_name: Path, template_filename="user_task_prompt.md") -> str:
    # Read the template and context sphere from their respective files
    template_content = read_prompts(template_filename)
    context_sphere = context_file_name.read_text().strip()

    # Use Python's str.format() to replace the placeholder
    formatted_markdown_prompt = template_content.format(context_sphere=context_sphere)
    return formatted_markdown_prompt


#@traceable(name="build_conversation")
# We can build the chain, but would need to implement the child logic in traces
def simulate_conversation(task_prompt) -> List[Content]:
    # Simulate the conversation flow
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "model", "content": feedback_prompt},
        {"role": "user", "content": task_prompt},

    ]
    messages = [
        Content(
            role="user",
            parts=[Part.from_text(system_prompt)]
        ),
        Content(
            role="model",
            parts=[Part.from_text(feedback_prompt)]
        ),
        Content(
            role="user",
            parts=[Part.from_text(task_prompt)]
        )
    ]

    return messages

@traceable(
    run_type="chain",
    name="EmotionAnalysis Request",
    tags=[f"{model_name}"])
def request_emotion_analysis(
        user_id: int,
        response_schema: dict,
        response_schema2: dict,
        prompt: List[Content],
        role_play_prompt_without_context_for_eval: List[Content],
        context_sphere_for_eval: str,
        run_tree: RunTree,
        model_name: str = "gemini-1.5-flash-002",
        temperature: float = 0.0,
        top_p: float = 0.0,
) -> tuple[Any, Any, Any]:
    """
    Call the Google Gemini API with basic configuration.
    """
    # Initialize the model
    model = GenerativeModel(model_name)

    client.create_feedback(
        run_tree.id,
        key="user_id",
        value=str(user_id),
        comment="ID of the current processed user"
    )


    # Configure generation parameters
    generation_config = GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema,
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=8000,  # Adjust as needed
    )


    @traceable(name="llm", run_type="llm", tags=[f"{user_id}"])
    def call_api(prompt, generation_config, safety_settings) -> GenerationResponse:
        response = model.generate_content(
            contents=prompt,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False
        )
        return response


    response = call_api(prompt=prompt,
                        generation_config=generation_config,
                        safety_settings=default_safety_settings)

    send_feedback_to_trace(response =response,
                           client = client,
                           run_tree=run_tree)

    print("RAW RESPONSE: ", response)


    @traceable(name="Response to Dict", run_type="parser")
    def transform_output(response: GenerationResponse) -> dict:
        python_dict = json.loads(response.text)
        return python_dict

    # transform response.text into a python_dict for further processing
    # Is similar to parse_model_response_to_data_model_structure, but this one trusts that google is doing the ordering
    # of properties correctly.
    #transform_output(response)


    @traceable(name="Parse LLM response structure", run_type="parser")
    def parse_model_response_to_data_model_structure(input_text,target_schema) -> dict:
        data = parse_emotion_analysis(text=input_text, schema=target_schema)
        return data

    parsed_data = parse_model_response_to_data_model_structure(input_text=response.text,
                                                 target_schema=response_schema)



    @traceable(name="Validate Output Format", run_type="parser")
    def validate_response_property_order(parsed_data, schema_with_specific_ordering) -> bool:
        if check_property_ordering(parsed_data, schema_with_specific_ordering):
            print("Output matches schema ordering exactly!")
            return True
        else:
            print("Warning: Output does not match schema ordering")
            return False

    print_emotion_analysis(parsed_data, width=200)

    # Feedback for loggin in Langsmith
    client.create_feedback(
        run_tree.id,
        key = "llm_output_format_validation",
        score = validate_response_property_order(parsed_data, response_schema),
        comment = "1 = True: The model used the correct propertyOrder. False, the model did not!"
    )

 #   new_content = Content(role="model", parts=[Part.from_text(response.text)])
    # Append the new Content object to the messages list using +=
 #   prompt += [new_content]
    @traceable(name="Summarize Analysis", run_type="chain")
    def create_holistic_analysis(response: GenerationResponse) -> tuple[Any, list[Content]]:
        try:
            # Access the first candidate Content object in the response
            content_from_response = response.candidates[0].content

            # Append the Content object to the messages list
            prompt.append(content_from_response)

            second_task_prompt = Content(role="user", parts=[Part.from_text(read_prompts("user_task_followup_prompt.md"))])
            prompt.append(second_task_prompt)

            print(prompt)
            print("TYPE OF RESPONSE SCHEMA",type(response_schema2))
            generation_config_2 = GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema2,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=8000,  # Adjust as needed
            )

            response_2 = call_api(
                prompt=prompt,
                generation_config=generation_config_2,
                safety_settings=default_safety_settings,
            )
            print(response_2.text)
            python_dict = transform_output(response = response_2)

            validate_response_property_order(parsed_data=python_dict,schema_with_specific_ordering=response_schema2)

            content_from_response_2 = response_2.candidates[0].content

            # Append the Content object to the messages list
            prompt.append(content_from_response_2)

            return python_dict, prompt

        except IndexError:
            print("Error")

    holistic_profile, message_history = create_holistic_analysis(response=response)



    return parsed_data, holistic_profile, message_history





# Perform setup operations without repetition
schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
schema.pop("$defs", None)
schema_with_specific_ordering = add_specific_property_ordering(schema)

schema_holistic_profile = HolisticEmotionalProfile.model_json_schema()
schema_with_specific_ordering_holistic_profile = add_property_ordering_single_class(schema_holistic_profile)
print(schema_with_specific_ordering_holistic_profile)

print("\n --- schema 1 --- ", schema_with_specific_ordering, "\n --- schema --- \n")
print("\n --- schema 2--- ", schema_with_specific_ordering_holistic_profile, "\n --- schema --- \n")

system_prompt = read_prompts("LFB_role_setting_prompt.md")
feedback_prompt = read_prompts("LFB_role_feedback_prompt.md")
task_prompt_without_context = read_prompts("user_task_prompt.md")


def create_dataset(parsed_data):
    print(parsed_data.core_affect_analysis)
    pass


def process_markdown_files_in_folder(folder_path: Path, batch_id, dataset_name):
    results = []  # To store the results for all processed files

    for markdown_file in folder_path.glob("*.md"):
        # Extract user ID from the markdown file name
        file_stem = markdown_file.stem
        user_id_from_filename = file_stem.split('_')[1]  # Assuming consistent naming
        print("START ANALYSIS OF USER: ", user_id_from_filename)

        # Keep it in to validate if the Hallucination Eval works - input different users into the with and without context
        task_prompt_with_context = insert_context_sphere_into_prompt(
            context_file_name=markdown_file)

        # Keep in to check if Hallucination Eval works
        context_sphere = markdown_file.read_text()

        # print("\n --- TASK PROMPT --- \n", task_prompt_with_context, "\n --- output --- \n")
        role_play_prompt = simulate_conversation(task_prompt_with_context)
        role_play_prompt_without_context = simulate_conversation(task_prompt_without_context)
        print("\n --- ROLE PLAY PROMPT START --- \n", role_play_prompt, "\n --- ROLE PLAY PROMPT END --- \n")

        holistic_analysis, holistic_profile, message_history = request_emotion_analysis(
            user_id=user_id_from_filename,
            response_schema=schema_with_specific_ordering,
            response_schema2=schema_with_specific_ordering_holistic_profile,
            prompt=role_play_prompt,
            role_play_prompt_without_context_for_eval=role_play_prompt_without_context,
            context_sphere_for_eval=context_sphere,
            model_name=model_name)

        # Dataset gets created wiuth only one entry. better use the traced to create the dataset.
        #create_langsmith_dataset(holistic_analysis, holistic_profile, message_history,
        #                         batch_id, dataset_name=dataset_name)

        #results.append((holistic_analysis, holistic_profile, message_history))

    return results  # Return after processing all files

if __name__ == "__main__":
    # Process each folder independently
    folder = "sp2"

    folder_path = Path(f"./inputs/{folder}")
    random_uuid = uuid.uuid4()
    process_markdown_files_in_folder(folder_path, batch_id=random_uuid, dataset_name = "Testing")



# TODO: Add output to dataset
# data set creatin through the gaterhin of traces
#print("\n --- output ---", parsed_data, "\n --- output --- \n")



