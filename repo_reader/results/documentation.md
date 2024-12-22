# Repository Documentation

## `Documentation/deprecated_data_models/data_models_deprecated_on_31_10_2024.py`

```
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
```

## `Documentation/deprecated_data_models/data_models_deprected_04_11_2024.py`

```
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
```

## `Documentation/deprecated_data_models/data_models_deprecated_03_11_2024 copy.py`

```
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
```

## `Documentation/deprecated_data_models/data_models_07_11_2024.py`

```
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
```

### TODOs in `Documentation/deprecated_data_models/data_models_07_11_2024.py`

<TODOs>
  <TODO>Update the data model classes to include the necessary fields and descriptions.</TODO>
</TODOs>

## `Documentation/deprecated_data_models/data_models.py`

```
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Annotated, List

class BasicNeed(StrEnum):
    KNOWLEDGE = "Knowledge"
    UNDERSTANDING = "Understanding"
    FEELING = "Feeling"
    DOING = "Doing"

class UserNeed(StrEnum):
    KEEP_ME_ENGAGED = "Keep me engaged"
    UPDATE_ME = "Update me"
    EDUCATE_ME = "Educate me"
    GIVE_ME_PERSPECTIVE = "Give me perspective"
    DIVERT_ME = "Divert me"
    INSPIRE_ME = "Inspire me"
    CONNECT_ME = "Connect me"
    HELP_ME = "Help me"

class EmotionalAspect(BaseModel):
    """Represents a single thought-classification pair for an emotional aspect."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing the aspect. Go step by step "
                          "and be cautious. Try to include information relevant to understand the user. What "
                          "is different from other users, how does he behave in the communication with others, and "
                          "dependent on the Article? Try to grasp the full context of the user and not just single "
                          "statements he made, but statements in relation to its context.")
    ]
    classification: Annotated[
        str,
        Field(description="Classify the emotional aspect based on the thought process, referencing contextual and theoretical insights.")
    ]
    
class ValenceAnalysis(BaseModel):
    """Represents the analysis for emotion valence."""
    aspect: Annotated[
        EmotionalAspect,
        Field(description="Thought and classification for emotion valence in emotional subtleties.")
    ]

class EngagementAnalysis(BaseModel):
    """Represents the analysis for engagement level."""
    aspect: Annotated[
        EmotionalAspect,
        Field(description="Thought and classification for engagement level using emotional subtleties.")
    ]

class PolarizationAnalysis(BaseModel):
    """Represents the analysis for emotional polarization."""
    aspect: Annotated[
        EmotionalAspect,
        Field(description="Thought and classification for emotional polarization using emotional subtleties")
    ]

class EmotionalBlends(BaseModel):
    """Represents the analysis for emotional blends."""
    aspect: Annotated[
        EmotionalAspect,
        Field(description="Are there multiple emotions intertwined within the text?  If so, describe how these emotions interact and contribute to the overall emotional tone.")
    ]

class UserNeedAnalysis(BaseModel):
    thought: Annotated[str, Field(description="Detailed thought process for analyzing the user need.")]
    basic_needs: Annotated[List[BasicNeed], Field(description="List of basic needs the comment fulfills.")]
    user_needs: Annotated[
    List[UserNeed],
    Field(description="List of user needs the comment fulfills. Each user need corresponds to a specific question wording:\n"
                        "- Keep me engaged: 'News that keeps me engaged with issues in society'\n"
                        "- Update me: 'News that keeps me up to date with what's going on'\n"
                        "- Educate me: 'News that helps me learn more about topics and events'\n"
                        "- Give me perspective: 'News that offers different perspectives on topical issues'\n"
                        "- Divert me: 'News that is entertaining'\n"
                        "- Inspire me: 'News that makes me feel better about the world'\n"
                        "- Connect me: 'News that makes me feel connected to others in society'\n"
                        "- Help me: 'News that provides practical information and advice for day-to-day life'")
]
    
class EmotionalAspectExtended(BaseModel):
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing the aspect, considering context, cognitive appraisals, cultural factors, and any dynamic changes in emotion.")
    ]
    classification: Annotated[
        str,
        Field(description="Classify the emotional aspect based on the thought process, referencing contextual and theoretical insights.")
    ]
    context: Annotated[
        str,
        Field(description="Describe any contextual factors influencing the emotion.")
    ]
    cognitive_appraisal: Annotated[
        str,
        Field(description="Explain the user's interpretations or judgments affecting their emotional state.")
    ]
    cultural_influence: Annotated[
        str,
        Field(description="Note any cultural aspects that may shape the emotion.")
    ]
    emotional_dynamics: Annotated[
        str,
        Field(description="Indicate any changes in emotion throughout the comment.")
    ]

class EmotionAnalysisOutput(BaseModel):
    valence: ValenceAnalysis
    engagement: EngagementAnalysis
    polarization: PolarizationAnalysis
    emotional_blend : EmotionalBlends
    user_need: UserNeedAnalysis
    extendet_aspects: EmotionalAspectExtended
```

## `Dump/testing_notebooks/langsmith_dataset.py`

```
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
```

## `Dump/testing_notebooks/reponse_schema_sonnet_approach.py`

```
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
```

## `Dump/testing_notebooks/single_processing_of_input_main.py`

```
import importlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm
from save_output_to_csv import main as save_output_to_csv
from langchain_core.tracers.context import collect_runs
from uuid import UUID
from typing import Tuple
from pathlib import Path
from datetime import datetime
from langsmith import Client
from data_models import EmotionAnalysisOutput


path_folder = Path("./inputs/sample_24_09_27__12_58_size_20_tokens_1000_to_3000")

# Load environment variables
load_dotenv()

# Dynamically import the module
models = importlib.import_module("data_models")

def load_system_prompt(filename: str, folder: Path = Path("./prompts")):
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path = path_folder):
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature):
    """
    Create and return the emotion analysis chain.

    Returns:
        Chain: The configured emotion analysis chain.
    """
    queries_schema = dereference_refs(EmotionAnalysisOutput.model_json_schema())
    queries_schema.pop("$defs", None)

    prompt = ChatPromptTemplate(
        [
            ("human", load_system_prompt("LFB_role_setting_prompt.md")),
            ("ai", load_system_prompt("LFB_role_feedback_prompt.md")),
            ("human", load_system_prompt("user_task_prompt.md"))
        ]
    ).partial(context_sphere="context_sphere")

    llm = create_llm(
        model_name="gemini-1.5-pro-002",
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
    )

    return prompt | llm | PydanticOutputParser(pydantic_object=EmotionAnalysisOutput)

def run_emotion_analysis(context_sphere: str, user_id: str) -> Tuple[EmotionAnalysisOutput, UUID]:
    """
    Run the emotion analysis chain and collect the run information.

    Args:
        context_sphere (str): The context sphere containing the text to analyze.
        user_id (str): The user ID for metadata and tracing.

    Returns:
        Tuple[EmotionAnalysisOutput, UUID]: A tuple containing the emotion analysis output
        and the run ID for tracing.
    """
    emotion_analysis_chain = create_emotion_analysis_chain()

    with collect_runs() as runs_collector:
        analysis_result = emotion_analysis_chain.invoke(
            {"context_sphere": context_sphere},
            config={
                "metadata": {"user_id": user_id},
                "run_name": "Emotion_Analysis_Chain"
            }
        )

        run_id = runs_collector.traced_runs[0].id if runs_collector.traced_runs else None

    return analysis_result, run_id


def process_input_file(input_file: Path, client: Client, enable_feedback: bool, enable_csv_output: bool):
    """
    Process a single input file for emotion analysis.

    Args:
        input_file (Path): The path to the input file.
        client (Client): The LangSmith client for feedback.
        enable_feedback (bool): Flag to enable/disable feedback.
        enable_csv_output (bool): Flag to enable/disable CSV output.
    """
    user_id = input_file.stem
    context_sphere = load_input(input_file.name)

    emotion_analysis, run_id = run_emotion_analysis(context_sphere, user_id)

    print(f"Run ID: {run_id}")
    print(f"User ID: {user_id}")
    print(emotion_analysis)

    if enable_feedback and run_id:
        client.create_feedback(
            run_id=run_id,
            key="Valence",
            value=emotion_analysis.core_affect_analysis.valence,
            comment=emotion_analysis.core_affect_analysis.thought
        )
        client.create_feedback(
            run_id=run_id,
            key="Arousal",
            value=emotion_analysis.core_affect_analysis.arousal,
            comment=emotion_analysis.core_affect_analysis.thought
        )

    if enable_csv_output:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_output_to_csv(emotion_analysis, user_id, timestamp)


from typing import List, Dict
from pathlib import Path
from langchain_core.runnables import RunnableConfig
from uuid import uuid4

def process_input_files_batch(
        input_folder: Path,
        client: Client,
        model_temperature: float,
        enable_feedback: bool,
        enable_csv_output: bool,
        batch_size: int,
        max_concurrency: int
) -> None:
    """
    Process multiple input files in batches using LangChain's batch processing.

    Args:
        input_folder (Path): The folder containing input files.
        client (Client): The LangSmith client for feedback.
        enable_feedback (bool): Flag to enable/disable feedback.
        enable_csv_output (bool): Flag to enable/disable CSV output.
        batch_size (int): Number of files to process in each batch.
        max_concurrency (int): Maximum number of concurrent requests.
    """
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature = model_temperature)
    input_files = list(input_folder.glob("*.md"))

    for i in range(0, len(input_files), batch_size):
        batch_files = input_files[i:i+batch_size]
        batch_inputs = []

        for file in batch_files:
            user_id = file.stem
            context_sphere = load_input(file.name, folder=input_folder)
            batch_inputs.append({
                "context_sphere": context_sphere,
                "user_id": user_id
            })

        config = RunnableConfig(
            callbacks=None,
            tags=["emotion_analysis_batch"],
            metadata={"batch_id": str(uuid4()),
                      "run_name": "Batch Run: EA_Chain"},
            max_concurrency=max_concurrency
        )

        with collect_runs() as runs_collector:
            batch_results = emotion_analysis_chain.batch(
                batch_inputs,
                config=config
            )

        for file, result, run in zip(batch_files, batch_results, runs_collector.traced_runs):
            user_id = file.stem
            print(f"Run ID: {run.id}")
            print(f"User ID: {user_id}")
            print(result)

            if enable_feedback and run.id:
                client.create_feedback(
                    run_id=run.id,
                    key="Core Valence",
                    value=result.core_affect_analysis.valence,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Core Arousal",
                    value=result.core_affect_analysis.arousal,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Aspect Extended",
                    value=result.emotional_aspect_extended.nuanced_classification,
                    comment=result.emotional_aspect_extended.thought
                )
                """
                client.create_feedback(
                    run_id=run.id,
                    key="Blends",
                    value=", ".join(result.emotional_blend_analysis.classifications),
                    comment=result.emotional_blend_analysis.thought
                )
                """



            if enable_csv_output:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_output_to_csv(emotion_analysis = result,
                                   model_temperature=model_temperature,
                                   user_id= user_id,
                                   timestamp = timestamp)

if __name__ == "__main__":
    client = Client()
    input_folder = Path("./inputs/sp1")

    # Configure which optional steps to perform
    enable_feedback = True
    enable_csv_output = True
    model_temperature = 1

    #for input_file in input_folder.glob("*.md"):
    #    process_input_file(input_file, client, enable_feedback, enable_csv_output)
    print("---- Start of Batch processing ----")
    process_input_files_batch(
        input_folder=input_folder,
        client=client,
        model_temperature = model_temperature,
        enable_feedback=True,
        enable_csv_output=True,
        batch_size=10,
        max_concurrency=5
    )

def create_dataset_if_enabled(client: Client, dataset_name: str, run_id: UUID, enable_dataset_creation: bool):
    """
    Create a dataset in LangSmith if enabled.

    Args:
        client (Client): The LangSmith client.
        dataset_name (str): The name of the dataset to create.
        run_id (UUID): The run ID to include in the dataset.
        enable_dataset_creation (bool): Flag to enable/disable dataset creation.
    """
    if enable_dataset_creation and run_id:
        # Implement dataset creation logic here
        pass



```

## `Dump/testing_notebooks/main_deprecated_due_to_new_data_model_02_11_2024.py`

```
import importlib
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm
from save_output_to_csv import main as save_output_to_csv
from langchain_core.tracers.context import collect_runs
from uuid import uuid4
from typing import Dict
from datetime import datetime
from langsmith import Client
from data_models import EmotionAnalysisOutput
from langchain_core.callbacks import StdOutCallbackHandler
from langchain_core.runnables import RunnableConfig
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate



# Load environment variables
load_dotenv()

# Dynamically import the module
models = importlib.import_module("data_models")

def load_system_prompt(filename: str) -> Dict[str, str]:
    folder = Path(f"./prompts/{prompts_version}")
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path):
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature):
    queries_schema = dereference_refs(EmotionAnalysisOutput.model_json_schema())
    queries_schema.pop("$defs", None)

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_setting_prompt.md"))),
            AIMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_feedback_prompt.md"))),
            HumanMessagePromptTemplate.from_template(str(load_system_prompt("user_task_prompt.md")))
        ]
    ).partial(context_sphere="context_sphere")

    llm = create_llm(
        model_name=model_name,
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
        top_p=top_p
    )

    parser = PydanticOutputParser(pydantic_object=EmotionAnalysisOutput)


    return prompt | llm | parser

def process_input_files_batch(
        input_folder: Path,
        client: Client,
        model_temperature: float,
        top_p:float,
        enable_feedback: bool,
        enable_csv_output: bool,
        batch_size: int,
        max_concurrency: int
) -> None:
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature=model_temperature)
    input_files = list(input_folder.glob("*.md"))

    # Create a callback handler
    callback_handler = StdOutCallbackHandler()

    for i in range(0, len(input_files), batch_size):
        batch_files = input_files[i:i+batch_size]
        batch_inputs = []

        for file in batch_files:
            user_id = file.name.split('_')[1]
            context_sphere = load_input(file.name, folder=input_folder)
            batch_inputs.append({
                "context_sphere": context_sphere,
                "user_id": user_id
            })
        batch_id = str(uuid4())
        tag_str = "batch: " + batch_id + " , temp: " + str(model_temperature)

        config = RunnableConfig(
            callbacks=None,
            tags=["EA_Batch_"],
            metadata={"batch_id": batch_id,
                      "temperature": model_temperature,
                      "top_p":top_p,
                      "model_name": model_name,
                      "prompt_template_version": prompts_version},
            max_concurrency=max_concurrency,
            run_name="Batch Run: EA_Chain",
        )

        with collect_runs() as runs_collector:
            batch_results = emotion_analysis_chain.batch(
                batch_inputs,
                config=config
            )

        for file, result, run in zip(batch_files, batch_results, runs_collector.traced_runs):
            user_id = file.name.split('_')[1]
            print(f"Run ID: {run.id}")
            print(f"User ID: {user_id}")
            print(result)

            if enable_feedback and run.id:
                client.create_feedback(
                    run_id=run.id,
                    key="Core Valence",
                    value=result.core_affect_analysis.valence,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Core Arousal",
                    value=result.core_affect_analysis.arousal,
                    comment=result.core_affect_analysis.thought
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Aspect Extended",
                    value=result.emotional_aspect_extended.nuanced_classification,
                    comment=result.emotional_aspect_extended.thought
                )

            if enable_csv_output:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_output_to_csv(emotion_analysis=result,
                                   model_temperature=model_temperature,
                                   top_p=top_p,
                                   batch_id=batch_id,
                                   user_id=user_id,
                                   run_id=run.id,
                                   timestamp=timestamp,
                                   model_name=model_name,
                                   prompt_template_version=prompts_version)

if __name__ == "__main__":
    client = Client()
    input_folder = Path("./inputs/sp0")

    # Configure which optional steps to perform
    enable_feedback = True
    enable_csv_output = True
    # Metadata variables maybe to externalize?
    # model name
    # model temperature
    # batch run
    # model configuration top_n etc.
    # prompt folder v1 / v2 / v3 / ...

    prompts_version = "v3"
    model_name = "gemini-1.5-pro-002"
    top_p = 0
    model_temperature = 0
    test_set = ""

    print("---- Start of Batch processing ----")
    process_input_files_batch(
        input_folder=input_folder,
        client=client,
        model_temperature=model_temperature,
        top_p=top_p,
        enable_feedback=True,
        enable_csv_output=True,
        batch_size=1,
        max_concurrency=1
    )
```

## `Dump/testing_notebooks/main_old_langchain_batch_processing_without_propertyOrder.py`

```
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from utils.model import create_llm
from utils.save_output_to_csv import main as save_output_to_csv
from utils.langsmith_dataset import create_langsmith_dataset
from langchain_core.tracers.context import collect_runs
from uuid import uuid4
from typing import Dict
from datetime import datetime
from langsmith import Client
from langchain_core.runnables import RunnableConfig
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate

# Import the new data model
from utils.data_models import HolisticEmotionAnalysis

# Load environment variables
load_dotenv()


def load_system_prompt(filename: str) -> Dict[str, str]:
    folder = Path(f"./inputs/prompts/{prompts_version}")
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path):
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature):
    queries_schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
    queries_schema.pop("$defs", None)
    """
    # Add propertyOrder to all levels
    queries_schema["propertyOrder"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
        "holistic_emotional_profile"
    ]

    # Add propertyOrder for nested objects
    queries_schema["properties"]["core_affect_analysis"]["propertyOrder"] = [
        "thought_process",
        "valence",
        "arousal",
        "rationale"
    ]

    queries_schema["properties"]["cognitive_appraisal_and_conceptualization"]["propertyOrder"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]

    queries_schema["properties"]["cultural_and_social_context"]["propertyOrder"] = [
        "thought_process",
        "discussion",
        "rationale"
    ]

    queries_schema["properties"]["emotion_construction_analysis"]["propertyOrder"] = [
        "analysis",
        "rationale"
    ]

    queries_schema["properties"]["emotional_dynamics_and_changes"]["propertyOrder"] = [
        "analysis",
        "rationale"
    ]

    queries_schema["properties"]["holistic_emotional_profile"]["propertyOrder"] = [
        "description",
        "nuanced_classification",
        "rationale"
    ]
    """
    print(queries_schema)

    prompt = ChatPromptTemplate(
        messages=[
            #SystemMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_setting_prompt.md"))),
            #AIMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_feedback_prompt.md"))),
            HumanMessagePromptTemplate.from_template(str(load_system_prompt("user_task_prompt.md")))
        ]
    ).partial(context_sphere="context_sphere")

    llm = create_llm(
        model_name=model_name,
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
        top_p=top_p
    )

    parser = PydanticOutputParser(pydantic_object=HolisticEmotionAnalysis)

    return prompt | llm | parser

def process_input_files_batch(
        input_folder: Path,
        client: Client,
        model_temperature: float,
        top_p: float,
        enable_feedback: bool,
        enable_csv_output: bool,
        enable_dataset_creation: bool,
        batch_size: int,
        max_concurrency: int
) -> None:
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature=model_temperature)
    input_files = list(input_folder.glob("*.md"))
    batch_id = str(uuid4())
    
    # Create CSV filename with batch_id
    batch_results_for_dataset = []  # New list to collect all results

    for i in range(0, len(input_files), batch_size):
        batch_files = input_files[i:i+batch_size]
        batch_inputs = []

        for file in batch_files:
            user_id = file.name.split('_')[1]
            context_sphere = load_input(file.name, folder=input_folder)
            batch_inputs.append({
                "context_sphere": context_sphere,
                "user_id": user_id
            })

        config = RunnableConfig(
            callbacks=None,
            tags=["EA_Batch_"],
            metadata={
                "batch_id": batch_id,
                "temperature": model_temperature,
                "top_p": top_p,
                "model_name": model_name,
                "prompt_template_version": prompts_version
            },
            max_concurrency=max_concurrency,
            run_name="Batch Run: EA_Chain",
        )

        with collect_runs() as runs_collector:
            batch_results = emotion_analysis_chain.batch(
                batch_inputs,
                config=config
            )

        for file, result, run in zip(batch_files, batch_results, runs_collector.traced_runs):
            user_id = file.name.split('_')[1]
            context_sphere = batch_inputs[batch_files.index(file)]["context_sphere"]
            
            batch_results_for_dataset.append({
                "context_sphere": context_sphere,
                "emotion_analysis": result,
                "user_id": user_id,
                "run_id": run.id
            })
            
            print(f"Run ID: {run.id}")
            print(f"User ID: {user_id}")
            print(result)

            if enable_feedback and run.id:
                client.create_feedback(
                    run_id=run.id,
                    key="Core Affect Analysis",
                    value=result.core_affect_analysis.valence,
                    comment=result.core_affect_analysis.thought_process
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Cognitive Appraisal",
                    value=result.cognitive_appraisal_and_conceptualization.analysis,
                    comment=result.cognitive_appraisal_and_conceptualization.thought_process
                )
                client.create_feedback(
                    run_id=run.id,
                    key="Holistic Profile",
                    value=result.holistic_emotional_profile.nuanced_classification,
                    comment=result.holistic_emotional_profile.description
                )

            if enable_csv_output:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_output_to_csv(
                    emotion_analysis_input=context_sphere,
                    emotion_analysis=result,
                    model_temperature=model_temperature,
                    top_p=top_p,
                    batch_id=batch_id,
                    user_id=user_id,
                    run_id=run.id,
                    timestamp=timestamp,
                    model_name=model_name,
                    prompt_template_version=prompts_version
                )

    # Create dataset after all processing is complete
    if enable_dataset_creation:
        dataset_name = f"Emotion_Analysis_Batch_{batch_id}"
        dataset_description = (
            f"Emotion analysis results for batch {batch_id}. "
            f"Model: {model_name}, Temperature: {model_temperature}, "
            f"Top P: {top_p}, Prompt Version: {prompts_version}"
        )
        try:
            create_langsmith_dataset(
                batch_results=batch_results_for_dataset,
                batch_id=batch_id,
                dataset_name=dataset_name,
                dataset_description=dataset_description,
                client=client
            )
        except Exception as e:
            print(f"Warning: Dataset creation failed: {str(e)}")

if __name__ == "__main__":
    client = Client()
    input_folder = Path("./inputs/sp0")

    enable_feedback = True
    enable_csv_output = True
    enable_dataset_creation = True  # New configuration
    
    prompts_version = "v5"
    model_name = "gemini-1.5-pro-002"
    top_p = 0
    model_temperature = 0
    test_set = ""

    print("---- Start of Batch processing ----")
    process_input_files_batch(
        input_folder=input_folder,
        client=client,
        model_temperature=model_temperature,
        top_p=top_p,
        enable_feedback=enable_feedback,
        enable_csv_output=enable_csv_output,
        enable_dataset_creation=enable_dataset_creation,  # New parameter
        batch_size=10,
        max_concurrency=10
    )
```

## `Dump/testing_notebooks/new_data_model.py`

```
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.utils.json_schema import dereference_refs
from model import create_llm  # Assuming you have this utility function
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate



# Import your new data model
from data_models import HolisticEmotionAnalysis

# Load environment variables
load_dotenv()

def load_system_prompt(filename: str) -> str:
    folder = Path(f"./prompts/{prompts_version}")
    return (folder / filename).read_text()

def load_input(filename: str, folder: Path) -> str:
    return (folder / filename).read_text()

def create_emotion_analysis_chain(model_temperature: float):
    # Get the schema for the new data model
    queries_schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
    queries_schema.pop("$defs", None)

    # Create a simple prompt template
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_setting_prompt.md"))),
            AIMessagePromptTemplate.from_template(str(load_system_prompt("LFB_role_feedback_prompt.md"))),
            HumanMessagePromptTemplate.from_template(str(load_system_prompt("user_task_prompt.md")))
        ]
    ).partial(context_sphere="context_sphere")

    # Create the LLM
    llm = create_llm(
        model_name=model_name,
        temperature=model_temperature,
        response_mime_type="application/json",
        response_schema=queries_schema,
    )

    # Create the parser for the new data model
    parser = PydanticOutputParser(pydantic_object=HolisticEmotionAnalysis)

    # Create the chain
    return prompt | llm | parser

def process_single_input(input_folder: Path, model_temperature: float) -> None:
    # Create the analysis chain
    emotion_analysis_chain = create_emotion_analysis_chain(model_temperature=model_temperature)
    
    # Get the first input file
    input_file = next(input_folder.glob("*.md"))
    
    # Load the context
    context_sphere = load_input(input_file.name, folder=input_folder)
    
    # Process the input
    result = emotion_analysis_chain.invoke(
        {"context_sphere": context_sphere}
    )
    
    # Print the result
    print(result)

if __name__ == "__main__":
    # Basic configuration
    input_folder = Path("./inputs/sp0")
    prompts_version = "v4"
    model_name = "gemini-1.5-pro-002"
    model_temperature = 0

    print("---- Starting Simple Analysis ----")
    process_single_input(
        input_folder=input_folder,
        model_temperature=model_temperature
    )
```

## `Dump/testing_notebooks/simple_chains.py`

```
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

_ = load_dotenv()


def grade_emotionality():
    class GradeEmotionality(BaseModel):
        """Reason on how Emotional the given context is. After that give a Score on how you would rate the emotionality"""

        reasoning: str = Field(
            description="Reason on the emotionality of the given context."
        )
        score: int = Field(
            description="Score between 0 and 100 on how Emotional the given context is.",
            ge=0,
            le=100
        )


    # LLM with function call
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeEmotionality)

    # Prompt
    system = """You are a grader assessing the extend of emtionality in a given context. \n
    1. You first reason in about 5-10 Sentences why this context, or if the given context is emotional. \n
    2. Give a Score between 0 and 100 how emotional the context is."""
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Context: \n\n <context>{context}</context> \n\n"),
        ]
    )

    emotionality_grader = hallucination_prompt | structured_llm_grader
    return emotionality_grader

```

## `src_llm_pipeline/__init__.py`

```

```

## `src_llm_pipeline/emotion_classification.py`

