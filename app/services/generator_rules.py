import random
from typing import List, Dict
from app.models.schemas import StoryRequest, StoryStructure

class RuleBasedGenerator:
    """
    Step 1 of the pipeline: Generates the 'skeleton' of the story without AI.
    This ensures we don't ask the LLM to 'invent' grammar or teaching goals,
    saving tokens and ensuring quality/consistency.
    """

    # Mock vocabulary database - in production this would be a proper DB or larger JSON
    VOCAB_DB = {
        "daily life": {
            "A1": ["wake up", "breakfast", "bus", "work", "sleep", "eat"],
            "A2": ["commute", "prepare", "schedule", "grocery", "relax"],
            "B1": ["routine", "organized", "unexpected", "manage", "exhausted"]
        }
    }

    # Mock grammar curriculum
    GRAMMAR_CURRICULUM = {
        "A1": ["Present Simple", "Present Continuous"],
        "A2": ["Past Simple", "Future Simple (will)"],
        "B1": ["Present Perfect", "Past Continuous"]
    }

    def generate_structure(self, request: StoryRequest) -> StoryStructure:
        """
        Deterministically (or semi-randomly) creates the prompt constraints.
        """
        level = request.level
        topic = request.topic.lower()

        # 1. Select Vocabulary
        # Fallback to general words if topic not found
        available_vocab = self.VOCAB_DB.get(topic, {}).get(level, ["thing", "do", "go", "good"])
        selected_vocab = random.sample(available_vocab, k=min(3, len(available_vocab)))

        # 2. Select Grammar Focus
        available_grammar = self.GRAMMAR_CURRICULUM.get(level, ["Present Simple"])
        grammar_focus = random.choice(available_grammar)

        # 3. Define Constraints based on specific grammar
        target_forms = []
        if grammar_focus == "Present Simple":
            target_forms = [f"I {v}" for v in selected_vocab] # Simplified example
        elif grammar_focus == "Past Simple":
            target_forms = [f"I {v}ed" for v in selected_vocab] # Very naive, just for structure demo

        # 4. Length rules
        length_map = {"A1": 80, "A2": 120, "B1": 180}
        
        return StoryStructure(
            topic=request.topic,
            target_forms=target_forms,  # These will be refined forms like "ran", "ate" later
            target_vocabulary=selected_vocab,
            length_guideline=length_map.get(level, 100),
            grammar_focus=grammar_focus
        )
