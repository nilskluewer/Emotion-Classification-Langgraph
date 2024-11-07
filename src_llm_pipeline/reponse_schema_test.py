import vertexai
import json
from typing import List, Tuple, Dict, Any
from langsmith.run_helpers import traceable
from vertexai.generative_models import GenerationConfig, GenerativeModel, GenerationResponse
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.utils.json_schema import dereference_refs
from utils.data_models import HolisticEmotionAnalysis
from vertexai.generative_models import Content, Part
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
from src_llm_pipeline.utils.output_parser import parse_emotion_analysis, print_emotion_analysis, check_property_ordering

# Load environment variables
load_dotenv()

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


def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
        "holistic_emotional_profile"
    ]

    # Core affect analysis ordering
    schema["properties"]["core_affect_analysis"]["propertyOrdering"] = [
        "thought_process",
        "valence",
        "arousal",
        "rationale"
    ]

    # Cognitive appraisal ordering
    schema["properties"]["cognitive_appraisal_and_conceptualization"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]

    # Cultural and social context ordering
    schema["properties"]["cultural_and_social_context"]["propertyOrdering"] = [
        "thought_process",
        "discussion",
        "rationale"
    ]

    # Emotion construction analysis ordering
    schema["properties"]["emotion_construction_analysis"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]

    # Holistic emotional profile ordering
    schema["properties"]["holistic_emotional_profile"]["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "rationale"
    ]

    return schema


schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
schema.pop("$defs", None)

# Assuming your original schema is stored in a variable called 'schema'
schema_with_specific_ordering = add_specific_property_ordering(schema)

print("\n --- schema --- ", schema, "\n --- schema --- \n")


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
    run_type="llm",
    name="Gemini Call",
    tags=["gemini"],
)
def call_google(
        response_schema: dict,
        formatted_prompt: List[Content],
        model_name: str = "gemini-1.5-pro-002",
        temperature: float = 0.0,
        top_p: float = 0.0,
) -> tuple[str, GenerationResponse]:
    """
    Call the Google Gemini API with basic configuration.
    
    Args:
        response_schema (dict): The schema for structuring the response
        formatted_prompt (str): The formatted input prompt
        model_name (str): Name of the Gemini model to use
        temperature (float): Controls randomness in the response (0.0 to 1.0)
        top_p (float): Controls diversity of the response (0.0 to 1.0)
    
    Returns:
        str: The model's response text
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

    response = model.generate_content(
        contents=formatted_prompt,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False
    )
    return response.text, response


# Use the functions

system_prompt = read_prompts("LFB_role_setting_prompt.md")
feedback_prompt = read_prompts("LFB_role_feedback_prompt.md")

task_prompt_with_context = insert_context_sphere_into_prompt(
    context_file_name=Path("./inputs/sp0/user_12698_comments_12365_tokens.md"))

# print("\n --- TASK PROMPT --- \n", task_prompt_with_context, "\n --- output --- \n")

role_play_prompt = simulate_conversation(task_prompt_with_context)

print("\n --- ROLE PLAY PROMPT START --- \n", role_play_prompt, "\n --- ROLE PLAY PROMPT END --- \n")
response_text, response = call_google(
    response_schema=schema_with_specific_ordering,
    formatted_prompt=role_play_prompt,
    model_name="gemini-1.5-flash-002")

print("\n --- output ---", response_text, "\n --- output --- \n")

print("\n TOKEN USAGE \n")
print(response.usage_metadata)

parsed_data = parse_emotion_analysis(text= response_text, schema=schema_with_specific_ordering)
print_emotion_analysis(parsed_data, width=200)

if check_property_ordering(parsed_data, schema_with_specific_ordering):
    print("Output matches schema ordering exactly!")
    print_emotion_analysis(parsed_data, width=200)
else:
    print("Warning: Output does not match schema ordering")