```
import json
from pathlib import Path
from typing import List
import time

import vertexai
from dotenv import load_dotenv
from langchain_core.utils.json_schema import dereference_refs
from langsmith import Client
from langsmith import RunTree
from langsmith.run_helpers import traceable
from vertexai.generative_models import (
    GenerativeModel,
    Part,
    Content,
    GenerationConfig,
    GenerationResponse,
    SafetySetting,
)
from google.api_core.exceptions import ResourceExhausted
from icecream import ic


from .inputs.prompts.v12.data_models import (
    HolisticEmotionAnalysis,
    add_property_ordering_single_class,
    add_specific_property_ordering,
)

# from utils.langsmith_dataset import create_langsmith_dataset
from .utils.helper_functions import default_safety_settings
from .utils.langsmith_feedback import send_generation_response_feedback_to_trace
from .utils.output_parser import (
    parse_emotion_analysis,
    print_emotion_analysis,
    check_property_ordering,
)
from .utils.enums import MESSAGE_MAP
from .utils.eval_aspects import aspect_evaluator, aspect_evaluator_all_aspects, Aspect, hallucination_confabulation_evaluator

# Load environment variables
load_dotenv()
client = Client()

# --- load variables from config.json ---
with open("src_llm_pipeline/config.json", "r") as config_file:
    config = json.load(config_file)

model_name = config["model_name"]
prompts_version = config["prompt_version"]
debug_api_call = config["debug_api_call"]
debug_schema = config["debug_schema"]
llm_endpoint_location = config["llm_endpoint_location"]
check_for_hallucinations = config["check_for_hallucinations"]
dataset_tag = config["dataset_tag"]
temperature = config["temperature"]
top_p = config["top_p"]
eval_all_aspects = config["eval_all_aspects"]
validate_output_structure = config["validate_output_structure"]


# --- init vertexai ---
vertexai.init(project="rd-ri-genai-dev-2352", location=llm_endpoint_location)


# -- Helper functions --
def read_prompt(filename: str) -> str:
    """Load system prompt from file."""
    folder = Path(f"src_llm_pipeline/inputs/prompts/{prompts_version}")
    return (folder / filename).read_text()


def insert_context_sphere_into_prompt(
    context_file_name: Path, usere_task_prompt="user_task_prompt.md"
) -> str:
    context_sphere = context_file_name.read_text().strip()
    return usere_task_prompt.format(context_sphere=context_sphere)


@traceable(name="Simulate Conversation for Role Play Prompting", run_type="prompt")
def simulate_conversation(
    role_setting_prompt: str, role_feedback_prompt: str, user_task_prompt: str
) -> List[Content]:
    # Simulate the conversation flow with role play prompting
    # Consisting of a System prompt setting the scene, feedback prompt prefilling the models response
    # and the task prompt with the actual task.
    messages_google = [
        Content(role="user", parts=[Part.from_text(role_setting_prompt)]),
        Content(role="model", parts=[Part.from_text(role_feedback_prompt)]),
        Content(role="user", parts=[Part.from_text(user_task_prompt)]),
    ]
    messages_langchain = [
        {"role": "user", "content": f"{role_setting_prompt}"},
        {"role": "model", "content": f"{role_feedback_prompt}"},
        {"role": "user", "content": f"{user_task_prompt}"},
    ]
    return messages_google, messages_langchain


@traceable(name="Simulate Conversation for Role Play Prompting", run_type="prompt")
def simulate_conversation_2(
    text_0, text_1, text_2, classification, summary_classification_prompt
):
    messages_google = [
        (Content(role="model", parts=[Part.from_text(text_0)])),
        (Content(role="user", parts=[Part.from_text(text_1)])),
        (Content(role="model", parts=[Part.from_text(text_2)])),
        (Content(role="user", parts=[Part.from_text(summary_classification_prompt)])),
    ]

    messages_langchain = [
        {"role": "model", "content": text_0},
        {"role": "user", "content": text_1},
        {"role": "model", "content": text_2},
        {"role": "user", "content": summary_classification_prompt},
    ]

    return messages_google, messages_langchain

@traceable(name="Create Config with Output Instructions", run_type="tool")
def create_generation_config(
    temperature, top_p, response_schema_model=None, response_mime_type=None
) -> GenerationConfig:
    # Configure generation parameters
    generation_config = GenerationConfig(
        response_mime_type=response_mime_type,  # "application/json",
        response_schema=response_schema_model,
        temperature=temperature,
        top_p=top_p,
        # seed=1,
        max_output_tokens=8000,  # Adjust as needed
    )
    return generation_config


@traceable(name="Configue LLM with Generation Config", run_type="tool")
def configure_llm(model_name, generation_config: GenerationConfig) -> GenerativeModel:
    return GenerativeModel(model_name=model_name, generation_config=generation_config)


@traceable(
    name="LLM Call",
    run_type="llm",
    tags=["api_call"],
    metadata={"ls_model_name": f"{model_name}"},
)
def call_api(
    messages: List[dict],
    configured_llm: GenerativeModel,
    prompt: List[Content],
    safety_settings: list[SafetySetting],
    run_tree: RunTree,
) -> GenerationResponse:
    max_retries = 5
    initial_delay = 5  # initial delay in seconds for exponential backoff
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = configured_llm.generate_content(
                contents=prompt, safety_settings=safety_settings, stream=False
            )
            if debug_api_call:
                ic(response)

            messages.append({"role": "model", "content": f"{response.text}"})

            usage_metadata = response.usage_metadata
            result_dict = {
                "choices": messages,
                "usage_metadata": {
                    "input_tokens": usage_metadata.prompt_token_count,
                    "output_tokens": usage_metadata.candidates_token_count,
                    "total_tokens": usage_metadata.total_token_count,
                },
            }

            ic(result_dict)
            send_generation_response_feedback_to_trace(
                response=response, client=client, run_tree=run_tree
            )

            return result_dict

        except ResourceExhausted as e:
            print(
                f"Resource exhausted. Retry {retry_count + 1} in {initial_delay} seconds."
            )
            print("Error message: ", str(e))
            retry_count += 1
            time.sleep(initial_delay)
            initial_delay *= 2

        except Exception as e:
            # Handle any other exceptions that might occur
            print("An error occurred: ", str(e))
            return {"error": str(e)}

    # If all retries fail
    print("Maximum retries reached. Please try again later.")
    return {"error": "Resource exhausted. Maximum retries reached."}


@traceable(name="Final Output Parser", run_type="parser")
def convert_to_dict(messages: List[Content]) -> dict:
    result_dict = {}

    for index, message in enumerate(messages):
        key = f"{message.role}-{MESSAGE_MAP.get(index)}"
        result_dict[key] = " ".join(part.text for part in message.parts)

    # result_dict["full_output_unstructured"] = str(messages)
    return result_dict


@traceable(name="Append LLM Response to Conversation", run_type="parser")
def append_response(message: List, message_to_append: Content) -> List[Content]:
    message.append(message_to_append)
    return message


@traceable(name="Add Task Prompt for Summarization", run_type="parser")
def append_prompt(message: List, message_to_append: Content) -> List[Content]:
    message.append(message_to_append)
    return message


@traceable(name="Parse LLM Structure for Validation", run_type="parser")
def parse_model_response_to_data_model_structure(input_text, target_schema) -> dict:
    data = parse_emotion_analysis(text=input_text, schema=target_schema)
    return data


@traceable(name="Validate Output Structure", run_type="parser")
def validate_response_property_order(
    parsed_data, schema_with_specific_ordering
) -> bool:
    if check_property_ordering(parsed_data, schema_with_specific_ordering):
        print("Output matches schema ordering exactly!")
        return True
    else:
        print("Warning: Output does not match schema ordering")
        return False


@traceable(name="Step 1: Classification", run_type="chain")
def step_1_emotion_classification_with_structured_output(
    messages: List[dict], temperature, top_p, run_tree: RunTree
):
    # Keep it in to validate if the Hallucination Eval works - input different users into the with and without context
    role_setting_prompt = read_prompt("LFB_role_setting_prompt.md")
    role_feedback_prompt = read_prompt("LFB_role_feedback_prompt.md")
    user_task_prompt = read_prompt("user_task_prompt.md")
    context_sphere = messages[1]["content"]

    user_task_prompt_with_context = user_task_prompt.format(
        context_sphere=context_sphere
    )
    role_play_prompt_google, role_play_conversation_langchain = simulate_conversation(
        role_setting_prompt, role_feedback_prompt, user_task_prompt_with_context
    )

    # Perform setup operations without repetition
    response_schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
    response_schema.pop("$defs", None)
    response_schema_properties_ordered = add_specific_property_ordering(response_schema)
    if debug_schema:
        ic(response_schema_properties_ordered)

    llm_config = create_generation_config(
        response_schema_model=response_schema_properties_ordered,
        response_mime_type="application/json",
        temperature=temperature,
        top_p=top_p,
    )

    configured_llm = configure_llm(model_name=model_name, generation_config=llm_config)

    response = call_api(
        messages=role_play_conversation_langchain,
        configured_llm=configured_llm,
        prompt=role_play_prompt_google,
        safety_settings=default_safety_settings,
    )
    response_message = response["choices"][3]["content"]

    # Validate result
    if validate_output_structure:
        # Parse data to valide output structure
        parsed_data = parse_model_response_to_data_model_structure(
            input_text=response_message,
            target_schema=response_schema_properties_ordered,
        )
        validation_result = validate_response_property_order(
            parsed_data, response_schema_properties_ordered
        )

        # Feedback of validation result in Langsmith
        client.create_feedback(
            run_tree.id,
            key="llm_output_format_validation",
            value=validation_result,
            comment="1 = True: The model used the correct propertyOrder. False, the model did not!",
        )

    # Access the first candidate Content object in the response
    message_history = append_response(
        role_play_conversation_langchain, response_message
    )

    if debug_api_call:
        print_emotion_analysis(parsed_data, width=200)

    return message_history


@traceable(name="Step 2: Profile creation based on Classification", run_type="chain")
def step_2_summarization_of_classification(
    messages: List[dict], temperature, top_p, run_tree: RunTree
) -> List[dict]:
    """
    Created a Profile out of a given Classification. Using messages to maintain readability in langsmith.
    Args:
        messages (List[dict]): _description_
        temperature (_type_): _description_
        top_p (_type_): _description_
        run_tree (RunTree): _description_

    Returns:
        List[dict]: _description_
    """
    summary_task_prompt = read_prompt("step_2_summary_prompt.md")

    classification = messages[3]["content"]

    summary_classification_prompt = summary_task_prompt.format(
        classificaton=classification
    )
    role_play_prompt_google, role_play_prompt_langchain = simulate_conversation_2(
        text_0=messages[0]["content"],
        text_1= messages[1]["content"],
        text_2=messages[2]["content"],
        classification=summary_classification_prompt,
        summary_classification_prompt=summary_classification_prompt,
    )

    # Configure the generation parameters
    llm_config = create_generation_config(temperature=temperature, top_p=top_p)

    # Configure the LLM with the generation config
    configured_llm = configure_llm(model_name=model_name, generation_config=llm_config)

    response = call_api(
        messages=role_play_prompt_langchain,
        configured_llm=configured_llm,
        prompt=role_play_prompt_google,
        safety_settings=default_safety_settings,
    )
    response_message = response["choices"][4]["content"]

    message_history = append_response(
        message=role_play_prompt_langchain, message_to_append=response_message
    )

    return message_history


def request_emotion_analysis_with_user_id(context_sphere, user_id: int) -> dict:
    """
    Helper function to wrap main call with user_id + traceable
    """
    @traceable(
        run_type="chain",
        name="Context Aware Emotion Classification",
        tags=[
            f"{model_name}",
            f"User_ID: {user_id}",
            f"{dataset_tag}",
            f"{prompts_version}",
        ],
        metadata={
            "check_hallucinations": check_for_hallucinations,
            "eval_all_aspects": eval_all_aspects,
        },
    )
    def request_emotion_analysis(messages: List[dict], run_tree: RunTree):
        """
        Call the Google Gemini API with basic configuration.
        """

        message_history = step_1_emotion_classification_with_structured_output(
            messages, temperature, top_p
        )
        classification = message_history[3]["content"]
        
        if debug_api_call:
            ic(classification)

        hallucination_check_result = True
        hallucination_confabulation_evaluator(
            question=str(message_history[:3]),
            answer=str(classification),
            run_tree_parent_id=run_tree.id,
        )
        
        if hallucination_check_result:
            message_history = step_2_summarization_of_classification(
                messages=message_history, temperature=temperature, top_p=top_p
            )
            summary = message_history[4]["content"]
            ic(summary)
            # dict_list = convert_to_dict(message_history)
        else:
            return {"error": "Hallucination detected"}

        @traceable(name="Evaluate all aspects", run_type="chain")
        def evaluate_with_all_aspects():
            aspect_evaluator_all_aspects(
                classification,
                summary,
                llm_model_name="gpt-4o-mini",
                run_tree_parent_id=run_tree.id,
            )
            aspect_evaluator_all_aspects(
                classification,
                summary,
                llm_model_name="claude-3-5-haiku-20241022",
                run_tree_parent_id=run_tree.id,
            )

        if eval_all_aspects:
            evaluate_with_all_aspects()

        aspect_evaluator(
            classification,
            summary,
            aspect=Aspect.COMPREHENSIVENESS,
            llm_model_name="gpt-4o-mini",
            run_tree_parent_id=run_tree.id,
            langsmith_extra={"tags": [f"{Aspect.COHERENCE}"]},
        )

        return summary

    message_history = request_emotion_analysis(
        messages=[
            {"role": "user", "content": f"Subject of Analysis is: {user_id}"},
            {"role": "user", "content": f"{context_sphere}"},
        ]
    )
    return message_history

```

## `src_llm_pipeline/TODO.py`

```

# URGENT ------ URGENT

# TODO: RUN Pipeline on LLama3 -> Server RecSys L40 GPU?
# TODO: Mathias Pre-Study
# TODO: mindest token grenze für pipeline -> bring nichts einen satz zu analyisren. 

# TODO: Add cycle for improvment taking the critique from the evaluation and then improve summary
# TODO: Wenn richtig evaluiert muss man die llm as a judge auch evaluieren, + few shot examples für gut oder schlechte classifications für max alignment. Eher boolean classification. 

# OFFEN ------ OFFEN
# TODO: Benutzername "unbekannt" ersetzten durch random name oder unbekannt nummer X und dann iterrieren oder so.
# TODO: Cohere, OpenAi, Anthropic, Google anbinden
# TODO Use greedy decoding
# Cite: “we use greedy decoding for all the experiments by setting the temperature to 0, making the results deterministic. See more details in Appendix A.3.” ([Kong et al., 2024, p. 5](zotero://select/groups/5477470/items/FHNMK6LD)) ([pdf](zotero://open-pdf/groups/5477470/items/TH5V4M39?page=5&annotation=7LK49AVW))




# ERLEDIGT ----- ERLEDIGT #

# TODO: Evaluator bauen -> Dataset abspeichern zu den jeweiligen Categorien also einmal core und einmal
#  emotiona anylsis extend. Input ist thought / output ist dann die classfication. Dann evaluieren wie auch
#  in der survey, mit den gleichen fragne???
# TODO: https://platform.openai.com/docs/guides/evals
# TODO: OneShot prompting - TASK, THOUGHT, CLASSFICATION - statt - TASK, THOUGHT; ACTION

# TODO Use Cases: Einbinden das es auch für Terror detection genutzt werden könnte

# TODO: Evaluation des **Inner Monoglogue** dann immer Inner monologue vs. analyse -> HumanEval
# TODO: Write a very bad first summary and then improve it with the model
# TODO SUrvey finden - Survey items bauen!
# TODO: Summary auch strukturieren wie die initial zusammenfassung
# TODO: Added examples to summary call 
# TODO: Classification attributes festlegen durch papers
# TODO: auch auf parameter evaluieren wie: factuality, valid JSON, text quality? Mit OPENAI Evaluators?
    # store: true parameter für evaluation https://platform.openai.com/docs/guides/evals
# TODO: Latence, einfach als metric aufnehmen für evaluation!
# TODO **So, is Role-Play Prompting essentially CoT?** -> It's not quite the same, but rather a potential trigger for it.
# TODO: Labels für die classification: Erregung, Valenz, soziale Verbundenheit, Polarization, Emotionality, Polarization
# TODO: Self-consitentcy implemtneiren wie in SELF-CONSISTENCY IMPROVES CHAIN OF THOUGHT REASONING IN LANGUAGE MODELS beschrieben,
#  aber mit similarity über embeddings statt über paths & wahrscehinlichkeiten,
#  weil wir die log probs nicht für alle modell bekommen. ( 40 request pro model machen -> dann majority voting)
#  ähnlich zu More Agents is all you need
#  ODER
#  **Ensemble-Methoden:**  Hier werden mehrere Modelle mit unterschiedlichen Parametern oder Architekturen kombiniert.
#  Aus Paper Self-Consistency Improves Chain of Thought Reasoning in Language Models

# TODO: Reihenfolge im datamodel ändern das classification immer am ende kommt wegen autoregressiv
# TODO: Vereinfachung vom Data model und nur auf concept von feldmann barrett konzentrieren. FOKUS
# TOOD: Batch processing der anfragen geht schenller und ist günstiger!
# TODO: Prompt herausfinden für Lisa Feldmann Barrett
# TODO: Zero-Shot Role play prompting mit SC (Self consitency) )(Beweis Table 9, paper: Better Zero-Shot Reasoning through Role play prompting)
# TODO: Reasoning step pro attribute
# TODO: Validierungs script 
# TODO: Reworked completly the creation of commen threadss to reduce token count by approaximatly 20% - 25%
# TODO: Recursive emthod for markdown creation work much better as bevore



```

### TODOs in `src_llm_pipeline/TODO.py`

<TODOs>
  <TODO>RUN Pipeline on LLama3 -> Server RecSys L40 GPU?</TODO>
  <TODO>Mathias Pre-Study</TODO>
  <TODO>mindest token grenze für pipeline -> bring nichts einen satz zu analyisren.</TODO>
  <TODO>Add cycle for improvment taking the critique from the evaluation and then improve summary</TODO>
  <TODO>Wenn richtig evaluiert muss man die llm as a judge auch evaluieren, + few shot examples für gut oder schlechte classifications für max alignment. Eher boolean classification.</TODO>
  <TODO>Benutzername "unbekannt" ersetzten durch random name oder unbekannt nummer X und dann iterrieren oder so.</TODO>
  <TODO>Cohere, OpenAi, Anthropic, Google anbinden</TODO>
  <TODO>Use greedy decoding</TODO>
  <TODO>Evaluator bauen -> Dataset abspeichern zu den jeweiligen Categorien also einmal core und einmal</TODO>
  <TODO>https://platform.openai.com/docs/guides/evals</TODO>
  <TODO>OneShot prompting - TASK, THOUGHT, CLASSFICATION - statt - TASK, THOUGHT; ACTION</TODO>
  <TODO>Use Cases: Einbinden das es auch für Terror detection genutzt werden könnte</TODO>
  <TODO>Evaluation des **Inner Monoglogue** dann immer Inner monologue vs. analyse -> HumanEval</TODO>
  <TODO>Write a very bad first summary and then improve it with the model</TODO>
  <TODO>SUrvey finden - Survey items bauen!</TODO>
  <TODO>Summary auch strukturieren wie die initial zusammenfassung</TODO>
  <TODO>Added examples to summary call</TODO>
  <TODO>Classification attributes festlegen durch papers</TODO>
  <TODO>auch auf parameter evaluieren wie: factuality, valid JSON, text quality? Mit OPENAI Evaluators?</TODO>
  <TODO>Latence, einfach als metric aufnehmen für evaluation!</TODO>
  <TODO>**So, is Role-Play Prompting essentially CoT?** -> It's not quite the same, but rather a potential trigger for it.</TODO>
  <TODO>Labels für die classification: Erregung, Valenz, soziale Verbundenheit, Polarization, Emotionality, Polarization</TODO>
  <TODO>Self-consitentcy implemtneiren wie in SELF-CONSISTENCY IMPROVES CHAIN OF THOUGHT REASONING IN LANGUAGE MODELS beschrieben,</TODO>
  <TODO>Reihenfolge im datamodel ändern das classification immer am ende kommt wegen autoregressiv</TODO>
  <TODO>Vereinfachung vom Data model und nur auf concept von feldmann barrett konzentrieren. FOKUS</TODO>
  <TODO>Prompt herausfinden für Lisa Feldmann Barrett</TODO>
  <TODO>Zero-Shot Role play prompting mit SC (Self consitency) )(Beweis Table 9, paper: Better Zero-Shot Reasoning through Role play prompting)</TODO>
  <TODO>Reasoning step pro attribute</TODO>
  <TODO>Validierungs script</TODO>
  <TODO>Reworked completly the creation of commen threadss to reduce token count by approaximatly 20% - 25%</TODO>
  <TODO>Recursive emthod for markdown creation work much better as bevore</TODO>
</TODOs>

## `src_llm_pipeline/utils/enums.py`

```
from enum import Enum
#https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters#unsafe_responses

FINISH_REASON_MAP = {
    0: "FINISH_REASON_UNSPECIFIED",
    1: "STOP",
    2: "MAX_TOKENS",
    3: "SAFETY",
    4: "RECITATION",
    5: "OTHER",
    6: "BLOCKLIST",
    7: "PROHIBITED_CONTENT",
    8: "SPII",
    9: "MALFORMED_FUNCTION_CALL",
}


#https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters#configurable-filters
CATEGORY_MAP = {
    0: "HARM_UNSPECIFIED",
    1: "HARM_HATE_SPEECH",
    2: "HARM_DANGEROUS_CONTENT",
    3: "HARM_HARASSMENT",
    4: "HARM_SEXUALLY_EXPLICIT",
    # Add other categories as necessary
}

PROBABILITY_MAP = {
    0: "PROBABILITY_UNSPECIFIED",
    1: "VERY_UNLIKELY",
    2: "UNLIKELY",
    3: "NEGLIGIBLE",
    4: "LIKELY",
    5: "VERY_LIKELY",
    # Add other probability levels if there are any
}

SEVERITY_MAP = {
    0: "SEVERITY_UNSPECIFIED",
    1: "HARM_SEVERITY_NEGLIGIBLE",
    2: "HARM_SEVERITY_MINOR",
    3: "HARM_SEVERITY_SERIOUS",
    4: "HARM_SEVERITY_EXTREME",
    # Add other severity levels if there are any
}

MESSAGE_MAP = {
    0: "Role-Setting-Prompt",
    1: "Role-Feedback-Prompt",
    2: "Classification_Prompt",
    3: "Step 1: Classification",
    4: "Summarization_Prompt",
    5: "Step 2: Summarization",
    6: "Feedback_Prompt",
    7: "Step 3: Revised Summarization"
}

class Aspect(Enum):
    COHERENCE = (
        "Coherence",
        "Incoherence",
        "the logical flow and clarity within the passage. Consider whether the passage maintains a logical sequence, clear connections between ideas, and an overall sense of understanding."
    )
    RELEVANCE = (
        "Relevance",
        "Irrelevance",
        "how well the summarized emotion classification relates to the original in-depth classification. Does the summary accurately reflect the key emotional categories and their relationships identified in the classification?"
    )
    CONSISTENCY = (
        "Consistency",
        "Inconsistency",
        "whether the emotional categories and their assigned probabilities in the summary are consistent with the findings of the original in-depth classification. Are there any contradictions or inconsistencies between the two?"
    )
    HELPFULNESS = (
        "Helpfulness",
        "Unhelpfulness",
        "how useful the summarized emotion classification is for understanding the overall emotional tone of the text. Does it provide a clear and concise representation of the key emotions and their intensities?"
    )
    COMPREHENSIVENESS = (
        "Comprehensiveness",
        "Incompleteness",
        "whether the summary captures all the significant emotional categories and nuances identified in the original in-depth classification. Are there any important emotions or details missing from the summary?"
    )
    
    # Potentially add more aspects like:
    #  -  Bias (Fairness/Neutrality of the emotion classification)
    #  -  Confidence (Certainty expressed by the LLM in its classification)
    #  -  Specificity/Granularity (Level of detail in the emotion classification)
```

## `src_llm_pipeline/utils/helper_functions.py`

```
from vertexai.generative_models import SafetySetting

# Safety settings
# https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters
default_safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
]



```

## `src_llm_pipeline/utils/save_output_to_csv.py`

```
from utils.data_models import HolisticEmotionAnalysis
import csv
from pathlib import Path

def clean_text(text: str) -> str:
    """Clean text by removing line breaks and escaping semicolons"""
    if text is None:
        return ""
    return str(text).replace('\n', ' ').replace('\r', ' ').replace(';', ',').strip()

def main(
    emotion_analysis_input: str,
    emotion_analysis: HolisticEmotionAnalysis, 
    model_temperature: float, 
    top_p: float,
    batch_id: str, 
    user_id: str, 
    run_id: str,
    timestamp: str, 
    model_name: str,
    prompt_template_version: str
) -> str:
    
    # Create Analysis_Output directory if it doesn't exist
    output_dir = Path("./outputs/csv_batch_results")
    output_dir.mkdir(exist_ok=True)
    
    # Create filename with batch_id
    filename = output_dir / f"emotion_analysis_batch_{batch_id}.csv"
    
    file_exists = filename.exists()

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL, quotechar='"')

        if not file_exists:
            header = [
                "Timestamp", 
                "Run ID", 
                "User ID", 
                "Batch ID", 
                "Model Name", 
                "Prompt Template Version",
                # Model Parameters
                "Model Temperature",
                "Top P",
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
                "Holistic Rationale"
            ]
            writer.writerow(header)

        row = [
            clean_text(timestamp),
            clean_text(run_id),
            clean_text(user_id),
            clean_text(batch_id),
            clean_text(model_name),
            clean_text(prompt_template_version),
            # Model Parameters
            model_temperature,
            top_p,
            # Core Affect Analysis
            clean_text(emotion_analysis.core_affect_analysis.thought_process),
            clean_text(emotion_analysis.core_affect_analysis.valence),
            clean_text(emotion_analysis.core_affect_analysis.arousal),
            clean_text(emotion_analysis.core_affect_analysis.rationale),
            # Cognitive Appraisal
            clean_text(emotion_analysis.cognitive_appraisal_and_conceptualization.thought_process),
            clean_text(emotion_analysis.cognitive_appraisal_and_conceptualization.analysis),
            clean_text(emotion_analysis.cognitive_appraisal_and_conceptualization.rationale),
            # Cultural and Social Context
            clean_text(emotion_analysis.cultural_and_social_context.thought_process),
            clean_text(emotion_analysis.cultural_and_social_context.discussion),
            clean_text(emotion_analysis.cultural_and_social_context.rationale),
            # Emotion Construction
            clean_text(emotion_analysis.emotion_construction_analysis.analysis),
            clean_text(emotion_analysis.emotion_construction_analysis.rationale),
            # Emotional Dynamics
            clean_text(emotion_analysis.emotional_dynamics_and_changes.analysis),
            clean_text(emotion_analysis.emotional_dynamics_and_changes.rationale),
            # Holistic Profile
            clean_text(emotion_analysis.holistic_emotional_profile.description),
            clean_text(emotion_analysis.holistic_emotional_profile.nuanced_classification),
            clean_text(emotion_analysis.holistic_emotional_profile.rationale)
        ]
        writer.writerow(row)

    return str(filename)
```

## `src_llm_pipeline/utils/__init__.py`

```

```

## `src_llm_pipeline/utils/output_parser.py`

```
import json
import textwrap
from typing import Dict, List

def parse_emotion_analysis(text: str, schema: Dict) -> Dict:
    """
    Parses the emotion analysis JSON string and enforces the schema's property ordering.

    Args:
        text: JSON string from LLM
        schema: Schema with property ordering information

    Returns:
        Dict: Parsed and reordered data matching schema ordering
    """
    data = json.loads(text)
    ordered_data = {}

    # Get root level ordering from schema
    root_ordering = schema.get("propertyOrdering", [])
    if not root_ordering:
        raise ValueError("Schema must define propertyOrdering")

    # Enforce root level ordering
    for key in root_ordering:
        if key in data:
            ordered_data[key] = {}
            sub_schema = schema["properties"].get(key, {})
            sub_ordering = sub_schema.get("propertyOrdering", [])

            # Enforce sub-level ordering
            if sub_ordering:
                for sub_key in sub_ordering:
                    if sub_key in data[key]:
                        ordered_data[key][sub_key] = data[key][sub_key]
                    else:
                        print(f"Warning: Expected property {sub_key} missing in {key}")

    # Validate that all required properties are present
    missing_props = [key for key in root_ordering if key not in ordered_data]
    if missing_props:
        raise ValueError(f"Missing required properties: {missing_props}")

    return ordered_data

def check_property_ordering(data: Dict, schema: Dict) -> bool:
    """
    Validates that the data strictly follows the schema's property ordering.

    Args:
        data: The parsed and ordered emotion analysis data
        schema: The schema with property ordering information

    Returns:
        bool: True if ordering matches exactly, False otherwise
    """
    # Check root level ordering
    root_ordering = schema.get("propertyOrdering", [])
    actual_root_keys = list(data.keys())

    if actual_root_keys != root_ordering:
        print("\nRoot level property ordering mismatch:")
        print(f"Expected: {root_ordering}")
        print(f"Actual: {actual_root_keys}")
        return False

    # Check sub-level ordering for each main section
    for section in root_ordering:
        if section in data and section in schema["properties"]:
            sub_schema = schema["properties"][section]
            sub_ordering = sub_schema.get("propertyOrdering", [])

            if sub_ordering:
                actual_sub_keys = list(data[section].keys())
                if actual_sub_keys != sub_ordering:
                    print(f"\nProperty ordering mismatch in {section}:")
                    print(f"Expected: {sub_ordering}")
                    print(f"Actual: {actual_sub_keys}")
                    return False

    return True

def print_emotion_analysis(data: Dict, width: int = 80):
    """
    Prints the emotion analysis data in a simplified format.

    Args:
        data: Parsed emotion analysis dictionary
        width: Maximum width for text wrapping
    """
    for section_name, section_content in data.items():
        print(f"\n{section_name.upper().replace('_', ' ')}")
        for key, value in section_content.items():
            print(f"{key.capitalize().replace('_', ' ')}:")
            print(textwrap.fill(str(value), width=width))
            print("---")
```

## `src_llm_pipeline/utils/add_runs_to_dataset.py`

