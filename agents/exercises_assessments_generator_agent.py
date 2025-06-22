# agents/exercises_assessments_generator_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("ExercisesAssessmentsGeneratorAgent")

class ExercisesAssessmentsGeneratorAgent(BaseAgent):
    """
    وكيل "مولّد التمارين والتقييمات".
    متخصص في تحويل المحتوى التعليمي إلى أسئلة وتمارين تفاعلية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "exercises_generator",
            name="مولّد التمارين والتقييمات",
            description="يصمم أسئلة متنوعة (فهم، تحليل، اختيار من متعدد) بناءً على محتوى درس معين."
        )

    async def generate_exercises_for_lesson(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يولد مجموعة من التمارين لدرس معين.
        'context' يجب أن يحتوي على:
        - lesson_content: النص الكامل للدرس.
        - lesson_title: عنوان الدرس.
        - exercise_types: قائمة بأنواع التمارين المطلوبة (e.g., ['comprehension', 'analysis', 'mcq']).
        - difficulty: مستوى الصعوبة المطلوب (e.g., 'easy', 'medium', 'hard').
        """
        lesson_content = context.get("lesson_content")
        lesson_title = context.get("lesson_title")
        exercise_types = context.get("exercise_types", ['comprehension', 'analysis'])
        difficulty = context.get("difficulty", "medium")

        if not lesson_content or not lesson_title:
            return {"status": "error", "message": "Lesson content and title are required."}

        logger.info(f"Generating '{difficulty}' level exercises for lesson: '{lesson_title}'")

        prompt = self._build_generation_prompt(lesson_content, lesson_title, exercise_types, difficulty)
        
        # هذا النوع من المهام يستفيد من مخرجات JSON المنظمة
        response = await llm_service.generate_json_response(prompt, temperature=0.5)

        if "error" in response:
            return {"status": "error", "message": "Failed to generate exercises from LLM.", "details": response}
        
        return {
            "status": "success",
            "content": {"exercises": response.get("exercises", [])},
            "summary": f"Generated {len(response.get('exercises', []))} exercises for the lesson."
        }

    def _build_generation_prompt(self, content: str, title: str, types: List[str], difficulty: str) -> str:
        
        type_descriptions = {
            "comprehension": "أسئلة فهم مباشر (من هو؟ ماذا؟ عرّف...).",
            "analysis": "أسئلة تحليل ومقارنة (لماذا؟ كيف؟ قارن بين...).",
            "mcq": "أسئلة اختيار من متعدد مع 3 خيارات خاطئة وخيار واحد صحيح.",
            "application": "أسئلة تطبيقية (اكتب فقرة تطبق فيها المفهوم...)."
        }
        
        requested_types = [type_descriptions[t] for t in types if t in type_descriptions]
        
        return f"""
مهمتك: أنت أستاذ وخبير في تصميم التمارين والتقييمات التربوية لمادة الفلسفة والتاريخ لطلاب البكالوريا في تونس.

**محتوى الدرس للتحليل:**
---
العنوان: {title}
المحتوى: {content}
---

**المطلوب:**
بناءً على محتوى الدرس أعلاه، قم بتوليد مجموعة من التمارين والأسئلة.
- **مستوى الصعوبة المطلوب:** {difficulty}
- **أنواع التمارين المطلوبة:** {', '.join(requested_types)}

أرجع ردك **حصريًا** بتنسيق JSON. يجب أن يحتوي الرد على مفتاح واحد هو "exercises"، وقيمته قائمة (list) من الكائنات (objects).
كل كائن في القائمة يجب أن يتبع الهيكل التالي:
{{
  "question": "string // نص السؤال بوضوح.",
  "type": "string // نوع السؤال (مثال: 'فهم'، 'تحليل'، 'اختيار من متعدد').",
  "difficulty": "string // مستوى صعوبة السؤال (سهل، متوسط، صعب).",
  "options": ["string"] // (اختياري) قائمة الخيارات لأسئلة الاختيار من متعدد.,
  "correct_answer": "string // (اختياري) الإجابة الصحيحة لأسئلة الاختيار من متعدد.",
  "guidance_answer": "string // إرشادات أو نقاط أساسية للإجابة على الأسئلة المفتوحة."
}}
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.generate_exercises_for_lesson(context)

# إنشاء مثيل وحيد
exercises_assessments_generator_agent = ExercisesAssessmentsGeneratorAgent()
