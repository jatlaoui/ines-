# agents/tunisian_history_advisor_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("TunisianHistoryAdvisorAgent")

class TunisianHistoryAdvisorAgent(BaseAgent):
    """
    وكيل متخصص في التاريخ التونسي.
    يقدم معلومات دقيقة ويتحقق من صحة التفاصيل التاريخية في النصوص السردية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "tunisian_history_advisor",
            name="المستشار في تاريخ تونس",
            description="يضمن الدقة التاريخية للأحداث، الملابس، والمصطلحات في سياق تونسي."
        )
        # قاعدة المعرفة هذه يمكن توسيعها بشكل كبير في نظام حقيقي
        self.history_kb = {
            "carthaginian": "الفترة القرطاجية: الصراع مع روما، عبادة بعل حمون وتانيت، التجارة البحرية.",
            "ottoman": "الفترة العثمانية: حكم البايات، بناء المساجد والأسواق، دور القراصنة.",
            "post_2011": "فترة ما بعد 2011: حرية التعبير، تحديات اقتصادية، صعود تيارات سياسية جديدة."
        }

    async def provide_historical_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يقدم تفاصيل تاريخية دقيقة لفترة معينة.
        """
        time_period_id = context.get("time_period_id", "post_2011")
        topic = context.get("topic")

        if not topic:
            return {"status": "error", "message": "A topic is required to get historical context."}

        logger.info(f"Providing historical context for period '{time_period_id}' on topic '{topic}'.")
        
        prompt = self._build_context_prompt(time_period_id, topic)
        response = await llm_service.generate_json_response(prompt)

        return {"status": "success", "content": {"historical_context": response}}

    def _build_context_prompt(self, period: str, topic: str) -> str:
        base_info = self.history_kb.get(period, "فترة تاريخية عامة.")
        return f"""
مهمتك: أنت مؤرخ متخصص في تاريخ تونس.

**الفترة الزمنية المطلوبة:** {period}
**المعلومات الأساسية عن الفترة:** {base_info}
**الموضوع المحدد للبحث:** "{topic}"

**المطلوب:**
بناءً على الفترة والموضوع، قدم قائمة من 3-5 حقائق أو تفاصيل دقيقة ومثيرة للاهتمام يمكن استخدامها في عمل روائي. ركز على تفاصيل الحياة اليومية، العلاقات الاجتماعية، أو المصطلحات الشائعة في تلك الفترة.

أرجع ردك بتنسيق JSON يحتوي على قائمة من الحقائق `facts`.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.provide_historical_context(context)

# إنشاء مثيل وحيد
tunisian_history_advisor_agent = TunisianHistoryAdvisorAgent()
