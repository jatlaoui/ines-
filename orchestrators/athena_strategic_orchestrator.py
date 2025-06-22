# orchestrators/athena_strategic_orchestrator.py (وكيل جديد)
import logging
from typing import Dict, Any, List

from ..agents.base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..core.workflow_templates import TaskType # استيراد أنواع المهام

logger = logging.getLogger("AthenaStrategicOrchestrator")

class AthenaStrategicOrchestrator(BaseAgent):
    """
    "أثينا" - المنسق الاستراتيجي.
    وكيل عالي المستوى وظيفته التخطيط واتخاذ القرار. يحدد المهمة التالية
    الأنسب بناءً على الحالة الحالية للمشروع والهدف النهائي.
    """
    def __init__(self, agent_id: str = "athena_orchestrator"):
        super().__init__(
            agent_id=agent_id,
            name="أثينا - المخطط الاستراتيجي",
            description="تقرر الخطوة التالية في العملية الإبداعية بشكل ديناميكي."
        )

    async def decide_next_task(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تقرر المهمة التالية.
        'context' يجب أن يحتوي على:
        - project_goal: الهدف النهائي للمشروع (e.g., "كتابة رواية كاملة").
        - project_state: الحالة الحالية الكاملة للمشروع (المخرجات، التقييمات).
        - last_task_output: مخرجات آخر مهمة تم تنفيذها.
        """
        project_goal = context.get("project_goal")
        project_state = context.get("project_state")
        last_task_output = context.get("last_task_output")

        if not project_goal or not project_state:
            return {"status": "error", "message": "Project goal and state are required."}
            
        logger.info("Athena: Strategizing next optimal task...")

        prompt = self._build_decision_prompt(project_goal, project_state, last_task_output)
        decision = await llm_service.generate_json_response(prompt, temperature=0.1)

        if "error" in decision:
            return {"status": "error", "message": "Athena failed to make a strategic decision.", "details": decision}

        # التحقق من أن المهمة المقترحة من الأنواع المعروفة
        try:
            TaskType(decision.get("next_task_type"))
        except ValueError:
            logger.error(f"Athena suggested an invalid task type: {decision.get('next_task_type')}")
            # خطة بديلة: اقتراح مهمة مراجعة عامة
            decision["next_task_type"] = TaskType.CHECK_CONSISTENCY.value
            decision["justification"] = "Fallback: Reviewing overall consistency due to strategic error."

        return {
            "status": "success",
            "content": {"strategic_decision": decision},
            "summary": f"Athena's decision: '{decision.get('next_task_type')}' - Reason: {decision.get('justification')}"
        }

    def _build_decision_prompt(self, goal: str, state: Dict, last_output: Dict) -> str:
        
        # تحويل حالة المشروع إلى نص مفهوم للـ LLM
        state_summary = f"""
- **الفكرة الأساسية:** {state.get('idea', {}).get('premise')}
- **المخطط:** {len(state.get('blueprint', {}).get('chapters', []))} فصول مخطط لها.
- **الفصول المكتوبة:** {len(state.get('written_chapters', []))} فصول مكتوبة.
- **آخر تقييم جودة:** {state.get('latest_critique', {}).get('overall_score', 'N/A')}
- **آخر ملاحظات الناقد:** {state.get('latest_critique', {}).get('issues', [])}
        """

        return f"""
مهمتك: أنت "أثينا"، ذكاء اصطناعي استراتيجي فائق متخصص في إدارة المشاريع الإبداعية. وظيفتك ليست الكتابة، بل التفكير والتخطيط. بناءً على الهدف النهائي للمشروع وحالته الحالية، قرر ما هي **المهمة المنطقية التالية** التي يجب تنفيذها.

**الهدف النهائي للمشروع:**
"{goal}"

**ملخص حالة المشروع الحالية:**
{state_summary}

**مخرجات آخر مهمة تم تنفيذها:**
{str(last_output)[:1000]}

**قائمة المهام المتاحة (TaskType):**
{', '.join([e.value for e in TaskType])}

**المطلوب:**
بناءً على كل ما سبق، اتخذ قرارًا استراتيجيًا. يجب أن يكون قرارك في صيغة JSON ويحتوي على:
- **next_task_type:** (string) معرف المهمة التالية التي يجب تنفيذها من القائمة أعلاه.
- **input_data:** (object) قاموس بالمدخلات المحددة التي تحتاجها هذه المهمة.
- **justification:** (string) جملة واحدة تشرح **لماذا** اخترت هذه المهمة تحديدًا في هذه اللحظة.

**أمثلة على التفكير الاستراتيجي:**
- إذا كانت جودة الفصل الأخير منخفضة، قد تكون المهمة التالية هي `REFINE_TEXT` أو استدعاء ناقد متخصص `CUSTOM_AGENT_TASK`.
- إذا كانت القصة تفتقر إلى التشويق، قد تكون المهمة التالية هي `CUSTOM_AGENT_TASK` مع `agent_id: 'creative_chaos_agent'`.
- إذا تم الانتهاء من كتابة كل الفصول، قد تكون المهمة التالية هي `CHECK_CONSISTENCY`.

**قرارك الاستراتيجي (JSON):**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.decide_next_task(context)

# إنشاء مثيل وحيد
athena_orchestrator = AthenaStrategicOrchestrator()
