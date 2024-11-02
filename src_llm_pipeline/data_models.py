from pydantic import BaseModel, Field


class OverallThoughtProcess(BaseModel):
    analysis: str = Field(
        ...,
        description=(
            "Provide a comprehensive analysis of the user's emotional experiences across all interactions. "
            "Consider the user's behavior holistically, integrating context, language, cultural influences, "
            "and social dynamics as per Barrett's theory of constructed emotion. "
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear rationale explaining how you arrived at your conclusions, referencing specific observations.**"
        )
    )

class CoreAffectOverview(BaseModel):
    summary: str = Field(
        ...,
        description=(
           "Summarize the user's general core affect (valence and arousal) throughout their interactions. "
            "Explain how these dimensions manifest in the user's behavior, supported by specific examples. "
        )
    )
    rationale: str = Field(
        ...,
        description=(
             "**Provide a rationale for your assessment based on patterns observed in the user's expressions and interactions.**"
        )
    )

class EmotionConstructionAnalysis(BaseModel):
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's emotions are constructed through the interplay of core affect, conceptualization, "
            "contextual factors, and cultural influences. "
         )
    )
    rationale: str = Field(
        ...,
        description=(
          "**Explain your reasoning by illustrating how these components combine to shape the user's emotional experiences.**"
        )
    )

class ConceptualizationAndLanguage(BaseModel):
    examination: str = Field(
        ...,
        description=(
           "Examine the role of conceptual knowledge and language in shaping the user's emotional experiences. "
            "Provide examples of language use that indicate how the user constructs their emotions. "
         )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a rationale explaining how specific language patterns reflect the user's conceptualization processes.**"
        )
    )

class CulturalAndSocialContext(BaseModel):
    discussion: str = Field(
        ...,
        description=(
            "Discuss how cultural norms, societal values, and social interactions influence the user's emotional experiences. "
            "Incorporate relevant contextual information from the user's environment. "
         )
    )
    rationale: str = Field(
        ...,
        description=(
           "**Provide a rationale explaining the impact of these factors on the user's emotions, with supporting observations.**"
        )
    )

class HolisticEmotionalProfile(BaseModel):
    description: str = Field(
        ...,
        description=(
           "Describe the user's overall emotional profile in a nuanced, context-dependent manner. "
            "Avoid fixed emotion labels, acknowledging the variability and complexity of emotions as constructed experiences. "
        )
    )
    rationale: str = Field(
        ...,
        description=(
             "**Provide a rationale that synthesizes insights from previous sections to present a coherent emotional profile.**"
        )
    )

class HolisticEmotionAnalysis_OLD(BaseModel):
    """
    The HolisticEmotionAnalysis model provides a comprehensive framework for analyzing a user's emotional experiences
    based on Lisa Feldman Barrett's theory of constructed emotion. This model emphasizes a holistic approach,
    considering the user's behavior across all interactions within their context sphere.

    **Purpose:**
    - To analyze how emotions are constructed through the interplay of core affect, conceptualization, language,
      cultural influences, and social context.
    - To provide a nuanced, context-dependent emotional profile of the user.
    - To ensure that each aspect of the analysis includes a clear rationale, enhancing transparency and replicability.

    **Instructions for Use:**
    - **Holistic Approach:** Evaluate the user's overall behavior and interactions rather than isolating individual comments.
    - **Integrate Context:** Consider situational factors, cultural and societal norms, and social dynamics influencing the user.
    - **Provide Rationales:** Include detailed explanations in each field, justifying how you arrived at your conclusions.
    - **Avoid Fixed Labels:** Describe emotions in a nuanced manner, acknowledging variability and complexity.

    **Note:** This model is designed to guide analysts in producing a thoughtful and theoretically aligned analysis
    of a user's emotional experiences, suitable for applications in research aligned with Barrett's theory.
    """
    overall_thought_process: OverallThoughtProcess = Field(
        ...,
        description="Analysis and rationale for the user's emotional experiences across all interactions."
    )
    core_affect_overview: CoreAffectOverview = Field(
        ...,
        description="Summary and rationale for the user's core affect throughout interactions."
    )
    emotion_construction_analysis: EmotionConstructionAnalysis = Field(
        ...,
        description="Analysis and rationale of emotion construction."
    )
    conceptualization_and_language: ConceptualizationAndLanguage = Field(
        ...,
        description="Examination and rationale of conceptualization and language role."
    )
    cultural_and_social_context: CulturalAndSocialContext = Field(
        ...,
        description="Discussion and rationale of cultural and social context's influence."
    )
    holistic_emotional_profile: HolisticEmotionalProfile = Field(
        ...,
        description="Description and rationale of the user's holistic emotional profile."
    )
    
    
    
