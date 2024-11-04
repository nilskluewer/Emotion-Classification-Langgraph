from pydantic import BaseModel, Field
# The following classes are used to define the data model for the output of the emotion analysis pipeline.

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of user's affective experiences.
class CoreAffectAnalysis(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed thought process for analyzing core affect, considering both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over time. Reference specific expressions, language, and contextual factors."
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
        description="**Include a clear rationale explaining how you arrived at your conclusions, supported by observations.**"
    )

# CognitiveAppraisalAndConceptualization examines how users' interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    thought_process: str = Field(
        ...,
        description="Provide a detailed thought process for analyzing the user's cognitive appraisals and conceptualizations. Reference specific interpretations, judgments, language use, and conceptual knowledge."
    )
    analysis: str = Field(
        ...,
        description="Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions."
    )
    rationale: str = Field(
        ...,
        description="**Explain your reasoning by illustrating how these cognitive processes shape the user's emotional experiences.**"
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    thought_process: str = Field(
        ...,
        description="Examine situational, cultural, and social contextual factors influencing the user's emotions, including past experiences and expectations."
    )
    discussion: str = Field(
        ...,
        description="Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences influence the user's emotional experiences."
    )
    rationale: str = Field(
        ...,
        description="**Provide a rationale explaining the impact of these factors on the user's emotions, with supporting observations.**"
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    analysis: str = Field(
        ...,
        description="Synthesize how the user's emotions are constructed through the interplay of core affect, cognitive appraisals, conceptualization, and contextual factors."
    )
    rationale: str = Field(
        ...,
        description="**Explain your reasoning by integrating insights from previous sections to demonstrate the dynamic construction of emotions.**"
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
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
    description: str = Field(
        ...,
        description="Describe the user's overall emotional profile in a nuanced, context-dependent manner, avoiding fixed emotion labels and acknowledging complexity."
    )
    nuanced_classification: str = Field(
        ...,
        description="Provide a nuanced classification of the user's emotional state, integrating insights from the analysis. Use emotion labels if appropriate, acknowledging their constructed nature."
    )
    rationale: str = Field(
        ...,
        description="**Provide a rationale that synthesizes insights from previous sections to present a coherent emotional profile.**"
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
    holistic_emotional_profile: HolisticEmotionalProfile