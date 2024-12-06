import vertexai
from typing import List, Optional, Dict, Any
from langsmith.run_helpers import traceable
from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel, SafetySetting, Part, GenerationConfig
from pathlib import Path
from langchain_core.utils.json_schema import dereference_refs
from utils.data_models import HolisticEmotionAnalysis


# Load environment variables
load_dotenv()


prompts_version = "v5"

def load_system_prompt(filename: str) -> str:
    """Load system prompt from file."""
    folder = Path(f"./inputs/prompts/{prompts_version}")
    return (folder / filename).read_text()

def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Add specific property ordering to schema."""
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

# Define safety settings
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

@traceable(run_type="llm")
def initialize_chat_with_history(
    response_schema: Dict[str, Any],
    model: str = "gemini-1.5-pro-002",
    temperature: float = 0.0,
    top_p: float = 0.0,
) -> Dict[str, Any]:
    """
    Initialize a chat with pre-filled history and system messages
    """
    # Load the three prompts
    system_role = load_system_prompt("LFB_role_setting_prompt.md")
    system_feedback = load_system_prompt("LFB_role_feedback_prompt.md")
    user_task = load_system_prompt("prompt_testing.md")

    # Initialize the model with system instruction
    model = GenerativeModel(
        model,
        system_instruction=system_role
    )

    # Start chat
    chat = model.start_chat()
    
    # Send initial messages to establish context
    chat.send_message(
        system_feedback,
        generation_config=GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
        safety_settings=safety_settings
    )
    
    response = chat.send_message(
        user_task,
        generation_config=GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
        safety_settings=safety_settings
    )
    
    result = {
        "response": response.text,
        "chat": chat,
        "metadata": {
            "model": model,
            "temperature": temperature,
            "top_p": top_p
        }
    }
    
    return result

def main():
    # Initialize Vertex AI
    vertexai.init(project="rd-ri-genai-dev-2352", location="europe-west4")
    
    # Load and process schema
    schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
    schema.pop("$defs", None)
    schema_with_ordering = add_specific_property_ordering(schema)
    
    # Initialize chat with history
    chat_session = initialize_chat_with_history(
        response_schema=schema_with_ordering,
    )
    
    print(f"\n --- Initial chat state --- {chat_session['response']} \n --- Initial chat state --- \n")
    
    # The chat object is available for further interactions
    chat = chat_session['chat']
    
    return chat_session

if __name__ == "__main__":
    main()