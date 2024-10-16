import os
from data_models import EmotionAnalysisOutput, BasicNeed
import csv

def main(emotion_analysis: EmotionAnalysisOutput, model_temperature: float, top_p: float,
         batch_id, user_id: str, run_id: str,timestamp: str, model_name,
         prompt_template_version, filename: str = "emotion_analysis.csv",
         ):
    file_exists = os.path.isfile(filename)

    # Get all possible BasicNeed values
    #all_basic_needs = [need.value for need in BasicNeed]

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")

        if not file_exists:
            header = [
                         "Timestamp", "Run ID", "User ID", "batch_id", "Model Name", "Prompt Template Version",
                         "Core Affect Thought", "Valence", "Arousal",
                         "Emotional Aspect Thought", "Emotional Aspect Nuanced Classification", "Context",
                         "Cognitive Appraisal", "Conceptualization", "Cultural Influence",
                         "Predictions and Simulations", "Emotional Dynamics",
                         "model_temperature", "top_p"
        #                 "Emotional Blend Thought", "Emotional Blend Classifications",
        #                 "User Need Thought"
        #             ] + all_basic_needs  # Add all basic needs as separate columns
                ]
            writer.writerow(header)

        # Prepare the basic needs flags
        #basic_needs_flags = [1 if need in emotion_analysis.user_need_analysis.basic_needs else 0 for need in all_basic_needs]

        row = [
                  timestamp, run_id,user_id, batch_id, model_name, prompt_template_version,
                  emotion_analysis.core_affect_analysis.thought,
                  emotion_analysis.core_affect_analysis.valence,
                  emotion_analysis.core_affect_analysis.arousal,
                  emotion_analysis.emotional_aspect_extended.thought,
                  emotion_analysis.emotional_aspect_extended.nuanced_classification,
                  emotion_analysis.emotional_aspect_extended.context,
                  emotion_analysis.emotional_aspect_extended.cognitive_appraisal,
                  emotion_analysis.emotional_aspect_extended.conceptualization,
                  emotion_analysis.emotional_aspect_extended.cultural_influence,
                  emotion_analysis.emotional_aspect_extended.predictions_and_simulations,
                  emotion_analysis.emotional_aspect_extended.emotional_dynamics,
            model_temperature, top_p
    #              emotion_analysis.emotional_blend_analysis.thought,
    #           ", ".join(emotion_analysis.emotional_blend_analysis.classifications),
    #          emotion_analysis.user_need_analysis.thought
    #         ] + basic_needs_flags  # Add the flags to the row
        ]
        writer.writerow(row)

    print(f"Data has been appended to {filename}")