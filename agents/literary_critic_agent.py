# agents/literary_critic_agent.py (V3 - The Comparative Critic)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("LiteraryCriticAgent")

class LiteraryCriticAgent(BaseAgent):
    """
    الناقد الأدبي المقارن (V3).
    لم يعد يعطي درجات مطلقة، بل يحلل النص، يصف خصائصه،
    ويولد بدائل بأساليب مختلفة ليختار منها المستخدم.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "literary_critic",
            name="الناقد الأدبي المقارن",
            description="يحلل النصوص ويقدم بدائل إبداعية بدلاً من التقييم الرقمي."
        )

    async def provide_comparative_critique(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يحلل النص ويولد 3 نسخ بديلة لفقرة محورية.
        'context' يجب أن يحتوي على:
        - text_content: النص الكامل للمراجعة.
        - pivotal_paragraph: الفقرة المحورية التي سيتم إعادة كتابتها.
        """
        text_content = context.get("text_content")
        pivotal_paragraph = context.get("pivotal_paragraph")

        if not text_content or not pivotal_paragraph:
            return {"status": "error", "message": "Text content and a pivotal paragraph are required."}

        logger.info("Providing comparative critique...")

        prompt = self._build_critique_prompt(text_content, pivotal_paragraph)
        response = await llm_service.generate_json_response(prompt, temperature=0.7)

        if "error" in response:
            return {"status": "error", "message": "LLM call for critique.", "details": response}

        return {"status": "success", "content": {"critique_report": response}}

    def _build_critique_prompt(self, full_text: str, pivotal_paragraph: str) -> str:
        return f"""
مهمتك: أنت محرر أدبي خبير ومبدع. مهمتك هي تحليل النص التالي وتقديم نقد وصفي، ثم إعادة كتابة "الفقرة المحورية" بثلاثة أساليب مختلفة.

**النص الكامل (للسياق العام):**
---
{full_text[:3000]}
---

**الفقرة المحورية للتحليل وإعادة الكتابة:**
---
{pivotal_paragraph}
---

**المطلوب:**
1.  **التحليل الوصفي (descriptive_analysis):**
    *   صف الأسلوب الحالي للفقرة المحورية. ركز على: النبرة (tone)، الإيقاع (pacing)، وكثافة الصور (imagery_density). لا تعطِ درجات.

2.  **البدائل الإبداعية (creative_alternatives):**
    *   أعد كتابة "الفقرة المحورية" ثلاث مرات، كل مرة بأسلوب مختلف:
        *   **البديل الحسي (sensory_version):** ركز على الحواس الخمس (الأصوات، الروائح، الملمس) لغمر القارئ في المشهد.
        *   **البديل النفسي (psychological_version):** ركز على الأفكار والمشاعر الداخلية للشخصية (المونولوج الداخلي).
        *   **البديل الحركي (action_oriented_version):** ركز على الأفعال والحركة السريعة لدفع الأحداث.

أرجع ردك **حصريًا** بتنسيق JSON صالح يتبع الهيكل التالي:
{{
  "descriptive_analysis": {{
    "tone": "string",
    "pacing": "string",
    "imagery_density": "string (e.g., منخفضة، متوسطة، عالية)"
  }},
  "creative_alternatives": {{
    "sensory_version": "string",
    "psychological_version": "string",
    "action_oriented_version": "string"
  }}
}}
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.provide_comparative_critique(context)

# إنشاء مثيل وحيد
literary_critic_agent = LiteraryCriticAgent()
