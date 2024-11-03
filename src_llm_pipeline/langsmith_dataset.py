from langsmith import Client
from typing import Optional, List, Dict
import pandas as pd

def create_langsmith_dataset(
    batch_results: List[Dict],
    batch_id: str,
    dataset_name: str,
    dataset_description: str = "Emotion Analysis Dataset",
    client: Optional[Client] = None,
) -> None:
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
            dataset_name=dataset_name,
            description=dataset_description,
            metadata={"batch_id" : batch_id}
        )

        # Add examples to dataset
        for result in batch_results:
            client.create_example(
                inputs={
                    "context_sphere": result["context_sphere"]
                },
                outputs={
                    # Core Affect Analysis
                    "core_affect_thought_process": result["emotion_analysis"].core_affect_analysis.thought_process,
                    "valence": result["emotion_analysis"].core_affect_analysis.valence,
                    "arousal": result["emotion_analysis"].core_affect_analysis.arousal,
                    "core_affect_rationale": result["emotion_analysis"].core_affect_analysis.rationale,
                    
                    # Cognitive Appraisal
                    "cognitive_thought_process": result["emotion_analysis"].cognitive_appraisal_and_conceptualization.thought_process,
                    "cognitive_analysis": result["emotion_analysis"].cognitive_appraisal_and_conceptualization.analysis,
                    "cognitive_rationale": result["emotion_analysis"].cognitive_appraisal_and_conceptualization.rationale,
                    
                    # Cultural and Social Context
                    "cultural_thought_process": result["emotion_analysis"].cultural_and_social_context.thought_process,
                    "cultural_discussion": result["emotion_analysis"].cultural_and_social_context.discussion,
                    "cultural_rationale": result["emotion_analysis"].cultural_and_social_context.rationale,
                    
                    # Emotion Construction
                    "construction_analysis": result["emotion_analysis"].emotion_construction_analysis.analysis,
                    "construction_rationale": result["emotion_analysis"].emotion_construction_analysis.rationale,
                    
                    # Emotional Dynamics
                    "dynamics_analysis": result["emotion_analysis"].emotional_dynamics_and_changes.analysis,
                    "dynamics_rationale": result["emotion_analysis"].emotional_dynamics_and_changes.rationale,
                    
                    # Holistic Profile
                    "holistic_description": result["emotion_analysis"].holistic_emotional_profile.description,
                    "nuanced_classification": result["emotion_analysis"].holistic_emotional_profile.nuanced_classification,
                    "holistic_rationale": result["emotion_analysis"].holistic_emotional_profile.rationale
                },
                dataset_id=dataset.id
            )
        
        print(f"Successfully created dataset '{dataset_name}' in LangSmith with {len(batch_results)} examples")
        return dataset
    except Exception as e:
        print(f"Error creating dataset: {str(e)}")
        raise