# Old Data model

from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Annotated, List

# I use : "dimensional properties" -> "Focusing on core affect (valence and arousal) might be a useful starting point, recognizing that these are dimensional properties rather than discrete categories"

class CoreAffectAnalysis(BaseModel):
    """Represents the analysis of core affect as **dimensional properties**, including valence and arousal on the theory of Lisa Feldmann Barrett.
     Use more nuanced and specific language that captures the complexity of emotion classification after Lisa Feldmann Barrett"""
    thought: Annotated[
        str,
        Field(description="Provide a detailed step by step thought process for analyzing core affect as dimensional properties, considering both valence (pleasantness) and arousal (activation). Reference specific expressions, language, and contextual factors that indicate the user's emotional state.")
    ]
    valence: Annotated[
        str,
        Field(description="Classify the valence of the user's emotional state, reflecting the degree of pleasantness or unpleasantness. ")
    ]
    arousal: Annotated[
        str,
        Field(description="Classify the arousal level of the user's emotional state, indicating the activation or energy level.")
    ]

class EmotionalAspectExtended(BaseModel):
    """Provides an in-depth analysis of the user's emotional experience, incorporating key components of the theory of
     constructed emotions by Lisa Feldmann Barrett."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing the emotional aspect, considering the user's context, cognitive appraisals, conceptualization, cultural factors, predictions, and emotional dynamics. Reference specific language and expressions used by the user.")
    ]
    context: Annotated[
        str,
        Field(description="Describe situational and social contextual factors influencing the emotion, such as the topic of discussion, current events, or interactions with other users.")
    ]
    cognitive_appraisal: Annotated[
        str,
        Field(description="Explain the user's interpretations, judgments, and meaning-making processes affecting their emotional state. Consider their perspective on events discussed.")
    ]
    conceptualization: Annotated[
        str,
        Field(description="Describe how the user's conceptual knowledge, language use, and cultural background contribute to the construction of their emotion. Reference specific concepts or metaphors used.")
    ]
    cultural_influence: Annotated[
        str,
        Field(description="Note any cultural or societal norms, values, or beliefs that may shape the user's emotional experience. Consider cultural references or shared understandings.")
    ]
    predictions_and_simulations: Annotated[
        str,
        Field(description="Discuss how the user's past experiences, memories, and expectations (predictions) influence their current emotional responses. Consider references to past events or anticipated outcomes.")
    ]
    emotional_dynamics: Annotated[
        str,
        Field(description="Indicate any changes or fluctuations in emotion throughout the comments, noting shifts in valence or arousal. Describe how emotions evolve over time or in response to interactions.")
    ]
    nuanced_classification: Annotated[
        str,
        Field(description="Classify the emotional aspect based nuanced based on the thought process, context, cognitive_appraisal, conceptualization, cultural_influence, predictions_and_simulations, emotional_dynamics. Referencing contextual and theoretical insights. Use emotion labels if appropriate, acknowledging their constructed nature.")
    ]

class EmotionalBlendAnalysis(BaseModel):
    """Represents the analysis of emotional blends in the user's experience."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for identifying and analyzing multiple emotions that are intertwined within the user's comments. Describe how these emotions interact and contribute to the overall emotional experience.")
    ]
    classifications: Annotated[
        List[str],
        Field(description="List the emotions identified in the blend, acknowledging their constructed nature.")
    ]

class BasicNeed(StrEnum):
    PHYSIOLOGICAL = "Physiological"
    SAFETY = "Safety"
    LOVE_BELONGING = "Love/Belonging"
    ESTEEM = "Esteem"
    SELF_ACTUALIZATION = "Self-Actualization"

class UserNeedAnalysis(BaseModel):
    """Analyzes the user's expressed needs based on psychological theories."""
    thought: Annotated[
        str,
        Field(description="Detailed thought process for analyzing the user's needs based on their comments. Consider psychological theories of motivation and needs (e.g., Maslow's Hierarchy of Needs, Self-Determination Theory). Reference specific expressions that indicate these needs.")
    ]
    basic_needs: Annotated[
        List[BasicNeed],
        Field(description="List of basic needs fulfilled or expressed in the user's comments. Select from categories such as Physiological, Safety, Love/Belonging, Esteem, and Self-Actualization.")
    ]

class EmotionAnalysisOutput(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    emotional_aspect_extended: EmotionalAspectExtended
#    emotional_blend_analysis: EmotionalBlendAnalysis
#    user_need_analysis: UserNeedAnalysis



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