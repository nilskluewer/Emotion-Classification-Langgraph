from pydantic import BaseModel, Field
from typing import Dict, Any

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal.
class CoreAffectAnalysis(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Detail the step-by-step reasoning in analyzing core affect, considering valence (pleasantness) and arousal (activation). "
            "Reference specific expressions, language, and contextual factors influencing the user's core affect."
        )
    )
    valence: str = Field(
        ...,
        description="Classify the valence of the user's emotional state (e.g., positive, neutral, negative), noting any fluctuations."
    )
    arousal: str = Field(
        ...,
        description="Classify the arousal level of the user's emotional state (e.g., low, moderate, high), indicating activation or energy levels."
    )
    rationale: str = Field(
        ...,
        description=(
            "Provide theoretical justification for your analysis, explaining how Barrett's concepts of core affect support your conclusions. "
            "Include brief citations where appropriate."
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions.
class CognitiveAppraisalAndConceptualization(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Detail the reasoning in analyzing the user's cognitive appraisals and conceptualizations. "
            "Reference specific interpretations, judgments, language use, and conceptual knowledge."
        )
    )
    analysis: str = Field(
        ...,
        description="Present your findings on how the user's interpretations and conceptual knowledge contribute to their emotional construction."
    )
    rationale: str = Field(
        ...,
        description=(
            "Explain your reasoning with theoretical support from Barrett's work, illustrating how these cognitive processes shape the user's emotions. "
            "Include brief citations."
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions.
class CulturalAndSocialContext(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Analyze the situational, cultural, and social contextual factors influencing the user's emotions. "
            "Include relevant past experiences and expectations."
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences influence the user's emotions."
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "Provide theoretical justification, explaining how Barrett's theory accounts for the impact of these factors on emotional experiences. "
            "Include brief citations."
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions.
class EmotionConstructionAnalysis(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Explain your reasoning in synthesizing insights from core affect, cognitive appraisals, conceptualization, and cultural/social context."
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Present your findings on how the user's emotions are dynamically constructed through the interplay of these elements."
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "Demonstrate how Barrett's dynamic interaction model supports your analysis, using evidence from the context. "
            "Include brief citations."
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time.
class EmotionalDynamicsAndChanges(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Detail your reasoning in analyzing emotional dynamics and changes over time within the user's interactions."
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Identify changes or fluctuations in the user's emotions throughout their interactions, noting shifts in valence and arousal."
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "Explain how these dynamics reflect the user's emotional processing over time, referencing Barrett's concepts. "
            "Include brief citations."
        )
    )

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state.
class HolisticEmotionalProfile(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Integrate all insights from your analyses to compose a holistic emotional profile of the user."
        )
    )
    description: str = Field(
        ...,
        description=(
            "Provide a nuanced, context-dependent description of the user's overall emotional profile, avoiding fixed labels."
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "Explain your reasoning clearly, synthesizing insights from all analyses, and relating it to Barrett's theoretical framework. "
            "Include brief citations."
        )
    )

# HolisticEmotionAnalysis encompasses all aspects of the analysis.
class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
    holistic_emotional_profile: HolisticEmotionalProfile
    
    
 # TODO: Update the data model classes to include the necessary fields and descriptions.   
    
from pydantic import BaseModel, Field
# The following classes are used to define the data model for the output of the emotion analysis pipeline.

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of user's affective experiences.
class CoreAffectAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step by step thought process of how you intent to analyse the core affect, considering"
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over"
            "time. Reference specific expressions, language, and contextual factors."
        )
    )
    valence: str = Field(
        ...,
        description="Classify the valence of the user's emotional state, noting any fluctuations."
    )
    arousal: str = Field(
        ...,
        description="Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any changes over time."
    )
    rationale: str = Field(
        ...,
        description="**Include a clear short rationale explaining on how you arrived at your conclusions, supported by"
                    "your research.**"
    )

# CognitiveAppraisalAndConceptualization examines how users' interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description="Provide a detailed step-by-step thought process of how you intend to analyse the user's cognitive appraisals and conceptualizations. Refer to specific interpretations, judgements, language use, and conceptual knowledge."
    )
    analysis: str = Field(
        ...,
        description="Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
                    "Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences."
    )
    rationale: str = Field(
        ...,
        description="**Include a clear short rationale explaining on how you arrived at your conclusions, supported by"
                    "your research.**"
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description="Provide a detailed step by step thought process how you want to discuss the situational, cultural, and social contextual factors influencing the user's emotions, including past experiences and expectations."
    )
    discussion: str = Field(
        ...,
        description="Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences could influence the user's emotional experiences. "
                    "Support your discussion by explaining the impact of these factors on the user's emotions, with supporting observations."
    )
    rationale: str = Field(
        ...,
        description="**Include a clear short rationale explaining on how you arrived at your conclusions, supported by"
                    "your research.**"
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=""
    )
    analysis: str = Field(
        ...,
        description="Analyse how the user's emotions are constructed through the interplay of core affect, cognitive"
                    " appraisals, conceptualization, and contextual factors. Integrate the insights you gain during the"
                    " generation of the previous analyses parts.")
    rationale: str = Field(
        ...,
        description="**Explain your reasoning by integrating insights from previous sections to demonstrate the dynamic construction of emotions.**"
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    thought_process: str = Field(
        ...,
        description=""
    )
    analysis: str = Field(
        ...,
        description="Indicate any changes or fluctuations in the user's emotions throughout their interactions, noting shifts in valence and arousal."
    )
    rationale: str = Field(
        ...,
        description="**Explain how these emotional dynamics reflect the user's emotional processing and construction over time.**"
    )

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    thought_process: str = Field(
        ...,
        description="Describe the user's overall emotional profile in a nuanced, context-dependent manner, avoiding fixed emotion labels and acknowledging complexity."
    )
    nuanced_classification: str = Field(
        ...,
        description="Provide a nuanced classification of the user's emotional state, integrating insights from the analysis. Use emotion labels if appropriate, acknowledging their constructed nature."
    )
    rationale: str = Field(...,
        description="**Provide a rationale that synthesizes insights from previous sections to present a coherent emotional profile.**"
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
    holistic_emotional_profile: HolisticEmotionalProfile
    
    @classmethod
    def model_json_schema(cls, **kwargs) -> Dict[str, Any]:
        schema = super().model_json_schema(**kwargs)
        schema["propertyOrdering"] = [
            "core_affect_analysis",
            "cognitive_appraisal_and_conceptualization",
            "cultural_and_social_context",
            "emotion_construction_analysis",
            "emotional_dynamics_and_changes",
            "holistic_emotional_profile"
        ]
        return schema