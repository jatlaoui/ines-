# agents/creative_chaos_agent.py (V2 - The Mutation Injector)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("CreativeChaosAgent")

class CreativeChaosAgent(BaseAgent):
    """
    وكيل الفوضى المبدعة (V2).
    يعمل كـ "مُحقِّن طفرات" يقترح انتهاكات مدروسة لقواعد القصة
    لفتح مسارات سردية جديدة وغير متوقعة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "creative_chaos_agent",
            name="مُحقِّن الفوضى المبدعة",
            description="يكسر الأنماط المتوقعة ويقترح تحولات جذرية في الحبكة."
        )

    async def inject_mutation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يقترح "طفرة" سردية مدروسة.
        'context' يجب أن يحتوي على:
        - story_context: ملخص للقصة حتى الآن.
        - established_rules: قائمة بالقواعد التي تم تأسيسها (مثل "علي شجاع"، "السحر غير موجود").
        """
        story_context = context.get("story_context")
        established_rules = context.get("established_rules", [])

        if not story_context:
            return {"status": "error", "message": "Story context is required."}

        logger.info("Injecting creative mutation into the narrative...")
        
        prompt = self._build_mutation_prompt(story_context, established_rules)
        response = await llm_service.generate_json_response(prompt, temperature=0.9)

        if "error" in response:
            return {"status": "error", "message": "LLM call failed for mutation injection.", "details": response}

        return {"status": "success", "content": {"mutation_suggestion": response}}

    def _build_mutation_prompt(self, context: str, rules: List[str]) -> str:
        return f"""
مهمتك: أنت كاتب سيناريو عبقري وخبير في إحداث الصدمات الدرامية (Plot Twists). مهمتك هي قراءة سياق القصة وقواعدها، ثم اقتراح "طفرة" أو انتهاك واحد لهذه القواعد يمكن أن يقلب القصة رأسًا على عقب بطريقة مثيرة.

**سياق القصة الحالي:**
---
{context}
---

**القواعد الراسخة في عالم القصة حتى الآن:**
---
{', '.join(rules) if rules else "لا توجد قواعد محددة بشكل صارم بعد."}
---

**المطلوب:**
اقترح "طفرة سردية" واحدة. يجب أن يكون الاقتراح جريئًا وغير متوقع.
لكل اقتراح، قدم:
- **mutation_idea:** الفكرة الأساسية للطفرة (مثال: الشخصية الأكثر ولاءً هي في الحقيقة الخائن).
- **dramatic_justification:** تبرير درامي قصير يشرح لماذا هذا الانتهاك سيجعل القصة أفضل وأكثر عمقًا.

أرجع ردك **حصريًا** بتنسيق JSON.
{{
  "mutation_idea": "string",
  "dramatic_justification": "string"
}}
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.inject_mutation(context)

# إنشاء مثيل وحيد
creative_chaos_agent = CreativeChaosAgent()
