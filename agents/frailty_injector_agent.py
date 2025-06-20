# agents/frailty_injector_agent.py
"""
AuthenticFrailtyInjectorAgent (وكيل حقن الضعف الأصيل)
يقوم بإضافة لمسات من "النقص" الإنساني الواقعي على النصوص.
"""
import logging
import random
from typing import Dict, Any, Optional

from .base_agent import BaseAgent

logger = logging.getLogger("FrailtyInjectorAgent")

class AuthenticFrailtyInjectorAgent(BaseAgent):
    """
    وكيل متخصص في "إعادة أنسنة" النصوص عبر إضافة لمسات من الضعف الواقعي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="المُنكسِر (حاقن الضعف)",
            description="يضيف لمسة من الصدق الإنساني عن طريق محاكاة النقص والتردد."
        )
        self.frailty_techniques = {
            "hesitation": self._inject_hesitation,
            "simplification": self._inject_simplification,
            "interruption": self._inject_interruption
        }
        logger.info("AuthenticFrailtyInjectorAgent initialized.")

    async def humanize_text(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ نصًا ويعيد صياغته بلمسة من الضعف الإنساني.
        """
        text_content = context.get("text_content")
        if not text_content:
            raise ValueError("محتوى النص مطلوب لعملية الأنسنة.")
        
        character_mood = context.get("character_mood", "neutral") # حزين, متردد, غاضب
        
        logger.info(f"Humanizing text with character mood: {character_mood}...")

        # تطبيق تقنيات مختلفة
        modified_text = self._inject_hesitation(text_content, character_mood)
        modified_text = self._inject_simplification(modified_text, character_mood)
        modified_text = self._inject_interruption(modified_text, character_mood)
        
        return {
            "content": {
                "original_text": text_content,
                "humanized_text": modified_text
            },
            "summary": "تمت إضافة لمسات من التردد والبساطة لجعل النص أكثر واقعية."
        }
        
    def _inject_hesitation(self, text: str, mood: str) -> str:
        """إضافة التردد أو الوقفات في الحوار."""
        if mood not in ["متردد", "حزين"]:
            return text
            
        # استبدال جمل مباشرة بأخرى مترددة
        replacements = {
            "أنا أحبك.": "أنا... لا أعرف كيف أقولها، لكن... أحبك.",
            "يجب أن نذهب.": "أعتقد... ربما يجب أن... نذهب الآن؟",
            "فعلت ذلك.": "لا أعرف لماذا، لكن... نعم، فعلت ذلك."
        }
        for original, hesitant in replacements.items():
            if original in text:
                text = text.replace(original, hesitant)
                break # تطبيق تغيير واحد فقط لكل مرة
        return text

    def _inject_simplification(self, text: str, mood: str) -> str:
        """استبدال تشبيه بليغ بآخر أبسط وأكثر صدقًا."""
        if mood not in ["بسيط", "متعب"]:
            return text

        # البحث عن تشبيهات بليغة
        complex_metaphors = [
            "كانت عيناها كجمرتين متقدتين في ليل الصحراء",
            "صوته كان سيمفونية من الحكمة والقوة"
        ]
        
        for metaphor in complex_metaphors:
            if metaphor in text:
                # استبداله بتشبيه أبسط
                simple_replacement = "كانت عيناه... حزينتين."
                text = text.replace(metaphor, simple_replacement)
                break
        return text

    def _inject_interruption(self, text: str, mood: str) -> str:
        """إضافة مقاطعة أو جملة غير مكتملة."""
        if mood not in ["غاضب", "مضطرب"]:
            return text

        sentences = text.split('.')
        if len(sentences) > 2:
            # قطع الجملة قبل الأخيرة
            last_sentence = sentences[-2].strip()
            words = last_sentence.split()
            if len(words) > 5:
                interrupted_sentence = " ".join(words[:len(words)//2]) + "..."
                sentences[-2] = interrupted_sentence
                text = ". ".join(sentences)

        return text
