# agents/learning_path_architect_agent.py (V2 - Remedial Path Specialist)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("LearningPathArchitectAgent")

class LearningPathArchitectAgent(BaseAgent):
    """
    وكيل "مهندس مسارات التعلم" (V2).
    يصمم رحلات تعليمية مخصصة، بما في ذلك مسارات علاجية لمعالجة نقاط الضعف المحددة،
    ومسارات إثرائية للطلاب المتفوقين.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "learning_path_architect",
            name="مهندس مسارات التعلم",
            description="يصمم مسارات مراجعة متكيفة تربط بين الدروس والمفاهيم المختلفة."
        )

    async def design_learning_path(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [مُحدَّث] الوظيفة الرئيسية: يصمم مسار تعلم مخصص بناءً على الهدف.
        """
        curriculum_map = context.get("curriculum_map")
        path_type = context.get("path_type", "quick_review")
        # [جديد] استقبال نقطة الضعف أو موضوع الإثراء
        focus_area = context.get("focus_area")

        if not curriculum_map:
            return {"status": "error", "message": "Curriculum map is required."}

        logger.info(f"Designing a '{path_type}' learning path. Focus Area: {focus_area}")
        
        prompt = self._build_design_prompt(curriculum_map, path_type, focus_area)
        response = await llm_service.generate_json_response(prompt, temperature=0.3)

        if "error" in response:
            return {"status": "error", "message": "Failed to design learning path from LLM.", "details": response}

        return {
            "status": "success",
            "content": {"learning_path": response},
            "summary": f"Designed a learning path of type '{path_type}' with {len(response.get('steps', []))} steps."
        }
    
    def _build_design_prompt(self, curriculum_map: Dict, path_type: str, focus_area: Optional[str] = None) -> str:
        # [مُحدَّث] إضافة منطق خاص بالمسار العلاجي والإثرائي
        prompt_map = {
            "quick_review": "صمم 'مسار المراجعة السريعة' الذي يغطي فقط أهم المفاهيم الأساسية والتعاريف من كل درس.",
            "deep_dive": "صمم 'مسار التعمق' الذي يربط بين المفاهيم من محاور مختلفة، ويقترح أسئلة مقارنة وتحليل.",
            "remedial": (
                f"صمم 'مسارًا علاجيًا' (Remedial Path) لطالب يواجه صعوبة محددة في فهم '{focus_area}'.\n"
                "1. حدد المفاهيم الأساسية التي يجب على الطالب فهمها أولاً قبل معالجة نقطة الصعوبة.\n"
                "2. ابدأ المسار بأنشطة بسيطة (مثل مراجعة بطاقة مصطلحات أو مشاهدة فيديو شرح مبسط).\n"
                "3. ابنِ الفهم تدريجيًا وصولاً إلى الدرس المستهدف.\n"
                "4. اختتم المسار بتمرين تطبيقي مباشر على نقطة الضعف."
            ),
            "enrichment": (
                f"صمم 'مسارًا إثرائيًا' (Enrichment Path) لطالب أتقن درس '{focus_area}'.\n"
                "1. اقترح قراءات خارجية أو مقالات أكاديمية مبسطة حول الموضوع.\n"
                "2. اربط المفهوم بتطبيقاته في مجالات أخرى أو بفلاسفة آخرين.\n"
                "3. اقترح سؤالاً بحثيًا أو موضوعًا للنقاش يتحدى فهم الطالب."
            )
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
  "path_name": "string // اسم المسار (مثال: 'مسار علاجي لفهم إشكالية الدولة').",
  "path_description": "string // وصف موجز للهدف من هذا المسار.",
  "steps": [
    {{
      "step_number": "integer",
      "lesson_title": "string // عنوان الدرس ذي الصلة.",
      "focus": "string // المهمة المطلوبة (مثال: 'مراجعة مفهوم السلطة'، 'حل التمرين رقم 1').",
      "rationale": "string // [مهم جدًا] لماذا هذه الخطوة ضرورية ومفيدة للطالب في هذا المسار."
    }}
  ]
}}
"""
        
    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.design_learning_path(context)

# إنشاء مثيل وحيد
learning_path_architect_agent = LearningPathArchitectAgent()
