# agents/learning_path_architect_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("LearningPathArchitectAgent")

class LearningPathArchitectAgent(BaseAgent):
    """
    وكيل "مهندس مسارات التعلم".
    يصمم رحلات تعليمية مخصصة بناءً على أهداف الطالب ومستواه.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "learning_path_architect",
            name="مهندس مسارات التعلم",
            description="يصمم مسارات مراجعة متكيفة تربط بين الدروس والمفاهيم المختلفة."
        )

    async def design_learning_path(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يصمم مسار تعلم مخصص.
        'context' يجب أن يحتوي على:
        - curriculum_map: خريطة المنهج الكاملة.
        - path_type: نوع المسار المطلوب (e.g., 'quick_review', 'deep_dive', 'remedial').
        - student_profile: (اختياري) ملف تعريف الطالب لتخصيص أكبر.
        """
        curriculum_map = context.get("curriculum_map")
        path_type = context.get("path_type", "quick_review")

        if not curriculum_map:
            return {"status": "error", "message": "Curriculum map is required."}

        logger.info(f"Designing a '{path_type}' learning path...")
        
        prompt = self._build_design_prompt(curriculum_map, path_type)
        response = await llm_service.generate_json_response(prompt, temperature=0.4)

        if "error" in response:
            return {"status": "error", "message": "Failed to design learning path from LLM.", "details": response}

        return {
            "status": "success",
            "content": {"learning_path": response},
            "summary": f"Designed a learning path of type '{path_type}' with {len(response.get('steps', []))} steps."
        }
    
    def _build_design_prompt(self, curriculum_map: Dict, path_type: str) -> str:
        prompt_map = {
            "quick_review": "صمم 'مسار المراجعة السريعة' الذي يغطي فقط أهم المفاهيم الأساسية والتعاريف من كل درس. يجب أن يكون قصيراً ومباشراً.",
            "deep_dive": "صمم 'مسار التعمق' الذي يربط بين المفاهيم من محاور مختلفة، ويقترح أسئلة مقارنة وتحليل تتطلب تفكيراً نقدياً.",
            "remedial": "صمم 'مسارًا علاجيًا' لطالب يواجه صعوبة. ابدأ بالدروس الأسهل التي تمهد للمفاهيم الصعبة، وركز على الأمثلة والتطبيقات."
        }
        
        return f"""
مهمتك: أنت خبير في تصميم المناهج الرقمية المتكيفة. بناءً على خريطة المنهج الكاملة التالية، قم بتصميم مسار تعلمي محدد.

**خريطة المنهج:**
---
{str(curriculum_map)}
---

**المطلوب:**
{prompt_map.get(path_type, prompt_map['quick_review'])}

أرجع ردك **حصريًا** بتنسيق JSON. يجب أن يتبع الرد الهيكل التالي:
{{
  "path_name": "string // اسم المسار (مثال: 'مراجعة سريعة للفلسفة').",
  "path_description": "string // وصف موجز للهدف من هذا المسار.",
  "steps": [
    {{
      "step_number": "integer",
      "lesson_title": "string // عنوان الدرس ذي الصلة.",
      "focus": "string // المهمة المطلوبة في هذه الخطوة (مثال: 'مراجعة الملخص'، 'حل التمرين رقم 3'، 'حفظ بطاقة المراجعة')."
    }}
  ]
}}
"""
        
    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.design_learning_path(context)

# إنشاء مثيل وحيد
learning_path_architect_agent = LearningPathArchitectAgent()
