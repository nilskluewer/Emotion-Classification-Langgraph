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