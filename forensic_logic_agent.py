# forensic_logic_agent.py
"""
ForensicLogicAgent
وكيل متخصص في تحليل المنطق الجنائي في النصوص السردية.
يستخدم أداة ForensicLogicAnalyzer لتنفيذ مهامه.
"""
import logging
from typing import Dict, Any, Optional

# استيراد الأدوات والنماذج اللازمة
from base_agent import BaseAgent # نفترض وجود فئة أساسية للوكلاء
from tools.forensic_logic_analyzer import ForensicLogicAnalyzer, CrimeType # استيراد الأداة المتخصصة

logger = logging.getLogger("ForensicLogicAgent")

class ForensicLogicAgent(BaseAgent):
    """
    وكيل متخصص في التحليل الجنائي للمحتوى السردي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="المحقق الجنائي",
            description="وكيل متخصص في تحليل الدقة الإجرائية والمنطقية في قصص الجريمة والغموض."
        )
        # كل وكيل يمتلك أدواته الخاصة
        self.forensic_analyzer = ForensicLogicAnalyzer()
        logger.info("ForensicLogicAgent initialized.")

    async def analyze_crime_scene(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية للوكيل: تحليل مشهد جريمة.
        """
        text_content = context.get("text_content")
        if not text_content:
            raise ValueError("محتوى النص مطلوب لتحليل مشهد الجريمة.")
        
        logger.info(f"Analyzing crime scene from text content (length: {len(text_content)})...")
        
        # استدعاء الأداة المتخصصة
        analysis_result = await self.forensic_analyzer.analyze(
            content=text_content,
            context=context.get("narrative_context", {}),
            options=context.get("analysis_options", {})
        )
        
        # إرجاع النتيجة بتنسيق موحد
        return {
            "content": analysis_result, # المحتوى هنا هو نتيجة التحليل
            "summary": f"تم تحليل مشهد الجريمة. نوع الجريمة المقترح: {analysis_result.get('analysis', {}).get('crime_type')}. تم العثور على {analysis_result.get('analysis', {}).get('evidence_count')} دليل."
        }

    # --- يمكن إضافة دوال أخرى للمهام المتخصصة ---
    async def verify_evidence_chain(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        # ... منطق للتحقق من سلسلة الأدلة ...
        return {"content": {"chain_status": "consistent"}, "summary": "سلسلة الأدلة متماسكة."}
