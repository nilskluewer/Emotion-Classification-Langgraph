from uuid import UUID

import vertexai
import json
from typing import List, Tuple, Dict, Any
from langsmith.run_helpers import traceable
from vertexai.generative_models import GenerationConfig, GenerativeModel, GenerationResponse
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.utils.json_schema import dereference_refs
from utils.data_models import HolisticEmotionAnalysis, add_specific_property_ordering
from vertexai.generative_models import Content, Part
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
from src_llm_pipeline.utils.output_parser import parse_emotion_analysis, print_emotion_analysis, check_property_ordering
from langsmith import RunTree
from langsmith import Client



# Load environment variables
load_dotenv()

client = Client()

model_name = "gemini-1.5-pro-002"

vertexai.init(project="rd-ri-genai-dev-2352", location="europe-west4")

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

schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
schema.pop("$defs", None)

# Assuming your original schema is stored in a variable called 'schema'
schema_with_specific_ordering = add_specific_property_ordering(schema)

print("\n --- schema --- ", schema, "\n --- schema --- \n")

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
    tags=[f"{model_name}"],
)
def call_google(
        response_schema: dict,
        prompt: List[Content],
        role_play_prompt_without_context_for_eval: List[Content],
        context_sphere_for_eval: str,
        run_tree: RunTree,
        model_name: str = "gemini-1.5-flash-002",
        temperature: float = 0.0,
        top_p: float = 0.0,

) -> tuple[Any, Any, UUID]:
    """
    Call the Google Gemini API with basic configuration.
    """
    # Initialize the model
    model = GenerativeModel(model_name)

    # Configure generation parameters
    generation_config = GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema,
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=8192,  # Adjust as needed
    )

    # Safety settings
    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
    ]
    @traceable(name="llm")
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
                        safety_settings=safety_settings)

    @traceable(name="Response to Dict")
    def transform_output(response: GenerationResponse) -> dict:
        python_dict = json.loads(response.text)
        return python_dict

    # transform response.text into a python_dict for further processing
    transform_output(response)

    print("\n TOKEN USAGE \n")
    print(response.usage_metadata)

    @traceable(name="Parse LLM response structure")
    def parse_model_response_to_data_model_structure(input_text,target_schema) -> dict:
        data = parse_emotion_analysis(text=input_text, schema=target_schema)
        return data

    parsed_data = parse_model_response_to_data_model_structure(input_text=response.text,
                                                 target_schema=response_schema)


    @traceable(name="Validate Output Format")
    def validate_response_property_order(parsed_data, schema_with_specific_ordering) -> bool:
        if check_property_ordering(parsed_data, schema_with_specific_ordering):
            print("Output matches schema ordering exactly!")
            print_emotion_analysis(parsed_data, width=200)
            return True
        else:
            print("Warning: Output does not match schema ordering")
            return False

    print_emotion_analysis(parsed_data, width=200)

    client.create_feedback(
        run_tree.id,
        key = "llm_output_format_validation",
        score = validate_response_property_order(parsed_data, response_schema),
    )

    return parsed_data


# Use the functions

system_prompt = read_prompts("LFB_role_setting_prompt.md")
feedback_prompt = read_prompts("LFB_role_feedback_prompt.md")
task_prompt_without_context = read_prompts("user_task_prompt.md")

# Keep it in to validate if the Hallucination Eval works
task_prompt_with_context = insert_context_sphere_into_prompt(
    context_file_name=Path("./inputs/sp0/user_67780_comments_7522_tokens.md"))

# Keep in to check if Hallucination Eval works
context_sphere = Path("./inputs/sp0/user_67780_comments_7522_tokens.md").read_text()


# print("\n --- TASK PROMPT --- \n", task_prompt_with_context, "\n --- output --- \n")

role_play_prompt = simulate_conversation(task_prompt_with_context)
role_play_prompt_without_context = simulate_conversation(task_prompt_without_context)



print("\n --- ROLE PLAY PROMPT START --- \n", role_play_prompt, "\n --- ROLE PLAY PROMPT END --- \n")
parsed_data = call_google(
    response_schema=schema_with_specific_ordering,
    prompt=role_play_prompt,
    role_play_prompt_without_context_for_eval=role_play_prompt_without_context,
    context_sphere_for_eval=context_sphere,
    model_name=model_name)



# TODO: Add output to dataset


print("\n --- output ---", parsed_data, "\n --- output --- \n")



