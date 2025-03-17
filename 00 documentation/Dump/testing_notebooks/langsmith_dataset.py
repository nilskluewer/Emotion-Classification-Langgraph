from langsmith import Client
from typing import Optional, List, Dict
import pandas as pd
from langsmith.schemas import Dataset


def create_langsmith_dataset(
    data_analysis,
    data_profile,
    message_history,
    batch_id: str,
    dataset_name: str,
    dataset_description: str = "Emotion Analysis Dataset",
    client: Optional[Client] = None,
) -> Dataset:
    """
    Creates a LangSmith dataset directly from batch results.
    
    Args:
        batch_results: List of dictionaries containing input and output data
        dataset_name: Name for the dataset in LangSmith
        dataset_description: Description for the dataset
        client: LangSmith client instance (optional)
    """
    if client is None:
        client = Client()

    try:
        # Create dataset
        dataset = client.create_dataset(
            dataset_name=dataset_name + str(batch_id),
            description=dataset_description,
            metadata={"batch_id" : batch_id}
        )

        client.create_example(
            inputs={
                "context_sphere": message_history
            },
            outputs = {
                # Access subfields for core_affect_analysis
                "core_affect_thought_process": data_analysis.get("core_affect_analysis").get("thought_process"),
                "core_affect_valence": data_analysis.get("core_affect_analysis").get("valence"),
                "core_affect_arousal":  data_analysis.get("core_affect_analysis").get("arousal"),
                "core_affect_rationale": data_analysis.get("core_affect_analysis").get("rationale"),

                    # Access subfields for cognitive_appraisal_and_conceptualization
                "cognitive_appraisal_thought_process": data_analysis.get("cognitive_appraisal_and_conceptualization").get("thought_process"),
                "cognitive_appraisal_analysis": data_analysis.get("cognitive_appraisal_and_conceptualization").get("analysis"),
                "cognitive_appraisal_rationale": data_analysis.get("cognitive_appraisal_and_conceptualization").get("rationale"),

                    # Access subfields for cultural_and_social_context
                "cultural_context_thought_process": data_analysis.get("cultural_and_social_context").get("thought_process"),
                "cultural_context_analysis": data_analysis.get("cultural_and_social_context").get("discussion"),
                "cultural_context_rationale": data_analysis.get("cultural_and_social_context").get("rationale"),

                    # Access subfields for emotion_construction_analysis
                "emotion_construction_thought_process": data_analysis.get("emotion_construction_analysis").get("thought_process"),
                "emotion_construction_analysis": data_analysis.get("emotion_construction_analysis").get("analysis"),
                "emotion_construction_rationale": data_analysis.get("emotion_construction_analysis").get("rationale"),

                    # Access subfields for emotional_dynamics_and_changes
                "emotional_dynamics_thought_process": data_analysis.get("emotional_dynamics_and_changes").get("thought_process"),
                "emotional_dynamics_analysis": data_analysis.get("emotional_dynamics_and_changes").get("analysis"),
                "emotional_dynamics_rationale": data_analysis.get("emotional_dynamics_and_changes").get("rationale"),

                    # Access subfields for emotional_profile
                "emotional_profile_thought_process": data_profile.get("thought_process"),
                "emotional_profile_nuanced_classification": data_profile.get("nuanced_classification"),
                "emotional_profile_rationale": data_profile.get("rationale")
            },
            dataset_id=dataset.id)
        
        print(f"Successfully added run to dataset '{dataset_name}'")
        return dataset
    except Exception as e:
        print(f"Error creating dataset: {str(e)}")
        raise