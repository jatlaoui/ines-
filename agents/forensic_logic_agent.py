# agents/forensic_logic_agent.py (V2 - Functional)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("ForensicLogicAgent")

class ForensicLogicAgent(BaseAgent):
    """
    وكيل المنطق الجنائي (V2).
    يستخدم LLM لتحليل مسارح الجريمة في النصوص السردية،
    والكشف عن التناقضات والأخطاء الإجرائية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "forensic_logic_agent",
            name="المحقق الجنائي المنطقي",
            description="يحلل الدقة الإجرائية والمنطقية في قصص الجريمة والغموض."
        )
        # لم نعد بحاجة إلى الأداة الوهمية، سنعتمد على prompt ذكي
        logger.info("✅ Functional Forensic Logic Agent (V2) Initialized.")

    async def analyze_crime_scene(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تحليل مشهد جريمة.
        """
        text_content = context.get("text_content")
        if not text_content:
            return {"status": "error", "message": "Crime scene text content is required."}
        
        logger.info(f"Analyzing crime scene from text content...")
        
        prompt = self._build_analysis_prompt(text_content)
        analysis_result = await llm_service.generate_json_response(prompt, temperature=0.2)

        if "error" in analysis_result:
            return {"status": "error", "message": "LLM call for forensic analysis failed.", "details": analysis_result}
        
        return {
            "status": "success",
            "content": {"forensic_analysis": analysis_result},
            "summary": f"Forensic analysis complete. Crime type: {analysis_result.get('crime_type')}"
        }

    def _build_analysis_prompt(self, scene_text: str) -> str:
        return f"""
مهمتك: أنت محقق جنائي خبير ومستشار للروائيين. مهمتك هي قراءة النص الذي يصف مشهد جريمة، ثم تقديم تحليل دقيق للمنطق الجنائي والإجرائي.

**نص مشهد الجريمة:**
---
{scene_text}
---

**التعليمات:**
قم بتحليل النص أعلاه وأرجع تقريرك **حصريًا** بتنسيق JSON، يغطي النقاط التالية:
1.  **crime_type:** حدد نوع الجريمة الموصوفة (مثال: "جريمة قتل بآلة حادة"، "سرقة مع اقتحام").
2.  **evidence_analysis:** حلل الأدلة المذكورة. لكل دليل، اذكر نوعه (مادي، بيولوجي، رقمي) وقيمته المحتملة في التحقيق.
3.  **procedural_errors:** اذكر أي أخطاء إجرائية واضحة قام بها المحققون في مسرح الجريمة (مثال: "لم يتم تأمين مسرح الجريمة"، "تم لمس الدليل بدون قفازات").
4.  **logical_inconsistencies:** اذكر أي تناقضات منطقية في المشهد (مثال: "الضحية مصابة بطلق ناري ولكن لا يوجد ذكر لصوت إطلاق نار").
5.  **recommendations:** قدم توصيتين لتحسين واقعية المشهد الجنائي.

**تقرير التحليل الجنائي (JSON):**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.analyze_crime_scene(context)

# إنشاء مثيل وحيد
forensic_logic_agent = ForensicLogicAgent()
