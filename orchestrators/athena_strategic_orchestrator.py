# orchestrators/athena_strategic_orchestrator.py (V2 - Reasoning & Memory-Aware)
import logging
from typing import Dict, Any, List

# استيراد المكونات الأساسية
from core.base_agent import BaseAgent
from core.llm_service import llm_service
from core.workflow_templates_models import TaskType # استيراد أنواع المهام
from core.core_narrative_memory import narrative_memory # [جديد] الوصول إلى الذاكرة

logger = logging.getLogger("AthenaStrategicOrchestrator")

class AthenaStrategicOrchestrator(BaseAgent):
    """
    "أثينا" - المنسق الاستراتيجي (V2).
    تستخدم سلسلة الأفكار والذاكرة السردية لاتخاذ قرارات ديناميكية ومستنيرة.
    """
    def __init__(self, agent_id: str = "athena_orchestrator"):
        super().__init__(
            agent_id=agent_id,
            name="أثينا - المخطط الاستراتيجي",
            description="تقرر الخطوة التالية في العملية الإبداعية بشكل ديناميكي."
        )
        logger.info("✅ Athena Strategic Orchestrator (V2) initialized.")

    async def decide_next_task(self, project_goal: str, project_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        الوظيفة الرئيسية: تقرر المهمة التالية.
        """
        logger.info("Athena: Strategizing next optimal task...")

        # [جديد] استعلام الذاكرة للحصول على سياق إضافي
        unresolved_conflicts = narrative_memory.query("What are the unresolved conflicts in the story?", top_k=2)
        
        prompt = self._build_decision_prompt(project_goal, project_state, unresolved_conflicts)
        
        # أثينا تحتاج إلى مخرجات منظمة لضمان موثوقية قراراتها
        decision = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=StrategicDecision, # سنحتاج لتعريف هذا النموذج
            system_instruction="أنت 'أثينا'، ذكاء استراتناعي استراتيجي فائق. وظيفتك هي التفكير خطوة بخطوة لاتخاذ القرار الأمثل للمهمة التالية.",
            temperature=0.0 # درجة حرارة منخفضة جدًا للقرارات المنطقية
        )
        
        if not decision:
            logger.error("Athena failed to make a strategic decision.")
            return None
        
        logger.info(f"Athena's Decision: Task '{decision.next_task_type}' - Justification: {decision.justification}")
        return decision.dict()

    def _build_decision_prompt(self, goal: str, state: Dict, unresolved_conflicts: List[Dict]) -> str:
        
        state_summary = f"""
- **آخر مهمة:** {state.get('last_task_type', 'N/A')}
- **ملخص آخر مخرجات:** {str(state.get('last_task_output', {}).get('summary'))[:200]}
- **آخر تقييم جودة:** {state.get('latest_critique', {}).get('overall_score', 'N/A')}
- **أهم ملاحظات الناقد:** {state.get('latest_critique', {}).get('issues', [])}
- **صراعات لم تُحل (من الذاكرة):** {[c['content'] for c in unresolved_conflicts]}
        """

        return f"""
**الهدف النهائي للمشروع:**
"{goal}"

**ملخص حالة المشروع الحالية:**
{state_summary}

**قائمة المهام المتاحة:**
{', '.join([e.value for e in TaskType])}

**مهمتك: فكر خطوة بخطوة لتحديد أفضل مهمة تالية.**
1.  **تحليل الوضع:** ما هي المشكلة الأكثر إلحاحًا الآن بناءً على حالة المشروع؟ (مثال: الجودة منخفضة، الحبكة متوقفة، هناك صراع لم يتم استكشافه).
2.  **تحديد الهدف:** ما هو الهدف المباشر للخطوة التالية؟ (مثال: تحسين الفصل الأخير، إدخال حبكة فرعية جديدة، كسر روتين القصة).
3.  **اختيار الأداة (الوكيل):** من هو الوكيل الأنسب لتحقيق هذا الهدف؟
4.  **تحديد المهمة:** ما هي المهمة المحددة (`TaskType`) التي يجب أن ينفذها هذا الوكيل؟
5.  **تجميع القرار:** بناءً على ما سبق، صغِ قرارك النهائي.

**قم بتعبئة القرار النهائي فقط في البنية المحددة.**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        decision = await self.decide_next_task(
            project_goal=context.get("project_goal"),
            project_state=context.get("project_state")
        )
        if decision:
            return {"status": "success", "content": {"strategic_decision": decision}}
        else:
            return {"status": "error", "message": "Athena could not reach a decision."}

# --- [جديد] تعريف نموذج Pydantic لقرار أثينا ---
class StrategicDecision(BaseModel):
    next_task_type: TaskType = Field(description="المعرف الدقيق للمهمة التالية التي يجب تنفيذها.")
    input_data: Dict[str, Any] = Field(description="القاموس الذي يحتوي على المدخلات اللازمة للمهمة التالية (مثل agent_id).")
    justification: str = Field(description="جملة واحدة تشرح لماذا هذا القرار هو الأمثل استراتيجيًا الآن.")

# إنشاء مثيل وحيد
athena_orchestrator = AthenaStrategicOrchestrator()
