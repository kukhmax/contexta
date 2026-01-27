import os
from openai import AsyncOpenAI
from app.models.schemas import StoryStructure

class LLMService:
    def __init__(self):
        # We use OpenAI client which is compatible with DeepSeek URL
        self.api_key = os.getenv("LLM_API_KEY", "sk-mock-key")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
        self.model = os.getenv("LLM_MODEL", "deepseek-chat")
        
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def generate_story_text(self, structure: StoryStructure) -> str:
        """
        Step 2: Generate the story text based on strict constraints.
        Using a cheap model (DeepSeek-V3 or similar).
        """
        system_prompt = """You are a helpful language teacher. 
Your task is to write a SHORT, SIMPLE story based EXACTLY on the provided constraints.
Do NOT use complex vocabulary unless requested.
Do NOT exceed the word count significantly.
Wrap the story in nothing. Just return the text."""

        user_prompt = f"""
Topic: {structure.topic}
Target Vocabulary to use: {', '.join(structure.target_vocabulary)}
Grammar Focus: {structure.grammar_focus}
Forms to include: {', '.join(structure.target_forms) if structure.target_forms else "Appropriate forms for the grammar"}
Approximate Word Count: {structure.length_guideline}

Write the story now.
"""
        
        # Mock mode if no real key provided (for testing effectively freely)
        if self.api_key == "sk-mock-key":
            return f"[MOCK STORY about {structure.topic} using {structure.grammar_focus}. Vocab: {structure.target_vocabulary}]"

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "Error generating story. Please try again."
