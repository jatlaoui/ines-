# agents/tunisian_socio_political_analyst_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..services.web_search_service import web_search_service
from ..core.llm_service import llm_service

logger = logging.getLogger("TunisianSocioPoliticalAnalystAgent")

class TunisianSocioPoliticalAnalystAgent(BaseAgent):
    """
    وكيل متخصص في تحليل السياق الاجتماعي والسياسي التونسي المعاصر.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "tunisian_socio_political_analyst",
            name="محلل الواقع التونسي",
            description="يحلل المواضيع الرائجة والنقاشات المجتمعية لربط السرد بالواقع."
        )
        self.web_service = web_search_service

    async def get_current_pulse(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يبحث عن المواضيع الرائجة ويحللها.
        """
        logger.info("Analyzing the current socio-political pulse of Tunisia...")
        
        # 1. البحث عن المواضيع الرائجة (محاكاة)
        # search_results = await self.web_service.search("أهم مواضيع النقاش في تونس اليوم")
        search_results_summary = "النقاشات الحالية تدور حول غلاء المعيشة، مستقبل الشباب، والعلاقة بين التكنولوجيا والمجتمع."
        
        # 2. تحليل النتائج بواسطة LLM
        prompt = f"""
مهمتك: أنت صحفي ومحلل اجتماعي تونسي. بناءً على هذا الملخص للنقاشات الرائجة، استخلص 3 محاور صراع أو مواضيع درامية يمكن استخدامها في مسلسل اجتماعي معاصر.

**ملخص النقاشات:**
"{search_results_summary}"

**المطلوب:**
أرجع ردك بصيغة JSON يحتوي على قائمة `dramatic_themes`.
"""
        response = await llm_service.generate_json_response(prompt)
        
        return {"status": "success", "content": response}

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.get_current_pulse(context)

# إنشاء مثيل وحيد
tunisian_socio_political_analyst_agent = TunisianSocioPoliticalAnalystAgent()