```
import json
from langsmith import Client
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import requests

def load_config():
    current_script_dir = Path(__file__).resolve().parent
    config_path = current_script_dir.parent / 'config.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def add_runs_to_dataset():
    load_dotenv()
    
    config = load_config()

    client = Client()
    
    dataset_tag = config["dataset_tag"]
    delete_dataset = config["delete_dataset"]
    split = config["split"]
    share_dataset = config["share_dataset"]
    

    timestamp = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    dataset_name = f"{dataset_tag}_{timestamp}"
    
    print("Dataset name:", dataset_name)
    print("Dataset tag:", dataset_tag)
    
    # Filter runs to add to the dataset
    runs = list(client.list_runs(
        project_name="LLM-Classification-Pipeline",
        run_type="chain",
        is_root=True,
        filter=f'has(tags, "{dataset_tag}")',
        error=False,
    ))

    if not runs:
        print("No runs found matching the criteria.")
        return None

    if delete_dataset:
        if client.has_dataset(dataset_name=dataset_name):
            client.delete_dataset(dataset_name=dataset_name)
            print("Deleted existing dataset")
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description="Default Dataset for Langsmith Development runs last 14 days",
            inputs_schema={
                "type": "object",
                "title": "dataset_input_schema",
                "required": ["step_1_classification"],
                "properties": {
                    "step_1_classification": {"type": "object"},
                },
            },
            outputs_schema={
                "type": "object",
                "title": "dataset_output_schema",
                "required": ["step_2_classification_summary"],
                "properties": {
                    "step_2_classification_summary": {"type": "string"}
                }
            }
        )
        existing_run_ids = set()
    else:
        if client.has_dataset(dataset_name=dataset_name):
            dataset = client.read_dataset(dataset_name=dataset_name)
            print("Loaded existing dataset")
            # Fetch existing examples to avoid duplicates
            existing_examples = client.list_examples(dataset_id=dataset.id)
            existing_run_ids = {example.source_run_id for example in existing_examples if example.source_run_id}
        else:
            dataset = client.create_dataset(
                dataset_name=dataset_name,
                description="Default Dataset for Langsmith Development runs last 14 days",
                inputs_schema={
                    "type": "object",
                    "title": "dataset_input_schema",
                    "required": ["step_1_classification"],
                    "properties": {
                        "step_1_classification": {"type": "object"},
                    },
                },
                outputs_schema={
                    "type": "object",
                    "title": "dataset_output_schema",
                    "required": ["step_2_classification_summary"],
                    "properties": {
                        "step_2_classification_summary": {"type": "string"}
                    }
                }
            )
            print("Created new dataset")
            existing_run_ids = set()

    # Filter out runs that have already been added
    new_runs = [run for run in runs if run.id not in existing_run_ids]

    if not new_runs:
        print("All runs are already in the dataset.")
        # Try to read existing shared link
        try:
            share_info = client.read_dataset_shared_schema(dataset_id=dataset.id)
            print(f"Your dataset is already shared. Shareable link: {share_info['url']}")
        except Exception as e:
            print(f"Failed to retrieve existing share link: {e}")
        return share_info["url"] if 'share_info' in locals() else None

    # Add new runs to the dataset
    examples_to_add = []
    for run in new_runs:
        # Retrieve and use optional metadata from the run
        prompt_tokens = getattr(run, 'prompt_tokens', None)
        completion_tokens = getattr(run, 'completion_tokens', None)
        total_tokens = getattr(run, 'total_tokens', None)
        tags = getattr(run, 'tags', [])
        run_id = str(run.id)
        feedback = getattr(run, 'feedback_stats', {})
        print(run.feedback_stats)

        input_data = run.outputs.get("model-Step 1: Classification")
        output_data = run.outputs.get("model-Step 2: Summarization")

        if isinstance(input_data, str):
            input_data = json.loads(input_data)

        # Prepare metadata dictionary including additional data
        example_metadata = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "avg. coherence" : run.feedback_stats["coherence"]["avg"],
            "tags": tags,
            "run_id": run_id,
            "feedback": feedback,
            "user_id": tags[1] if len(tags) > 1 else None,
        }

        example = {
            "inputs": {"step_1_classification": input_data},
            "outputs": {"step_2_classification_summary": output_data},
            "metadata": {k: v for k, v in example_metadata.items() if v is not None}, # only include non-None metadata
            "created_at": run.end_time,
            "dataset_id": dataset.id,
            "split": split,
            "source_run_id": run.id,
        }
        examples_to_add.append(example)

    # Use bulk creation for efficiency
    client.create_examples(
        inputs=[ex["inputs"] for ex in examples_to_add],
        outputs=[ex["outputs"] for ex in examples_to_add],
        metadata=[ex["metadata"] for ex in examples_to_add],
        splits=[ex["split"] for ex in examples_to_add],
        source_run_ids=[ex["source_run_id"] for ex in examples_to_add],
        dataset_id=dataset.id,
    )

    # Try to share the dataset
    if share_dataset:
        try:
            share_info = client.share_dataset(dataset_id=dataset.id)
            print(f"Your dataset is now public. Shareable link: {share_info['url']}")
        except requests.exceptions.HTTPError as e:
            if "409 Client Error: Conflict" in str(e) and "already shared" in str(e):
                # Handle existing shared link
                share_info = client.read_dataset_shared_schema(dataset_id=dataset.id)
                print(f"Your dataset was already shared. Shareable link: {share_info['url']}")
            else:
                raise
        return share_info["url"]
    return "Not Shared - Change config to create sharable link"

    

if __name__ == '__main__':
    link = add_runs_to_dataset()
    if link:
        print(f"Dataset link: {link}")
```

## `src_llm_pipeline/utils/eval_aspects.py`

```
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
import json

from langsmith.run_helpers import traceable
from src_llm_pipeline.utils.enums import Aspect

# TODO ander aspect typen adden
# TODO maybe critique einfügen das man auch weiß was laut model hätte besser sein können

class EvaluationResult(BaseModel):
    aspect: str
    score: bool = Field()
    reasoning: str = Field(description="The reasoning for the score. Max three sentences!")
    critique: str = Field(description="Suggested improvements to the summary. Short precise key points! Max. 3 points.")

class CoherenceEvaluation(EvaluationResult):
    aspect: str = "coherence" # fixed value

class RelevanceEvaluation(EvaluationResult):
    aspect: str = "relevance" # fixed value

class ConsistencyEvaluation(EvaluationResult):
    aspect: str = "consistency" # fixed value

class HelpfulnessEvaluation(EvaluationResult):
    aspect: str = "helpfulness" # fixed value

class ComprehensivenessEvaluation(EvaluationResult):
    aspect: str = "comprehensiveness" # fixed value

def load_config():
    config_path = Path('src_llm_pipeline/config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

load_dotenv()

client = Client()

config = load_config()


dataset_tag = config["dataset_tag"]
delete_dataset = config["delete_dataset"]
model_name_eval = config["model_name_eval"]
prompts_version = config["prompt_version"]

dataset_tag = "default_dataset_2024-11-28:13:03:39"




def read_prompts(filename: str) -> str:
    """Load system prompt from file."""
    folder = Path(f"src_llm_pipeline/inputs/prompts/{prompts_version}")
    return (folder / filename).read_text()

llm_evaluator_prompt_text = read_prompts("prompt_eval_aspects.md")
instructions_summary = read_prompts("step_2_summary_prompt.md")


@traceable(name="Evaluate Aspects", run_type="chain")
def aspect_evaluator(step_1_classification, step_2_classification_summary, aspect: Aspect,llm_model_name : str, run_tree_parent_id):    
    aspect, ant_aspect, aspect_inst = aspect.value
    task_ins = "summary of an in-depth classification"
    
    # Select the appropriate Pydantic model based on the aspect
    print("ASPECT:", aspect)
    if aspect == "Coherence":
        pydantic_model = CoherenceEvaluation
    elif aspect == "Relevance":
        pydantic_model = RelevanceEvaluation
    elif aspect == "Consistency":
        pydantic_model = ConsistencyEvaluation
    elif aspect == "Helpfulness":
        pydantic_model = HelpfulnessEvaluation
    elif aspect == "Comprehensiveness":
        pydantic_model = ComprehensivenessEvaluation
    else:
        raise ValueError(f"Aspect {aspect} not supported")
    
    # TODO: if model string start with gpt string then use the model name and use ChatOpenAi
    
    if llm_model_name.startswith("gpt"):
        llm = ChatOpenAI(
                model_name=llm_model_name,
                max_tokens=2000,
                temperature=0.0,
                
            )
    elif llm_model_name.startswith("claude"):
        llm = ChatAnthropic(
                model_name=llm_model_name,
                max_tokens=1000,
                temperature=0.0,
            )

    llm = llm.with_structured_output(pydantic_model)
    prompt = PromptTemplate.from_template(llm_evaluator_prompt_text)
    chain = (prompt | llm).with_config({"tags": [f"{aspect}"]})
    
    response = chain.invoke({"task-ins": task_ins,
                             "aspect" : aspect,
                             "ant-aspect" : ant_aspect,
                             "aspect-inst": aspect_inst,
                             "step_1_classification": step_1_classification,
                             "step_2_classification_summary": step_2_classification_summary,
                            "instructions_summary": instructions_summary})
    #print(response)
    print("The Score from OpenAi is:", response.score)
    print("The Reasoning from OpenAi is:", response.reasoning)
    print("The Critique from OpenAi is:", response.critique)
    
    client.create_feedback(
        run_id=run_tree_parent_id,
        key=aspect,
        value=response.critique,
        score=response.score,
        comment=response.reasoning,
        feedback_source_type="api",
        source_info={"model": llm_model_name}
    )
    return response



@traceable(name="Evaluate Confabulation", run_type="chain")
def hallucination_confabulation_evaluator(question, answer, run_tree_parent_id):
    eval_prompt = read_prompts("prompt_eval_confabulation.md")
    eval_prompt = PromptTemplate.from_template(eval_prompt)
    
    #eval_prompt = eval_prompt.format(question=question, answer=answer)

    
    class ConfabulationEvaluation(BaseModel):
        explanation: str = Field(description="Short explanation if there is confabulation. Based on the given queustion and corresponding answer. Provde the 1:1 text example confabulation is present Keep the initial question given in mind when thinking about confabulation.")
        scale_rating: int =  Field(description="The rating of the confabulation on a scale from 1 to 10. 1 means no confabulation, 10 means high confabulation. The score should ONLY reflect the aspect of confabulation.")
        #confabulated: bool = Field(description="True if the answer is confabulated, False otherwise.")
    
    
    llm_A = ChatOpenAI(
            model_name="gpt-4o",
            max_tokens=2000,
            temperature=0.0,
            
        )
    llm_B = ChatAnthropic(
            model_name="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=0.0,
        )
    
    llm_C = ChatAnthropic(
            model_name="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.0,
        )
    
    llm_D = ChatVertexAI(
            model_name="gemini-1.5-flash-002",
            max_tokens=1000,
            temperature=0.0,
        
    )
    
    
    llm_A_structured = llm_A.with_structured_output(ConfabulationEvaluation)
    llm_B_structured = llm_B.with_structured_output(ConfabulationEvaluation)
    llm_C_structured = llm_C.with_structured_output(ConfabulationEvaluation)
    llm_D_structured = llm_D.with_structured_output(ConfabulationEvaluation)
    
    chain_A = (eval_prompt | llm_A_structured ).with_config({"tags": ["confabulation"]})
    chain_B = (eval_prompt | llm_B_structured).with_config({"tags": ["confabulation"]})
    chain_C = (eval_prompt | llm_C_structured).with_config({"tags": ["confabulation"]})
    chain_D = (eval_prompt | llm_D_structured).with_config({"tags": ["confabulation"]})
    
    response_A = chain_A.invoke({"question": question, "answer": answer})
    response_B = chain_B.invoke({"question": question, "answer": answer})
    response_C = chain_C.invoke({"question": question, "answer": answer})
    response_D = chain_D.invoke({"question": question, "answer": answer})
    
    print(response_A)
    print(response_B)
    print(response_C)
    print(response_D)
    
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_A.explanation,
        score=response_A.scale_rating,
        feedback_source_type="api",
        source_info={"model": "gpt-4o"}
    )
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_B.explanation,
        score=response_B.scale_rating,
        feedback_source_type="api",
        source_info={"model": "claude-3-5-haiku-20241022"}
    )
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_C.explanation,
        score=response_C.scale_rating,
        feedback_source_type="api",
        source_info={"model": "claude-3-5-sonnet-20241022"}
    )
    client.create_feedback(
        run_id=run_tree_parent_id,
        key="confabulation",
        comment=response_D.explanation,
        score=response_D.scale_rating,
        feedback_source_type="api",
        source_info={"model": "gemini-flash-experimental"}
    )

    return True

def aspect_evaluator_all_aspects(step_1_classification, step_2_classification_summary,llm_model_name : str, run_tree_parent_id):    
    for aspect in Aspect:
        aspect_evaluator(step_1_classification, step_2_classification_summary, aspect, llm_model_name, run_tree_parent_id, langsmith_extra={"tags": [f"{aspect}"]})
        
        

if __name__ == "__main__":
    #aspect_evaluator_all_aspects()
    hallucination_confabulation_evaluator("What is the capital of France?", "The capital of France is Paris.") 

```

### TODOs in `src_llm_pipeline/utils/eval_aspects.py`

<TODOs>
  <TODO>ander aspect typen adden</TODO>
  <TODO>maybe critique einfügen das man auch weiß was laut model hätte besser sein können</TODO>
  <TODO>if model string start with gpt string then use the model name and use ChatOpenAi</TODO>
</TODOs>

## `src_llm_pipeline/utils/langsmith_feedback.py`

```
from vertexai.generative_models import GenerationResponse
from .enums import FINISH_REASON_MAP, CATEGORY_MAP


def send_generation_response_feedback_to_trace(
    response: GenerationResponse, client, run_tree
):
    candidate = response.candidates[0]
    finish_reason_str = FINISH_REASON_MAP.get(candidate.finish_reason, "NOT DEFINED")
    client.create_feedback(
        run_tree.id,
        key="finishReason",
        value=finish_reason_str,
        feedback_source_type="model",
    )

    # Iterate over the safty_ratings
    for idx, safety_rating in enumerate(candidate.safety_ratings):
        category_str = CATEGORY_MAP.get(safety_rating.category, "UNKNOWN_CATEGORY")

        # Create feedback
        # Additionally, send feedback for scores
        client.create_feedback(
            run_tree.id,
            key="prob_" + category_str,
            score=safety_rating.probability_score,
            comment="Score for how probable the Harm is.  0 to 1. Low to High",
            feedback_source_type="model",
        )
        client.create_feedback(
            run_tree.id,
            key="severity_" + category_str,
            score=safety_rating.severity_score,
            comment="Score for how severe the Harm is. 0 to 1. Low to High",
            feedback_source_type="model",
        )

    client.create_feedback(run_tree.id, key="avgLogprobs", score=candidate.avg_logprobs)

    # Feedback for Usage Metadata
    usage_metadata = response.usage_metadata
    client.create_feedback(
        run_tree.id,
        key="promptTokenCount",
        score=usage_metadata.prompt_token_count,
        feedback_source_type="model",
    )
    client.create_feedback(
        run_tree.id,
        key="responseTokenCount",
        score=usage_metadata.candidates_token_count,
        feedback_source_type="model",
    )
    client.create_feedback(
        run_tree.id,
        key="totalTokenCount",
        score=usage_metadata.total_token_count,
        feedback_source_type="model",
    )

    if finish_reason_str != "STOP":
        raise ValueError(
            "Model could not finish successfully due to reason: ", finish_reason_str
        )

```

## `src_llm_pipeline/inputs/prompts/__init__.py`

```

```

## `src_llm_pipeline/inputs/prompts/v6/data_models.py`

```
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from typing import ClassVar

# The following classes are used to define the data model for the output of the emotion analysis pipeline.

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
class CoreAffectAnalysis(BaseModel):

    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the core affect, *including "
            "specific quotes and examples from the user's comments to illustrate your points*, considering "  # Added instruction to include specific quotes and examples.
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over "
            "time. Reference specific expressions, language, and contextual factors."
        )
    )
    valence: str = Field(
        ...,
        description=(
            "Classify the valence of the user's emotional state, noting any fluctuations. *Cite specific comments or "  # Added instruction to cite specific comments.
            "phrases that indicate the valence.*"
        )
    )
    arousal: str = Field(
        ...,
        description=(
            "Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any "
            "changes over time. *Cite specific comments or phrases that indicate the arousal level.*"  # Added instruction to cite specific comments.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the user's cognitive appraisals "
            "and conceptualizations. Refer to specific interpretations, judgments, language use, and conceptual "
            "knowledge. *Include specific comments and phrases from the user to illustrate these points.*"  # Added instruction to include specific comments.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
            "*Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences, "
            "citing specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you want to discuss the situational, cultural, and social "
            "contextual factors influencing the user's emotions, including past experiences and expectations. *Reference "
            "specific comments that indicate cultural or social influences.*"  # Added instruction to reference specific comments.
        )
    )
    discussion: str = Field(
        ...,
        description=(
            "Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences could "
            "influence the user's emotional experiences. *Support your discussion by explaining the impact of these factors "
            "on the user's emotions, with supporting observations and specific examples from the user's comments.*"  # Added instruction to support discussion with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process on how you want to analyze the user's emotion construction "
            "process through the interplay of emotional core affect, cognitive appraisals, conceptualization, "
            "and contextual factors. *Integrate the insights you gained during the generation of the previous analysis parts, "
            "referencing specific examples from the user's comments.*"  # Added instruction to integrate insights and reference specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Provide your analysis planned in the thought_process on how the user's emotions are constructed "
            "through the interplay of core affect, cognitive appraisals, conceptualization, and contextual "
            "factors. *Integrate the insights you gained during the generation of the previous analysis parts, and support "
            "your points with specific examples from the user's comments.*"  # Added instruction to integrate insights and support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step thought process on how you want to identify these shifts/dynamic "
            "changes in the user's emotionality. Are these shifts already visible through the already generated "
            "analysis of core affect, cognitive appraisals, conceptualization, and contextual factors? "
            "*Explain how these emotional dynamics reflect the user's emotional processing and construction over time, "
            "citing specific examples from the user's comments.*"  # Added instruction to cite specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze if there are any changes or fluctuations in the user's emotions throughout their interactions. "
            "Shifts such as in valence and arousal or in behavior towards other users. *Use examples to display "
            "these shifts, citing specific comments that illustrate changes over time.*"  # Added instruction to cite specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
#    holistic_emotional_profile: HolisticEmotionalProfile


def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
 #       "holistic_emotional_profile"
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
        "thought_process",
        "analysis",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]


    return schema

def add_property_ordering_single_class(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Ordering for HolisticEmotionalProfile fields
    schema["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "rationale"
    ]
    return schema

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step plan on how you want to conduct the nuanced_classification using the context and the already "
            "generated analysis and thoughts. *Describe the user's overall emotional profile in a nuanced, "
            "context-dependent manner, avoiding fixed emotion labels and acknowledging complexity. Reference specific examples "
            "from the user's comments to support your classification.*"  # Added instruction to reference specific examples.
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Provide a final nuanced classification using the previous analysis as basis."
            "*Use emotion labels if appropriate, acknowledging their constructed nature, and support your "
            "classification with specific examples from the user's comments.*"  # Added instruction to support classification with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Provide a rationale that synthesizes insights from previous sections to present a coherent emotional profile, "
            "*supported by specific examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )


profile_schema = HolisticEmotionalProfile.model_json_schema()
schema_with_order = add_property_ordering_single_class(profile_schema)
print(schema_with_order)

```

## `src_llm_pipeline/inputs/prompts/v8/data_models.py`

```
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from typing import ClassVar

# The following classes are used to define the data model for the output of the emotion analysis pipeline.

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
class CoreAffectAnalysis(BaseModel):

    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the core affect, *including "
            "specific quotes and examples from the user's comments to illustrate your points*, considering "  # Added instruction to include specific quotes and examples.
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over "
            "time. Reference specific expressions, language, and contextual factors."
        )
    )
    valence: str = Field(
        ...,
        description=(
            "Classify the valence of the user's emotional state, noting any fluctuations. *Cite specific comments or "  # Added instruction to cite specific comments.
            "phrases that indicate the valence.*"
        )
    )
    arousal: str = Field(
        ...,
        description=(
            "Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any "
            "changes over time. *Cite specific comments or phrases that indicate the arousal level.*"  # Added instruction to cite specific comments.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the user's cognitive appraisals "
            "and conceptualizations. Refer to specific interpretations, judgments, language use, and conceptual "
            "knowledge. *Include specific comments and phrases from the user to illustrate these points.*"  # Added instruction to include specific comments.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
            "*Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences, "
            "citing specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you want to discuss the situational, cultural, and social "
            "contextual factors influencing the user's emotions, including past experiences and expectations. *Reference "
            "specific comments that indicate cultural or social influences.*"  # Added instruction to reference specific comments.
        )
    )
    discussion: str = Field(
        ...,
        description=(
            "Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences could "
            "influence the user's emotional experiences. *Support your discussion by explaining the impact of these factors "
            "on the user's emotions, with supporting observations and specific examples from the user's comments.*"  # Added instruction to support discussion with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process on how you want to analyze the user's emotion construction "
            "process through the interplay of emotional core affect, cognitive appraisals, conceptualization, "
            "and contextual factors. *Integrate the insights you gained during the generation of the previous analysis parts, "
            "referencing specific examples from the user's comments.*"  # Added instruction to integrate insights and reference specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Provide your analysis planned in the thought_process on how the user's emotions are constructed "
            "through the interplay of core affect, cognitive appraisals, conceptualization, and contextual "
            "factors. *Integrate the insights you gained during the generation of the previous analysis parts, and support "
            "your points with specific examples from the user's comments.*"  # Added instruction to integrate insights and support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step thought process on how you want to identify these shifts/dynamic "
            "changes in the user's emotionality. Are these shifts already visible through the already generated "
            "analysis of core affect, cognitive appraisals, conceptualization, and contextual factors? "
            "*Explain how these emotional dynamics reflect the user's emotional processing and construction over time, "
            "citing specific examples from the user's comments.*"  # Added instruction to cite specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze if there are any changes or fluctuations in the user's emotions throughout their interactions. "
            "Shifts such as in valence and arousal or in behavior towards other users. *Use examples to display "
            "these shifts, citing specific comments that illustrate changes over time.*"  # Added instruction to cite specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
#    holistic_emotional_profile: HolisticEmotionalProfile


def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
 #       "holistic_emotional_profile"
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
        "thought_process",
        "analysis",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]


    return schema

def add_property_ordering_single_class(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Ordering for HolisticEmotionalProfile fields
    schema["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "discussion_behaviour"
    ]
    return schema

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Go step-by-step through your previous analysis, picking out the most influencal points for a nuanced classification."
            "Focus on capturing unique emotional patterns specific to the user's behavior, avoiding generic statements that could apply to anyone. "
            "Utilize specific examples from the user's comments to highlight key emotional tendencies."
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Provide a nuanced classification based on prior analysis, ensuring the identification of distinct emotional"
            "expressions unique to the user. Avoid universal characterizations that lack specificity. Use emotion labels"
            " appropriately, acknowledging their dependency on context, and back your classification with precise examples "
            "from the user's comments."  # Added instruction to support classification with specific examples.
        )
    )
    discussion_behaviour: str = Field(
        ...,
        description=(
            "Analyze and describe the user's discussion behavior, focusing on how they express emotions and interact in conversational contexts."
        )
    )


profile_schema = HolisticEmotionalProfile.model_json_schema()
schema_with_order = add_property_ordering_single_class(profile_schema)
print(schema_with_order)

```

## `src_llm_pipeline/inputs/prompts/v9/data_models.py`

```
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_core.utils.json_schema import dereference_refs
from typing import ClassVar

# The following classes are used to define the data model for the output of the emotion analysis pipeline.

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
class CoreAffectAnalysis(BaseModel):

    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the core affect, *including "
            "specific quotes and examples from the user's comments to illustrate your points*, considering "  # Added instruction to include specific quotes and examples.
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over "
            "time. Reference specific expressions, language, and contextual factors."
        )
    )
    valence: str = Field(
        ...,
        description=(
            "Classify the valence of the user's emotional state, noting any fluctuations. *Cite specific comments or "  # Added instruction to cite specific comments.
            "phrases that indicate the valence.*"
        )
    )
    arousal: str = Field(
        ...,
        description=(
            "Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any "
            "changes over time. *Cite specific comments or phrases that indicate the arousal level.*"  # Added instruction to cite specific comments.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the user's cognitive appraisals "
            "and conceptualizations. Refer to specific interpretations, judgments, language use, and conceptual "
            "knowledge. *Include specific comments and phrases from the user to illustrate these points.*"  # Added instruction to include specific comments.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
            "*Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences, "
            "citing specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you want to discuss the situational, cultural, and social "
            "contextual factors influencing the user's emotions, including past experiences and expectations. *Reference "
            "specific comments that indicate cultural or social influences.*"  # Added instruction to reference specific comments.
        )
    )
    discussion: str = Field(
        ...,
        description=(
            "Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences could "
            "influence the user's emotional experiences. *Support your discussion by explaining the impact of these factors "
            "on the user's emotions, with supporting observations and specific examples from the user's comments.*"  # Added instruction to support discussion with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process on how you want to analyze the user's emotion construction "
            "process through the interplay of emotional core affect, cognitive appraisals, conceptualization, "
            "and contextual factors. *Integrate the insights you gained during the generation of the previous analysis parts, "
            "referencing specific examples from the user's comments.*"  # Added instruction to integrate insights and reference specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Provide your analysis planned in the thought_process on how the user's emotions are constructed "
            "through the interplay of core affect, cognitive appraisals, conceptualization, and contextual "
            "factors. *Integrate the insights you gained during the generation of the previous analysis parts, and support "
            "your points with specific examples from the user's comments.*"  # Added instruction to integrate insights and support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step thought process on how you want to identify these shifts/dynamic "
            "changes in the user's emotionality. Are these shifts already visible through the already generated "
            "analysis of core affect, cognitive appraisals, conceptualization, and contextual factors? "
            "*Explain how these emotional dynamics reflect the user's emotional processing and construction over time, "
            "citing specific examples from the user's comments.*"  # Added instruction to cite specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze if there are any changes or fluctuations in the user's emotions throughout their interactions. "
            "Shifts such as in valence and arousal or in behavior towards other users. *Use examples to display "
            "these shifts, citing specific comments that illustrate changes over time.*"  # Added instruction to cite specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
#    holistic_emotional_profile: HolisticEmotionalProfile


def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
 #       "holistic_emotional_profile"
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
        "thought_process",
        "analysis",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]


    return schema

def add_property_ordering_single_class(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Ordering for HolisticEmotionalProfile fields
    schema["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "discussion_behaviour"
    ]
    return schema

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Go step-by-step through your previous analysis, picking out the most influencal points for a nuanced classification."
            "Focus on capturing unique emotional patterns specific to the user's behavior, avoiding generic statements that could apply to anyone. "
            "Utilize specific examples from the user's comments to highlight key emotional tendencies."
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Provide a nuanced classification based on prior analysis, ensuring the identification of distinct emotional"
            "expressions unique to the user. Avoid universal characterizations that lack specificity. Use emotion labels"
            " appropriately, acknowledging their dependency on context, and back your classification with precise examples "
            "from the user's comments."  # Added instruction to support classification with specific examples.
        )
    )
    discussion_behaviour: str = Field(
        ...,
        description=(
            "Analyze and describe the user's discussion behavior, focusing on how they express emotions and interact in conversational contexts."
        )
    )


#profile_schema = HolisticEmotionAnalysis.model_json_schema()
#schema_with_order = add_property_ordering_single_class(profile_schema)
#schema_with_order = add_specific_property_ordering((profile_schema))
#print(schema_with_order)

#schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
#schema.pop("$defs", None)
#schema_with_specific_ordering = add_specific_property_ordering(schema)
#print(schema_with_specific_ordering)

```

## `src_llm_pipeline/inputs/prompts/v7/data_models.py`

