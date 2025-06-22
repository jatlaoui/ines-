# agents/screenplay_formatter_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..tools.professional_exporter import professional_exporter # الأداة الجديدة

logger = logging.getLogger("ScreenplayFormatterAgent")

class ScreenplayFormatterAgent(BaseAgent):
    """
    وكيل متخصص في تحويل النصوص السردية أو المسرحية الخام
    إلى سيناريوهات منسقة بالصيغة العالمية الاحترافية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "screenplay_formatter",
            name="منسق السيناريو",
            description="يحول النصوص الخام إلى صيغة سيناريو احترافية (fdx, pdf)."
        )
        self.exporter = professional_exporter

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ نصًا خامًا ويقوم بتنسيقه.
        """
        raw_script = context.get("raw_script")
        if not raw_script:
            return {"status": "error", "message": "Raw script content is required."}
            
        logger.info("Formatting raw script into professional screenplay format...")
        
        # استدعاء الأداة المتخصصة للقيام بالتحويل الفعلي
        formatted_script = self.exporter.to_standard_script_format(raw_script)
        
        # في نظام حقيقي، يمكننا هنا استخدام مكتبة لتوليد ملفات .fdx أو PDF
        
        return {
            "status": "success",
            "content": {
                "formatted_script_text": formatted_script,
                "output_format": "standard_screenplay_text"
            },
            "summary": "Script has been formatted successfully."
        }

# إنشاء مثيل وحيد
screenplay_formatter_agent = ScreenplayFormatterAgent()
