from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class StoryRequest(BaseModel):
    topic: str = Field(..., description="Topic of the story (e.g., 'daily life')")
    level: str = Field("A1", description="CEFR level (A1, A2, B1)")
    language: str = Field("en", description="Target language code")

class StoryStructure(BaseModel):
    """Step 1: Generated entirely by rules, NO AI"""
    topic: str
    target_forms: List[str] = Field(..., description="List of grammar forms to include (e.g. ['run', 'ran'])")
    target_vocabulary: List[str] = Field(..., description="Key vocabulary words to use")
    length_guideline: int = Field(..., description="Approximate word count")
    grammar_focus: str = Field(..., description="Main grammar point (e.g. 'Past Simple')")

class GeneratedStory(BaseModel):
    """Final output"""
    title: str
    content: str
    audio_url: Optional[str] = None
    structure: StoryStructure
