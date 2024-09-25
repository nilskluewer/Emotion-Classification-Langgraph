from pydantic import BaseModel, Field
from typing import Annotated, List

class EmotionalAspect(BaseModel):
    """Represents a single thought-classification pair for an emotional aspect."""
    thought: Annotated[
        str,
        Field(description="Provide a detailed thought process for analyzing the emotional aspect.")
    ]
    classification: Annotated[
        str,
        Field(description="Classify the emotional aspect based on the thought process, referencing contextual and theoretical insights.")
    ]
    score: Annotated[
        float,
        Field(description="Score from 0 to 1, low to high", ge=0, le=1)
    ]

class EmotionValence(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for emotion valence.")
    ]

class EmotionIntensity(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for analyzing the intensity of the emotion expressed.")
    ]

class ContextualRelevance(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for evaluating the relevance of the emotion in the given context.")
    ]

class EngagementLevel(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for assessing the level of engagement or involvement of the commenter.")
    ]

class EmotionRegulation(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification of emotion regulation strategies by the user.")
    ]

class Polarization(BaseModel):
    components: Annotated[
        List[EmotionalAspect],
        Field(description="Thought and classification for assessing polarization in emotional expressions, considering how extreme or divisive the emotions might be.")
    ]

class ClassificationOutput(BaseModel):
    """Aggregates all emotional aspect classes into a comprehensive schema."""
    emotion_valence: EmotionValence
    emotion_intensity: EmotionIntensity
    contextual_relevance: ContextualRelevance
    engagement_level: EngagementLevel
    emotion_regulation: EmotionRegulation
    polarization: Polarization