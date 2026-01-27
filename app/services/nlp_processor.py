import spacy
from typing import List, Dict, Any
from app.models.schemas import StoryStructure

class NLPService:
    def __init__(self):
        # Load small English model (already installed in Step 1)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spacy model...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def process_text(self, text: str, structure: StoryStructure) -> Dict[str, Any]:
        """
        Step 3: Highlight targets without asking AI.
        Returns the text with metadata about where target words are found.
        """
        doc = self.nlp(text)
        
        highlights = []
        
        # 1. Find target vocabulary (lemmatized search)
        target_lemmas = [t.lower() for t in structure.target_vocabulary]
        
        for token in doc:
            # Check overlap with target vocab
            if token.lemma_.lower() in target_lemmas or token.text.lower() in target_lemmas:
                highlights.append({
                    "word": token.text,
                    "type": "vocabulary",
                    "start": token.idx,
                    "end": token.idx + len(token.text),
                    "explanation": f"Target word: {token.lemma_}"
                })
        
        # 2. Find specific grammar forms (Rule-based approximation)
        # Verify if the requested forms actually appeared
        # This is a simple implementation; full grammar detection is complex
        # Here we just look for the exact strings or simple variations if provided in targets
        if structure.target_forms:
             for form in structure.target_forms:
                # Naive string search for the exact form in the text
                start_index = text.lower().find(form.lower())
                if start_index != -1:
                     highlights.append({
                        "word": text[start_index : start_index + len(form)],
                        "type": "grammar",
                        "start": start_index,
                        "end": start_index + len(form),
                        "explanation": f"Grammar pattern: {structure.grammar_focus}"
                    })

        return {
            "original_text": text,
            "processed_html": self._create_highlighted_html(text, highlights),
            "highlights": highlights
        }

    def _create_highlighted_html(self, text: str, highlights: List[Dict]) -> str:
        """
        Simple helper to wrap text in <span> tags for frontend rendering.
        Note: Overlapping highlights need handling, but for MVP we assume minimal overlap.
        """
        if not highlights:
            return text
            
        # Sort by start position reversed to replace from end without messing up indices
        highlights.sort(key=lambda x: x["start"], reverse=True)
        
        processed = list(text)
        for h in highlights:
            start = h["start"]
            end = h["end"]
            cls = "highlight-vocab" if h["type"] == "vocabulary" else "highlight-grammar"
            
            # Very basic check to avoid messing up if something already changed?
            # Actually easier to rebuild string from list
            replacement = f'<span class="{cls}" title="{h["explanation"]}">{text[start:end]}</span>'
            processed[start:end] = list(replacement)
            
        return "".join(processed)