```
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from typing import ClassVar

# The following classes are used to define the data model for the output of the emotion analysis pipeline.

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
class CoreAffectAnalysis(BaseModel):

    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the core affect, *including "
            "specific quotes and examples from the user's comments to illustrate your points*, considering "  # Added instruction to include specific quotes and examples.
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over "
            "time. Reference specific expressions, language, and contextual factors."
        )
    )
    valence: str = Field(
        ...,
        description=(
            "Classify the valence of the user's emotional state, noting any fluctuations. *Cite specific comments or "  # Added instruction to cite specific comments.
            "phrases that indicate the valence.*"
        )
    )
    arousal: str = Field(
        ...,
        description=(
            "Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any "
            "changes over time. *Cite specific comments or phrases that indicate the arousal level.*"  # Added instruction to cite specific comments.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the user's cognitive appraisals "
            "and conceptualizations. Refer to specific interpretations, judgments, language use, and conceptual "
            "knowledge. *Include specific comments and phrases from the user to illustrate these points.*"  # Added instruction to include specific comments.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
            "*Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences, "
            "citing specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you want to discuss the situational, cultural, and social "
            "contextual factors influencing the user's emotions, including past experiences and expectations. *Reference "
            "specific comments that indicate cultural or social influences.*"  # Added instruction to reference specific comments.
        )
    )
    discussion: str = Field(
        ...,
        description=(
            "Discuss how cultural norms, societal values, social interactions, and predictions based on past experiences could "
            "influence the user's emotional experiences. *Support your discussion by explaining the impact of these factors "
            "on the user's emotions, with supporting observations and specific examples from the user's comments.*"  # Added instruction to support discussion with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process on how you want to analyze the user's emotion construction "
            "process through the interplay of emotional core affect, cognitive appraisals, conceptualization, "
            "and contextual factors. *Integrate the insights you gained during the generation of the previous analysis parts, "
            "referencing specific examples from the user's comments.*"  # Added instruction to integrate insights and reference specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Provide your analysis planned in the thought_process on how the user's emotions are constructed "
            "through the interplay of core affect, cognitive appraisals, conceptualization, and contextual "
            "factors. *Integrate the insights you gained during the generation of the previous analysis parts, and support "
            "your points with specific examples from the user's comments.*"  # Added instruction to integrate insights and support analysis with specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step thought process on how you want to identify these shifts/dynamic "
            "changes in the user's emotionality. Are these shifts already visible through the already generated "
            "analysis of core affect, cognitive appraisals, conceptualization, and contextual factors? "
            "*Explain how these emotional dynamics reflect the user's emotional processing and construction over time, "
            "citing specific examples from the user's comments.*"  # Added instruction to cite specific examples.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze if there are any changes or fluctuations in the user's emotions throughout their interactions. "
            "Shifts such as in valence and arousal or in behavior towards other users. *Use examples to display "
            "these shifts, citing specific comments that illustrate changes over time.*"  # Added instruction to cite specific examples.
        )
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.***"  # Added instruction to support rationale with specific examples.
        )
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges
#    holistic_emotional_profile: HolisticEmotionalProfile


def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
 #       "holistic_emotional_profile"
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
        "thought_process",
        "analysis",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "rationale"
    ]


    return schema

def add_property_ordering_single_class(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Ordering for HolisticEmotionalProfile fields
    schema["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "discussion_behaviour"
    ]
    return schema

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Go step-by-step through your previous analysis, picking out the most influencal points for a nuanced classification."
            "Focus on capturing unique emotional patterns specific to the user's behavior, avoiding generic statements that could apply to anyone. "
            "Utilize specific examples from the user's comments to highlight key emotional tendencies."
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Provide a nuanced classification based on prior analysis, ensuring the identification of distinct emotional"
            "expressions unique to the user. Avoid universal characterizations that lack specificity. Use emotion labels"
            " appropriately, acknowledging their dependency on context, and back your classification with precise examples "
            "from the user's comments."  # Added instruction to support classification with specific examples.
        )
    )
    discussion_behaviour: str = Field(
        ...,
        description=(
            "Analyze and describe the user's discussion behavior, focusing on how they express emotions and interact in conversational contexts."
        )
    )


profile_schema = HolisticEmotionalProfile.model_json_schema()
schema_with_order = add_property_ordering_single_class(profile_schema)
print(schema_with_order)

```

## `src_llm_pipeline/inputs/prompts/v12/data_models.py`

```
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_core.utils.json_schema import dereference_refs
from langsmith import traceable


# The following classes are used to define the data model for the output of the emotion analysis pipeline.
# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
class CoreAffectAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the core affect, *including "
            "specific quotes and examples from the user's comments to illustrate your points*, considering "  # Added instruction to include specific quotes and examples.
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over "
            "time. Reference specific expressions, language, and contextual factors. **Consider how insights from other "
            "disciplines like sociology or neuroscience might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    valence: str = Field(
        ...,
        description=(
            "Classify the valence of the user's emotional state, noting any fluctuations. *Cite specific comments or "  # Added instruction to cite specific comments.
            "phrases that indicate the valence.*"
        )
    )
    arousal: str = Field(
        ...,
        description=(
            "Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any "
            "changes over time. *Cite specific comments or phrases that indicate the arousal level.*"  # Added instruction to cite specific comments.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's core affect across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's core affect deviates from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like news events "
            "or broader societal trends might contribute to the observed emotional state.**"  # Encourages consideration of contextual factors.
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the user's cognitive appraisals "
            "and conceptualizations. Refer to specific interpretations, judgments, language use, and conceptual "
            "knowledge. *Include specific comments and phrases from the user to illustrate these points.* **Consider how "
            "insights from other disciplines like psychology or cognitive science might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
            "*Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences, "
            "citing specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's cognitive appraisals and conceptualizations across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's cognitive appraisals or conceptualizations deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like cultural "
            "norms or social trends might contribute to the observed cognitive processes.**"  # Encourages consideration of contextual factors.
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you want to discuss the situational, cultural, and social "
            "contextual factors influencing the user's emotions, including past experiences and expectations. *Reference "
            "specific comments that indicate cultural or social influences.* **Consider how insights from other disciplines "
            "like sociology or anthropology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how cultural norms, societal values, social interactions, and predictions based on past experiences could "
            "influence the user's emotional experiences. *Support your analysis by explaining the impact of these factors "
            "on the user's emotions, with supporting observations and specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the cultural and social factors influencing the user's emotions across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the cultural and social factors influencing the user's emotions deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like political events "
            "or historical context might contribute to the observed cultural and social influences.**"  # Encourages consideration of contextual factors.
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process on how you want to analyze the user's emotion construction "
            "process through the interplay of emotional core affect, cognitive appraisals, conceptualization, "
            "and contextual factors. *Integrate the insights you gained during the generation of the previous analysis parts, "
            "referencing specific examples from the user's comments.* **Consider how insights from other disciplines like "
            "neuroscience or psychology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Provide your analysis planned in the thought_process on how the user's emotions are constructed "
            "through the interplay of core affect, cognitive appraisals, conceptualization, and contextual "
            "factors. *Integrate the insights you gained during the generation of the previous analysis parts, and support "
            "your points with specific examples from the user's comments.*"  # Added instruction to integrate insights and support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's emotion construction process across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's emotion construction process deviates from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like individual "
            "experiences or social media trends might contribute to the observed emotion construction process.**"  # Encourages consideration of contextual factors.
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step thought process on how you want to identify these shifts/dynamic "
            "changes in the user's emotionality. Are these shifts already visible through the already generated "
            "analysis of core affect, cognitive appraisals, conceptualization, and contextual factors? "
            "*Explain how these emotional dynamics reflect the user's emotional processing and construction over time, "
            "citing specific examples from the user's comments.* **Consider how insights from other disciplines like "
            "developmental psychology or social psychology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze if there are any changes or fluctuations in the user's emotions throughout their interactions. "
            "Shifts such as in valence and arousal or in behavior towards other users. *Use examples to display "
            "these shifts, citing specific comments that illustrate changes over time.*"  # Added instruction to cite specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's emotional dynamics across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's emotional dynamics deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like the "
            "topic of discussion or the online community's culture might contribute to the observed emotional dynamics.**"  # Encourages consideration of contextual factors.
        )
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges

def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
 #       "holistic_emotional_profile"
    ]

    # Core affect analysis ordering
    schema["properties"]["core_affect_analysis"]["propertyOrdering"] = [
        "thought_process",
        "valence",
        "arousal",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Cognitive appraisal ordering
    schema["properties"]["cognitive_appraisal_and_conceptualization"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Cultural and social context ordering
    schema["properties"]["cultural_and_social_context"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Emotion construction analysis ordering
    schema["properties"]["emotion_construction_analysis"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]
    return schema

def add_property_ordering_single_class(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Ordering for HolisticEmotionalProfile fields
    schema["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "patterns_observed",
        "anomalous_observations",
        "discussion_behaviour"
    ]
    return schema

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Go step-by-step through your previous analysis, picking out the most influencal points for a nuanced classification."
            "Focus on capturing unique emotional patterns specific to the user's behavior, avoiding generic statements that could apply to anyone. "
            "Utilize specific examples from the user's comments to highlight key emotional tendencies."
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Provide a nuanced classification based on prior analysis, ensuring the identification of distinct emotional"
            "expressions unique to the user. Avoid universal characterizations that lack specificity. Use emotion labels"
            " appropriately, acknowledging their dependency on context, and back your classification with precise examples "
            "from the user's comments."  # Added instruction to support classification with specific examples.
        )
    )
    discussion_behaviour: str = Field(
        ...,
        description=(
            "Analyze and describe the user's discussion behavior, focusing on how they express emotions and interact in conversational contexts."
        )
    )


#profile_schema = HolisticEmotionAnalysis.model_json_schema()
#schema_with_order = add_property_ordering_single_class(profile_schema)
#schema_with_order = add_specific_property_ordering((profile_schema))
#print(schema_with_order)

#schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
#schema.pop("$defs", None)
#schema_with_specific_ordering = add_specific_property_ordering(schema)
#print(schema_with_specific_ordering)

```

## `src_llm_pipeline/inputs/prompts/v11/data_models.py`

```
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_core.utils.json_schema import dereference_refs
from langsmith import traceable


# The following classes are used to define the data model for the output of the emotion analysis pipeline.
# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
class CoreAffectAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the core affect, *including "
            "specific quotes and examples from the user's comments to illustrate your points*, considering "  # Added instruction to include specific quotes and examples.
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over "
            "time. Reference specific expressions, language, and contextual factors. **Consider how insights from other "
            "disciplines like sociology or neuroscience might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    valence: str = Field(
        ...,
        description=(
            "Classify the valence of the user's emotional state, noting any fluctuations. *Cite specific comments or "  # Added instruction to cite specific comments.
            "phrases that indicate the valence.*"
        )
    )
    arousal: str = Field(
        ...,
        description=(
            "Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any "
            "changes over time. *Cite specific comments or phrases that indicate the arousal level.*"  # Added instruction to cite specific comments.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's core affect across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's core affect deviates from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like news events "
            "or broader societal trends might contribute to the observed emotional state.**"  # Encourages consideration of contextual factors.
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the user's cognitive appraisals "
            "and conceptualizations. Refer to specific interpretations, judgments, language use, and conceptual "
            "knowledge. *Include specific comments and phrases from the user to illustrate these points.* **Consider how "
            "insights from other disciplines like psychology or cognitive science might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
            "*Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences, "
            "citing specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's cognitive appraisals and conceptualizations across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's cognitive appraisals or conceptualizations deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like cultural "
            "norms or social trends might contribute to the observed cognitive processes.**"  # Encourages consideration of contextual factors.
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you want to discuss the situational, cultural, and social "
            "contextual factors influencing the user's emotions, including past experiences and expectations. *Reference "
            "specific comments that indicate cultural or social influences.* **Consider how insights from other disciplines "
            "like sociology or anthropology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how cultural norms, societal values, social interactions, and predictions based on past experiences could "
            "influence the user's emotional experiences. *Support your analysis by explaining the impact of these factors "
            "on the user's emotions, with supporting observations and specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the cultural and social factors influencing the user's emotions across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the cultural and social factors influencing the user's emotions deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like political events "
            "or historical context might contribute to the observed cultural and social influences.**"  # Encourages consideration of contextual factors.
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process on how you want to analyze the user's emotion construction "
            "process through the interplay of emotional core affect, cognitive appraisals, conceptualization, "
            "and contextual factors. *Integrate the insights you gained during the generation of the previous analysis parts, "
            "referencing specific examples from the user's comments.* **Consider how insights from other disciplines like "
            "neuroscience or psychology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Provide your analysis planned in the thought_process on how the user's emotions are constructed "
            "through the interplay of core affect, cognitive appraisals, conceptualization, and contextual "
            "factors. *Integrate the insights you gained during the generation of the previous analysis parts, and support "
            "your points with specific examples from the user's comments.*"  # Added instruction to integrate insights and support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's emotion construction process across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's emotion construction process deviates from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like individual "
            "experiences or social media trends might contribute to the observed emotion construction process.**"  # Encourages consideration of contextual factors.
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step thought process on how you want to identify these shifts/dynamic "
            "changes in the user's emotionality. Are these shifts already visible through the already generated "
            "analysis of core affect, cognitive appraisals, conceptualization, and contextual factors? "
            "*Explain how these emotional dynamics reflect the user's emotional processing and construction over time, "
            "citing specific examples from the user's comments.* **Consider how insights from other disciplines like "
            "developmental psychology or social psychology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze if there are any changes or fluctuations in the user's emotions throughout their interactions. "
            "Shifts such as in valence and arousal or in behavior towards other users. *Use examples to display "
            "these shifts, citing specific comments that illustrate changes over time.*"  # Added instruction to cite specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's emotional dynamics across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's emotional dynamics deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like the "
            "topic of discussion or the online community's culture might contribute to the observed emotional dynamics.**"  # Encourages consideration of contextual factors.
        )
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges

def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
 #       "holistic_emotional_profile"
    ]

    # Core affect analysis ordering
    schema["properties"]["core_affect_analysis"]["propertyOrdering"] = [
        "thought_process",
        "valence",
        "arousal",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Cognitive appraisal ordering
    schema["properties"]["cognitive_appraisal_and_conceptualization"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Cultural and social context ordering
    schema["properties"]["cultural_and_social_context"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Emotion construction analysis ordering
    schema["properties"]["emotion_construction_analysis"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]
    return schema

def add_property_ordering_single_class(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Ordering for HolisticEmotionalProfile fields
    schema["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "patterns_observed",
        "anomalous_observations",
        "discussion_behaviour"
    ]
    return schema

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Go step-by-step through your previous analysis, picking out the most influencal points for a nuanced classification."
            "Focus on capturing unique emotional patterns specific to the user's behavior, avoiding generic statements that could apply to anyone. "
            "Utilize specific examples from the user's comments to highlight key emotional tendencies."
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Provide a nuanced classification based on prior analysis, ensuring the identification of distinct emotional"
            "expressions unique to the user. Avoid universal characterizations that lack specificity. Use emotion labels"
            " appropriately, acknowledging their dependency on context, and back your classification with precise examples "
            "from the user's comments."  # Added instruction to support classification with specific examples.
        )
    )
    discussion_behaviour: str = Field(
        ...,
        description=(
            "Analyze and describe the user's discussion behavior, focusing on how they express emotions and interact in conversational contexts."
        )
    )


#profile_schema = HolisticEmotionAnalysis.model_json_schema()
#schema_with_order = add_property_ordering_single_class(profile_schema)
#schema_with_order = add_specific_property_ordering((profile_schema))
#print(schema_with_order)

#schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
#schema.pop("$defs", None)
#schema_with_specific_ordering = add_specific_property_ordering(schema)
#print(schema_with_specific_ordering)

```

## `src_llm_pipeline/inputs/prompts/v10/data_models.py`

```
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_core.utils.json_schema import dereference_refs

# The following classes are used to define the data model for the output of the emotion analysis pipeline.

# CoreAffectAnalysis captures fluctuations in basic emotional states—valence and arousal—providing a foundational understanding of the user's affective experiences.
class CoreAffectAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the core affect, *including "
            "specific quotes and examples from the user's comments to illustrate your points*, considering "  # Added instruction to include specific quotes and examples.
            "both valence (pleasantness) and arousal (activation), and noting any emotional dynamics or changes over "
            "time. Reference specific expressions, language, and contextual factors. **Consider how insights from other "
            "disciplines like sociology or neuroscience might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    valence: str = Field(
        ...,
        description=(
            "Classify the valence of the user's emotional state, noting any fluctuations. *Cite specific comments or "  # Added instruction to cite specific comments.
            "phrases that indicate the valence.*"
        )
    )
    arousal: str = Field(
        ...,
        description=(
            "Classify the arousal level of the user's emotional state, indicating activation or energy levels, and any "
            "changes over time. *Cite specific comments or phrases that indicate the arousal level.*"  # Added instruction to cite specific comments.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's core affect across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's core affect deviates from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like news events "
            "or broader societal trends might contribute to the observed emotional state.**"  # Encourages consideration of contextual factors.
        )
    )

# CognitiveAppraisalAndConceptualization examines how the user's interpretations and knowledge shape emotions, reflecting Barrett's concept of constructed emotional experiences.
class CognitiveAppraisalAndConceptualization(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you intend to analyze the user's cognitive appraisals "
            "and conceptualizations. Refer to specific interpretations, judgments, language use, and conceptual "
            "knowledge. *Include specific comments and phrases from the user to illustrate these points.* **Consider how "
            "insights from other disciplines like psychology or cognitive science might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how the user's interpretations and conceptual knowledge contribute to the construction of their emotions. "
            "*Support your analysis by illustrating how these cognitive processes shape the user's emotional experiences, "
            "citing specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's cognitive appraisals and conceptualizations across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's cognitive appraisals or conceptualizations deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like cultural "
            "norms or social trends might contribute to the observed cognitive processes.**"  # Encourages consideration of contextual factors.
        )
    )

# CulturalAndSocialContext considers societal and cultural influences on emotions, highlighting the context-dependent nature of emotional experiences.
class CulturalAndSocialContext(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process of how you want to discuss the situational, cultural, and social "
            "contextual factors influencing the user's emotions, including past experiences and expectations. *Reference "
            "specific comments that indicate cultural or social influences.* **Consider how insights from other disciplines "
            "like sociology or anthropology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze how cultural norms, societal values, social interactions, and predictions based on past experiences could "
            "influence the user's emotional experiences. *Support your analysis by explaining the impact of these factors "
            "on the user's emotions, with supporting observations and specific examples from the user's comments.*"  # Added instruction to support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the cultural and social factors influencing the user's emotions across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the cultural and social factors influencing the user's emotions deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like political events "
            "or historical context might contribute to the observed cultural and social influences.**"  # Encourages consideration of contextual factors.
        )
    )

# EmotionConstructionAnalysis synthesizes how affect, cognition, and context interact to construct emotions, embodying a holistic view of emotional dynamics.
class EmotionConstructionAnalysis(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a detailed step-by-step thought process on how you want to analyze the user's emotion construction "
            "process through the interplay of emotional core affect, cognitive appraisals, conceptualization, "
            "and contextual factors. *Integrate the insights you gained during the generation of the previous analysis parts, "
            "referencing specific examples from the user's comments.* **Consider how insights from other disciplines like "
            "neuroscience or psychology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Provide your analysis planned in the thought_process on how the user's emotions are constructed "
            "through the interplay of core affect, cognitive appraisals, conceptualization, and contextual "
            "factors. *Integrate the insights you gained during the generation of the previous analysis parts, and support "
            "your points with specific examples from the user's comments.*"  # Added instruction to integrate insights and support analysis with specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's emotion construction process across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's emotion construction process deviates from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like individual "
            "experiences or social media trends might contribute to the observed emotion construction process.**"  # Encourages consideration of contextual factors.
        )
    )

# EmotionalDynamicsAndChanges tracks emotional shifts over time, illustrating the fluid and process-oriented nature of emotions in response to user interactions.
class EmotionalDynamicsAndChanges(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Provide a step-by-step thought process on how you want to identify these shifts/dynamic "
            "changes in the user's emotionality. Are these shifts already visible through the already generated "
            "analysis of core affect, cognitive appraisals, conceptualization, and contextual factors? "
            "*Explain how these emotional dynamics reflect the user's emotional processing and construction over time, "
            "citing specific examples from the user's comments.* **Consider how insights from other disciplines like "
            "developmental psychology or social psychology might inform your analysis.**"  # Encourages interdisciplinary thinking.
        )
    )
    analysis: str = Field(
        ...,
        description=(
            "Analyze if there are any changes or fluctuations in the user's emotions throughout their interactions. "
            "Shifts such as in valence and arousal or in behavior towards other users. *Use examples to display "
            "these shifts, citing specific comments that illustrate changes over time.*"  # Added instruction to cite specific examples.
        )
    )
    patterns_observed: str = Field(
        ...,
        description="Document any recurring patterns in the user's emotional dynamics across comments, linking them to specific instances."
    )
    anomalous_observations: str = Field(
        ...,
        description="Highlight any comments where the user's emotional dynamics deviate from expected patterns based on the context."
    )
    rationale: str = Field(
        ...,
        description=(
            "**Include a clear short rationale explaining how you arrived at your conclusions, *supported by specific "
            "examples from the text and your research.* Consider how **external contextual factors** like the "
            "topic of discussion or the online community's culture might contribute to the observed emotional dynamics.**"  # Encourages consideration of contextual factors.
        )
    )

class HolisticEmotionAnalysis(BaseModel):
    core_affect_analysis: CoreAffectAnalysis
    cognitive_appraisal_and_conceptualization: CognitiveAppraisalAndConceptualization
    cultural_and_social_context: CulturalAndSocialContext
    emotion_construction_analysis: EmotionConstructionAnalysis
    emotional_dynamics_and_changes: EmotionalDynamicsAndChanges

def add_specific_property_ordering(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Root level ordering
    schema["propertyOrdering"] = [
        "core_affect_analysis",
        "cognitive_appraisal_and_conceptualization",
        "cultural_and_social_context",
        "emotion_construction_analysis",
        "emotional_dynamics_and_changes",
 #       "holistic_emotional_profile"
    ]

    # Core affect analysis ordering
    schema["properties"]["core_affect_analysis"]["propertyOrdering"] = [
        "thought_process",
        "valence",
        "arousal",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Cognitive appraisal ordering
    schema["properties"]["cognitive_appraisal_and_conceptualization"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Cultural and social context ordering
    schema["properties"]["cultural_and_social_context"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Emotion construction analysis ordering
    schema["properties"]["emotion_construction_analysis"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]

    # Emotional dynamics and changes ordering
    schema["properties"]["emotional_dynamics_and_changes"]["propertyOrdering"] = [
        "thought_process",
        "analysis",
        "patterns_observed",
        "anomalous_observations",
        "rationale"
    ]
    return schema

def add_property_ordering_single_class(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Ordering for HolisticEmotionalProfile fields
    schema["propertyOrdering"] = [
        "thought_process",
        "nuanced_classification",
        "patterns_observed",
        "anomalous_observations",
        "discussion_behaviour"
    ]
    return schema

# HolisticEmotionalProfile integrates insights to describe the user's overall emotional state, avoiding fixed labels and embracing complexity and nuance.
class HolisticEmotionalProfile(BaseModel):
    """
    Do not be lazy while working on your tasks!
    """
    thought_process: str = Field(
        ...,
        description=(
            "Go step-by-step through your previous analysis, picking out the most influencal points for a nuanced classification."
            "Focus on capturing unique emotional patterns specific to the user's behavior, avoiding generic statements that could apply to anyone. "
            "Utilize specific examples from the user's comments to highlight key emotional tendencies."
        )
    )
    nuanced_classification: str = Field(
        ...,
        description=(
            "Provide a nuanced classification based on prior analysis, ensuring the identification of distinct emotional"
            "expressions unique to the user. Avoid universal characterizations that lack specificity. Use emotion labels"
            " appropriately, acknowledging their dependency on context, and back your classification with precise examples "
            "from the user's comments."  # Added instruction to support classification with specific examples.
        )
    )
    discussion_behaviour: str = Field(
        ...,
        description=(
            "Analyze and describe the user's discussion behavior, focusing on how they express emotions and interact in conversational contexts."
        )
    )


#profile_schema = HolisticEmotionAnalysis.model_json_schema()
#schema_with_order = add_property_ordering_single_class(profile_schema)
#schema_with_order = add_specific_property_ordering((profile_schema))
#print(schema_with_order)

#schema = dereference_refs(HolisticEmotionAnalysis.model_json_schema())
#schema.pop("$defs", None)
#schema_with_specific_ordering = add_specific_property_ordering(schema)
#print(schema_with_specific_ordering)

```

## `repo_reader/index_repo.py`

```
import os
import re
import sys
from lxml import etree
import pathspec
import argparse

def load_ignore_files(repo_path):
    ignore_patterns = []
    
    # Load .gitignore
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read().splitlines()
        ignore_patterns.extend(gitignore_content)
        print("Loaded patterns from .gitignore")
    else:
        print("No .gitignore file found.")
    
    # Load .indexignore
    indexignore_path = os.path.join(repo_path, '.indexignore')
    if os.path.isfile(indexignore_path):
        with open(indexignore_path, 'r', encoding='utf-8') as f:
            indexignore_content = f.read().splitlines()
        ignore_patterns.extend(indexignore_content)
        print("Loaded patterns from .indexignore")
    else:
        print("No .indexignore file found.")
    
    if ignore_patterns:
        spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, ignore_patterns)
        return spec
    else:
        return None

def is_ignored(path, spec):
    if spec is None:
        return False
    # Convert path to use forward slashes and remove leading './' if present
    path = path.replace(os.sep, '/').lstrip('./')
    return spec.match_file(path)

def create_xml_element(tag, text=None, attrib=None):
    element = etree.Element(tag, attrib=attrib if attrib else {})
    if text:
        element.text = text
    return element

def traverse_directory(root_path, input_folders, spec, allowed_extensions, script_extensions):
    content_root = create_xml_element('Repository', attrib={'name': os.path.basename(root_path)})
    structure_root = create_xml_element('RepositoryStructure', attrib={'name': os.path.basename(root_path)})

    for input_folder in input_folders:
        abs_input_folder = os.path.join(root_path, input_folder)
        if not os.path.isdir(abs_input_folder):
            print(f"Input folder '{input_folder}' does not exist or is not a directory.", file=sys.stderr)
            continue

        for dirpath, dirnames, filenames in os.walk(abs_input_folder):
            # Compute relative path
            rel_dir = os.path.relpath(dirpath, root_path)
            rel_dir = '.' if rel_dir == '.' else rel_dir.replace(os.sep, '/')

            # Modify dirnames in-place to skip ignored folders
            dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(rel_dir, d), spec)]

            # Navigate/Create XML elements based on relative path
            parent_content = content_root
            parent_structure = structure_root
            if rel_dir != '.':
                parts = rel_dir.split('/')
                for part in parts:
                    # For content XML
                    sub_dir = parent_content.find(f"./Directory[@name='{part}']")
                    if sub_dir is None:
                        sub_dir = create_xml_element('Directory', attrib={'name': part})
                        parent_content.append(sub_dir)
                    parent_content = sub_dir

                    # For structure XML
                    struct_sub_dir = parent_structure.find(f"./Directory[@name='{part}']")
                    if struct_sub_dir is None:
                        struct_sub_dir = create_xml_element('Directory', attrib={'name': part})
                        parent_structure.append(struct_sub_dir)
                    parent_structure = struct_sub_dir

            for filename in filenames:
                rel_file_path = os.path.join(rel_dir, filename).replace(os.sep, '/')
                if is_ignored(rel_file_path, spec):
                    continue  # Skip ignored files
                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                if allowed_extensions and ext not in allowed_extensions:
                    continue  # Skip files not in allowed extensions
                file_path = os.path.join(dirpath, filename)
                try:
                    # Read and clean content
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Clean content to remove NULL bytes or control characters
                        content = ''.join(c for c in content if c.isprintable() or c in '\n\t\r')
                except Exception as e:
                    print(f"Error reading {file_path}: {e}", file=sys.stderr)
                    content = ""

                # For content XML
                file_element = create_xml_element('File', attrib={'name': filename, 'path': rel_file_path})
                content_element = create_xml_element('Content', text=content)
                file_element.append(content_element)
                parent_content.append(file_element)

                # For structure XML
                struct_file_element = create_xml_element('File', attrib={'name': filename, 'path': rel_file_path})
                parent_structure.append(struct_file_element)

    return content_root, structure_root

def extract_todos_and_scripts(xml_root, script_extensions):
    markdown_lines = ["# Repository Documentation\n"]
    for file_elem in xml_root.findall('.//File'):
        file_name = file_elem.get('name')
        file_path = file_elem.get('path')
        content = file_elem.find('Content').text or ''
        # Extract TODOs based on file extension
        todos = []
        ext = os.path.splitext(file_name)[1].lower()
        comment_patterns = {
            '.py': r'#\s*TODO:? (.*)',
            '.js': r'//\s*TODO:? (.*)',
            '.java': r'//\s*TODO:? (.*)',
            '.sh': r'#\s*TODO:? (.*)',
            '.rb': r'#\s*TODO:? (.*)',
            '.ts': r'//\s*TODO:? (.*)',
            '.cpp': r'//\s*TODO:? (.*)',
            '.c': r'//\s*TODO:? (.*)',
            '.cs': r'//\s*TODO:? (.*)',
            '.go': r'//\s*TODO:? (.*)',
            '.html': r'<!--\s*TODO:? (.*?)-->',
            '.css': r'/\*\s*TODO:? (.*?)\*/',
            '.scss': r'/\*\s*TODO:? (.*?)\*/',
        }
        pattern = comment_patterns.get(ext)
        if pattern:
            todos = re.findall(pattern, content, re.MULTILINE)

        # Extract scripts
        if script_extensions and ext in script_extensions:
            code = content
            markdown_lines.append(f"## `{file_path}`\n")
            markdown_lines.append("```")
            markdown_lines.append(code)
            markdown_lines.append("```\n")
        if todos:
            markdown_lines.append(f"### TODOs in `{file_path}`\n")
            markdown_lines.append("<TODOs>")
            for todo in todos:
                markdown_lines.append(f"  <TODO>{todo.strip()}</TODO>")
            markdown_lines.append("</TODOs>\n")
    return '\n'.join(markdown_lines)

