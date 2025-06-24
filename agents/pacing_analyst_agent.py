# agents/pacing_analyst_agent.py
import logging
from typing import Dict, Any, List, Optional
import numpy as np
from pydantic import BaseModel, Field

# استيراد المكونات الأساسية
from core.base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("PacingAnalystAgent")

# --- نموذج Pydantic لتقرير الإيقاع ---
class PacingReport(BaseModel):
    """
    يمثل تقرير تحليل إيقاع مجموعة من الفصول.
    """
    overall_pacing: str = Field(description="التقييم العام للإيقاع (e.g., 'سريع'، 'بطيء'، 'متوازن').")
    dialogue_to_narrative_ratio: float = Field(description="نسبة الحوار إلى السرد. نسبة عالية تعني إيقاعًا أسرع.")
    action_scene_density: float = Field(description="كثافة مشاهد الحركة. كثافة عالية تعني إيقاعًا أسرع.")
    descriptive_scene_density: float = Field(description="كثافة المشاهد الوصفية. كثافة عالية تعني إيقاعًا أبطأ.")
    recommendation: str = Field(description="توصية واضحة للكاتب بخصوص الفصل التالي (مثال: 'الفصل التالي يجب أن يحتوي على حدث كبير لتسريع الإيقاع').")

class PacingAnalystAgent(BaseAgent):
    """
    يحلل الإيقاع العام للرواية عبر عدة فصول ويقدم توصيات
    للحفاظ على اهتمام القارئ.
    """
    def __init__(self, agent_id: Optional[str] = "pacing_analyst_agent"):
        super().__init__(
            agent_id=agent_id,
            name="محلل إيقاع السرد",
            description="يحلل سرعة تدفق الأحداث ويقدم توصيات للحفاظ على التوازن."
        )
        logger.info("✅ PacingAnalystAgent initialized.")

    async def analyze_pacing_of_chapters(self, chapter_texts: List[str]) -> Optional[PacingReport]:
        """
        الوظيفة الرئيسية: تحلل مجموعة من نصوص الفصول.

        Args:
            chapter_texts: قائمة تحتوي على نصوص الفصول الأخيرة (مثلاً, آخر 3 فصول).

        Returns:
            كائن PacingReport أو None في حالة الفشل.
        """
        if not chapter_texts:
            logger.warning("No chapters provided for pacing analysis.")
            return None

        logger.info(f"Analyzing pacing for the last {len(chapter_texts)} chapters...")
        
        # دمج النصوص في نص واحد للتحليل الشامل
        full_text = "\n\n--- NEW CHAPTER ---\n\n".join(chapter_texts)

        prompt = self._build_pacing_analysis_prompt(full_text)

        report = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=PacingReport,
            system_instruction="أنت محرر خبير في بنية الروايات وإيقاعها. مهمتك هي تحليل سرعة السرد وتقديم توصيات واضحة."
        )

        if report:
            logger.info(f"Pacing analysis complete. Overall assessment: {report.overall_pacing}")
        else:
            logger.error("Failed to generate pacing analysis report.")
            
        return report

    def _build_pacing_analysis_prompt(self, text: str) -> str:
        """
        يبني موجهًا لتحليل الإيقاع.
        """
        return f"""
قم بتحليل الإيقاع السردي (Pacing) للنصوص التالية، التي تمثل الفصول الأخيرة من رواية.

**النصوص للمراجعة:**
---
{text[:8000]}
---

**التحليل المطلوب:**
1.  **ประเมิน الإيقاع العام:** هل السرد سريع ومثير، أم بطيء وتأملي، أم متوازن؟
2.  **حلل نسبة الحوار إلى السرد:** هل يغلب الحوار (إيقاع سريع) أم الوصف (إيقاع أبطأ)؟
3.  **حلل كثافة مشاهد الحركة:** هل هناك الكثير من الأحداث والصراعات؟
4.  **حلل كثافة المشاهد الوصفية/التأملية:** هل هناك الكثير من التوقف للوصف أو التفكير؟
5.  **قدم توصية واحدة ومحددة:** بناءً على تحليلك، ماذا يجب أن يكون نوع الفصل التالي للحفاظ على اهتمام القارئ؟ (مثال: فصل حركة، فصل حوار يكشف معلومات، فصل تأملي هادئ).

قم بملء تقرير تحليل الإيقاع التالي.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة.
        """
        chapter_texts = context.get("chapter_texts")
        if not chapter_texts or not isinstance(chapter_texts, list):
            return {"status": "error", "message": "A list of 'chapter_texts' is required."}

        report = await self.analyze_pacing_of_chapters(chapter_texts)

        if report:
            return {
                "status": "success",
                "content": {"pacing_report": report.dict()},
                "summary": f"Pacing analysis complete. Recommendation: {report.recommendation}"
            }
        else:
            return {
                "status": "error",
                "message": "Could not perform pacing analysis."
            }

# إنشاء مثيل وحيد
pacing_analyst_agent = PacingAnalystAgent()
