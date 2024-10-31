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

class HolisticEmotionAnalysis(BaseModel):
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