def main():
    parser = argparse.ArgumentParser(description='Index selected folders in the repository.')
    parser.add_argument('folders', nargs='*', help='List of folders to process (relative to repository root). If empty, defaults to all folders.')
    parser.add_argument('--xml_output', default='results/index.xml', help='Output XML file name for content.')
    parser.add_argument('--structure_output', default='results/folder_structure.xml', help='Output XML file name for folder structure.')
    parser.add_argument('--md_output', default='results/documentation.md', help='Output Markdown file name.')
    args = parser.parse_args()

    # Configuration
    allowed_extensions = [
        '.py', '.js', '.sh', '.rb', '.java', '.md', '.html', '.css', '.ts', '.cpp', '.c', '.cs', '.go'
        # Add or remove extensions based on your requirements
    ]

    script_extensions = [
        '.py', '.js', '.sh', '.rb', '.java', '.ts', '.cpp', '.c', '.cs', '.go'
        # Add or remove script extensions as needed
    ]

    # Determine repository root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.abspath(os.path.join(script_dir, '..'))  # One level up from repo_reader

    # Define output paths within repo_reader/results/
    xml_output = os.path.join(script_dir, args.xml_output)
    md_output = os.path.join(script_dir, args.md_output)
    structure_output = os.path.join(script_dir, args.structure_output)
    log_file = os.path.join(script_dir, 'results', 'script_log.txt')

    # Ensure the results directory exists
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    # Initialize logging
    with open(log_file, 'w', encoding='utf-8') as log_f:
        log_f.write(f"Script started. Repository path: {repo_path}\n")

    try:
        print("Loading ignore files...")
        spec = load_ignore_files(repo_path)

        # Determine input folders
        if args.folders:
            input_folders = args.folders
        else:
            # If no folders specified, process all top-level directories excluding those in .gitignore/.indexignore
            top_level_dirs = [name for name in os.listdir(repo_path) if os.path.isdir(os.path.join(repo_path, name))]
            input_folders = top_level_dirs
            print(f"No specific folders provided. Defaulting to top-level folders: {', '.join(input_folders)}")

        print("Traversing directories and building XML structures...")
        content_root, structure_root = traverse_directory(repo_path, input_folders, spec, allowed_extensions, script_extensions)

        print(f"Writing content XML to `{xml_output}`...")
        tree = etree.ElementTree(content_root)
        tree.write(xml_output, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print(f"Writing folder structure XML to `{structure_output}`...")
        struct_tree = etree.ElementTree(structure_root)
        struct_tree.write(structure_output, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print("Extracting scripts and TODOs to generate Markdown documentation...")
        markdown_content = extract_todos_and_scripts(content_root, script_extensions)

        print(f"Writing Markdown to `{md_output}`...")
        with open(md_output, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)

        print("Process completed successfully.")

    except Exception as e:
        error_message = f"An error occurred: {e}\n"
        print(error_message, file=sys.stderr)
        with open(log_file, 'a', encoding='utf-8') as log_f:
            log_f.write(error_message)

if __name__ == "__main__":
    main()
```

## `Evaluation/evaluation.py`

```

```

## `preprocessing/create_sample_set.py`

```
import json
import os
import shutil
import glob
import random
from tqdm import tqdm
from datetime import datetime

def create_sample_from_files():
    # Load configuration from a JSON file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    markdown_folder = config['output_folder_markdown_generation']
    output_sample_folder = config['output_folder_samples']
    min_token_count = config['MIN_TOKEN_COUNT']
    max_token_count = config['MAX_TOKEN_COUNT']
    sample_size = config['SAMPLE_SIZE']

    # Create a timestamped directory for the sample output
    now = datetime.now()
    timestamp = now.strftime("%y_%m_%d__%H_%M")
    
    sample_output_dir = os.path.join(
        output_sample_folder,
        f"sample_{timestamp}_size_{sample_size}_tokens_{min_token_count}_to_{max_token_count}"
    )
    print(f"Creating sample output directory: {sample_output_dir}")
    os.makedirs(sample_output_dir, exist_ok=True)

    # Gather all metadata files
    metadata_files = glob.glob(os.path.join(markdown_folder, "*_metadata.json"))
    print(f"Found {len(metadata_files)} metadata files.")
    
    # Verify files and tokens
    eligible_files = []
    for metadata_file in tqdm(metadata_files, desc="Filtering Files"):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        token_count = metadata.get('total_tokens', 0)
        user_id = metadata['user_id']
        
        print(f"Checking file {metadata_file}: Token count is {token_count}")
        
        if min_token_count <= token_count <= max_token_count:
            print(f"File eligible: user_id={user_id} with token_count={token_count}")
            eligible_files.append(user_id)
        else:
            print(f"File not eligible: user_id={user_id}, token_count={token_count}, requires between {min_token_count} and {max_token_count}")
    
    # Randomize eligible files
    random.shuffle(eligible_files)
    
    # Limit results to specified sample size
    selected_files = eligible_files[:sample_size]
    print(f"Selected files for sampling: {selected_files}")

    for user_id in tqdm(selected_files, desc="Copying Files"):
        # Find Markdown file for user
        md_file_pattern = f"user_{user_id}_comments_*_tokens.md"
        md_files = glob.glob(os.path.join(markdown_folder, md_file_pattern))
        print(f"Found markdown files for user_id={user_id}: {md_files}")
        
        # Copy Markdown files
        for md_file in md_files:
            try:
                shutil.copy(md_file, sample_output_dir)
                print(f"Copied {md_file} to {sample_output_dir}")
            except Exception as e:
                print(f"Failed to copy {md_file}: {e}")
        
        # Copy metadata JSON file
        metadata_file = os.path.join(markdown_folder, f"user_{user_id}_metadata.json")
        if os.path.exists(metadata_file):
            try:
                shutil.copy(metadata_file, sample_output_dir)
                print(f"Copied {metadata_file} to {sample_output_dir}")
            except Exception as e:
                print(f"Failed to copy {metadata_file}: {e}")
    
    print(f"Sample generated in {sample_output_dir}")

# Example invocation of the function
create_sample_from_files()
```

## `preprocessing/__init__.py`

```

```

## `preprocessing/build_context_md.py`

```
import json
import os
import pickle
import tiktoken
from tqdm import tqdm  # Importiere tqdm für Fortschrittsanzeige
from datetime import datetime
import locale

def format_date(date_string):
    """
    Formats a given date string to include only up to minutes.
    Utilizes a flexible parser to handle various date formats.
    """
    # Setzt die Locale auf Deutsch für macOS
    locale.setlocale(locale.LC_TIME, 'de_AT.UTF-8') 
    
    # Parse den ursprünglichen Datumsstring
    date_object = datetime.strptime(date_string[:16], "%Y-%m-%dT%H:%M")

    # Formatiere das Datum in das gewünschte Format
    formatted_date = date_object.strftime("%-d. %B %Y, %H:%M Uhr")

    return formatted_date

# Token-Zählfunktion definieren
def count_tokens(text):
    """
    Encodes the given text using a specific tokenization model and returns the count of tokens.
    This is useful for understanding the token consumption for text input, particularly 
    in environments where token count might affect computational resources or cost.
    """
    encoder = tiktoken.get_encoding("cl100k_base")  # Verwende das gpt2 Modell-Encoding als Beispiel
    tokens = encoder.encode(text)
    return len(tokens)

# Lade die Konfigurationen
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

input_json_path = config['input_json_path']
output_folder = config['output_folder_markdown_generation']
pkl_path = config['pkl_path_input_build_context']  # Der Pfad zur .pkl-Datei in config.json
metadata = config['metadata_file']

os.makedirs(output_folder, exist_ok=True)

# Öffne und lade die JSON-Eingabedatei
with open(input_json_path, 'r') as f:
    data = json.load(f)

# Hilfsfunktion für die Überprüfung der Benutzeraktivität
def user_in_comment_or_replies(comment, user_id):
    """
    Checks if a specific user_id is either the author of a comment or any of its replies.
    This recursive function helps traverse nested comment-reply structures 
    to locate the presence of the user in any depth level of the conversation.
    """
    if comment['user_id'] == user_id:
        return True
    for reply in comment.get('replies', []):
        if user_in_comment_or_replies(reply, user_id):
            return True
    return False

# Filterfunktion, die nur relevante Kommentare behält
def filter_comments_by_user(comments, user_id, user_id_to_anon_name, anon_user_counter, level=0):
    """
    Filters comments for a specific user and constructs a new list of comments 
    with associated details, maintaining recursive depth structure.
    It captures all comments and replies made by the user 
    and formats them for Markdown conversion while retaining indentation for hierarchy visualization.
    Anonymizes user names while preserving unique identifiers.
    """
    filtered_comments = []
    indent = "  " * level

    for comment in comments:
        if user_in_comment_or_replies(comment, user_id):
            # Determine the anonymous user name
            if comment['user_id'] == user_id:
                anon_username = "Analyse Zielnutzer"
            else:
                if comment['user_id'] not in user_id_to_anon_name:
                    anon_name = f"User {anon_user_counter[0]}"
                    user_id_to_anon_name[comment['user_id']] = anon_name
                    anon_user_counter[0] += 1
                anon_username = user_id_to_anon_name[comment['user_id']]
            
            new_comment = {
                "user_name": anon_username,
                "comment_headline": comment['comment_headline'],
                "comment_text": comment['comment_text'],
                "comment_created_at": comment['comment_created_at'],
                "replies": filter_comments_by_user(
                    comment.get('replies', []), user_id, user_id_to_anon_name, anon_user_counter, level + 1
                )
            }
            filtered_comments.append(new_comment)

    return filtered_comments

# Funktion zur Generierung einer Markdown-Struktur
def generate_comment_markdown(comments, level=0):
    """
    Generates a Markdown formatted string from a list of comments, recursively handling replies.
    Ensures that the hierarchical structure of comments and replies is represented 
    visually through indentation, making the output user-friendly and easy to read.
    """
    markdown = ""
    indent = "  " * level

    for comment in comments:
        # Sicherstellen, dass immer eine Headline angezeigt wird
        if level == 0:
            markdown += f"{indent}> {comment['user_name']} schreibt:\n"
        else:
            markdown += f"{indent}> {comment['user_name']} antwortet:\n"
        headline = comment.get('comment_headline')
        if not headline:
            headline = "Empty Heading"

        # Füge Headline zum Markdown-Output hinzu
        markdown += f"{indent}> **Headline**: {headline}\n"
        
        markdown += f"{indent}> **Kommentar**: {comment['comment_text']}\n"
        markdown += f"{indent}> **Kommentiert am** {format_date(comment['comment_created_at'])}\n\n"
        
        if 'replies' in comment and comment['replies']:
            markdown += generate_comment_markdown(comment['replies'], level + 1)

    return markdown

# Funktion zur Erstellung der Metadatendatei für einen Benutzer
def create_metadata_file(user_id, user_name, user_gender, user_created_at, total_tokens, comments_extracted):
    """
    Creates a JSON metadata file for a user, encapsulating user details 
    and statistics about their commenting activity. 
    This function supports tracking user engagement and data analysis by 
    logging structured profile data and comment history.
    """
    # Overwrite user_name to anonymize
    user_name = "Analyse Zielnutzer"
    metadata = {
        "user_id": int(user_id),
        "user_name": user_name,
        "user_gender": user_gender,
        "user_created_at": user_created_at,
        "total_tokens": int(total_tokens),
        "comments_extracted": int(comments_extracted)
    }

    metadata_filename = os.path.join(output_folder, f"user_{user_id}_metadata.json")
    with open(metadata_filename, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata file '{metadata_filename}' created.")

# Prozessiert Kommentare eines bestimmten Benutzers
def process_user_comments(data, target_user_id):
    """
    Processes comments for a designated user by finding, filtering, and 
    formatting user-specific comments and replies. Utilizes recursive 
    strategies to fully explore thread structures and collates user detail 
    and engagement information for Markdown generation.
    """
    all_user_comments = ""
    target_user_name, target_gender, target_created_at = "Unbekannt", "Unbekannt", "Unbekannt"

    # Initialize the mapping from user_id to anonymous names
    user_id_to_anon_name = {}
    anon_user_counter = [1]  # Using a list to make it mutable in recursion

    for article_id, article in data.items():
        user_details = find_user_details_in_comments(article.get('comment_threads', []), target_user_id)
        if user_details:
            target_user_name, target_gender, target_created_at = user_details

        header = f"### Artikel: {article['article_title']}\n\n"
        # ID itself has no meaning for classification
        #header += f"- Artikel ID: {article['article_id']}\n"
        header += f"- Veröffentlicht am: {format_date(article['article_publish_date'])}\n"
        header += f"- Kanal: {article['article_channel']}\n"
        header += f"- Ressort: {article['article_ressort_name']}\n"
        header += f"- Gesamtanzahl Kommentare: {article['total_comments']}\n\n"
        header += "#### Kommentare\n\n"

        comments = article.get('comment_threads', [])
        user_comments = filter_comments_by_user(
            comments, target_user_id, user_id_to_anon_name, anon_user_counter
        )
        body = generate_comment_markdown(user_comments)

        if body:
            all_user_comments += header + body

    if all_user_comments:
        target_user_name = "Analyse Zielnutzer"  # Overwrite for anonymity
        intro = f"# Benutzeraktivität von {target_user_name}\n\n"
        intro += f"Es folgt die Benutzeraktivität von {target_user_name}\n\n"
        #intro += "## Benutzerdetails\n\n"
        #intro += f"- Benutzername: {target_user_name}\n"
        # Has no relevance for classification
        #intro += f"- Benutzer-ID: {target_user_id}\n"
        #intro += f"- Geschlecht: {target_gender}\n"
        #intro += f"- Konto erstellt am: {format_date(target_created_at)}\n\n---\n\n"
        intro += "## Kommentare und Threads\n\n"
        intro += "Die Kommatre sind nach Artikel sortiert. Wenn der Artikel aufgeführt ist, hat der Analyse Zielnutzer mindestenz einen Kommentar unter dem Artikel geschrieben. Es werden nicht alle Kommantare aufgeführt, sondern nur diese, in denen der Analyse Zielnutzer aktiv war. Threads in denen der Analyse Zielnutzer keinen Kommentar geschrieben hat, sind nicht inkludiert. \n\n"

        complete_content = intro + all_user_comments
        token_count = count_tokens(complete_content)
        comments_count = complete_content.count('schreibt:') 

        filename = os.path.join(
            output_folder, f"user_{target_user_id}_comments_{token_count}_tokens.md"
        )
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(complete_content)
        if metadata:
            create_metadata_file(
                target_user_id, target_user_name, target_gender, target_created_at,
                token_count, comments_count)
        
        
def find_user_details_in_comments(comments, target_user_id):
    """
    Searches for user information within a collection of comments, 
    employing recursion to navigate nested replies. This approach 
    ensures that no matter how deeply nested the user's comments are, 
    their details are successfully extracted.
    """
    for comment in comments:
        if comment['user_id'] == target_user_id:
            return comment['user_name'], comment['user_gender'], comment['user_created_at']
        
        # Recursively search in replies
        user_details = find_user_details_in_comments(comment.get('replies', []), target_user_id)
        if user_details:
            return user_details
    
    return None

# Prozessiert alle Benutzer aus der .pkl Datei
def process_all_users():
    """
    Loads a list of user IDs from a provided .pkl file and processes 
    each user's comments and metadata. Utilizes multiprocessing and 
    progress tracking to efficiently handle and monitor large datasets 
    during user data extraction.
    """
    with open(pkl_path, 'rb') as file:
        user_data = pickle.load(file)
        
    if 'ID_CommunityIdentity' not in user_data.columns:
        raise KeyError("The key 'ID_CommunityIdentity' is not found in the DataFrame. Available keys: ", user_data.columns)

    user_ids = user_data['ID_CommunityIdentity'].unique()

    for user_id in tqdm(user_ids, desc="Processing Users"):
        process_user_comments(data, user_id)


# Hauptaufruf
process_all_users()
```

## `preprocessing/validation_script.py`

```
import pickle
import pandas as pd
import json
from tqdm import tqdm

# Configuration loading
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

markdown_folder = config['output_folder_markdown_generation']
pkl_path = config['input_pkl_path']
json_path = config['input_json_path']

# Step 1: Load the PKL file and extract unique user names
def load_unique_user_names():
    # Load the PKL data
    with open(pkl_path, 'rb') as file:
        pkl_data = pickle.load(file)

    # Ensure the necessary column is present
    if 'UserCommunityName' not in pkl_data.columns:
        raise KeyError("The 'UserCommunityName' column is missing from the DataFrame.")

    # Get unique user names
    unique_user_names = pkl_data['UserCommunityName'].unique()
    print(f"Unique user names from PKL: {unique_user_names}")

    return unique_user_names, pkl_data

unique_user_names, pkl_data = load_unique_user_names()

# Step 2: Count how often each user name appears in the PKL file
def count_user_occurrences_in_pkl(unique_user_names, pkl_data):
    pkl_user_counts = {}

    for user_name in tqdm(unique_user_names, desc="Counting in PKL"):
        count = (pkl_data['UserCommunityName'] == user_name).sum()
        pkl_user_counts[user_name] = count

    return pkl_user_counts

pkl_user_counts = count_user_occurrences_in_pkl(unique_user_names, pkl_data)

# Step 3: Count how often each user name appears in the JSON file using recursion
def count_user_in_json(json_data, target_user_name):
    count = 0

    for article_id, article_data in json_data.items():
        count += count_user_in_threads(article_data.get('comment_threads', []), target_user_name)

    return count

def count_user_in_threads(threads, target_user_name):
    count = 0

    for thread in threads:
        # Check the current comment
        if thread['user_name'] == target_user_name:
            count += 1
        
        # Recursively search replies
        count += count_user_in_threads(thread.get('replies', []), target_user_name)

    return count

def count_user_occurrences_in_json(unique_user_names):
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    json_user_counts = {}

    # Traverse the JSON data and count occurrences using recursion
    for user_name in tqdm(unique_user_names, desc="Counting in JSON"):
        count = count_user_in_json(json_data, user_name)
        json_user_counts[user_name] = count
        print(f"User '{user_name}' appears {count} times in the JSON file.")

    return json_user_counts

json_user_counts = count_user_occurrences_in_json(unique_user_names)

# Step 4: Validate counts between PKL and JSON and provide a summary
def validate_user_name_counts(pkl_user_counts, json_user_counts):
    successful_validations = 0
    failed_validations = 0

    for user_name in pkl_user_counts.keys():
        pkl_count = pkl_user_counts.get(user_name, 0)
        json_count = json_user_counts.get(user_name, 0)

        if pkl_count == json_count:
            successful_validations += 1
        else:
            failed_validations += 1
            print(f"Discrepancy for User '{user_name}': PKL={pkl_count}, JSON={json_count}")

    print("\nValidation Summary:")
    print(f"Successful validations: {successful_validations}")
    print(f"Failed validations: {failed_validations}")

validate_user_name_counts(pkl_user_counts, json_user_counts)
```

## `preprocessing/analyse_articles.py`

```
import pandas as pd
import pickle
import os
import json


class ArticleAnalyzer:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the ArticleAnalyzer with the preprocessed data.

        Args:
            df (pd.DataFrame): The preprocessed data containing article information.
        """
        self.df = df

    def analyze_articles(self):
        """
        Perform analysis on articles to get insights into article count, channels, and resources.
        """
        article_count = self.df['ID_Article'].nunique()
        channel_counts = self.df['ArticleChannel'].value_counts()
        ressort_counts = self.df['ArticleRessortName'].value_counts()

        analysis = {
            'total_articles': article_count,
            'channel_distribution': channel_counts.to_dict(),
            'ressort_distribution': ressort_counts.to_dict()
        }
        
        return analysis

    def filter_and_save_by_ressort(self, ressort_name: str, output_path: str):
        """
        Filter the dataframe to include only entries from the specified ressort and save to a new pickle file.

        Args:
            ressort_name (str): The name of the ressort to filter by.
            output_path (str): The path where the filtered data will be saved.
        """
        filtered_df = self.df[self.df['ArticleRessortName'] == ressort_name]
        
        with open(output_path, 'wb') as f:
            pickle.dump(filtered_df, f)
        
        print(f"Filtered data containing only the '{ressort_name}' ressort saved to {output_path}")


def main():
    preprocessed_file = r"../data/preprocessed/preprocessed_data.pkl"
    preprocessed_file = r"../data/preprocessed/preprocessed_data_inland.pkl"

    if not os.path.exists(preprocessed_file):
        raise FileNotFoundError(f"Preprocessed data not found at {preprocessed_file}. Please ensure the file exists.")
    else:
        print("Loading preprocessed data...")
        with open(preprocessed_file, 'rb') as f:
            df = pickle.load(f)

    analyzer = ArticleAnalyzer(df)
    analysis_result = analyzer.analyze_articles()

    # Save the analysis result to a JSON file
    analysis_output_path = "spheres/article_analysis_inland.json"
    with open(analysis_output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, indent=2)
    print(f"Article analysis saved to {analysis_output_path}")

def main_filter():
    preprocessed_file = r"../data/preprocessed/preprocessed_data.pkl"

    if not os.path.exists(preprocessed_file):
        raise FileNotFoundError(f"Preprocessed data not found at {preprocessed_file}. Please ensure the file exists.")
    else:
        print("Loading preprocessed data...")
        with open(preprocessed_file, 'rb') as f:
            df = pickle.load(f)
    # Filter by ressort (e.g., "Inland") and save
    analyzer = ArticleAnalyzer(df)
    analysis_result = analyzer.analyze_articles()

    filtered_output_path = "../data/preprocessed/preprocessed_data_inland.pkl"
    analyzer.filter_and_save_by_ressort("Inland", filtered_output_path)

if __name__ == "__main__":
    main()
    #main_filter()
```

## `preprocessing/build_base_json.py`

```
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import os
import json
from typing import List, Dict


# Lade die Konfigurationen
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


class DataPreprocessor:
    def __init__(self, file_path: str):
        """
        Initialize the DataPreprocessor with the file path.

        Args:
            file_path (str): The path to the CSV file containing the data.
        """
        self.file_path = file_path
        self.df = None

    def process(self):
        """
        Process the data by loading it from the CSV file and applying various preprocessing steps.
        """
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        """
        Convert date columns to datetime format.
        """
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        """
        Handle missing values in the data by filling them with appropriate values.
        """
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        """
        Convert ID columns to integer type.
        """
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        """
        Create new features based on existing columns.
        """
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    def save_preprocessed_data(self, output_path: str):
        """
        Save the preprocessed data to a pickle file.

        Args:
            output_path (str): The path where the preprocessed data will be saved.
        """
        with open(output_path, 'wb') as f:
            pickle.dump(self.df, f)
        print(f"Preprocessed data saved to {output_path}")

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        """
        Load the preprocessed data from a pickle file.

        Args:
            input_path (str): The path to the pickle file containing the preprocessed data.

        Returns:
            DataPreprocessor: An instance of DataPreprocessor with the loaded data.
        """
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor

class CommentThreadManager:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the CommentThreadManager with the preprocessed data.

        Args:
            df (pd.DataFrame): The preprocessed data containing comment information.
        """
        self.df = df

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int) -> List[Dict]:
        """
        Build a hierarchical structure of comments and their replies.

        Args:
            comments (pd.DataFrame): The comments data for a specific article.
            parent_id (int): The ID of the parent comment.

        Returns:
            List[Dict]: A list of dictionaries representing the comment thread.
        """
        replies = comments[comments['ID_Posting_Parent'] == parent_id]
        return [{
            'id': int(reply['ID_Posting']),
            'parent_id': int(reply['ID_Posting_Parent']) if pd.notnull(reply['ID_Posting_Parent']) else None,
            'user_id': int(reply['ID_CommunityIdentity']),
            'user_name': reply['UserCommunityName'],
            'user_gender': reply['UserGender'],
            'user_created_at': reply['UserCreatedAt'].isoformat() if pd.notnull(reply['UserCreatedAt']) else None,
            'comment_headline': reply['PostingHeadline'],
            'comment_text': reply['PostingComment'],
            'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(reply['PostingCreatedAt']) else None,
            'comment_length': int(reply['CommentLength']),
            'article_id': int(reply['ID_Article']),
            'article_publish_date': reply['ArticlePublishingDate'].isoformat() if pd.notnull(reply['ArticlePublishingDate']) else None,
            'article_title': reply['ArticleTitle'],
            'article_channel': reply['ArticleChannel'],
            'article_ressort_name': reply['ArticleRessortName'],
            'replies': self.build_comment_thread(comments, int(reply['ID_Posting']))
        } for _, reply in replies.iterrows()]

    def get_article_threads(self) -> Dict[int, Dict]:
        """
        Get the comment threads for all articles.

        Returns:
            Dict[int, Dict]: A dictionary where keys are article IDs and values are dictionaries representing the article's comment threads.
        """
        articles = {}
        for article_id, article_df in self.df.groupby('ID_Article'):
            root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]
            threads = self.build_comment_thread(article_df, 0)
            article_meta = article_df.iloc[0]

            articles[int(article_id)] = {
                'article_id': int(article_id),
                'article_title': article_meta['ArticleTitle'],
                'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(article_meta['ArticlePublishingDate']) else None,
                'article_channel': article_meta['ArticleChannel'],
                'article_ressort_name': article_meta['ArticleRessortName'],
                'total_comments': len(article_df),
                'root_comments': len(root_comments),
                'comment_threads': threads
            }
        return articles

def main():
    # Main execution
    preprocessed_pkl_path = config["input_pkl_path"]
    input_csv_path = config["input_csv_path"]
    output_path_json = config["output_path_build_json"]

    if not os.path.exists(preprocessed_pkl_path):
        print("Preprocessed data not found. Preprocessing...")
        preprocessor = DataPreprocessor(input_csv_path)
        preprocessor.process()
        preprocessor.save_preprocessed_data(preprocessed_pkl_path)
    else:
        print("Loading preprocessed data...")
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_pkl_path)

    thread_manager = CommentThreadManager(preprocessor.df)
    articles_with_threads = thread_manager.get_article_threads()

    # Save the comprehensive data structure to a JSON file
    
    with open(output_path_json, 'w', encoding='utf-8') as f:
        json.dump(articles_with_threads, f, indent=2)
    print(f"Comprehensive data structure saved to {output_path_json}")

if __name__ == "__main__":
    main()
```

## `preprocessing/token_distribution.py`

```
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_tokens_from_json(directory):
    total_tokens_list = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):  # Ensure we process only JSON files
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                total_tokens = data.get("total_tokens", 0)
                total_tokens_list.append(total_tokens)
    
    return total_tokens_list

def analyze_tokens(tokens):
    tokens_array = np.array(tokens)

    mean = np.mean(tokens_array)
    median = np.median(tokens_array)
    quantile_25 = np.quantile(tokens_array, 0.25)
    quantile_50 = np.quantile(tokens_array, 0.50)
    quantile_75 = np.quantile(tokens_array, 0.75)
    quantile_95 = np.quantile(tokens_array, 0.95)
    std_dev = np.std(tokens_array)

    # Identifying outliers using z-score
    z_scores = (tokens_array - mean) / std_dev
    outliers = tokens_array[abs(z_scores) > 3]  # More than 3 standard deviations from the mean
    tokens_no_outliers = tokens_array[abs(z_scores) <= 3]

    print(f'Mean: {mean}')
    print(f'Median: {median}')
    print(f'25th Quantile: {quantile_25}')
    print(f'50th Quantile (Median): {quantile_50}')
    print(f'75th Quantile: {quantile_75}')
    print(f'95th Quantile: {quantile_95}')
    print(f'Outliers: {outliers}')

    return tokens_array, tokens_no_outliers, quantile_95

