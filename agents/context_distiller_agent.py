# agents/context_distiller_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
# هذا الوكيل يستدعي خدمة LLM محلية (Jan)
from ..core.local_llm_service import local_llm_service 

logger = logging.getLogger("ContextDistillerAgent")

class ContextDistillerAgent(BaseAgent):
    """
    وكيل "مُحضِّر السياق".
    متخصص في أخذ الحالة الكاملة للمشروع وإنشاء "موجز مهمة" مضغوط وموجه
    لوكيل آخر. هذا هو قلب بروتوكول MCP.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "context_distiller",
            name="مُحضِّر السياق",
            description="يضغط السياق الكامل للمشروع في موجز مهمة فعال."
        )

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يقوم بضغط السياق.
        'context' يجب أن يحتوي على:
        - full_project_state: الحالة الكاملة للمشروع.
        - next_task_description: وصف المهمة التالية.
        - target_agent_id: معرف الوكيل الذي سيستلم الموجز.
        """
        full_state = context.get("full_project_state")
        task_description = context.get("next_task_description")
        target_agent_id = context.get("target_agent_id")

        if not all([full_state, task_description, target_agent_id]):
            return {"status": "error", "message": "Full project state, task description, and target agent ID are required."}

        logger.info(f"Distilling context for task '{task_description}' for agent '{target_agent_id}'...")

        # بناء Prompt للنموذج المحلي
        prompt = self._build_distillation_prompt(full_state, task_description, target_agent_id)
        
        # استدعاء خدمة LLM المحلية (Jan) لتوليد السياق المضغوط
        distilled_context = await local_llm_service.generate_json_response(prompt)
        
        if "error" in distilled_context:
            return {"status": "error", "message": "Local LLM failed to distill context.", "details": distilled_context}

        return {
            "status": "success",
            "content": {"distilled_context": distilled_context},
            "summary": "Context distilled successfully."
        }

    def _build_distillation_prompt(self, state: Dict, task: str, target_agent: str) -> str:
        # تحويل حالة المشروع إلى نص موجز جدًا
        state_summary = f"""
- آخر حدث رئيسي: {state.get('latest_event', 'N/A')}
- الحالة العاطفية للشخصيات الرئيسية: {state.get('character_emotions', {})}
- أهم ملاحظات الناقد الأخيرة: {state.get('latest_critique', {})}
"""
        return f"""
مهمتك: أنت مدير مشروع ذكي. مهمتك هي تحضير موجز مهمة (Mission Brief) دقيق ومضغوط للوكيل المتخصص التالي.

**حالة المشروع الحالية (ملخص):**
{state_summary}

**المهمة التالية المطلوبة:**
"{task}"

**الوكيل المستهدف لتنفيذ المهمة:**
"{target_agent}"

**التعليمات:**
بناءً على مهمة الوكيل المستهدف، استخلص **فقط** المعلومات الضرورية التي يحتاجها من حالة المشروع الكاملة. لا تضف أي معلومات غير ذات صلة.

**أمثلة على التفكير:**
- إذا كان الوكيل المستهدف هو `PlaywrightAgent`، فإنه يحتاج إلى الملفات النفسية للشخصيات المعنية، الهدف الدرامي، وآخر حوار بينهم.
- إذا كان الوكيل المستهدف هو `LoreMasterAgent`، فإنه يحتاج إلى الوصول إلى كل شيء تقريبًا.
- إذا كان الوكيل المستهدف هو `VocalPerformanceDirectorAgent`، فإنه يحتاج فقط إلى النص الغنائي والبصمة الإيقاعية، وليس حبكة القصة.

أرجع ردك **حصريًا** بتنسيق JSON يحتوي على السياق المضغوط والموجه.

**السياق المضغوط (JSON):**
"""

# إنشاء مثيل وحيد
context_distiller_agent = ContextDistillerAgent()
