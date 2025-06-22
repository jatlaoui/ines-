# agents/production_analyst_agent.py (وكيل جديد)
import logging
import re
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("ProductionAnalystAgent")

class ProductionAnalystAgent(BaseAgent):
    """
    وكيل "محلل الإنتاج".
    يقرأ السيناريو ويصدر تقريرًا أوليًا عن الجدوى الإنتاجية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "production_analyst",
            name="محلل الإنتاج",
            description="يحلل السيناريو ويقدم تقريرًا عن المتطلبات الإنتاجية."
        )

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        يأخذ سيناريو منسقًا ويقوم بالعد الآلي والتحليل.
        """
        formatted_script = context.get("formatted_script_text")
        if not formatted_script:
            return {"status": "error", "message": "Formatted script is required."}

        logger.info("Analyzing script for production feasibility...")
        
        # 1. العد الآلي للعناصر الأساسية
        locations = re.findall(r"^(INT\.|EXT\.)(.*?)\s-", formatted_script, re.MULTILINE)
        unique_locations = set([loc[1].strip() for loc in locations])
        
        speaking_roles = set(re.findall(r"^\s{4}([A-Z\s]+)\n", formatted_script, re.MULTILINE))
        
        night_scenes = len(re.findall(r"- NIGHT", formatted_script, re.IGNORECASE))
        
        # 2. البحث عن الكلمات المفتاحية المكلفة
        costly_keywords = ["انفجار", "حريق", "مطر", "جمهور", "شجار", "مطاردة"]
        warnings = [f"تم ذكر كلمة '{kw}' التي قد تتطلب مؤثرات خاصة أو مجاميع." for kw in costly_keywords if kw in formatted_script]
        
        # 3. تجميع التقرير
        report = {
            "locations_analysis": {
                "count": len(unique_locations),
                "list": list(unique_locations),
                "notes": f"يتطلب {len(locations)} عملية انتقال بين المواقع."
            },
            "cast_analysis": {
                "speaking_roles_count": len(speaking_roles),
                "roles_list": list(speaking_roles)
            },
            "scheduling_notes": {
                "night_scenes_count": night_scenes
            },
            "budget_warnings": warnings,
            "overall_assessment": f"التقييم الأولي: جدوى إنتاجية {'مرتفعة' if len(unique_locations) < 5 and not warnings else 'متوسطة'}. التكاليف المتوقعة في النطاق المعقول لمسلسل تلفزيوني."
        }
        
        return {"status": "success", "content": {"feasibility_report": report}}

# إنشاء مثيل وحيد
production_analyst_agent = ProductionAnalystAgent()