def plot_distributions(tokens, tokens_no_outliers, output_directory):
    sns.set(style="whitegrid")

    # Histogram with Outliers
    plt.figure(figsize=(12, 6))
    sns.histplot(tokens, bins=30, kde=True, color='skyblue')
    plt.title('Distribution of Total Tokens (with Outliers)')
    plt.xlabel('Total Tokens')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'distribution_with_outliers.png'))
    plt.close()

    # Histogram without Outliers
    plt.figure(figsize=(12, 6))
    sns.histplot(tokens_no_outliers, bins=30, kde=True, color='salmon')
    plt.title('Distribution of Total Tokens (without Outliers)')
    plt.xlabel('Total Tokens')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'distribution_without_outliers.png'))
    plt.close()

def calculate_percentage_in_ranges(tokens, max_value, step=1000):
    total_files = len(tokens)
    ranges = [(i, i + step) for i in range(0, int(max_value), step)]
    filtered_results = []

    for lower_bound, upper_bound in ranges:
        count_in_range = sum(lower_bound <= t < upper_bound for t in tokens)
        percentage = (count_in_range / total_files) * 100
        if percentage > 1.0:  # Only include ranges with more than 1% of files
            filtered_results.append((lower_bound, upper_bound, count_in_range, percentage))

    return filtered_results

def plot_range_distribution(results, output_directory):
    labels = [f"{lb}-{ub}" for lb, ub, _, _ in results]
    percentages = [percentage for _, _, _, percentage in results]

    plt.figure(figsize=(14, 7))
    plt.bar(labels, percentages, color='slateblue')
    plt.xticks(rotation=90)
    plt.title('Percentage of Files by Token Range (>1% of Total)')
    plt.xlabel('Token Range')
    plt.ylabel('Percentage of Total Files')
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'token_range_distribution.png'))
    plt.close()

if __name__ == "__main__":
    directory_path = './Input_Output/Markdown'
    output_directory = './Documentation'
    os.makedirs(output_directory, exist_ok=True)
    
    tokens = load_tokens_from_json(directory_path)
    tokens_with_outliers, tokens_without_outliers, quantile_95 = analyze_tokens(tokens)
    
    plot_distributions(tokens_with_outliers, tokens_without_outliers, output_directory)

    # Analyze percentage distribution within calculated ranges
    range_results = calculate_percentage_in_ranges(tokens, quantile_95, step=1000)
    
    # Print range results
    print("\nToken Range Analysis (>1%):")
    for lower_bound, upper_bound, count, percentage in range_results:
        print(f"Range {lower_bound} - {upper_bound} tokens: {count} files, {percentage:.2f}% of total")

    # Plot token range distribution
    plot_range_distribution(range_results, output_directory)
```

## `preprocessing/Versions-pre-processing/data_preprocessor-v5.py`

```
import pandas as pd
import pickle

class DataPreprocessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def process(self):
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor

```

## `preprocessing/Versions-pre-processing/test_specific_user_markdown_function.py`

```
def test_specific_user_markdown(data, user_id=518684):
    """
    Generates a Markdown file for a specific user ID to validate 
    the handling of nested comment structures and user detail extraction.
    
    Parameters:
    - data: The JSON data containing all articles and comments.
    - user_id (int): The target user ID for which to generate the Markdown document.
    """
    all_user_comments = ""
    target_user_name, target_gender, target_created_at = "Unbekannt", "Unbekannt", "Unbekannt"

    for article_id, article in data.items():
        # Attempt to extract the user's details and comments
        user_details = find_user_details_in_comments(article.get('comment_threads', []), user_id)
        if user_details:
            target_user_name, target_gender, target_created_at = user_details

        # Prepare the article header for the markdown
        header = f"### {article['article_title']}\n"     
        header += f"- Artikel ID: {article['article_id']}\n"
        header += f"- Veröffentlicht am: {article['article_publish_date']}\n"
        header += f"- Kanal: {article['article_channel']}\n"
        header += f"- Ressort: {article['article_ressort_name']}\n"
        header += f"- Gesamtanzahl Kommentare: {article['total_comments']}\n\n"
        header += "#### Kommentare\n"

        comments = article.get('comment_threads', [])
        user_comments = filter_comments_by_user(comments, user_id)
        body = generate_comment_markdown(user_comments)

        if body:
            all_user_comments += header + body + "\n\n"

    if all_user_comments:
        intro = f"# Benutzeraktivität von {target_user_name}\n\n"
        intro += "## Benutzerdetails\n"
        intro += f"- Benutzername: {target_user_name}\n"
        intro += f"- Benutzer-ID: {user_id}\n"
        intro += f"- Geschlecht: {target_gender}\n"
        intro += f"- Konto erstellt am: {target_created_at}\n\n---\n\n"
        intro += "## Kommentare und Threads\n\n"

        complete_content = intro + all_user_comments
        token_count = count_tokens(complete_content)
        comments_count = complete_content.count('schreibt:')  # Count the number o
```

## `preprocessing/Versions-pre-processing/preprocessing-v4.py`

```
import pandas as pd
import pickle
import tiktoken
from typing import Dict, List, Tuple
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
from data_preprocessor import DataPreprocessor

'''
The modified cutoff_after_last_interaction method now better aligns with your requirements. Here's how it works:

a. We first traverse all threads to find the user's last interaction time.
b. We then remove any comments (including root comments) that occur after the user's last interaction.
c. This approach ensures that the context sphere only contains information up to the user's last interaction, assuming that anything after that should not be part of the context.

This is a good approach because:
- It preserves the chronological context of the user's interactions.
- It removes potentially irrelevant information that the user hasn't seen or interacted with.
- It helps in creating a more focused and relevant context sphere for the user.
'''

class CommentThreadManager:
    def __init__(self, df: pd.DataFrame):
        self.article_comments = {article_id: group for article_id, group in df.groupby('ID_Article')}

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int, depth: int = 0) -> List[Dict]:
        replies = comments[comments['ID_Posting_Parent'] == parent_id]
        return [{
            'id': int(reply['ID_Posting']),
            'parent_id': int(reply['ID_Posting_Parent']) if pd.notnull(reply['ID_Posting_Parent']) else None,
            'user_id': int(reply['ID_CommunityIdentity']),
            'user_name': reply['UserCommunityName'],
            'user_gender': reply['UserGender'],
            'user_created_at': reply['UserCreatedAt'].isoformat() if pd.notnull(reply['UserCreatedAt']) else None,
            'comment_headline': reply['PostingHeadline'],
            'comment_text': reply['PostingComment'],
            'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(reply['PostingCreatedAt']) else None,
            'comment_length': int(reply['CommentLength']),
            'depth': depth,
            'replies': self.build_comment_thread(comments, int(reply['ID_Posting']), depth + 1)
        } for _, reply in replies.iterrows()]

    def get_article_threads(self, article_id: int) -> Dict:
        if article_id not in self.article_comments:
            return None

        article_df = self.article_comments[article_id]
        root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]

        threads = self.build_comment_thread(article_df, 0)
        article_meta = article_df.iloc[0]

        return {
            'article_id': int(article_id),
            'article_title': article_meta['ArticleTitle'],
            'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(article_meta['ArticlePublishingDate']) else None,
            'article_channel': article_meta['ArticleChannel'],
            'article_ressort_name': article_meta['ArticleRessortName'],
            'total_comments': len(article_df),
            'root_comments': len(root_comments),
            'comment_threads': threads
        }

class UserContextSphere:
    def __init__(self, df: pd.DataFrame, thread_manager: CommentThreadManager):
        self.df = df
        self.thread_manager = thread_manager
        self.user_comments = defaultdict(list)
        self._populate_user_comments()

    def _populate_user_comments(self):
        for _, row in self.df.iterrows():
            self.user_comments[row['ID_CommunityIdentity']].append(row)

    def get_user_context(self, user_id: int) -> Dict:
        if user_id not in self.user_comments:
            return None

        user_df = pd.DataFrame(self.user_comments[user_id])
        total_comments = len(user_df)
        total_replies = len(user_df[user_df['ID_Posting_Parent'].notnull()])

        user_context = {
            'user_id': int(user_id),
            'user_name': user_df['UserCommunityName'].iloc[0],
            'user_gender': user_df['UserGender'].iloc[0],
            'user_created_at': user_df['UserCreatedAt'].iloc[0].isoformat(),
            'total_comments': total_comments,
            'total_replies': total_replies,
            'articles': {}
        }

        for article_id, article_comments in user_df.groupby('ID_Article'):
            article_id = int(article_id)
            article_thread = self.thread_manager.get_article_threads(article_id)

            if article_thread:
                user_context['articles'][article_id] = {
                    'article_title': article_thread['article_title'],
                    'article_publish_date': article_thread['article_publish_date'],
                    'user_comments_count': len(article_comments),
                    'user_replies_count': len(article_comments[article_comments['ID_Posting_Parent'].notnull()]),
                    'threads': [self.find_thread_for_comment(article_thread['comment_threads'], int(comment['ID_Posting']))
                                for _, comment in article_comments.iterrows()]
                }

        return user_context

    def find_thread_for_comment(self, threads: List[Dict], comment_id: int) -> Dict:
        for thread in threads:
            if thread['id'] == comment_id:
                return thread
            result = self.find_thread_for_comment(thread['replies'], comment_id)
            if result:
                return thread
        return None

    def cutoff_after_last_interaction(self, user_context: Dict, user_id: int) -> Tuple[Dict, int]:
        removed_comments = 0
        last_interaction_time = None

        def process_thread(thread: Dict) -> Tuple[Dict, int]:
            nonlocal removed_comments, last_interaction_time
            if thread['comment_created_at'] > last_interaction_time:
                return None, 1  # Remove this thread and all its replies

            if thread['user_id'] == user_id:
                if last_interaction_time is None or thread['comment_created_at'] > last_interaction_time:
                    last_interaction_time = thread['comment_created_at']

            new_replies = []
            for reply in thread['replies']:
                processed_reply, removed_count = process_thread(reply)
                removed_comments += removed_count
                if processed_reply:
                    new_replies.append(processed_reply)

            thread['replies'] = new_replies
            return thread, 0

        for article_id in user_context['articles']:
            new_threads = []
            for thread in user_context['articles'][article_id]['threads']:
                processed_thread, _ = process_thread(thread)
                new_threads.append(processed_thread)

            user_context['articles'][article_id]['threads'] = new_threads

        # Remove comments after the last interaction
        for article_id in user_context['articles']:
            user_context['articles'][article_id]['threads'] = [
                thread for thread in user_context['articles'][article_id]['threads']
                if thread['comment_created_at'] <= last_interaction_time
            ]
            removed_comments += len(user_context['articles'][article_id]['threads'])

        return user_context, removed_comments


    def escape_markdown(self, text: str) -> str:
        escape_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in escape_chars:
            text = text.replace(char, '\\' + char)
        return text.replace('`', "'")

    def format_comment_thread(self, comment: Dict) -> str:
        root = ET.Element("comment_thread")
        self.add_comment_to_xml(root, comment)
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def add_comment_to_xml(self, parent: ET.Element, comment: Dict):
        comment_elem = ET.SubElement(parent, "comment")
        author_elem = ET.SubElement(comment_elem, "author")
        author_elem.text = self.escape_markdown(comment['user_name'])
        content_elem = ET.SubElement(comment_elem, "content")
        content_elem.text = self.escape_markdown(comment['comment_text'])
        if comment['replies']:
            replies_elem = ET.SubElement(comment_elem, "replies")
            for reply in comment['replies']:
                self.add_comment_to_xml(replies_elem, reply)

    def generate_formatted_user_context(self, user_id: int) -> str:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}"

        output = []

        output.append("# User Context\n")
        output.append(f"- **User ID:** {user_context['user_id']}\n")
        output.append(f"- **Username:** {self.escape_markdown(user_context['user_name'])}\n")
        output.append(f"- **Gender:** {self.escape_markdown(user_context['user_gender'])}\n")
        output.append(f"- **Created At:** {user_context['user_created_at']}\n")
        output.append(f"- **Total Comments:** {user_context['total_comments']}\n")
        output.append(f"- **Total Replies:** {user_context['total_replies']}\n")
        output.append("\n---\n\n")

        for article_id, article_data in user_context['articles'].items():
            output.append("# Article Context\n")
            output.append(f"- **Article ID:** {article_id}\n")
            output.append(f"- **Article Title:** {self.escape_markdown(article_data['article_title'])}\n")
            output.append(f"- **Article Publish Date:** {article_data['article_publish_date']}\n")
            output.append(f"- **User Comments Count:** {article_data['user_comments_count']}\n")
            output.append(f"- **User Replies Count:** {article_data['user_replies_count']}\n")
            output.append("\n---\n\n")

            output.append("# Comment Threads\n\n")
            for i, thread in enumerate(article_data['threads'], 1):
                output.append(f"## Thread {i}\n\n")
                output.append(self.format_comment_thread(thread))
                output.append("\n---\n\n")

        output.append("# End of Context")
        return "".join(output)

    def generate_user_report_with_cutoff(self, user_id: int) -> Tuple[str, int, int]:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}", 0, 0

        user_context, removed_comments = self.cutoff_after_last_interaction(user_context, user_id)

        report = self.generate_formatted_user_context(user_id)
        encoding = tiktoken.get_encoding("cl100k_base")
        token_count = len(encoding.encode(report))

        return report, token_count, removed_comments

# Main execution
if __name__ == "__main__":
    preprocessed_file = "../data/preprocessed/preprocessed_data.pkl"

    if not os.path.exists(preprocessed_file):
        print("Preprocessed data not found. Preprocessing...")
        preprocessor = DataPreprocessor('../data/raw_csv/Postings_01052019_31052019.csv')
        preprocessor.process()
        with open(preprocessed_file, 'wb') as f:
            pickle.dump(preprocessor.df, f)
        print(f"Preprocessed data saved to {preprocessed_file}")
    else:
        print("Loading preprocessed data...")
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)

    thread_manager = CommentThreadManager(preprocessor.df)
    user_context_sphere = UserContextSphere(preprocessor.df, thread_manager)

    spheres_dir_no_cutoff = "spheres/no_cutoff"
    spheres_dir_cutoff = "spheres/cutoff"
    os.makedirs(spheres_dir_no_cutoff, exist_ok=True)
    os.makedirs(spheres_dir_cutoff, exist_ok=True)

    user_id = 675862  # Replace with the desired user ID

    formatted_context = user_context_sphere.generate_formatted_user_context(user_id)

    if formatted_context != f"No data found for user ID {user_id}":
        filename_no_cutoff = f"{spheres_dir_no_cutoff}/{user_id}.md"
        with open(filename_no_cutoff, 'w', encoding='utf-8') as f:
            f.write(formatted_context)
        print(f"User context without cutoff saved to {filename_no_cutoff}")

        report, token_count, removed_comments = user_context_sphere.generate_user_report_with_cutoff(user_id)

        filename_cutoff = f"{spheres_dir_cutoff}/{user_id}.md"
        with open(filename_cutoff, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"User context with cutoff saved to {filename_cutoff}")

        print(f"Token count: {token_count}")
        print(f"Removed comments: {removed_comments}")
    else:
        error_message = f"# Error\n\nNo data found for user ID {user_id}"

        for dir_path in [spheres_dir_no_cutoff, spheres_dir_cutoff]:
            filename = f"{dir_path}/{user_id}_error.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(error_message)
            print(f"Error message saved to {filename}")
```

## `preprocessing/Versions-pre-processing/build_user_json-v6.py`

```
import json
import os

def load_json(file_path):
    """
    Load the JSON file containing articles and comments.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_articles_with_user_comments(articles, user_id):
    """
    Find all articles where the user has written a comment.

    Args:
        articles (dict): The dictionary containing articles and comments.
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary of articles where the user has written a comment.
    """
    user_articles = {}
    for article_id, article_data in articles.items():
        for thread in article_data['comment_threads']:
            if user_has_comment_in_thread(thread, user_id):
                user_articles[article_id] = article_data
                break
    return user_articles

def user_has_comment_in_thread(thread, user_id):
    """
    Check if the user has a comment in the given thread or its replies.

    Args:
        thread (dict): The thread to check.
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user has a comment in the thread, False otherwise.
    """
    if thread['user_id'] == user_id:
        return True
    for reply in thread['replies']:
        if user_has_comment_in_thread(reply, user_id):
            return True
    return False

def find_user_threads_in_articles(articles, user_id):
    """
    Find all threads in the given articles where the user has written a comment.

    Args:
        articles (dict): The dictionary containing articles and comments.
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary of articles with threads where the user has written a comment.
    """
    user_articles = {}
    for article_id, article_data in articles.items():
        user_threads = []
        for thread in article_data['comment_threads']:
            filtered_thread = filter_thread_for_user(thread, user_id)
            if filtered_thread:
                user_threads.append(filtered_thread)

        if user_threads:
            user_articles[article_id] = {
                'article_id': article_data['article_id'],
                'article_title': article_data['article_title'],
                'article_publish_date': article_data['article_publish_date'],
                'article_channel': article_data['article_channel'],
                'article_ressort_name': article_data['article_ressort_name'],
                'total_comments': article_data['total_comments'],
                'root_comments': article_data['root_comments'],
                'user_threads': user_threads
            }

    return user_articles

def filter_thread_for_user(thread, user_id):
    """
    Filter the thread to include only the parts where the user has written a comment.

    Args:
        thread (dict): The thread to filter.
        user_id (int): The ID of the user.

    Returns:
        dict: The filtered thread, or None if the user has not written a comment in the thread.
    """
    if thread['user_id'] == user_id:
        filtered_replies = [filter_thread_for_user(reply, user_id) for reply in thread['replies']]
        filtered_replies = [reply for reply in filtered_replies if reply]
        filtered_thread = thread.copy()
        filtered_thread['replies'] = filtered_replies
        return filtered_thread
    else:
        filtered_replies = [filter_thread_for_user(reply, user_id) for reply in thread['replies']]
        filtered_replies = [reply for reply in filtered_replies if reply]
        if filtered_replies:
            filtered_thread = thread.copy()
            filtered_thread['replies'] = filtered_replies
            return filtered_thread
    return None

def save_json(data, file_path):
    """
    Save the data to a JSON file.

    Args:
        data (dict): The data to save.
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {file_path}")

# Beispiel für die Verwendung
file_path = '../spheres/JSON/articles_with_threads_full_tree.json'
articles_with_threads = load_json(file_path)

user_id = 5002

# Schritt 1: Finde alle Artikel, in denen der Benutzer einen Kommentar geschrieben hat
user_articles = find_articles_with_user_comments(articles_with_threads, user_id)
print(f"Artikel, in denen der Benutzer {user_id} einen Kommentar geschrieben hat:")
print(json.dumps(user_articles, indent=2))

# Schritt 2: Finde alle Threads in diesen Artikeln, in denen der Benutzer aktiv war
user_threads_in_articles = find_user_threads_in_articles(user_articles, user_id)
print(f"Threads, in denen der Benutzer {user_id} aktiv war:")
print(json.dumps(user_threads_in_articles, indent=2))

# Speichern der Ergebnisse in einer JSON-Datei
output_dir = '../spheres/JSON'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f'user_{user_id}_threads.json')
save_json(user_threads_in_articles, output_file)
```

## `preprocessing/Versions-pre-processing/preprocessing_v3-mit_cufoff.py`

```
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import tiktoken
from typing import Dict, List, Optional, Tuple
import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from html import escape  # Fügen Sie diesen Import hinzu


class DataPreprocessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def process(self):
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    def save_preprocessed_data(self, output_path: str):
        with open(output_path, 'wb') as f:
            pickle.dump(self.df, f)
        print(f"Preprocessed data saved to {output_path}")

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor


class CommentThreadManager:
    def __init__(self, df: pd.DataFrame):
        self.article_comments = {article_id: group for article_id, group in df.groupby('ID_Article')}

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int, depth: int = 0) -> List[Dict]:
        replies = comments[comments['ID_Posting_Parent'] == parent_id]
        return [{
            'id': int(reply['ID_Posting']),
            'parent_id': int(reply['ID_Posting_Parent']) if pd.notnull(reply['ID_Posting_Parent']) else None,
            'user_id': int(reply['ID_CommunityIdentity']),
            'user_name': reply['UserCommunityName'],
            'user_gender': reply['UserGender'],
            'user_created_at': reply['UserCreatedAt'].isoformat() if pd.notnull(reply['UserCreatedAt']) else None,
            'comment_headline': reply['PostingHeadline'],
            'comment_text': reply['PostingComment'],
            'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(
                reply['PostingCreatedAt']) else None,
            'comment_length': int(reply['CommentLength']),
            'depth': depth,
            'replies': self.build_comment_thread(comments, int(reply['ID_Posting']), depth + 1)
        } for _, reply in replies.iterrows()]

    def get_article_threads(self, article_id: int) -> Optional[Dict]:
        if article_id not in self.article_comments:
            return None

        article_df = self.article_comments[article_id]
        root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]

        threads = self.build_comment_thread(article_df, 0)
        article_meta = article_df.iloc[0]

        return {
            'article_id': int(article_id),
            'article_title': article_meta['ArticleTitle'],
            'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(
                article_meta['ArticlePublishingDate']) else None,
            'article_channel': article_meta['ArticleChannel'],
            'article_ressort_name': article_meta['ArticleRessortName'],
            'total_comments': len(article_df),
            'root_comments': len(root_comments),
            'comment_threads': threads
        }

    def get_article_ids(self) -> List[int]:
        return list(self.article_comments.keys())


class UserContextSphere:
    def __init__(self, df: pd.DataFrame, thread_manager: CommentThreadManager):
        self.df = df
        self.thread_manager = thread_manager
        self.user_comments = {user_id: group for user_id, group in df.groupby('ID_CommunityIdentity')}

    def get_user_context(self, user_id: int) -> Optional[Dict]:
        if user_id not in self.user_comments:
            return None

        user_df = self.user_comments[user_id]
        total_comments = len(user_df)
        total_replies = len(user_df[user_df['ID_Posting_Parent'].notnull()])

        user_context = {
            'user_id': int(user_id),
            'user_name': user_df['UserCommunityName'].iloc[0],
            'user_gender': user_df['UserGender'].iloc[0],
            'user_created_at': user_df['UserCreatedAt'].iloc[0].isoformat(),
            'total_comments': total_comments,
            'total_replies': total_replies,
            'articles': {}
        }

        for article_id, article_comments in user_df.groupby('ID_Article'):
            article_id = int(article_id)
            article_thread = self.thread_manager.get_article_threads(article_id)

            if article_thread:
                user_context['articles'][article_id] = {
                    'article_title': article_thread['article_title'],
                    'article_publish_date': article_thread['article_publish_date'],
                    'user_comments_count': len(article_comments),
                    'user_replies_count': len(article_comments[article_comments['ID_Posting_Parent'].notnull()]),
                    'threads': [
                        self.find_thread_for_comment(article_thread['comment_threads'], int(comment['ID_Posting']))
                        for _, comment in article_comments.iterrows()]
                }

        return user_context

    def find_thread_for_comment(self, threads: List[Dict], comment_id: int) -> Optional[Dict]:
        for thread in threads:
            if thread['id'] == comment_id:
                return thread
            result = self.find_thread_for_comment(thread['replies'], comment_id)
            if result:
                return thread
        return None

    def cutoff_after_last_interaction(self, user_context: Dict, user_id: int) -> Tuple[Dict, int]:
        removed_comments = 0

        def process_thread(thread: Dict, last_interaction_time: Optional[str]) -> Tuple[
            Optional[Dict], int, Optional[str]]:
            nonlocal removed_comments
            if thread['user_id'] == user_id:
                last_interaction_time = thread['comment_created_at']

            if last_interaction_time and thread['comment_created_at'] > last_interaction_time:
                removed_comments += 1
                return None, removed_comments, last_interaction_time

            new_replies = []
            for reply in thread['replies']:
                processed_reply, removed_comments, last_interaction_time = process_thread(reply, last_interaction_time)
                if processed_reply:
                    new_replies.append(processed_reply)

            thread['replies'] = new_replies
            return thread, removed_comments, last_interaction_time

        for article_id in user_context['articles']:
            new_threads = []
            last_interaction_time = None
            for thread in user_context['articles'][article_id]['threads']:
                processed_thread, removed_comments, last_interaction_time = process_thread(thread,
                                                                                           last_interaction_time)
                if processed_thread:
                    new_threads.append(processed_thread)
            user_context['articles'][article_id]['threads'] = new_threads

        return user_context, removed_comments

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens_lst = encoding.encode(text)
        return len(tokens_lst)

    def escape_markdown(self, text: str) -> str:
        """Escape Markdown syntax in the given text."""
        # Escape characters that have special meaning in Markdown
        escape_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in escape_chars:
            text = text.replace(char, '\\' + char)

        # Replace backticks with single quotes
        text = text.replace('`', "'")

        return text

    def format_comment_thread(self, comment: Dict) -> str:
        root = ET.Element("comment_thread")
        self.add_comment_to_xml(root, comment)
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def add_comment_to_xml(self, parent: ET.Element, comment: Dict):
        comment_elem = ET.SubElement(parent, "comment")
        author_elem = ET.SubElement(comment_elem, "author")
        author_elem.text = self.escape_markdown(comment['user_name'])
        content_elem = ET.SubElement(comment_elem, "content")
        content_elem.text = self.escape_markdown(comment['comment_text'])
        if comment['replies']:
            replies_elem = ET.SubElement(comment_elem, "replies")
            for reply in comment['replies']:
                self.add_comment_to_xml(replies_elem, reply)

    def generate_formatted_user_context(self, user_id: int) -> str:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}"

        output = []

        # User Context
        output.append("# User Context\n")
        output.append(f"- **User ID:** {user_context['user_id']}\n")
        output.append(f"- **Username:** {self.escape_markdown(user_context['user_name'])}\n")
        output.append(f"- **Gender:** {self.escape_markdown(user_context['user_gender'])}\n")
        output.append(f"- **Created At:** {user_context['user_created_at']}\n")
        output.append(f"- **Total Comments:** {user_context['total_comments']}\n")
        output.append(f"- **Total Replies:** {user_context['total_replies']}\n")
        output.append("\n---\n\n")

        for article_id, article_data in user_context['articles'].items():
            # Article Context
            output.append("# Article Context\n")
            output.append(f"- **Article ID:** {article_id}\n")
            output.append(f"- **Article Title:** {self.escape_markdown(article_data['article_title'])}\n")
            output.append(f"- **Article Publish Date:** {article_data['article_publish_date']}\n")
            output.append(f"- **User Comments Count:** {article_data['user_comments_count']}\n")
            output.append(f"- **User Replies Count:** {article_data['user_replies_count']}\n")
            output.append("\n---\n\n")

            # Comment Threads
            output.append("# Comment Threads\n\n")
            for i, thread in enumerate(article_data['threads'], 1):
                output.append(f"## Thread {i}\n\n")
                output.append(self.format_comment_thread(thread))
                output.append("\n---\n\n")

        output.append("# End of Context")
        return "".join(output)

    def generate_user_report_with_cutoff(self, user_id: int) -> Tuple[str, int, int]:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}", 0, 0

        user_context, removed_comments = self.cutoff_after_last_interaction(user_context, user_id)

        report = self.generate_formatted_user_context(user_id)
        token_count = self.count_tokens(report)

        return report, token_count, removed_comments


import json
import os

