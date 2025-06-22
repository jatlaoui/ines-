# agents/interactive_experience_architect.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..agents.adaptive_learning_agent import adaptive_learner

logger = logging.getLogger("InteractiveExperienceArchitect")

class InteractiveExperienceArchitect(BaseAgent):
    """
    وكيل "مهندس التجربة التفاعلية".
    يدير الحوار مع المستخدم، ويحلل تعديلاته، ويقدم خيارات إبداعية.
    إنه الواجهة الخلفية الذكية للتفاعل مع المستخدم.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "interactive_experience_architect",
            name="مهندس التجربة التفاعلية",
            description="يدير التفاعل الذكي مع المستخدم لتحسين العملية الإبداعية."
        )

    async def process_user_interaction(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تعالج تفاعل المستخدم وتقدم مخرجات ذكية.
        'context' يمكن أن يحتوي على:
        - user_id: معرف المستخدم.
        - interaction_type: 'edit', 'query', 'decision'.
        - original_text: النص الأصلي (في حالة التحرير).
        - edited_text: النص المعدل (في حالة التحرير).
        - user_query: سؤال المستخدم.
        - decision_context: سياق القرار الذي يجب اتخاذه.
        """
        interaction_type = context.get("interaction_type")
        user_id = context.get("user_id")

        if not user_id:
            return {"status": "error", "message": "User ID is required."}

        if interaction_type == "edit":
            original = context.get("original_text", "")
            edited = context.get("edited_text", "")
            await adaptive_learner.analyze_user_edit(user_id, original, edited)
            return {"status": "success", "message": f"User '{user_id}' style profile has been updated."}

        elif interaction_type == "query":
            # (مستقبلي) يمكن هنا تحليل سؤال المستخدم وتقديم إجابة ذكية
            return {"status": "success", "response": "This feature is under development."}
            
        elif interaction_type == "decision_prompt":
            # يولد سؤالاً للمستخدم عند نقطة تحول في القصة
            prompt = self._build_decision_prompt(context.get("decision_context"))
            return {"status": "success", "prompt_to_user": prompt}

        else:
            return {"status": "error", "message": f"Unknown interaction type: {interaction_type}"}

    def _build_decision_prompt(self, decision_context: Dict) -> Dict:
        """يبني سؤالاً تفاعلياً للمستخدم."""
        prompt_text = (f"لقد وصلنا إلى نقطة تحول في القصة. شخصية '{decision_context.get('character')}' "
                       f"تواجه الآن قراراً مصيرياً. بناءً على الأحداث، هناك عدة مسارات محتملة:")
        
        options = decision_context.get("options", [
            {"id": "path_a", "summary": "المسار أ: يقرر الانتقام."},
            {"id": "path_b", "summary": "المسار ب: يختار الغفران والتسامح."},
            {"id": "path_c", "summary": "المسار ج: يهرب من الموقف بأكمله."}
        ])

        return {
            "question": prompt_text,
            "options": options
        }

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.process_user_interaction(context)

# إنشاء مثيل وحيد
interactive_architect = InteractiveExperienceArchitect()
