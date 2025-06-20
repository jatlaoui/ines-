# agents/forensic_logic_agent.py
# (الكود كما هو في ردنا السابق)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from tools.forensic_logic_analyzer import ForensicLogicAnalyzer, CrimeType

logger = logging.getLogger("ForensicLogicAgent")

class ForensicLogicAgent(BaseAgent):
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id=agent_id, name="المحقق الجنائي", description="تحليل الدقة الإجرائية والمنطقية في قصص الجريمة.")
        self.forensic_analyzer = ForensicLogicAnalyzer()
        logger.info("ForensicLogicAgent initialized.")

    async def analyze_crime_scene(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        text_content = context.get("text_content")
        if not text_content:
            raise ValueError("محتوى النص مطلوب لتحليل مشهد الجريمة.")
        
        logger.info(f"Analyzing crime scene from text content (length: {len(text_content)})...")
        analysis_result = await self.forensic_analyzer.analyze(content=text_content, context={}, options={})
        
        return {"content": analysis_result, "summary": f"تم تحليل مشهد الجريمة."}