# Main execution
if __name__ == "__main__":
    preprocessed_file = "../data/preprocessed/preprocessed_data.pkl"

    if not os.path.exists(preprocessed_file):
        print("Preprocessed data not found. Preprocessing...")
        preprocessor = DataPreprocessor('../data/raw_csv/Postings_01052019_31052019.csv')
        preprocessor.process()
        preprocessor.save_preprocessed_data(preprocessed_file)
    else:
        print("Loading preprocessed data...")
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)

    thread_manager = CommentThreadManager(preprocessor.df)
    user_context_sphere = UserContextSphere(preprocessor.df, thread_manager)

    # Create the spheres directories if they don't exist
    spheres_dir_no_cutoff = "spheres/no_cutoff"
    spheres_dir_cutoff = "spheres/cutoff"
    os.makedirs(spheres_dir_no_cutoff, exist_ok=True)
    os.makedirs(spheres_dir_cutoff, exist_ok=True)

    user_id = 675862  # Replace with the desired user ID

    # Generate and save context without cutoff
    user_context_sphere = UserContextSphere(preprocessor.df, thread_manager)
    formatted_context = user_context_sphere.generate_formatted_user_context(user_id)

    if formatted_context != f"No data found for user ID {user_id}":
        filename_no_cutoff = f"{spheres_dir_no_cutoff}/{user_id}.md"
        with open(filename_no_cutoff, 'w', encoding='utf-8') as f:
            f.write(formatted_context)
        print(f"User context without cutoff saved to {filename_no_cutoff}")

        # Generate and save context with cutoff
        report, token_count, removed_comments = user_context_sphere.generate_user_report_with_cutoff(user_id)

        filename_cutoff = f"{spheres_dir_cutoff}/{user_id}.md"
        with open(filename_cutoff, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"User context with cutoff saved to {filename_cutoff}")

        print(f"Token count: {token_count}")
        print(f"Removed comments: {removed_comments}")
    else:
        error_message = f"# Error\n\nNo data found for user ID {user_id}"

        # Save error message to both directories
        for dir_path in [spheres_dir_no_cutoff, spheres_dir_cutoff]:
            filename = f"{dir_path}/{user_id}_error.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(error_message)
            print(f"Error message saved to {filename}")
```

## `preprocessing/Versions-pre-processing/build_context_sphere-v6.py`

```
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import tiktoken
from typing import Dict, List, Optional, Tuple
import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from html import escape  # Fügen Sie diesen Import hinzu

class DataPreprocessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def process(self):
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    def save_preprocessed_data(self, output_path: str):
        with open(output_path, 'wb') as f:
            pickle.dump(self.df, f)
        print(f"Preprocessed data saved to {output_path}")

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor


class CommentThreadManager:
    def __init__(self, df: pd.DataFrame):
        self.article_comments = {article_id: group for article_id, group in df.groupby('ID_Article')}

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int, depth: int = 0) -> List[Dict]:
        replies = comments[comments['ID_Posting_Parent'] == parent_id]
        return [{
            'id': int(reply['ID_Posting']),
            'parent_id': int(reply['ID_Posting_Parent']) if pd.notnull(reply['ID_Posting_Parent']) else None,
            'user_id': int(reply['ID_CommunityIdentity']),
            'user_name': reply['UserCommunityName'],
            'user_gender': reply['UserGender'],
            'user_created_at': reply['UserCreatedAt'].isoformat() if pd.notnull(reply['UserCreatedAt']) else None,
            'comment_headline': reply['PostingHeadline'],
            'comment_text': reply['PostingComment'],
            'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(
                reply['PostingCreatedAt']) else None,
            'comment_length': int(reply['CommentLength']),
            'depth': depth,
            'replies': self.build_comment_thread(comments, int(reply['ID_Posting']), depth + 1)
        } for _, reply in replies.iterrows()]

    def get_article_threads(self, article_id: int) -> Optional[Dict]:
        if article_id not in self.article_comments:
            return None

        article_df = self.article_comments[article_id]
        root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]

        threads = self.build_comment_thread(article_df, 0)
        article_meta = article_df.iloc[0]

        return {
            'article_id': int(article_id),
            'article_title': article_meta['ArticleTitle'],
            'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(
                article_meta['ArticlePublishingDate']) else None,
            'article_channel': article_meta['ArticleChannel'],
            'article_ressort_name': article_meta['ArticleRessortName'],
            'total_comments': len(article_df),
            'root_comments': len(root_comments),
            'comment_threads': threads
        }

    def get_article_ids(self) -> List[int]:
        return list(self.article_comments.keys())


class UserContextSphere:
    def __init__(self, df: pd.DataFrame, thread_manager: CommentThreadManager):
        self.df = df
        self.thread_manager = thread_manager
        self.user_comments = {user_id: group for user_id, group in df.groupby('ID_CommunityIdentity')}

    def get_user_context(self, user_id: int) -> Optional[Dict]:
        if user_id not in self.user_comments:
            return None

        user_df = self.user_comments[user_id]
        total_comments = len(user_df)
        total_replies = len(user_df[user_df['ID_Posting_Parent'].notnull()])

        user_context = {
            'user_id': int(user_id),
            'user_name': user_df['UserCommunityName'].iloc[0],
            'user_gender': user_df['UserGender'].iloc[0],
            'user_created_at': user_df['UserCreatedAt'].iloc[0].isoformat(),
            'total_comments': total_comments,
            'total_replies': total_replies,
            'articles': {}
        }

        for article_id, article_comments in user_df.groupby('ID_Article'):
            article_id = int(article_id)
            article_thread = self.thread_manager.get_article_threads(article_id)

            if article_thread:
                user_context['articles'][article_id] = {
                    'article_title': article_thread['article_title'],
                    'article_publish_date': article_thread['article_publish_date'],
                    'user_comments_count': len(article_comments),
                    'user_replies_count': len(article_comments[article_comments['ID_Posting_Parent'].notnull()]),
                    'threads': [
                        self.find_thread_for_comment(article_thread['comment_threads'], int(comment['ID_Posting']))
                        for _, comment in article_comments.iterrows()]
                }

        return user_context

    def find_thread_for_comment(self, threads: List[Dict], comment_id: int) -> Optional[Dict]:
        for thread in threads:
            if thread['id'] == comment_id:
                return thread
            result = self.find_thread_for_comment(thread['replies'], comment_id)
            if result:
                return thread
        return None

    def cutoff_after_last_interaction(self, user_context: Dict, user_id: int) -> Tuple[Dict, int]:
        removed_comments = 0

        def process_thread(thread: Dict, last_interaction_time: Optional[str]) -> Tuple[
            Optional[Dict], int, Optional[str]]:
            nonlocal removed_comments
            if thread['user_id'] == user_id:
                last_interaction_time = thread['comment_created_at']

            if last_interaction_time and thread['comment_created_at'] > last_interaction_time:
                removed_comments += 1
                return None, removed_comments, last_interaction_time

            new_replies = []
            for reply in thread['replies']:
                processed_reply, removed_comments, last_interaction_time = process_thread(reply, last_interaction_time)
                if processed_reply:
                    new_replies.append(processed_reply)

            thread['replies'] = new_replies
            return thread, removed_comments, last_interaction_time

        for article_id in user_context['articles']:
            new_threads = []
            last_interaction_time = None
            for thread in user_context['articles'][article_id]['threads']:
                processed_thread, removed_comments, last_interaction_time = process_thread(thread,
                                                                                           last_interaction_time)
                if processed_thread:
                    new_threads.append(processed_thread)
            user_context['articles'][article_id]['threads'] = new_threads

        return user_context, removed_comments

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens_lst = encoding.encode(text)
        return len(tokens_lst)

    def escape_markdown(self, text: str) -> str:
        """Escape Markdown syntax in the given text."""
        # Escape characters that have special meaning in Markdown
        escape_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in escape_chars:
            text = text.replace(char, '\\' + char)

        # Replace backticks with single quotes
        text = text.replace('`', "'")

        return text

    def format_comment_thread(self, comment: Dict) -> str:
        root = ET.Element("comment_thread")
        self.add_comment_to_xml(root, comment)
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def add_comment_to_xml(self, parent: ET.Element, comment: Dict):
        comment_elem = ET.SubElement(parent, "comment")
        author_elem = ET.SubElement(comment_elem, "author")
        author_elem.text = self.escape_markdown(comment['user_name'])
        content_elem = ET.SubElement(comment_elem, "content")
        content_elem.text = self.escape_markdown(comment['comment_text'])
        if comment['replies']:
            replies_elem = ET.SubElement(comment_elem, "replies")
            for reply in comment['replies']:
                self.add_comment_to_xml(replies_elem, reply)

    def generate_formatted_user_context(self, user_id: int) -> str:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}"

        output = []

        # User Context
        output.append("# User Context\n")
        output.append(f"- **User ID:** {user_context['user_id']}\n")
        output.append(f"- **Username:** {self.escape_markdown(user_context['user_name'])}\n")
        output.append(f"- **Gender:** {self.escape_markdown(user_context['user_gender'])}\n")
        output.append(f"- **Created At:** {user_context['user_created_at']}\n")
        output.append(f"- **Total Comments:** {user_context['total_comments']}\n")
        output.append(f"- **Total Replies:** {user_context['total_replies']}\n")
        output.append("\n---\n\n")

        for article_id, article_data in user_context['articles'].items():
            # Article Context
            output.append("# Article Context\n")
            output.append(f"- **Article ID:** {article_id}\n")
            output.append(f"- **Article Title:** {self.escape_markdown(article_data['article_title'])}\n")
            output.append(f"- **Article Publish Date:** {article_data['article_publish_date']}\n")
            output.append(f"- **User Comments Count:** {article_data['user_comments_count']}\n")
            output.append(f"- **User Replies Count:** {article_data['user_replies_count']}\n")
            output.append("\n---\n\n")

            # Comment Threads
            output.append("# Comment Threads\n\n")
            for i, thread in enumerate(article_data['threads'], 1):
                output.append(f"## Thread {i}\n\n")
                output.append(self.format_comment_thread(thread))
                output.append("\n---\n\n")

        output.append("# End of Context")
        return "".join(output)

    def generate_user_report_with_cutoff(self, user_id: int) -> Tuple[str, int, int]:
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}", 0, 0

        user_context, removed_comments = self.cutoff_after_last_interaction(user_context, user_id)

        report = self.generate_formatted_user_context(user_id)
        token_count = self.count_tokens(report)

        return report, token_count, removed_comments


import json
import os

# Main execution
if __name__ == "__main__":
    preprocessed_file = "../../data/preprocessed/preprocessed_data.pkl"

    if not os.path.exists(preprocessed_file):
        print("Preprocessed data not found. Preprocessing...")
        preprocessor = DataPreprocessor('../../data/raw_csv/Postings_01052019_31052019.csv')
        preprocessor.process()
        preprocessor.save_preprocessed_data(preprocessed_file)
    else:
        print("Loading preprocessed data...")
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)

    thread_manager = CommentThreadManager(preprocessor.df)
    user_context_sphere = UserContextSphere(preprocessor.df, thread_manager)

    # Create the spheres directories if they don't exist
    spheres_dir_no_cutoff = "no_cutoff"
    spheres_dir_cutoff = "cutoff"
    os.makedirs(spheres_dir_no_cutoff, exist_ok=True)
    os.makedirs(spheres_dir_cutoff, exist_ok=True)

    user_id = 675862  # Replace with the desired user ID

    # Generate and save context without cutoff
    user_context_sphere = UserContextSphere(preprocessor.df, thread_manager)
    formatted_context = user_context_sphere.generate_formatted_user_context(user_id)

    if formatted_context != f"No data found for user ID {user_id}":
        filename_no_cutoff = f"{spheres_dir_no_cutoff}/{user_id}.md"
        with open(filename_no_cutoff, 'w', encoding='utf-8') as f:
            f.write(formatted_context)
        print(f"User context without cutoff saved to {filename_no_cutoff}")

        # Generate and save context with cutoff
        report, token_count, removed_comments = user_context_sphere.generate_user_report_with_cutoff(user_id)

        filename_cutoff = f"{spheres_dir_cutoff}/{user_id}.md"
        with open(filename_cutoff, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"User context with cutoff saved to {filename_cutoff}")

        print(f"Token count: {token_count}")
        print(f"Removed comments: {removed_comments}")
    else:
        error_message = f"# Error\n\nNo data found for user ID {user_id}"

        # Save error message to both directories
        for dir_path in [spheres_dir_no_cutoff, spheres_dir_cutoff]:
            filename = f"{dir_path}/{user_id}_error.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(error_message)
            print(f"Error message saved to {filename}")
```

## `preprocessing/Versions-pre-processing/build_base_with_filter_json.py`

```
# NOTE: Das funktioniert nicht, da die struktur im sample npsäter nicht aussreicht um ealle beteiligten im thread abzubilden

# full_thread_sampling.py
from typing import Dict

import pandas as pd
import numpy as np
import json
import os
from build_base_json import DataPreprocessor, CommentThreadManager  # Assuming the base script is named base_script.py

