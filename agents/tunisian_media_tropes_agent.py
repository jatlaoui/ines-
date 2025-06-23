# agents/tunisian_media_tropes_agent.py
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("TunisianMediaTropesAgent")

class TunisianMediaTropesAgent(BaseAgent):
    """
    وكيل متخصص في تحليل الكليشيهات (Tropes) في الدراما والسينما التونسية.
    يمكنه تحليل النصوص للكشف عن الأنماط السائدة أو اقتراح طرق مبتكرة لكسرها.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "tunisian_media_tropes_analyzer",
            name="محلل الكليشيهات الإعلامية التونسية",
            description="يحلل ويحدد الأنماط السردية الشائعة في الإعلام التونسي لتعزيز الابتكار."
        )

    async def analyze_and_suggest(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يحلل نصًا للكشف عن الكليشيهات ويقترح طرقًا لكسرها.
        """
        text_content = context.get("text_content")
        if not text_content:
            return {"status": "error", "message": "Text content is required for trope analysis."}

        logger.info("Analyzing text for common Tunisian media tropes...")
        
        prompt = self._build_analysis_prompt(text_content)
        response = await llm_service.generate_json_response(prompt, temperature=0.5)

        if "error" in response:
            return {"status": "error", "message": "LLM call for trope analysis failed.", "details": response}

        return {"status": "success", "content": {"tropes_report": response}}

    def _build_analysis_prompt(self, text: str) -> str:
        return f"""
مهمتك: أنت ناقد وسيناريست تونسي خبير، لديك ذاكرة موسوعية بالدراما التلفزيونية والأفلام التونسية.
مهمتك هي قراءة المشهد التالي، تحديد أي كليشيهات أو أنماط سردية شائعة فيه، ثم اقتراح "كسر" مبتكر لهذه الكليشيهات لجعل المشهد أكثر أصالة وعمقًا.

**المشهد للمراجعة:**
---
{text}
---

**التعليمات:**
أرجع ردك **حصريًا** بتنسيق JSON.
1.  **identified_trope:**
    - `name`: اسم الكليشيه المحدد (مثال: "صراع الأجيال حول العمل"، "شخصية الأب المتسلط").
    - `critique`: نقد موجز يشرح لماذا هذا النمط مستهلك في الدراما التونسية.
2.  **subversion_suggestion:**
    - `idea`: فكرة جريئة ومبتكرة لكسر هذا الكليشيه (مثال: "بدلاً من أن يكون الابن كسولاً، هو يعمل في مشروع رقمي سري لا يفهمه الأب").
    - `impact`: اشرح كيف سيغير هذا الاقتراح ديناميكية المشهد والصراع.

**تقرير تحليل الكليشيهات (JSON):**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.analyze_and_suggest(context)

# إنشاء مثيل وحيد
tunisian_media_tropes_agent = TunisianMediaTropesAgent()
