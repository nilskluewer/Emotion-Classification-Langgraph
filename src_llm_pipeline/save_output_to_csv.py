import os
from data_models import HolisticEmotionAnalysis
import csv

def main(emotion_analysis: HolisticEmotionAnalysis, 
         model_temperature: float, 
         top_p: float,
         batch_id: str, 
         user_id: str, 
         run_id: str,
         timestamp: str, 
         model_name: str,
         prompt_template_version: str, 
         filename: str = "emotion_analysis.csv"):
    
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")

        if not file_exists:
            header = [
                "Timestamp", 
                "Run ID", 
                "User ID", 
                "Batch ID", 
                "Model Name", 
                "Prompt Template Version",
                # Core Affect Analysis
                "Core Affect Thought Process",
                "Valence",
                "Arousal",
                "Core Affect Rationale",
                # Cognitive Appraisal
                "Cognitive Appraisal Thought Process",
                "Cognitive Analysis",
                "Cognitive Rationale",
                # Cultural and Social Context
                "Cultural Context Thought Process",
                "Cultural Discussion",
                "Cultural Rationale",
                # Emotion Construction
                "Emotion Construction Analysis",
                "Emotion Construction Rationale",
                # Emotional Dynamics
                "Emotional Dynamics Analysis",
                "Emotional Dynamics Rationale",
                # Holistic Profile
                "Holistic Description",
                "Nuanced Classification",
                "Holistic Rationale",
                # Model Parameters
                "Model Temperature",
                "Top P"
            ]
            writer.writerow(header)

        row = [
            timestamp,
            run_id,
            user_id,
            batch_id,
            model_name,
            prompt_template_version,
            # Core Affect Analysis
            emotion_analysis.core_affect_analysis.thought_process,
            emotion_analysis.core_affect_analysis.valence,
            emotion_analysis.core_affect_analysis.arousal,
            emotion_analysis.core_affect_analysis.rationale,
            # Cognitive Appraisal
            emotion_analysis.cognitive_appraisal_and_conceptualization.thought_process,
            emotion_analysis.cognitive_appraisal_and_conceptualization.analysis,
            emotion_analysis.cognitive_appraisal_and_conceptualization.rationale,
            # Cultural and Social Context
            emotion_analysis.cultural_and_social_context.thought_process,
            emotion_analysis.cultural_and_social_context.discussion,
            emotion_analysis.cultural_and_social_context.rationale,
            # Emotion Construction
            emotion_analysis.emotion_construction_analysis.analysis,
            emotion_analysis.emotion_construction_analysis.rationale,
            # Emotional Dynamics
            emotion_analysis.emotional_dynamics_and_changes.analysis,
            emotion_analysis.emotional_dynamics_and_changes.rationale,
            # Holistic Profile
            emotion_analysis.holistic_emotional_profile.description,
            emotion_analysis.holistic_emotional_profile.nuanced_classification,
            emotion_analysis.holistic_emotional_profile.rationale,
            # Model Parameters
            model_temperature,
            top_p
        ]
        writer.writerow(row)

    print(f"Data has been appended to {filename}")