def load_full_tree_json(full_tree_path: str) -> Dict:
    """
    Load the full comment threads from a JSON file if it exists.

    Args:
        full_tree_path (str): The path to the full tree JSON data.

    Returns:
        Dict: The loaded JSON data as a dictionary.
    """
    if os.path.exists(full_tree_path):
        print(f"Loading full tree JSON from {full_tree_path}")
        with open(full_tree_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None

def save_full_tree_json(df: pd.DataFrame, full_tree_path: str):
    """
    Save the full comment threads to a JSON file.

    Args:
        df (pd.DataFrame): The preprocessed data.
        full_tree_path (str): The path where the full tree JSON data will be saved.
    """
    print("Creating full tree JSON...")
    thread_manager = CommentThreadManager(df)
    articles_with_threads = thread_manager.get_article_threads()

    with open(full_tree_path, 'w', encoding='utf-8') as f:
        json.dump(articles_with_threads, f, indent=2)
    print(f"Full tree JSON saved to {full_tree_path}")

def sample_users_from_full_tree(full_tree_data: Dict, num_users: int) -> Dict:
    """
    Sample a specified number of users from the full tree data.

    Args:
        full_tree_data (Dict): The full tree data loaded from JSON.
        num_users (int): Number of users to sample.

    Returns:
        Dict: A dictionary containing only the sampled users' threads.
    """
    # Extract all unique user IDs from the full tree data
    all_users = set()
    for article in full_tree_data.values():
        for thread in article['comment_threads']:
            all_users.add(thread['user_id'])
            for reply in thread['replies']:
                all_users.add(reply['user_id'])

    # Sample user IDs
    sampled_users = np.random.choice(list(all_users), size=min(num_users, len(all_users)), replace=False)

    # Filter threads to include only sampled users
    def filter_threads(threads):
        return [
            thread for thread in threads
            if thread['user_id'] in sampled_users or any(reply['user_id'] in sampled_users for reply in thread['replies'])
        ]

    sampled_data = {}
    for article_id, article in full_tree_data.items():
        sampled_data[article_id] = {
            **article,
            'comment_threads': filter_threads(article['comment_threads'])
        }

    return sampled_data

def save_sampled_json(sampled_data: Dict, output_path: str):
    """
    Save the sampled data to a JSON file.

    Args:
        sampled_data (Dict): The sampled data.
        output_path (str): The path where the JSON data will be saved.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sampled_data, f, indent=2)
    print(f"Sampled data saved to {output_path}")

def main():
    print("Checkmark 0")
    preprocessed_file = r"../../data/preprocessed/preprocessed_data.pkl"
    full_tree_path = "../spheres/articles_with_threads_full_tree.json"

    if not os.path.exists(preprocessed_file):
        raise FileNotFoundError("Preprocessed data not found. Please run the base script first.")
    print("Checkmark 1")
    # Load or create the full tree JSON
    full_tree_data = load_full_tree_json(full_tree_path)
    if full_tree_data is None:
        print("rebuild full JSON tree")
        # Load preprocessed data to create the full tree JSON
        preprocessor = DataPreprocessor.load_preprocessed_data(preprocessed_file)
        df = preprocessor.df
        save_full_tree_json(df, full_tree_path)
        full_tree_data = load_full_tree_json(full_tree_path)
    print("Checkmark 2")
    # Define parameters for sampling
    num_users = 1

    # Sample users from the full tree data
    sampled_data = sample_users_from_full_tree(full_tree_data, num_users)

    # Save the sampled data to JSON
    output_path = f"spheres/sampled_articles_with_threads_{num_users}.json"
    save_sampled_json(sampled_data, output_path)

if __name__ == "__main__":
    print("executemain")
    main()
```

## `preprocessing/Versions-pre-processing/old-preprocessing appraoch 26_09_2024/helper_functions.py`

```
import pickle

def get_all_user_ids(pkl_file_path: str) -> list:
    """
    Load a .pkl file and query for all user IDs.

    Args:
        pkl_file_path (str): The path to the .pkl file.

    Returns:
        list: A list of all user IDs.
    """
    with open(pkl_file_path, 'rb') as f:
        df = pickle.load(f)

    user_ids = df['ID_CommunityIdentity'].tolist()
    return user_ids
```

## `preprocessing/Versions-pre-processing/old-preprocessing appraoch 26_09_2024/main_single_user.py`

```
import a_build_user_json_v7
import b_build_user_context
from helper_functions import get_all_user_ids


path_article_full_tree = 'spheres/JSON/articles_with_threads_full_tree.json'
user_id = 49126



a_build_user_json_v7.main(path_article_full_tree, user_id)



input_path = f'spheres/JSON/user_{user_id}_threads.json'
full_output_path = f'spheres/MD/user_{user_id}_threads_full.md'
modified_output_path = f'spheres/MD/user_{user_id}_threads_cleaned.md'
b_build_user_context.main(input_path, full_output_path, modified_output_path, user_id=user_id)
```

## `preprocessing/Versions-pre-processing/old-preprocessing appraoch 26_09_2024/b_build_user_context.py`

```
import json
from xml.dom import minidom
from xml.sax.saxutils import escape

def escape_text(value):
    """
    Converts the value to a string and escapes XML special characters.
    """
    return escape(str(value)) if value is not None else ''

def json_to_xml(json_data):
    """
    Converts JSON data to XML DOM object.
    """
    doc = minidom.Document()
    root = doc.createElement("articles")
    doc.appendChild(root)

    for article_id, article_data in json_data.items():
        article_elem = doc.createElement("article")
        article_elem.setAttribute("id", str(article_id))
        root.appendChild(article_elem)

        for key in ['article_title', 'article_publish_date', 'article_channel', 'article_ressort_name']:
            elem = doc.createElement(key.replace('article_', ''))
            elem.appendChild(doc.createTextNode(escape_text(article_data.get(key, ''))))
            article_elem.appendChild(elem)

        for key in ['total_comments', 'root_comments']:
            elem = doc.createElement(key)
            elem.appendChild(doc.createTextNode(str(article_data.get(key, ''))))
            article_elem.appendChild(elem)

        user_threads_elem = doc.createElement("user_threads")
        article_elem.appendChild(user_threads_elem)

        for thread in article_data['user_threads']:
            thread_elem = doc.createElement("thread")
            thread_elem.setAttribute("id", str(thread['id']))
            user_threads_elem.appendChild(thread_elem)

            for key in ['user_name', 'user_gender', 'user_created_at', 'comment_headline', 'comment_text', 'comment_created_at']:
                if key in thread:
                    elem = doc.createElement(key)
                    elem.appendChild(doc.createTextNode(escape_text(thread[key])))
                    thread_elem.appendChild(elem)

            elem = doc.createElement("comment_length")
            elem.appendChild(doc.createTextNode(str(thread['comment_length'])))
            thread_elem.appendChild(elem)

            replies_elem = doc.createElement("replies")
            thread_elem.appendChild(replies_elem)

            for reply in thread.get('replies', []):
                reply_elem = doc.createElement("reply")
                reply_elem.setAttribute("id", str(reply['id']))
                replies_elem.appendChild(reply_elem)

                for key in ['user_id', 'user_name', 'user_gender', 'user_created_at', 'comment_headline', 'comment_text', 'comment_created_at']:
                    if key in reply:
                        elem = doc.createElement(key)
                        elem.appendChild(doc.createTextNode(escape_text(reply[key])))
                        reply_elem.appendChild(elem)

                elem = doc.createElement("comment_length")
                elem.appendChild(doc.createTextNode(str(reply['comment_length'])))
                reply_elem.appendChild(elem)

    return doc

def generate_full_markdown(json_data, target_user_id):
    """
    Generates a full Markdown string from the given JSON data.
    """
    output = []

    # Find the user information for the target user_id
    user_name = None
    for article_data in json_data.values():
        for thread in article_data['user_threads']:
            if str(thread.get('user_id')) == str(target_user_id):
                user_name = thread['user_name']
                break
        if user_name:
            break

    if not user_name:
        print(f"Warning: Could not find user_name for user_id {target_user_id}")
        user_name = f"Unknown (ID: {target_user_id})"

    output.append(f"# User: {user_name} (ID: {target_user_id})\n\n")
    output.append("This document contains the thread data for the above user across multiple articles.\n\n")
    output.append("---\n\n")

    for article_id, article_data in json_data.items():
        output.append(f"## Article ID: {article_id}\n")
        output.append(f"- **Title:** {escape_text(article_data['article_title'])}\n")
        output.append(f"- **Publish Date:** {article_data['article_publish_date']}\n")
        output.append(f"- **Channel:** {escape_text(article_data['article_channel'])}\n")
        output.append(f"- **Ressort Name:** {escape_text(article_data['article_ressort_name'])}\n")
        output.append(f"- **Total Comments:** {article_data['total_comments']}\n")
        output.append(f"- **Root Comments:** {article_data['root_comments']}\n")
        output.append("\n---\n\n")

        xml_doc = json_to_xml({article_id: article_data})
        xml_content = xml_doc.toprettyxml(indent="  ")
        xml_content = '\n'.join([line for line in xml_content.split('\n') if line.strip()])
        output.append("```xml\n")
        output.append(xml_content)
        output.append("\n```\n")

    return "".join(output)

def json_to_modified_xml(json_data):
    """
    Converts JSON data to a simplified XML DOM object with selected information.
    """
    doc = minidom.Document()
    root = doc.createElement("articles")
    doc.appendChild(root)

    for article_id, article_data in json_data.items():
        article_elem = doc.createElement("article")
        article_elem.setAttribute("id", str(article_id))
        root.appendChild(article_elem)

        user_threads_elem = doc.createElement("user_threads")
        article_elem.appendChild(user_threads_elem)

        for thread in article_data['user_threads']:
            thread_elem = doc.createElement("thread")
            thread_elem.setAttribute("id", str(thread['id']))
            user_threads_elem.appendChild(thread_elem)

            for key in ['user_name', 'comment_headline', 'comment_text', 'comment_created_at']:
                simple_key = 'cmnd_' + key.split('_')[-1] if key.startswith('comment_') else key
                if key in thread:
                    elem = doc.createElement(simple_key)
                    elem.appendChild(doc.createTextNode(escape_text(thread[key])))
                    thread_elem.appendChild(elem)

            elem = doc.createElement("cmnd_length")
            elem.appendChild(doc.createTextNode(str(thread['comment_length'])))
            thread_elem.appendChild(elem)

            replies_elem = doc.createElement("replies")
            thread_elem.appendChild(replies_elem)

            for reply in thread.get('replies', []):
                reply_elem = doc.createElement("reply")
                reply_elem.setAttribute("id", str(reply['id']))
                replies_elem.appendChild(reply_elem)

                for key in ['user_name', 'comment_headline', 'comment_text', 'comment_created_at']:
                    simple_key = 'cmnd_' + key.split('_')[-1] if key.startswith('comment_') else key
                    if key in reply:
                        elem = doc.createElement(simple_key)
                        elem.appendChild(doc.createTextNode(escape_text(reply[key])))
                        reply_elem.appendChild(elem)

                elem = doc.createElement("cmnd_length")
                elem.appendChild(doc.createTextNode(str(reply['comment_length'])))
                reply_elem.appendChild(elem)

    return doc

def generate_modified_markdown(json_data, target_user_id):
    """
    Generates a modified Markdown string from the given JSON data.
    """
    output = []

    # Find the user information for the target user_id
    user_name = None
    for article_data in json_data.values():
        for thread in article_data['user_threads']:
            if str(thread.get('user_id')) == str(target_user_id):
                user_name = thread['user_name']
                break
        if user_name:
            break

    if not user_name:
        print(f"Warning: Could not find user_name for user_id {target_user_id}")
        user_name = f"Unknown (ID: {target_user_id})"

    output.append(f"# User: {user_name} (ID: {target_user_id})\n\n")
    output.append("This document contains the thread data for the above user across multiple articles.\n\n")
    output.append("---\n\n")

    for article_id, article_data in json_data.items():
        output.append(f"## Article ID: {article_id}\n")
        output.append(f"- **Title:** {escape_text(article_data['article_title'])}\n")
        output.append(f"- **Publish Date:** {article_data['article_publish_date']}\n")
        output.append(f"- **Channel:** {escape_text(article_data['article_channel'])}\n")
        output.append(f"- **Ressort Name:** {escape_text(article_data['article_ressort_name'])}\n")
        output.append(f"- **Total Comments:** {article_data['total_comments']}\n")
        output.append(f"- **Root Comments:** {article_data['root_comments']}\n")
        output.append("\n---\n\n")

        xml_doc = json_to_modified_xml({article_id: article_data})
        xml_content = xml_doc.toprettyxml(indent="  ")
        xml_content = '\n'.join([line for line in xml_content.split('\n') if line.strip()])
        output.append("```xml\n")
        output.append(xml_content)
        output.append("\n```\n")

    return "".join(output)

def main(input_path, full_output_path, modified_output_path, user_id):
    """
    Main function to read JSON from input_path, generate Markdown, and write to output paths.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    full_markdown_content = generate_full_markdown(json_data, target_user_id=user_id)
    modified_markdown_content = generate_modified_markdown(json_data, target_user_id=user_id)

    with open(full_output_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown_content)

    with open(modified_output_path, 'w', encoding='utf-8') as f:
        f.write(modified_markdown_content)
"""
if __name__ == "__main__":
    user_id = 49126
    input_path = f'spheres/JSON/user_{user_id}_threads.json'
    full_output_path = f'spheres/MD/user_{user_id}_threads_full.md'
    modified_output_path = f'spheres/MD/user_{user_id}_threads_cleaned.md'
    main(input_path, full_output_path, modified_output_path, user_id)
"""

```

## `preprocessing/Versions-pre-processing/old-preprocessing appraoch 26_09_2024/main_pipeline.py`

```
import a_build_user_json_v7
import b_build_user_context
from helper_functions import get_all_user_ids
import concurrent.futures
import json
import os
import random
import tiktoken
import os
from datetime import datetime

# Am Anfang der Datei, fügen Sie diese Konstanten hinzu:
OUTPUT_BASE_DIR = 'samples'
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
PROGRESS_FILE = 'progress.json'
CHUNK_SIZE = 22
TOKEN_LOWER_BOUND = 500  # Minimum number of tokens
TOKEN_UPPER_BOUND = 2000   # Maximum number of tokens
DESIRED_SAMPLE_SIZE = 100
MAX_WORKERS = 8  # oder eine andere Zahl, die für Ihr System geeignet ist
FAILED_USERS_FILE = 'failed_users.json'

def load_failed_users():
    if os.path.exists(FAILED_USERS_FILE):
        with open(FAILED_USERS_FILE, 'r') as file:
            return set(json.load(file))
    return set()

def save_failed_users(failed_user_ids):
    with open(FAILED_USERS_FILE, 'w') as file:
        json.dump(list(failed_user_ids), file)

def create_output_directory():
    """Create a directory for the current sample run."""
    dir_name = f"{TIMESTAMP}_tokens_{TOKEN_LOWER_BOUND}_{TOKEN_UPPER_BOUND}_samples_{DESIRED_SAMPLE_SIZE}"
    full_path = os.path.join(OUTPUT_BASE_DIR, dir_name)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def create_full_output_directory(base_dir):
    full_dir = os.path.join(base_dir, 'full')
    os.makedirs(full_dir, exist_ok=True)
    return full_dir

def create_cleaned_output_directory(base_dir):
    cleaned_dir = os.path.join(base_dir, 'cleaned')
    os.makedirs(cleaned_dir, exist_ok=True)
    return cleaned_dir

def load_progress():
    """Load the progress from a JSON file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            return set(json.load(file))
    return set()

def clear_progress():
    """Clear the contents of the progress file."""
    with open(PROGRESS_FILE, 'w') as file:
        json.dump([], file)
    print(f"The progress has been cleared in {PROGRESS_FILE}.")

def save_progress(processed_user_ids):
    """Save the progress to a JSON file."""
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(list(processed_user_ids), file)

def count_tokens(text):
    """Count the number of tokens in the given text using tiktoken."""
    encoder = tiktoken.get_encoding("cl100k_base")  # Using the gpt2 model encoding as an example
    tokens = encoder.encode(text)
    return len(tokens)

def validate_output(input_path):
    """Check if the cleaned .md output meets token criteria and print details if rejected."""
    if os.path.exists(input_path):
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
            token_count = count_tokens(content)
            if TOKEN_LOWER_BOUND <= token_count <= TOKEN_UPPER_BOUND:
                return True
            else:
                print(f"File {input_path} has {token_count} tokens and was rejected.")
    return False

def process_user_data(user_id, path_article_full_tree, full_output_dir, cleaned_output_dir):
    """Process data for a single user."""
    json_path = f'spheres/JSON/user_{user_id}_threads.json'

    a_build_user_json_v7.main(path_article_full_tree, user_id)

    full_output_path = os.path.join(full_output_dir, f'user_{user_id}_threads_full.md')
    cleaned_output_path = os.path.join(cleaned_output_dir, f'user_{user_id}_threads_cleaned.md')
    b_build_user_context.main(json_path, full_output_path, cleaned_output_path, user_id)

    # Check if the cleaned .md meets the token criteria
    if not validate_output(cleaned_output_path):
        # If criteria not met, delete both .md files and the JSON file
        os.remove(full_output_path)
        os.remove(cleaned_output_path)
        os.remove(json_path)
        return False

    # After processing, delete the JSON file
    os.remove(json_path)

    return True

def main():
    """Main function to process user data."""
    base_output_dir = create_output_directory()
    full_output_dir = create_full_output_directory(base_output_dir)
    cleaned_output_dir = create_cleaned_output_directory(base_output_dir)

    path_article_full_tree = 'spheres/articles_with_threads_channel_inland.json'
    user_ids = get_all_user_ids("../data/preprocessed/preprocessed_data.pkl")
    processed_user_ids = load_progress()
    failed_user_ids = load_failed_users()
    user_ids_to_process = [user_id for user_id in user_ids if user_id not in processed_user_ids and user_id not in failed_user_ids]
    random.shuffle(user_ids_to_process)

    samples_saved = 0

    while samples_saved < DESIRED_SAMPLE_SIZE and user_ids_to_process:
        chunk = user_ids_to_process[:CHUNK_SIZE]
        user_ids_to_process = user_ids_to_process[CHUNK_SIZE:]

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(process_user_data, user_id, path_article_full_tree, full_output_dir, cleaned_output_dir): user_id for user_id in chunk}
            for future in concurrent.futures.as_completed(futures):
                user_id = futures[future]
                if future.result():
                    processed_user_ids.add(user_id)
                    samples_saved += 1
                    print(f"Sample saved: {samples_saved}/{DESIRED_SAMPLE_SIZE}")
                else:
                    failed_user_ids.add(user_id)
                if samples_saved >= DESIRED_SAMPLE_SIZE:
                    break

        save_progress(processed_user_ids)
        save_failed_users(failed_user_ids)

    clear_progress()
    # Optional: Möchten Sie auch die fehlgeschlagenen User zurücksetzen?
    os.remove(FAILED_USERS_FILE)

if __name__ == "__main__":
    main()
```

## `preprocessing/Versions-pre-processing/old-preprocessing appraoch 26_09_2024/count_list.py`

```
list_progress = [692224, 499726, 630799, 688156, 133153, 174116, 673831, 542766, 679989, 133175, 196669, 63550, 20552, 61520, 499793, 170067, 587862, 505942, 692312, 505945, 512097, 41062, 682089, 499820, 692342, 51320, 653437, 571524, 227468, 534691, 125092, 223407, 692404, 84149, 98495, 573636, 635076, 55498, 655569, 166103, 600283, 155869, 51425, 557282, 676067, 671974, 499944, 669933, 557303, 577784, 227578, 671995, 540924, 502011, 692479, 160001, 131334, 590087, 205063, 688393, 508172, 192783, 499994, 688412, 233762, 676131, 530727, 219439, 676147, 244020, 577860, 635206, 188754, 512341, 637272, 586078, 160100, 586086, 514407, 581995, 514413, 20847, 569717, 557434, 586124, 248209, 690593, 111010, 670115, 561575, 332203, 606647, 57783, 135627, 170445, 45524, 522716, 500191, 549343, 188895, 629225, 692724, 203265, 555524, 530949, 23048, 676360, 567820, 561688, 88605, 29217, 51746, 690726, 561708, 209454, 608815, 16943, 631354, 639548, 94788, 535111, 686666, 109133, 205391, 680531, 682580, 500315, 500324, 512614, 606823, 189032, 518761, 559719, 115313, 211573, 629369, 168570, 330370, 51848, 94859, 182924, 563854, 80529, 189074, 653971, 537252, 29362, 631477, 86710, 21180, 602824, 629450, 606924, 588494, 228053, 94936, 578267, 226018, 637667, 504549, 672489, 688877, 6900, 66293, 514814, 604940, 201487, 121617, 176914, 561942, 49945, 797, 500521, 633643, 545580, 76596, 566069, 64311, 76600, 637760, 13120, 185157, 107338, 652108, 170829, 52048, 684887, 691036, 637789, 99165, 562019, 551789, 676719, 525169, 119666, 652152, 689020, 539522, 582531, 605061, 525193, 584592, 152470, 607127, 603034, 31645, 588704, 72611, 234406, 5031, 500647, 547768, 607160, 607165, 666563, 535493, 23514, 46048, 87009, 576482, 25580, 605165, 164853, 513014, 300023, 533505, 144385, 685067, 95263, 588836, 508964, 582698, 674865, 527413, 126010, 691261, 676934, 46162, 607317, 572502, 574550, 183392, 85089, 513124, 525415, 210024, 160873, 691306, 97387, 177260, 689274, 580731, 130179, 568460, 13455, 533647, 203924, 640148, 527510, 507039, 568490, 564402, 105651, 7350, 574650, 564412, 533703, 539852, 120014, 527570, 31954, 574677, 74968, 552156, 543973, 607464, 185580, 128236, 691439, 105714, 589047, 558329, 570618, 550143, 652552, 554255, 666900, 220439, 179502, 101681, 630089, 533835, 566606, 537942, 183638, 320859, 25948, 683359, 189794, 537955, 527715, 56682, 138609, 560507, 679293, 691583, 667010, 570755, 175494, 572806, 152968, 3481, 239017, 630187, 32173, 247220, 75189, 144823, 517563, 687560, 187853, 630224, 603608, 669150, 179687, 654825, 552427, 224749, 243184, 112116, 521718, 632311, 534008, 636425, 687628, 85518, 106004, 50710, 214554, 36397, 685619, 534069, 681528, 5693, 245310, 669254, 220748, 165453, 503372, 652879, 161365, 220759, 575064, 542297, 163415, 667229, 681567, 554592, 581215, 499300, 562788, 556648, 509546, 499308, 687733, 652928, 237188, 585349, 534149, 233095, 200336, 231057, 552604, 589473, 681634, 655016, 46764, 632494, 34482, 638643, 190144, 685760, 638660, 100041, 16074, 583371, 91850, 75471, 573144, 106203, 233191, 5872, 681719, 30457, 689914, 38650, 513788, 507649, 694019, 108291, 233227, 677647, 499471, 671507, 108309, 241432, 603936, 321316, 687908, 30507, 587567, 48945, 220986, 243516, 10058, 94033, 178006, 130907, 687969, 235385, 540551, 556944, 522135, 522138, 634783, 75691, 499631, 556977, 589748, 206774, 235455, 690119, 604103, 675788, 561106, 540632, 563161, 20447, 679916, 686065, 499700, 686070, 235514]

print(len(list_progress))
```

## `preprocessing/Versions-pre-processing/old-preprocessing appraoch 26_09_2024/a_build_user_json_v7.py`

```
import json
import os

def load_json(file_path):
    """
    Load the JSON file containing articles and comments.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_articles_with_user_comments(articles, user_id):
    """
    Find all articles where the user has written a comment.

    Args:
        articles (dict): The dictionary containing articles and comments.
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary of articles where the user has written a comment.
    """
    user_articles = {}
    for article_id, article_data in articles.items():
        for thread in article_data['comment_threads']:
            if user_has_comment_in_thread(thread, user_id):
                user_articles[article_id] = article_data
                break
    return user_articles

def user_has_comment_in_thread(thread, user_id):
    """
    Check if the user has a comment in the given thread or its replies.

    Args:
        thread (dict): The thread to check.
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user has a comment in the thread, False otherwise.
    """
    if thread['user_id'] == user_id:
        return True
    for reply in thread['replies']:
        if user_has_comment_in_thread(reply, user_id):
            return True
    return False

def find_user_threads_in_articles(articles, user_id):
    """
    Find all threads in the given articles where the user has written a comment.

    Args:
        articles (dict): The dictionary containing articles and comments.
        user_id (int): The ID of the user.

    Returns:
        dict: A dictionary of articles with threads where the user has written a comment.
    """
    user_articles = {}
    for article_id, article_data in articles.items():
        user_threads = []
        for thread in article_data['comment_threads']:
            filtered_thread = filter_thread_for_user(thread, user_id)
            if filtered_thread:
                user_threads.append(filtered_thread)

        if user_threads:
            user_articles[article_id] = {
                'article_id': article_data['article_id'],
                'article_title': article_data['article_title'],
                'article_publish_date': article_data['article_publish_date'],
                'article_channel': article_data['article_channel'],
                'article_ressort_name': article_data['article_ressort_name'],
                'total_comments': article_data['total_comments'],
                'root_comments': article_data['root_comments'],
                'user_threads': user_threads
            }

    return user_articles

def filter_thread_for_user(thread, user_id):
    """
    Filter the thread to include only the parts where the user has written a comment.

    Args:
        thread (dict): The thread to filter.
        user_id (int): The ID of the user.

    Returns:
        dict: The filtered thread, or None if the user has not written a comment in the thread.
    """
    if thread['user_id'] == user_id:
        filtered_replies = [filter_thread_for_user(reply, user_id) for reply in thread['replies']]
        filtered_replies = [reply for reply in filtered_replies if reply]
        filtered_thread = thread.copy()
        filtered_thread['replies'] = filtered_replies
        return filtered_thread
    else:
        filtered_replies = [filter_thread_for_user(reply, user_id) for reply in thread['replies']]
        filtered_replies = [reply for reply in filtered_replies if reply]
        if filtered_replies:
            filtered_thread = thread.copy()
            filtered_thread['replies'] = filtered_replies
            return filtered_thread
    return None

def save_json(data, file_path):
    """
    Save the data to a JSON file.

    Args:
        data (dict): The data to save.
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {file_path}")

def main(path_articles_full_tree, user_id, ):
    articles_with_threads = load_json(path_articles_full_tree)

    # Schritt 1: Finde alle Artikel, in denen der Benutzer einen Kommentar geschrieben hat
    user_articles = find_articles_with_user_comments(articles_with_threads, user_id)
    print(f"Artikel, in denen der Benutzer {user_id} einen Kommentar geschrieben hat:")
    #print(json.dumps(user_articles, indent=2))

    # Schritt 2: Finde alle Threads in diesen Artikeln, in denen der Benutzer aktiv war
    user_threads_in_articles = find_user_threads_in_articles(user_articles, user_id)
    print(f"Threads, in denen der Benutzer {user_id} aktiv war:")
    #print(json.dumps(user_threads_in_articles, indent=2))

    # Speichern der Ergebnisse in einer JSON-Datei
    output_dir = 'spheres/JSON'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'user_{user_id}_threads.json')
    save_json(user_threads_in_articles, output_file)
    print("Success")
```

## `preprocessing/Versions-pre-processing/Old-v5/build_context_sphere.py`

```
import pandas as pd
import pickle
import tiktoken
from typing import Dict, List, Tuple
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
from data_preprocessor import DataPreprocessor
import copy
import logging
import json



class CommentThreadManager:
    """
    A class for managing comment threads associated with articles.

    This class provides functionality to build and retrieve comment threads
    for articles, maintaining the hierarchical structure of comments and replies.

    Attributes:
        article_comments (dict): A dictionary mapping article IDs to their respective comments.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the CommentThreadManager with a DataFrame of comments.

        Args:
            df (pd.DataFrame): A DataFrame containing comment data for multiple articles.
        """
        self.article_comments = {article_id: group for article_id, group in df.groupby('ID_Article')}

    def build_comment_thread(self, comments: pd.DataFrame, parent_id: int, depth: int = 0) -> List[Dict]:
        """
        Recursively build a comment thread starting from a given parent comment.

        Args:
            comments (pd.DataFrame): A DataFrame containing all comments for an article.
            parent_id (int): The ID of the parent comment to start building the thread from.
            depth (int, optional): The current depth of the comment in the thread hierarchy. Defaults to 0.

        Returns:
            List[Dict]: A list of dictionaries representing the comment thread, with each dictionary
                        containing comment details and a list of replies.
        """
        replies_grouped = comments.groupby('ID_Posting_Parent')

        def build_thread(pid: int, current_depth: int) -> List[Dict]:
            if pid not in replies_grouped.groups:
                return []

            return [{
                'id': int(reply['ID_Posting']),
                'parent_id': int(reply['ID_Posting_Parent']) if pd.notnull(reply['ID_Posting_Parent']) else None,
                'user_id': int(reply['ID_CommunityIdentity']),
                'user_name': reply['UserCommunityName'],
                'user_gender': reply['UserGender'],
                'user_created_at': reply['UserCreatedAt'].isoformat() if pd.notnull(reply['UserCreatedAt']) else None,
                'comment_headline': reply['PostingHeadline'],
                'comment_text': reply['PostingComment'],
                'comment_created_at': reply['PostingCreatedAt'].isoformat() if pd.notnull(reply['PostingCreatedAt']) else None,
                'comment_length': int(reply['CommentLength']),
                'depth': current_depth,
                'replies': build_thread(int(reply['ID_Posting']), current_depth + 1)
            } for _, reply in replies_grouped.get_group(pid).iterrows()]

        return build_thread(parent_id, depth)

    def get_article_threads(self, article_id: int) -> Dict:
        """
        Retrieve the comment threads for a specific article.

        Args:
            article_id (int): The ID of the article to retrieve comment threads for.

        Returns:
            Dict: A dictionary containing article metadata and its comment threads.
                  Returns None if the article ID is not found.

        The returned dictionary includes:
        - Article metadata (ID, title, publish date, channel, ressort name)
        - Total number of comments and root comments
        - A list of comment threads
        """
        if article_id not in self.article_comments:
            return None

        article_df = self.article_comments[article_id]
        root_comments = article_df[article_df['ID_Posting_Parent'].isnull() | (article_df['ID_Posting_Parent'] == 0)]

        threads = self.build_comment_thread(article_df, 0)
        article_meta = article_df.iloc[0]

        return {
            'article_id': int(article_id),
            'article_title': article_meta['ArticleTitle'],
            'article_publish_date': article_meta['ArticlePublishingDate'].isoformat() if pd.notnull(article_meta['ArticlePublishingDate']) else None,
            'article_channel': article_meta['ArticleChannel'],
            'article_ressort_name': article_meta['ArticleRessortName'],
            'total_comments': len(article_df),
            'root_comments': len(root_comments),
            'comment_threads': threads
        }


class UserContextSphere:
    """
    A class for managing and analyzing user context within comment threads.

    This class provides functionality to retrieve user-specific context information,
    including their comments and interactions across multiple articles. It also
    generates formatted reports of user activity.

    Attributes:
        df (pd.DataFrame): The DataFrame containing all comment data.
        thread_manager (CommentThreadManager): An instance of CommentThreadManager for retrieving article threads.
        user_comments (defaultdict): A dictionary mapping user IDs to their comments.
    """

    def __init__(self, df: pd.DataFrame, thread_manager: CommentThreadManager):
        """
        Initialize the UserContextSphere with comment data and a thread manager.

        Args:
            df (pd.DataFrame): The DataFrame containing all comment data.
            thread_manager (CommentThreadManager): An instance of CommentThreadManager for retrieving article threads.
        """
        self.df = df
        self.thread_manager = thread_manager
        self.user_comments = defaultdict(list)
        self._populate_user_comments()

    def _populate_user_comments(self):
        """
        Populate the user_comments dictionary with comments grouped by user ID.
        """
        for _, row in self.df.iterrows():
            self.user_comments[row['ID_CommunityIdentity']].append(row)

    def get_user_context(self, user_id: int) -> Dict:
        """
        Retrieve the context information for a specific user.

        Args:
            user_id (int): The ID of the user to retrieve context for.

        Returns:
            Dict: A dictionary containing user context information, including user details
                  and their interactions across articles. Returns None if the user is not found.
        """
        if user_id not in self.user_comments:
            return None

        user_df = pd.DataFrame(self.user_comments[user_id])
        total_interactions = len(user_df)

        user_context = {
            'user_id': int(user_id),
            'user_name': user_df['UserCommunityName'].iloc[0],
            'user_gender': user_df['UserGender'].iloc[0],
            'user_created_at': user_df['UserCreatedAt'].iloc[0].isoformat(),
            'total_interactions': total_interactions,
            'articles': {}
        }

        for article_id, article_comments in user_df.groupby('ID_Article'):
            article_id = int(article_id)
            article_thread = self.thread_manager.get_article_threads(article_id)

            if article_thread:
                user_context['articles'][article_id] = {
                    'article_title': article_thread['article_title'],
                    'article_publish_date': article_thread['article_publish_date'],
                    'threads': [self.find_thread_for_comment(article_thread['comment_threads'], int(comment['ID_Posting']))
                                for _, comment in article_comments.iterrows()]
                }

        return user_context

    def find_thread_for_comment(self, threads: List[Dict], comment_id: int) -> Dict:
        """
        Find the thread containing a specific comment.

        Args:
            threads (List[Dict]): A list of comment threads to search.
            comment_id (int): The ID of the comment to find.

        Returns:
            Dict: The thread containing the specified comment, or None if not found.
        """
        for thread in threads:
            if thread['id'] == comment_id:
                return thread
            result = self.find_thread_for_comment(thread['replies'], comment_id)
            if result:
                return thread
        return None


    def escape_markdown(self, text: str) -> str:
        """
        Escape special characters in text for Markdown formatting.

        Args:
            text (str): The text to escape.

        Returns:
            str: The input text with special Markdown characters escaped.
        """
        escape_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in escape_chars:
            text = text.replace(char, '\\' + char)
        return text.replace('`', "'")

    def format_comment_thread(self, comment: Dict) -> str:
        """
        Format a comment thread as an XML string.

        Args:
            comment (Dict): The root comment of the thread to format.

        Returns:
            str: A formatted XML string representing the comment thread.
        """
        root = ET.Element("comment_thread")
        self.add_comment_to_xml(root, comment)
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
        return pretty_xml

    def add_comment_to_xml(self, parent: ET.Element, comment: Dict):
        """
        Add a comment and its replies to an XML element.

        Args:
            parent (ET.Element): The parent XML element to add the comment to.
            comment (Dict): The comment data to add to the XML.
        """
        comment_elem = ET.SubElement(parent, "comment")
        author_elem = ET.SubElement(comment_elem, "author")
        author_elem.text = self.escape_markdown(comment['user_name'])
        content_elem = ET.SubElement(comment_elem, "content")
        content_elem.text = self.escape_markdown(comment['comment_text'])
        if comment['replies']:
            replies_elem = ET.SubElement(comment_elem, "replies")
            for reply in comment['replies']:
                self.add_comment_to_xml(replies_elem, reply)

    def generate_formatted_user_context(self, user_id: int) -> str:
        """
        Generate a formatted Markdown report of a user's context.

        Args:
            user_id (int): The ID of the user to generate the report for.

        Returns:
            str: A formatted Markdown string containing the user's context information.
        """
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}"

        output = []

        output.append("# User Context\n")
        output.append(f"- **User ID:** {user_context['user_id']}\n")
        output.append(f"- **Username:** {self.escape_markdown(user_context['user_name'])}\n")
        output.append(f"- **Gender:** {self.escape_markdown(user_context['user_gender'])}\n")
        output.append(f"- **Created At:** {user_context['user_created_at']}\n")
        output.append(f"- **Total Interactions:** {user_context['total_interactions']}\n")
        output.append("\n---\n\n")

        for article_data in user_context['articles'].values():
            output.append("# Article Context\n")
            output.append(f"- **Article Title:** {self.escape_markdown(article_data['article_title'])}\n")
            output.append(f"- **Article Publish Date:** {article_data['article_publish_date']}\n")
            output.append("\n---\n\n")

            output.append("# Comment Threads\n\n")
            for i, thread in enumerate(article_data['threads'], 1):
                output.append(f"## Thread {i}\n\n")
                output.append(self.format_comment_thread(thread))
                output.append("\n---\n\n")

        output.append("# End of Context")
        return "".join(output)

    def generate_user_report_with_cutoff(self, user_id: int, debug: bool = False) -> Tuple[str, int, int]:
        """
        Generate a user report with a cutoff applied to limit the context.

        Args:
            user_id (int): The ID of the user to generate the report for.
            debug (bool): If True, print debug information.

        Returns:
            Tuple[str, int, int]: A tuple containing the formatted report, token count,
                                  and the number of removed comments.
        """
        user_context = self.get_user_context(user_id)
        if not user_context:
            return f"No data found for user ID {user_id}", 0, 0

        original_context = copy.deepcopy(user_context)
        user_context, removed_comments = CutoffManager.cutoff_after_last_interaction(user_context, user_id, debug)

        if not CutoffManager.validate_cutoff(original_context, user_context, user_id, debug):
            logging.error(f"Cutoff validation failed for user ID {user_id}")
            if debug:
                print("Original context:")
                print(json.dumps(original_context, indent=2))
                print("\nCutoff context:")
                print(json.dumps(user_context, indent=2))
            raise ValueError("Cutoff validation failed")

        report = self.generate_formatted_user_context(user_id)
        encoding = tiktoken.get_encoding("cl100k_base")
        token_count = len(encoding.encode(report))

        return report, token_count, removed_comments

class CutoffManager:
    """
    A class for managing the cutoff of user context data based on the user's last interaction.
    """

    @staticmethod
    def cutoff_after_last_interaction(user_context: Dict, user_id: int, debug: bool = False) -> Tuple[Dict, int]:
        """
        Cuts off the user context after the last interaction of the specified user.

        Args:
            user_context (Dict): The original user context.
            user_id (int): The ID of the user whose last interaction is used as the cutoff point.
            debug (bool): If True, print debug information.

        Returns:
            Tuple[Dict, int]: A tuple containing the modified user context and the number of removed comments.
        """
        removed_comments = 0
        last_interaction_time = None

        def process_thread(thread: Dict) -> Tuple[Dict, int]:
            nonlocal removed_comments, last_interaction_time
            if thread is None or 'comment_created_at' not in thread:
                return None, 1

            thread_time = pd.to_datetime(thread['comment_created_at'])
            if thread['user_id'] == user_id:
                if last_interaction_time is None or thread_time > last_interaction_time:
                    last_interaction_time = thread_time
                    if debug:
                        print(f"Updated last interaction time: {last_interaction_time}")

            if last_interaction_time and thread_time > last_interaction_time:
                return None, 1

            new_replies = []
            for reply in thread.get('replies', []):
                processed_reply, removed_count = process_thread(reply)
                removed_comments += removed_count
                if processed_reply:
                    new_replies.append(processed_reply)

            thread['replies'] = new_replies
            return thread, 0

        for article_id in list(user_context['articles'].keys()):
            new_threads = []
            for thread in user_context['articles'][article_id]['threads']:
                processed_thread, _ = process_thread(thread)
                if processed_thread:
                    new_threads.append(processed_thread)
                else:
                    removed_comments += 1

            user_context['articles'][article_id]['threads'] = new_threads
            if not new_threads:
                del user_context['articles'][article_id]

        if debug:
            print(f"Last interaction time: {last_interaction_time}")
            print(f"Removed comments: {removed_comments}")

        return user_context, removed_comments

    @staticmethod
    def validate_cutoff(original_context: Dict, cutoff_context: Dict, user_id: int, debug: bool = False) -> bool:
        """
        Validates the cutoff operation by comparing the original and cutoff contexts.

        Args:
            original_context (Dict): The original user context before cutoff.
            cutoff_context (Dict): The user context after cutoff.
            user_id (int): The ID of the user whose interactions are being validated.
            debug (bool): If True, print debug information.

        Returns:
            bool: True if the cutoff is valid, False otherwise.
        """
        def get_last_interaction_time(context: Dict) -> pd.Timestamp:
            last_time = None
            for article in context['articles'].values():
                for thread in article['threads']:
                    if thread['user_id'] == user_id:
                        thread_time = pd.to_datetime(thread['comment_created_at'])
                        if last_time is None or thread_time > last_time:
                            last_time = thread_time
            return last_time

        original_last_time = get_last_interaction_time(original_context)
        cutoff_last_time = get_last_interaction_time(cutoff_context)

        if debug:
            print(f"Original last interaction time: {original_last_time}")
            print(f"Cutoff last interaction time: {cutoff_last_time}")

        if original_last_time != cutoff_last_time:
            if debug:
                print("Last interaction times do not match")
            return False

        original_comment_count = 0
        cutoff_comment_count = 0

        for article_id, article in original_context['articles'].items():
            for thread in article['threads']:
                original_comment_count += 1
                thread_time = pd.to_datetime(thread['comment_created_at'])
                if thread_time <= original_last_time:
                    if article_id not in cutoff_context['articles'] or \
                            thread not in cutoff_context['articles'][article_id]['threads']:
                        if debug:
                            print(f"Missing comment in cutoff context: {thread['id']}")
                        return False

        for article_id, article in cutoff_context['articles'].items():
            for thread in article['threads']:
                cutoff_comment_count += 1
                if pd.to_datetime(thread['comment_created_at']) > original_last_time:
                    if debug:
                        print(f"Comment after last interaction time found in cutoff context: {thread['id']}")
                    return False

        if cutoff_comment_count > original_comment_count:
            if debug:
                print(f"Cutoff comment count ({cutoff_comment_count}) is greater than original comment count ({original_comment_count})")
            return False

        return True


if __name__ == "__main__":
    import os
    import pickle
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # File paths
    preprocessed_file = "../../../data/preprocessed/preprocessed_data.pkl"
    spheres_dir_no_cutoff = "../no_cutoff"
    spheres_dir_cutoff = "../cutoff"

    # Create directories if they don't exist
    os.makedirs(spheres_dir_no_cutoff, exist_ok=True)
    os.makedirs(spheres_dir_cutoff, exist_ok=True)

    # Load preprocessed data
    if not os.path.exists(preprocessed_file):
        logging.error(f"Preprocessed data file not found: {preprocessed_file}")
        exit(1)

    logging.info("Loading preprocessed data...")
    with open(preprocessed_file, 'rb') as f:
        df = pickle.load(f)

    # Create instances
    thread_manager = CommentThreadManager(df)
    user_context_sphere = UserContextSphere(df, thread_manager)

    # List of user IDs to process
    user_ids = [675862, 12610, 499935]  # Add more user IDs as needed

    # Debug mode flag
    debug_mode = True

    # Process each user
    for user_id in user_ids:
        logging.info(f"Processing user ID: {user_id}")

        # Generate context without cutoff
        formatted_context = user_context_sphere.generate_formatted_user_context(user_id)
        if formatted_context != f"No data found for user ID {user_id}":
            filename_no_cutoff = f"{spheres_dir_no_cutoff}/{user_id}.md"
            with open(filename_no_cutoff, 'w', encoding='utf-8') as f:
                f.write(formatted_context)
            logging.info(f"User context without cutoff saved to {filename_no_cutoff}")

            # Generate context with cutoff
            try:
                report, token_count, removed_comments = user_context_sphere.generate_user_report_with_cutoff(user_id, debug=debug_mode)

                filename_cutoff = f"{spheres_dir_cutoff}/{user_id}.md"
                with open(filename_cutoff, 'w', encoding='utf-8') as f:
                    f.write(report)
                logging.info(f"User context with cutoff saved to {filename_cutoff}")
                logging.info(f"Token count: {token_count}")
                logging.info(f"Removed comments: {removed_comments}")

            except ValueError as e:
                logging.error(f"Error processing user {user_id} with cutoff: {str(e)}")
                error_filename = f"{spheres_dir_cutoff}/{user_id}_error.md"
                with open(error_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Error\n\n{str(e)}")
                logging.info(f"Error message saved to {error_filename}")

        else:
            logging.warning(f"No data found for user ID {user_id}")
            for dir_path in [spheres_dir_no_cutoff, spheres_dir_cutoff]:
                error_filename = f"{dir_path}/{user_id}_error.md"
                with open(error_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Error\n\nNo data found for user ID {user_id}")
                logging.info(f"Error message saved to {error_filename}")

    logging.info("Processing completed.")


```

## `preprocessing/Versions-pre-processing/Old-v5/data_preprocessor.py`

```
import pandas as pd
import pickle

class DataPreprocessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def process(self):
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor

```
