# agents/apprentice_local_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
# هذا الوكيل سيستدعي خدمة LLM محلية (Jan)
from ..core.local_llm_service import local_llm_service # نفترض وجود هذه الخدمة

logger = logging.getLogger("ApprenticeLocalAgent")

class ApprenticeLocalAgent(BaseAgent):
    """
    الوكيل المحلي المتدرب.
    يعمل محليًا لإدارة السياق الكامل، تنفيذ المهام الروتينية،
    وتحضير "موجز المهمة" المضغوط للوكيل المشرف (Gemini).
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "apprentice_local_agent",
            name="الوكيل المحلي المتدرب",
            description="يدير السياق الكامل ويقوم بضغط المهام."
        )

    async def prepare_mission_brief(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يقوم بالاستخلاص والتلخيص الذكي لإنشاء سياق مضغوط.
        'context' يجب أن يحتوي على:
        - full_project_state: الحالة الكاملة للمشروع (الفصول، الشخصيات...).
        - next_task_description: وصف المهمة الإبداعية التالية.
        """
        full_state = context.get("full_project_state")
        task_description = context.get("next_task_description")

        if not full_state or not task_description:
            return {"status": "error", "message": "Full project state and task description are required."}

        logger.info(f"Apprentice: Preparing mission brief for task: '{task_description}'")

        # بناء Prompt للنموذج المحلي
        prompt = self._build_briefing_prompt(full_state, task_description)
        
        # استدعاء خدمة LLM المحلية (Jan) لتوليد السياق المضغوط
        mission_brief = await local_llm_service.generate_json_response(prompt)
        
        if "error" in mission_brief:
            return {"status": "error", "message": "Local LLM failed to generate mission brief.", "details": mission_brief}

        return {
            "status": "success",
            "content": {"mission_brief": mission_brief},
            "summary": "Mission brief prepared for the Supervisor."
        }

    def _build_briefing_prompt(self, state: Dict, task: str) -> str:
        # تحويل حالة المشروع إلى نص موجز جدًا
        state_summary = f"""
- آخر حدث رئيسي: {state.get('last_major_event')}
- الحالة العاطفية للشخصية الرئيسية '{state.get('main_character_name')}': {state.get('main_character_emotion')}
- الهدف المباشر للشخصية: {state.get('main_character_goal')}
"""
        return f"""
مهمتك: أنت مساعد مدير إنتاج ذكي. مهمتك هي قراءة الحالة الكاملة للمشروع وتحضير "موجز مهمة" (Mission Brief) قصير ومضغوط جدًا لكاتب السيناريو الخبير (المشرف).

**الحالة الحالية للمشروع:**
{state_summary}

**المهمة الإبداعية المطلوبة من المشرف:**
"{task}"

**التعليمات:**
قم بإنشاء سياق مضغوط وموجه في صيغة JSON يحتوي فقط على المعلومات الضرورية **جدًا** التي يحتاجها المشرف لتنفيذ مهمته الإبداعية. يجب أن يحتوي الـ JSON على:
- `task_brief`: وصف دقيق وموجز للمهمة.
- `plot_context`: آخر حدث مهم في القصة.
- `character_state`: قاموس يحتوي على اسم الشخصية وحالتها العاطفية وهدفها المباشر.
- `scene_setting`: وصف موجز لمكان وزمان المشهد.
- `style_directives`: قائمة من 2-3 توجيهات أسلوبية دقيقة.

**موجز المهمة (JSON):**
"""

    async def expand_and_detail_scene(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        يستلم المشهد المحوري من المشرف ويقوم بتوسيعه وتفصيله.
        """
        core_scene = context.get("core_scene_from_supervisor")
        full_context = context.get("full_project_state")
        
        logger.info("Apprentice: Expanding and detailing the core scene received from Supervisor...")
        
        # بناء Prompt للنموذج المحلي لتوسيع المشهد
        prompt = f"""
أنت كاتب مساعد. لقد قام الكاتب الخبير بكتابة المشهد المحوري التالي:
---
{core_scene}
---
مهمتك هي توسيع هذا المشهد. أضف تفاصيل وصفية للمكان، ومونولوجات داخلية للشخصيات قبل وبعد الحوار الرئيسي، وتأكد من أن كل التفاصيل تتسق مع السياق الكامل للمشروع: {str(full_context)[:1000]}.
الفصل الكامل:
"""
        
        full_chapter = await local_llm_service.generate_text_response(prompt)
        
        return {"status": "success", "content": {"full_chapter": full_chapter}}


    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        task_type = context.get("apprentice_task_type")
        if task_type == "prepare_brief":
            return await self.prepare_mission_brief(context)
        elif task_type == "expand_scene":
            return await self.expand_and_detail_scene(context)
        else:
            return {"status": "error", "message": f"Unknown apprentice task: {task_type}"}

# إنشاء مثيل وحيد
apprentice_local_agent = ApprenticeLocalAgent()
