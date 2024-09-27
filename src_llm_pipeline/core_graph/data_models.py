from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Annotated, List

class CoreAffectAnalysis(BaseModel):
    """Represents the analysis of core affect, including valence and arousal."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing core affect, considering both valence (pleasantness) and arousal (activation). Reference specific expressions, language, and contextual factors that indicate the user's emotional state.")
    ]
    valence: Annotated[
        str,
        Field(description="Classify the valence of the user's emotional state (e.g., positive, neutral, negative), reflecting the degree of pleasantness or unpleasantness.")
    ]
    arousal: Annotated[
        str,
        Field(description="Classify the arousal level of the user's emotional state (e.g., high arousal, moderate arousal, low arousal), indicating the activation or energy level.")
    ]

class EmotionalAspectExtended(BaseModel):
    """Provides an in-depth analysis of the user's emotional experience, incorporating key components of the theory."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing the emotional aspect, considering the user's context, cognitive appraisals, conceptualization, cultural factors, predictions, and emotional dynamics. Reference specific language and expressions used by the user.")
    ]
    classification: Annotated[
        str,
        Field(description="Classify the emotional aspect based on the thought process, referencing contextual and theoretical insights. Use emotion labels if appropriate, acknowledging their constructed nature.")
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
    emotional_blend_analysis: EmotionalBlendAnalysis
    user_need_analysis: UserNeedAnalysis