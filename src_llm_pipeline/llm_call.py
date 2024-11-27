import json
import uuid
from pathlib import Path
from typing import List

import vertexai
from dotenv import load_dotenv
from langchain_core.utils.json_schema import dereference_refs
from langsmith import Client
from langsmith import RunTree
from langsmith.run_helpers import traceable
from vertexai.generative_models import GenerativeModel, Part, Content, GenerationConfig, \
    GenerationResponse

from inputs.prompts.v7.data_models import HolisticEmotionAnalysis, HolisticEmotionalProfile, add_property_ordering_single_class, add_specific_property_ordering
#from utils.langsmith_dataset import create_langsmith_dataset
from utils.model import default_safety_settings
from utils.langsmith_feedback import send_feedback_to_trace
from utils.output_parser import parse_emotion_analysis, print_emotion_analysis, check_property_ordering
from utils.enums import MESSAGE_MAP

# Load environment variables
load_dotenv()

client = Client()

# Lade die Konfigurationen
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
# Der Pfad zur .pkl-Datei in config.json

model_name = config["model_name"]
prompts_version = config["prompt_version"]
sample_folder = config["sample_folder"]
debug_chain = config["debug_chain"]
debug_schema = config["debug_schema"]
llm_endpoint_location = config["llm_endpoint_location"]
check_for_hallucinations = config["check_for_hallucinations"]

vertexai.init(project="rd-ri-genai-dev-2352", location=llm_endpoint_location)


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



@traceable(name="Simulate Conversation for Role Play Prompting", run_type="prompt")
def simulate_conversation(task_prompt) -> List[Content]:
    # Simulate the conversation flow with role play prompting
    # Consisting of a System prompt setting the scene, feedback prompt prefilling the models response
    # and the task prompt with the actual task.
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

@traceable(name="Create Generation Config with Output Instructions", run_type="tool")
def create_generation_config(temperature, top_p,response_schema_model = None, response_mime_type = None) -> GenerationConfig:
    # Configure generation parameters
    generation_config = GenerationConfig(
        response_mime_type= response_mime_type, #"application/json",
        response_schema=response_schema_model,
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=8000,  # Adjust as needed
    )
    return generation_config

@traceable(name="Configue LLM with Generation Config", run_type="tool")
def configure_llm(model_name, generation_config : GenerationConfig) -> GenerativeModel:
    return GenerativeModel(model_name=model_name, generation_config=generation_config)


@traceable(name="LLM Call", run_type="llm", 
           tags= ["api_call"], 
           metadata={"ls_provider": "Google", "ls_model_name": f"{model_name}"}
           )
def call_api(configured_llm: GenerativeModel, prompt: List[Content], safety_settings: list[default_safety_settings], run_tree: RunTree) -> GenerationResponse:

    response = configured_llm.generate_content(
        contents=prompt,
        safety_settings=safety_settings,
        stream=False
    )
    usage_metadata = response.usage_metadata

    dict = {
        "response" : response,
        "usage_metadata" : {
            "input_tokens": usage_metadata.prompt_token_count,
            "output_tokens": usage_metadata.candidates_token_count,
            "total_tokens": usage_metadata.total_token_count,
        },
    }
    return dict


@traceable(name="Response to Dict", run_type="parser")
def transform_output(response: GenerationResponse) -> dict:
    python_dict = json.loads(response.text)
    return python_dict

# Helper function to properly print Conversation History
def print_message_history(messages: List[Content]) -> dict:
    for message in messages:
        print(f"Role: {message.role}")
        for part in message.parts:
            print(f"Text: {part.text}")



@traceable(name="Final Output Parser", run_type="parser")
def convert_to_dict(messages: List[Content]) -> dict:
    result_dict = {}

    for index, message in enumerate(messages):
        key = f"{message.role}-{MESSAGE_MAP.get(index)}"
        result_dict[key] = " ".join(part.text for part in message.parts)

    #result_dict["full_output_unstructured"] = str(messages)

    if debug_chain:
        print_message_history(messages)
    return result_dict

# transform response.text into a python_dict for further processing
# Is similar to parse_model_response_to_data_model_structure, but this one trusts that google is doing the ordering
# of properties correctly.
#transform_output(response)

@traceable(name="Append LLM Response to Conversation", run_type="parser")
def append_response(prompt: List[Content], message_to_append: Content) -> List[Content]:
    prompt.append(message_to_append)
    return prompt

@traceable(name="Add Task Prompt for Summarization", run_type="parser")
def append_prompt(prompt: List[Content], message_to_append: Content) -> List[Content]:
    prompt.append(message_to_append)
    return prompt


@traceable(name="Parse LLM Structure for Validation", run_type="parser")
def parse_model_response_to_data_model_structure(input_text,target_schema) -> dict:
    data = parse_emotion_analysis(text=input_text, schema=target_schema)
    return data

@traceable(name="Validate Output Structure", run_type="parser")
def validate_response_property_order(parsed_data, schema_with_specific_ordering) -> bool:
    if check_property_ordering(parsed_data, schema_with_specific_ordering):
        print("Output matches schema ordering exactly!")
        return True
    else:
        print("Warning: Output does not match schema ordering")
        return False


