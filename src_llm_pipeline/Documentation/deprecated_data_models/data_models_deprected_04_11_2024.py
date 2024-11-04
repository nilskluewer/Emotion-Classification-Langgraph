The issue here is, that we have overlapping thought_process prompts with the actual analysis. It must be more distinct. Between thought, analysis and rationale.



from pydantic import BaseModel, Field
# The following classes are used to define the data model for the output of the emotion analysis pipeline.


# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
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

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed thought process for analyzing the user's cognitive appraisals and conceptualizations. Reference specific interpretations, judgments, language use, and conceptual knowledge."
        )
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
        description=(
            "Examine situational, cultural, and social contextual factors within the user's interactions that influence their emotions, including any relevant past experiences and expectations."
        )
    )
    discussion: str = Field(
        ...,
        description=(
            "Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences influence the user's emotional experiences."
        )
    )
    rationale: str = Field(
        ...,
        description="**Provide a rationale explaining the impact of these factors on the user's emotions, supported by observations from the context.**"
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Explan your thought process to analyse the insights from your analyses on core affect, cognitive appraisals, conceptualization, and cultural/social context to understand how the user's emotions are constructed."
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Synthesize how the user's emotions are dynamically constructed through the interplay of core affect, cognitive appraisals, conceptualization, and contextual factors."
        )
    )
    rationale: str = Field(
        ...,
        description="**Explain your reasoning by demonstrating the dynamic interaction of these elements in constructing the user's emotions, using evidence from the context.**"
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Analyze the emotional dynamics and changes over time within the user's interactions. Consider how the user's emotions fluctuate throughout their comment history, noting specific instances and contextual factors."
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Identify any changes or fluctuations in the user's emotions throughout their interactions, noting shifts in valence and arousal."
        )
    )
    rationale: str = Field(
        ...,
        description="**Explain how these emotional dynamics reflect the user's emotional processing and construction over time, referencing examples from the context.**"
    )

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed thought process integrating all insights from your already written analyses on how to compose a holistic emotional profile of the user. Consider the complexity and context-dependency of the user's emotional experiences."
        )
    )
    description: str = Field(
        ...,
        description=(
            "Provide a nuanced, context-dependent description of the user's overall emotional profile, avoiding fixed emotion labels and acknowledging the complexity of their emotional experiences."
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Offer a nuanced classification of the user's emotional state, integrating insights from your analyses. Use emotion labels if appropriate, while acknowledging their constructed and fluid nature."
        )
    )
    rationale: str = Field(
        ...,
        description="**Present a coherent emotional profile by synthesizing insights from all your analyses, explaining your reasoning clearly.**"
    )

# HolisticEmotionAnalysis encompasses all aspects of the analysis.
class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
    holistic_emotional_profile: HolisticEmotionalProfile
    
    
print(HolisticEmotionAnalysis.model_json_schema()) 