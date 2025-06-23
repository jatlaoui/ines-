# agents/dialect_authenticity_guardian_agent.py (V2 - Anti-Transliteration)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..engines.tunisian_culture_engine import tunisian_culture_engine

logger = logging.getLogger("DialectAuthenticityGuardianAgent")

class DialectAuthenticityGuardianAgent(BaseAgent):
    """
    حارس الأصالة اللهجية (V2).
    متخصص في اكتشاف التراكيب الفصيحة والترجمات الصوتية غير الأصيلة
    واقتراح بدائل عامية مناسبة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "dialect_authenticity_guardian",
            name="حارس الأصالة اللهجية",
            description="يراجع الحوارات ويقترح تعديلات لزيادة الأصالة اللهجية."
        )
        self.culture_engine = tunisian_culture_engine
        # [جديد] قائمة سوداء للترجمات الصوتية الشائعة التي يجب تجنبها
        self.transliteration_blacklist = ["بيك", "بوس", "كول", "نايس", "أوكي"]

    async def review_and_correct(self, context: Dict[str, Any]) -> Dict[str, Any]:
        text_content = context.get("text_content")
        dialect_id = context.get("dialect_id", "tunisois")
        character_profile = context.get("character_profile")

        if not text_content or not character_profile:
            return {"status": "error", "message": "Text content and character profile are required."}

        logger.info(f"Guardian V2: Reviewing text for '{dialect_id}' dialect and transliteration issues...")
        
        # [جديد] بناء prompt محسن
        prompt = self._build_review_prompt(text_content, dialect_id, character_profile)
        
        response = await llm_service.generate_json_response(prompt, temperature=0.1)

        if "error" in response:
            return {"status": "error", "message": "LLM call for dialect review failed.", "details": response}

        # يمكنك أيضًا إضافة فحص يدوي بسيط باستخدام القائمة السوداء هنا كطبقة حماية إضافية

        return {
            "status": "success",
            "content": {"review_report": response},
            "summary": "Dialect authenticity review complete."
        }

    def _build_review_prompt(self, text: str, dialect: str, profile: Dict) -> str:
        
        return f"""
مهمتك: أنت لغوي تونسي دقيق للغاية. مهمتك هي مراجعة الحوار التالي من منظورين: 1) التراكيب الفصيحة جدًا، 2) الترجمات الصوتية المباشرة (Transliteration) من لغات أخرى.

**اللهجة المستهدفة:** {dialect}
**ملف الشخصية المتحدثة:** {profile.get('description', 'شخصية عامة')}

**الحوار للمراجعة:**
---
{text}
---

**التعليمات:**
1.  اقرأ الحوار بعناية.
2.  **حدد أي جمل تبدو فصيحة بشكل غير طبيعي** لشخصية المتحدث.
3.  **حدد أي كلمات تبدو كترجمة صوتية مباشرة** من لغات أخرى (أمثلة شائعة لتجنبها: {', '.join(self.transliteration_blacklist)}).
4.  لكل تحديد، اقترح تعديلاً باللهجة التونسية الأصيلة يحافظ على المعنى.

أرجع ردك **حصريًا** بتنسيق JSON يحتوي على قائمة `corrections`. إذا كان النص أصيلاً، أرجع قائمة فارغة.
{{
  "corrections": [
    {{
      "original_phrase": "string // الكلمة أو الجملة التي تحتاج إلى تعديل.",
      "correction_type": "string // نوع الخطأ ('فصيح جدًا' أو 'ترجمة صوتية').",
      "suggested_correction": "string // الجملة البديلة والأكثر أصالة.",
      "justification": "string // لماذا البديل أفضل."
    }}
  ]
}}
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.review_and_correct(context)

# إنشاء مثيل وحيد
dialect_authenticity_guardian_agent = DialectAuthenticityGuardianAgent()
