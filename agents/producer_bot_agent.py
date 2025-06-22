# agents/producer_bot_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("ProducerBotAgent")

class ProducerBotAgent(BaseAgent):
    """
    وكيل "مساعد المنتج" (ProducerBot).
    متخصص في تحليل السيناريوهات من منظور إنتاجي وتقديم تقارير الجدوى.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "producer_bot",
            name="مساعد المنتج التحليلي",
            description="يحلل السيناريو ويصدر تقريرًا عن الجدوى الإنتاجية والتكاليف المحتملة."
        )

    async def generate_feasibility_report(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يقرأ سيناريو كامل ويولد تقرير جدوى إنتاجية.
        """
        script_content = context.get("script_content")
        if not script_content:
            return {"status": "error", "message": "Script content is required."}

        logger.info("ProducerBot: Generating Production Feasibility Report...")
        
        prompt = self._build_report_prompt(script_content)
        report = await llm_service.generate_json_response(prompt, temperature=0.2)

        return {"status": "success", "content": {"feasibility_report": report}}

    def _build_report_prompt(self, script: str) -> str:
        return f"""
مهمتك: أنت منتج سينمائي وتلفزيوني خبير (Line Producer) ولديك خبرة واسعة في تقدير ميزانيات الإنتاج. مهمتك هي قراءة السيناريو التالي وتقديم تقرير جدوى إنتاجية موجز.

**السيناريو للمراجعة:**
---
{script[:8000]}
---

**المطلوب:**
قم بتحليل السيناريو وأرجع تقريرك بتنسيق JSON. ركز على العناصر التي لها تأثير كبير على الميزانية واللوجستيات.
1.  **locations_analysis:**
    - `count`: عدد مواقع التصوير المختلفة المذكورة.
    - `notes`: ملاحظة حول مدى تعقيدها (مثال: "تتطلب مواقع تاريخية ومواقع خارجية متعددة").
2.  **cast_analysis:**
    - `main_characters`: عدد الشخصيات الرئيسية (لها حوار كثير).
    - `speaking_roles`: عدد الأدوار الثانوية التي لها حوار.
    - `extras_needed`: تقدير للمشاهد التي تتطلب مجاميع (crowd scenes) مع ملاحظة (مثال: "مشهد سوق يتطلب 50+ كومبارس").
3.  **production_warnings:**
    - `stunts`: قائمة بالمشاهد التي تتطلب مجازفات (e.g., "مطاردة سيارات").
    - `vfx`: قائمة بالمشاهد التي تتطلب مؤثرات بصرية خاصة (e.g., "انفجار سيارة").
    - `special_props`: قائمة بالأدوات أو المعدات الخاصة المطلوبة (e.g., "سيارات كلاسيكية من حقبة السبعينيات").
4.  **overall_assessment:** تقييم عام للميزانية المتوقعة (منخفضة، متوسطة، مرتفعة، مرتفعة جداً) مع تبرير موجز.

**تقرير الجدوى (JSON):**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.generate_feasibility_report(context)

# إنشاء مثيل وحيد
producer_bot_agent = ProducerBotAgent()
