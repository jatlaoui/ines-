# agents/instructional_designer_agent.py (النسخة المطورة V2)
import logging
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("InstructionalDesignerAgent")

class InstructionalDesignerAgent(BaseAgent):
    """
    وكيل متخصص في تصميم الهياكل السردية والتعليمية.
    يعمل في وضعين: "narrative" للقصص و "academic" للمناهج.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "instructional_designer",
            name="المصمم الهيكلي",
            description="يحول المواد الخام إلى هياكل منظمة (مخططات سردية أو خرائط مناهج)."
        )

    async def create_structure(self, context: Dict[str, Any]) -> Dict[str, Any]:
        mode = context.get("mode", "narrative") # الوضع الافتراضي هو السردي
        text_content = context.get("text_content")
        if not text_content:
            return {"status": "error", "message": "Text content is required."}

        logger.info(f"Structural Designer operating in '{mode}' mode.")
        
        if mode == "academic":
            return await self._design_curriculum_map(text_content, context)
        else: # (mode == "narrative")
            # هنا نستدعي المنطق القديم لبناء المخططات السردية
            # يمكن ربطه بوكيل `BlueprintArchitectAgent`
            return {"status": "error", "message": "Narrative blueprinting should be handled by BlueprintArchitectAgent."}

    async def _design_curriculum_map(self, content: str, context: Dict) -> Dict[str, Any]:
        """
        يصمم "خريطة منهج" (Curriculum Map) من محتوى تعليمي.
        """
        logger.info(f"Designing curriculum map for audience: {context.get('target_audience', 'N/A')}...")

        prompt = """
مهمتك: أنت مصمم مناهج خبير. بناءً على هذا النص من كتاب مدرسي، قم ببناء "خريطة منهج" منظمة.
لكل درس، حدد الهدف التعليمي (Learning Objective) والمهارة المستهدفة (تحليل، نقد، حفظ).

النص للتحليل:
---
{content}
---

أرجع ردك بتنسيق JSON يحتوي على:
{
  "title": "عنوان المنهج",
  "target_audience": "الجمهور المستهدف",
  "main_axes": [
    {
      "axis_title": "عنوان المحور",
      "lessons": [
        {
          "lesson_title": "عنوان الدرس",
          "learning_objective": "الهدف التعليمي من الدرس",
          "target_skill": "المهارة التي يكتسبها الطالب"
        }
      ]
    }
  ]
}
""".format(content=content[:8000]) # تحديد حجم النص لتجنب الأخطاء

        response = await llm_service.generate_json_response(prompt)
        if "error" in response:
            return {"status": "error", "message": "Failed to design curriculum map.", "details": response}
        
        return {"status": "success", "content": {"curriculum_map": response}}

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.create_structure(context)

# إنشاء مثيل وحيد
instructional_designer_agent = InstructionalDesignerAgent()