@traceable(name="Step 1: Classification", run_type="chain")
def step_1_emotion_classification_with_structured_output(task_prompt_with_context,response_schema, temperature, top_p, run_tree: RunTree):

    role_play_prompt = simulate_conversation(task_prompt_with_context)
    # Erstmla ausgeklammert für consistent langchain tracing
    #role_play_prompt_without_context = simulate_conversation(task_prompt_without_context)

    llm_config = create_generation_config(response_schema_model = response_schema,
                                          response_mime_type= "application/json",
                                          temperature = temperature,
                                          top_p = top_p)
    configured_llm = configure_llm(model_name=model_name, generation_config=llm_config)

    response = call_api(configured_llm=configured_llm,
                        prompt=role_play_prompt,
                        safety_settings=default_safety_settings)
    response = response["response"]
    send_feedback_to_trace(response =response,
                           client = client,
                           run_tree=run_tree)


    #Raw Response
    #print("RAW RESPONSE: ", response)

    # Parse data to valide output structure
    parsed_data = parse_model_response_to_data_model_structure(input_text=response.text,
                                                               target_schema=response_schema)

    # Validate result
    validation_result = validate_response_property_order(parsed_data, response_schema)

    # Feedback of validation result in Langsmith
    client.create_feedback(
        run_tree.id,
        key = "llm_output_format_validation",
        score = validation_result,
        comment = "1 = True: The model used the correct propertyOrder. False, the model did not!"
    )

    # Access the first candidate Content object in the response
    content_from_response = response.candidates[0].content
    conversation_history_step_1 = append_response(prompt = role_play_prompt, message_to_append = content_from_response)


    if debug_chain:
        print_emotion_analysis(parsed_data, width=200)

    return conversation_history_step_1


@traceable(name="Step 2: Summarization of Classification", run_type="chain")
def step_2_summarization_of_classification(conversation_history_step_1, temperature,top_p, run_tree: RunTree):
    step_2_task_prompt = Content(role="user", parts=[Part.from_text(read_prompts("user_task_followup_prompt.md"))])

    # Append to Conversation
    task_prompt_step_2 = append_prompt(conversation_history_step_1,step_2_task_prompt)

    llm_config = create_generation_config(temperature = temperature,
                                          top_p = top_p)

    configured_llm = configure_llm(model_name=model_name, generation_config=llm_config)

    response = call_api(configured_llm=configured_llm,
                        prompt=task_prompt_step_2,
                        safety_settings=default_safety_settings)
    response = response["response"]
    send_feedback_to_trace(response =response,
                           client = client,
                           run_tree=run_tree)

    content_from_response_2 = response.candidates[0].content
    message_history = append_response(task_prompt_step_2, content_from_response_2)
    return message_history

def request_emotion_analysis_with_user_id(user_id: int,
                                          response_schema: dict,
                                          response_schema2: dict,
                                          task_prompt_with_context,
                                          context_sphere_for_eval: str,
                                          model_name: str = "gemini-1.5-flash-002",
                                          temperature: float = 1,
                                          top_p: float = 0.95):
    @traceable(
        run_type="chain",
        name="Context Aware Emotion Classification",
        tags=[f"{model_name}", f"User_ID: {user_id}"],
        metadata={"check_hallucinations": check_for_hallucinations})
    def request_emotion_analysis(context_sphere,run_tree : RunTree) -> dict:
        """
        Call the Google Gemini API with basic configuration.
        """
        classification_result_step_1 = step_1_emotion_classification_with_structured_output(task_prompt_with_context,response_schema, temperature, top_p)
        message_history = step_2_summarization_of_classification(classification_result_step_1, temperature,top_p)
        dict_list = convert_to_dict(message_history)

        return  dict_list

    request_emotion_analysis(context_sphere = context_sphere_for_eval)


    return





# Perform setup operations without repetition
schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
schema.pop("$defs", None)
schema_with_specific_ordering = add_specific_property_ordering(schema)

schema_holistic_profile = HolisticEmotionalProfile.model_json_schema()
schema_with_specific_ordering_holistic_profile = add_property_ordering_single_class(schema_holistic_profile)


system_prompt = read_prompts("LFB_role_setting_prompt.md")
feedback_prompt = read_prompts("LFB_role_feedback_prompt.md")
task_prompt_without_context = read_prompts("user_task_prompt.md")


if debug_schema:
    print(schema_with_specific_ordering_holistic_profile)

    print("\n --- schema 1 --- ", schema_with_specific_ordering, "\n --- schema --- \n")
    print("\n --- schema 2--- ", schema_with_specific_ordering_holistic_profile, "\n --- schema --- \n")




def create_dataset(parsed_data):
    print(parsed_data.core_affect_analysis)
    pass

#@traceable(name="Batch Processing Emotion Classifications", type="chain")
def process_markdown_files_in_folder(batch_id, dataset_name):
    results = []  # To store the results for all processed files
    folder_path = Path(f"./inputs/{sample_folder}")
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

        result = request_emotion_analysis_with_user_id(
            user_id=user_id_from_filename,
            response_schema=schema_with_specific_ordering,
            response_schema2=schema_with_specific_ordering_holistic_profile,
            task_prompt_with_context=task_prompt_with_context,
            context_sphere_for_eval=context_sphere,
            model_name=model_name)
        results.append(result)

    return results  # Return after processing all files

if __name__ == "__main__":
    # Process each folder independently
    folder = "sp0"


    random_uuid = uuid.uuid4()
    process_markdown_files_in_folder(batch_id=random_uuid, dataset_name = "Testing")



# TODO: Add output to dataset
# data set creatin through the gaterhin of traces
#print("\n --- output ---", parsed_data, "\n --- output --- \n")

