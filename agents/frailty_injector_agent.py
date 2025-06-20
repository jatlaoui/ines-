# agents/frailty_injector_agent.py
import logging
from typing import Dict, Any, Optional
from .base_agent import BaseAgent

logger = logging.getLogger("FrailtyInjectorAgent")

class AuthenticFrailtyInjectorAgent(BaseAgent):
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id, name="المُنكسِر (حاقن الضعف)",
            description="يضيف لمسة من الصدق الإنساني عن طريق محاكاة النقص والتردد."
        )

    async def humanize_text(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        text = context.get("text_content")
        if not text: raise ValueError("محتوى النص مطلوب.")
        
        logger.info("Humanizing text by injecting authentic frailty...")
        
        # محاكاة بسيطة: إضافة وقفة أو جملة بسيطة
        sentences = text.split('.')
        if len(sentences) > 1:
            insertion_point = len(sentences) // 2
            frailty_phrases = ["... صمت للحظة.", "... وبدا التردد في صوته.", "... لم يجد الكلمات المناسبة."]
            sentences.insert(insertion_point, random.choice(frailty_phrases))
            modified_text = ". ".join(s.strip() for s in sentences if s) + "."
        else:
            modified_text = text

        return {
            "content": {"original_text": text, "humanized_text": modified_text},
            "summary": "تمت إضافة لمسة من الواقعية الإنسانية."
        }
