import vertexai
from typing import List
from langsmith.run_helpers import traceable
from vertexai.generative_models import GenerationConfig, GenerativeModel
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.utils.json_schema import dereference_refs
from utils.data_models import HolisticEmotionAnalysis
from vertexai.generative_models import Content, Part
from vertexai.generative_models import GenerativeModel, SafetySetting, Part



# Load environment variables
load_dotenv()


vertexai.init(project="rd-ri-genai-dev-2352", location="europe-west4")
    


prompts_version = "v5"

def load_prompt(filename: str) -> str:
    """Load system prompt from file."""
    folder = Path(f"./inputs/prompts/{prompts_version}")
    return (folder / filename).read_text()

def add_specific_property_ordering(schema):
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
        "analysis",
        "rationale"
    ]
    
    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "analysis",
        "rationale"
    ]
    
    # Holistic emotional profile ordering
    schema["properties"]["holistic_emotional_profile"]["propertyOrdering"] = [
        "description",
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
) -> str:
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
    )
    
    return response.text

# Use the functions

system_prompt = load_prompt("LFB_role_setting_prompt.md")
feedback_prompt = load_prompt("LFB_role_feedback_prompt.md")
task_prompt = load_prompt("prompt_testing.md")


formatted_prompt = simulate_conversation(task_prompt)
response_text = call_google(
    response_schema=schema_with_specific_ordering,
    formatted_prompt=formatted_prompt
)
print("\n --- output ---", response_text, "\n --- output --- \n")