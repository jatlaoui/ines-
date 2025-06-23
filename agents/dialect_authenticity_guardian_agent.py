# agents/dialect_authenticity_guardian_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..engines.tunisian_culture_engine import tunisian_culture_engine # يعتمد على المحرك الثقافي

logger = logging.getLogger("DialectAuthenticityGuardianAgent")

class DialectAuthenticityGuardianAgent(BaseAgent):
    """
    وكيل "حارس الأصالة اللهجية".
    متخصص في مراجعة النصوص والتأكد من أن الحوارات تتوافق مع
    الخصائص اللغوية للشخصيات واللهجة المطلوبة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "dialect_authenticity_guardian",
            name="حارس الأصالة اللهجية",
            description="يراجع الحوارات ويقترح تعديلات لزيادة الأصالة اللهجية."
        )
        self.culture_engine = tunisian_culture_engine

    async def review_and_correct(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يراجع النص ويقترح تعديلات لهجية.
        'context' يجب أن يحتوي على:
        - text_content: النص المراد مراجعته.
        - dialect_id: معرف اللهجة المستهدفة (e.g., "tunisois", "sfaxien").
        - character_profile: وصف للشخصية المتحدثة.
        """
        text_content = context.get("text_content")
        dialect_id = context.get("dialect_id", "tunisois")
        character_profile = context.get("character_profile")

        if not text_content or not character_profile:
            return {"status": "error", "message": "Text content and character profile are required."}

        logger.info(f"Guardian of Authenticity: Reviewing text for '{dialect_id}' dialect...")
        
        prompt = self._build_review_prompt(text_content, dialect_id, character_profile)
        
        # هذا النوع من المهام يستفيد من مخرجات JSON المنظمة
        response = await llm_service.generate_json_response(prompt, temperature=0.2)

        if "error" in response:
            return {"status": "error", "message": "LLM call for dialect review failed.", "details": response}

        return {
            "status": "success",
            "content": {"review_report": response},
            "summary": "Dialect authenticity review complete."
        }

    def _build_review_prompt(self, text: str, dialect: str, profile: Dict) -> str:
        
        dialect_sample = self.culture_engine.get_dialectal_sample(dialect)
        
        return f"""
مهمتك: أنت لغوي خبير ومتخصص في اللهجة التونسية بجميع تنوعاتها. مهمتك هي مراجعة الحوار التالي والتأكد من أصالته اللغوية.

**اللهجة المستهدفة:** {dialect} (مثال على لكنتها: "{dialect_sample}")
**ملف الشخصية المتحدثة:** {profile.get('description', 'شخصية عامة')}

**الحوار للمراجعة:**
---
{text}
---

**التعليمات:**
1.  اقرأ الحوار بعناية.
2.  حدد أي جمل أو تراكيب تبدو "فصيحة جدًا" أو "مترجمة" ولا تتناسب مع شخصية المتحدث أو اللهجة اليومية.
3.  اقترح تعديلاً لكل جملة محددة، بحيث يحافظ التعديل على المعنى الأصلي الذكي ولكنه يستخدم تركيبة عامية أكثر أصالة وطبيعية.
4.  إذا كان الحوار أصيلاً بالفعل، أرجع قائمة فارغة.

أرجع ردك **حصريًا** بتنسيق JSON. يجب أن يحتوي الرد على مفتاح واحد هو `corrections`، وقيمته قائمة (list) من الكائنات (objects).
كل كائن يجب أن يتبع الهيكل التالي:
{{
  "original_sentence": "string // الجملة التي تحتاج إلى تعديل.",
  "suggested_correction": "string // الجملة البديلة والأكثر أصالة.",
  "justification": "string // شرح موجز لماذا البديل أفضل (مثال: 'استخدام مصطلح عامي أكثر شيوعًا')."
}}
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.review_and_correct(context)

# إنشاء مثيل وحيد
dialect_authenticity_guardian_agent = DialectAuthenticityGuardianAgent()
