import spacy
from typing import List, Dict, Any, Tuple
from app.models.schemas import WordForm

class NLPService:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # Автоматическая загрузка, если нет модели
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def process_story(self, text: str, constraints: Dict) -> Tuple[str, List[WordForm]]:
        """
        Шаг 3: NLP обработка.
        1. Находит глаголы (или целевые слова).
        2. Оборачивает их в HTML <mark> для подсветки.
        3. Собирает список форм для обучения.
        """
        doc = self.nlp(text)
        
        forms = []
        highlighted_text = text
        
        # Находим глаголы, совпадающие с нашими target_vocab
        # Для простоты MVP - просто ищем леммы
        target_lemmas = [w.lower() for w in constraints['vocab']]
        
        # Собираем спаны для замены (обратный порядок, чтобы не сбить индексы)
        spans_to_highlight = []
        
        for token in doc:
            if token.lemma_.lower() in target_lemmas or token.pos_ == "VERB": # Подсвечиваем все глаголы для наглядности MVP
                spans_to_highlight.append((token.idx, token.idx + len(token.text), token))
                
                # Добавляем в список форм
                forms.append(WordForm(
                    form=token.text,
                    base=token.lemma_,
                    tense=constraints['grammar'], # Упрощение для MVP
                    translation="..." # Тут нужен переводчик, пока заглушка
                ))

        # Оборачиваем в HTML (идем с конца)
        spans_to_highlight.sort(key=lambda x: x[0], reverse=True)
        # Убираем дубликаты/пересечения (просто)
        last_start = float('inf')
        
        final_text = list(text)
        
        unique_forms = []
        seen_forms = set()
        
        for start, end, token in spans_to_highlight:
            if end <= last_start:
                # Вставляем теги
                replacement = f"<mark>{text[start:end]}</mark>"
                final_text[start:end] = list(replacement)
                last_start = start
                
                # Сохраняем форму, если новая
                if token.lemma_ not in seen_forms:
                    unique_forms.append(WordForm(
                        form=token.text,
                        base=token.lemma_,
                        tense=constraints['grammar'],
                        translation="[перевод]" 
                    ))
                    seen_forms.add(token.lemma_)

        return "".join(final_text), unique_forms[:5] # Вернем топ-5 слов
