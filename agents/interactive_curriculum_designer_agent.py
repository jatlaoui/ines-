# agents/interactive_curriculum_designer_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from .learning_path_architect_agent import learning_path_architect_agent
from ..services.web_search_service import web_search_service # للاقتراحات الخارجية

logger = logging.getLogger("InteractiveCurriculumDesignerAgent")

class InteractiveCurriculumDesignerAgent(BaseAgent):
    """
    وكيل "المصمم التعليمي التفاعلي".
    يحلل أداء الطالب ويقترح مسارات علاجية أو إثرائية بشكل ديناميكي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "interactive_curriculum_designer",
            name="المصمم التعليمي التفاعلي",
            description="يبني تجربة تعلم تكيفية بناءً على أداء الطالب."
        )
        self.learning_path_architect = learning_path_architect_agent
        self.web_service = web_search_service

    async def adapt_learning_path(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يحلل إجابة الطالب ويقترح الخطوة التالية.
        'context' يجب أن يحتوي على:
        - student_answer: إجابة الطالب على تمرين.
        - correct_answer_guidance: الإرشادات للإجابة الصحيحة.
        - curriculum_map: خريطة المنهج الكاملة.
        """
        student_answer = context.get("student_answer")
        guidance = context.get("correct_answer_guidance")
        curriculum_map = context.get("curriculum_map")

        if student_answer is None or not guidance or not curriculum_map:
            return {"status": "error", "message": "Student answer, guidance, and curriculum map are required."}

        logger.info("Adapting learning path based on student performance...")
        
        # 1. تقييم الإجابة (محاكاة)
        # سيتم استدعاء LLM لمقارنة إجابة الطالب بالإرشادات
        is_correct = "صحيح" in student_answer.lower() # محاكاة بسيطة

        # 2. اتخاذ قرار بناءً على التقييم
        if is_correct:
            # اقتراح محتوى إثرائي
            recommendation = await self._suggest_enrichment_content(context.get("current_lesson_title"))
            next_step = {"type": "enrichment", "recommendation": recommendation}
        else:
            # تصميم مسار علاجي
            remedial_path_context = {
                "curriculum_map": curriculum_map,
                "path_type": "remedial",
                "difficulty_area": context.get("current_lesson_title")
            }
            path_result = await self.learning_path_architect.design_learning_path(remedial_path_context)
            next_step = {"type": "remedial_path", "path": path_result.get("content")}

        return {
            "status": "success",
            "content": {"adaptive_next_step": next_step},
            "summary": f"Generated an adaptive next step of type '{next_step['type']}'."
        }

    async def _suggest_enrichment_content(self, topic: str) -> Dict:
        """يقترح محتوى إثرائي خارجي."""
        logger.info(f"Searching for enrichment content on topic: {topic}")
        # search_result = await self.web_service.search(f"مقالات أكاديمية مبسطة حول {topic}")
        return {
            "title": f"مقالة إثرائية حول {topic}",
            "summary": "ملخص لمقالة من مصدر خارجي موثوق...",
            "source_url": "https://example.com/article"
        }

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.adapt_learning_path(context)

# إنشاء مثيل وحيد
interactive_curriculum_designer_agent = InteractiveCurriculumDesignerAgent()
