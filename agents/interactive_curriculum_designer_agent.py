# agents/interactive_curriculum_designer_agent.py (V2 - The Adaptive Tutor)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from .learning_path_architect_agent import learning_path_architect_agent
from ..services.web_search_service import web_search_service
from ..core.llm_service import llm_service

logger = logging.getLogger("InteractiveCurriculumDesignerAgent")

class InteractiveCurriculumDesignerAgent(BaseAgent):
    """
    وكيل "المصمم التعليمي التفاعلي" (V2).
    يحلل أداء الطالب، ويتخذ قرارًا بشأن المسار التالي (علاجي أو إثرائي)،
    ثم ينسق مع `LearningPathArchitect` لبنائه.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "interactive_curriculum_designer",
            name="المرشد التعليمي المتكيف",
            description="يبني تجربة تعلم تكيفية بناءً على أداء الطالب."
        )
        self.learning_path_architect = learning_path_architect_agent
        self.web_service = web_search_service

    async def adapt_learning_path(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [مُحدَّث] الوظيفة الرئيسية: يحلل إجابة الطالب ويقترح الخطوة التالية.
        """
        student_answer = context.get("student_answer")
        guidance = context.get("correct_answer_guidance")
        curriculum_map = context.get("curriculum_map")
        current_lesson_title = context.get("current_lesson_title")

        if student_answer is None or not guidance or not curriculum_map or not current_lesson_title:
            return {"status": "error", "message": "Student answer, guidance, curriculum map and lesson title are required."}

        logger.info("Adaptive Tutor: Analyzing student performance to adapt learning path...")
        
        # [جديد] الخطوة 1: تقييم الإجابة باستخدام LLM
        assessment = await self._assess_student_answer(student_answer, guidance)
        
        if assessment.get("status") == "error":
            return assessment # تمرير الخطأ إذا فشل التقييم
            
        is_correct = assessment.get("is_correct", False)
        identified_weakness = assessment.get("identified_weakness")

        # الخطوة 2: اتخاذ قرار بناءً على التقييم
        if is_correct:
            # اقتراح محتوى إثرائي
            logger.info("Answer is correct. Designing enrichment path.")
            path_context = {
                "curriculum_map": curriculum_map,
                "path_type": "enrichment",
                "focus_area": current_lesson_title
            }
            path_result = await self.learning_path_architect.design_learning_path(path_context)
            next_step = {"type": "enrichment", "path": path_result.get("content"), "assessment": assessment}
        else:
            # تصميم مسار علاجي
            logger.info(f"Answer is incorrect. Designing remedial path for weakness: '{identified_weakness}'")
            path_context = {
                "curriculum_map": curriculum_map,
                "path_type": "remedial",
                "focus_area": identified_weakness or current_lesson_title
            }
            path_result = await self.learning_path_architect.design_learning_path(path_context)
            next_step = {"type": "remedial_path", "path": path_result.get("content"), "assessment": assessment}

        return {
            "status": "success",
            "content": {"adaptive_next_step": next_step},
            "summary": f"Generated an adaptive next step of type '{next_step['type']}'."
        }
    
    async def _assess_student_answer(self, student_answer: str, guidance: str) -> Dict:
        """[مُحدَّث] يقيم إجابة الطالب باستخدام LLM ويستخرج نقطة الضعف."""
        prompt = f"""
مهمتك: أنت أستاذ مصحح دقيق وبنّاء. قارن بين "إجابة الطالب" و"الإجابة النموذجية".

**إجابة الطالب:**
"{student_answer}"

**الإجابة النموذجية أو إرشاداتها:**
"{guidance}"

**المطلوب:**
أرجع تقييمك بتنسيق JSON:
1.  `is_correct` (boolean): هل الإجابة صحيحة بشكل عام (تحقق أكثر من 70% من المطلوب)؟
2.  `score` (float): درجة من 0.0 إلى 1.0 تعكس مدى دقة واكتمال الإجابة.
3.  `feedback` (string): ملاحظات بناءة وموجزة للطالب، تركز على ما يجب تحسينه.
4.  `identified_weakness` (string or null): **هذه هي الأهم.** حدد بدقة **نقطة الضعف المفاهيمية الرئيسية** في الإجابة إن وجدت (مثال: 'الخلط بين السلطة والدولة'، 'عدم فهم مفهوم العقد الاجتماعي'). إذا كانت الإجابة صحيحة، أرجع null.

**التقييم (JSON):**
"""
        response = await llm_service.generate_json_response(prompt, temperature=0.1)
        if "error" in response:
            return {"status": "error", "message": "Failed to assess student answer."}
        return response

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.adapt_learning_path(context)

# إنشاء مثيل وحيد
interactive_curriculum_designer_agent = InteractiveCurriculumDesignerAgent()
