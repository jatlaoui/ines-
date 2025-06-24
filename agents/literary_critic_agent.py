# agents/literary_critic_agent.py (V2 - Methodical & Actionable)
import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# استيراد المكونات الأساسية
from core.base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("LiteraryCriticAgent")

# --- [جديد] تعريف نموذج Pydantic لتقرير النقد ---
class CritiqueReport(BaseModel):
    """
    يمثل تقرير نقد أدبي منظم، يوفر تقييمًا رقميًا وملاحظات قابلة للتنفيذ.
    """
    overall_score: float = Field(..., ge=0.0, le=10.0, description="التقييم الإجمالي لجودة النص من 10.")
    strengths: List[str] = Field(description="قائمة بأهم 3 نقاط قوة في النص.")
    issues: List[str] = Field(description="قائمة بأهم 3-5 مشكلات أو نقاط ضعف تحتاج إلى تحسين. يجب أن تكون هذه الملاحظات محددة وقابلة للتنفيذ.")
    justification: str = Field(description="فقرة موجزة تبرر التقييم والملاحظات المذكورة.")

class LiteraryCriticAgent(BaseAgent):
    """
    الناقد الأدبي المنهجي (V2).
    يقدم نقدًا منظمًا وقابلاً للتنفيذ لتحسين جودة النصوص الإبداعية.
    """
    def __init__(self, agent_id: Optional[str] = "literary_critic"):
        super().__init__(
            agent_id=agent_id,
            name="الناقد الأدبي المنهجي",
            description="يقدم تقييمًا وملاحظات بناءة لتحسين الفصول الروائية."
        )
        logger.info("✅ LiteraryCriticAgent (V2) initialized.")

    async def review_chapter(self, chapter_content: str) -> Optional[CritiqueReport]:
        """
        الوظيفة الرئيسية: يراجع فصلًا روائيًا وينتج تقرير نقد منظم.
        """
        if not chapter_content or len(chapter_content) < 100:
            logger.warning("Chapter content is too short for a meaningful critique.")
            return None
            
        logger.info(f"Critiquing chapter content (length: {len(chapter_content)})...")
        
        prompt = self._build_critique_prompt(chapter_content)

        # استخدام المخرجات المنظمة لضمان تقرير نقد صالح
        report = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=CritiqueReport,
            system_instruction="أنت ناقد أدبي محترف ومحرر صارم ولكن عادل. مهمتك هي تقييم النصوص وتقديم ملاحظات بناءة تساعد الكاتب على تحسين عمله."
        )
        
        if report:
             logger.info(f"Critique complete. Overall Score: {report.overall_score}/10")
        else:
            logger.error("Failed to generate a valid critique report.")
            
        return report

    def _build_critique_prompt(self, chapter_text: str) -> str:
        """
        يبني موجهًا فعالاً لتقييم الفصل.
        """
        return f"""
قم بمراجعة الفصل الروائي التالي بعين الناقد الخبير.

**معايير التقييم:**
1.  **جودة السرد والأسلوب:** هل اللغة غنية؟ هل الوصف حي؟
2.  **تطور الشخصيات:** هل سلوك الشخصيات منطقي ومتسق؟ هل نرى تطورًا في شخصياتهم؟
3.  **الحبكة والإيقاع:** هل الأحداث تدفع القصة إلى الأمام؟ هل إيقاع الفصل مناسب (ليس بطيئًا جدًا أو سريعًا جدًا)؟
4.  **الحوار:** هل الحوار طبيعي ويعكس صوت كل شخصية؟
5.  **الأثر العاطفي:** هل ينجح الفصل في إثارة مشاعر القارئ؟

**النص للمراجعة:**
---
{chapter_text[:8000]} 
---

بناءً على المعايير أعلاه، قم بملء تقرير النقد. كن محددًا في ملاحظاتك وقدم اقتراحات يمكن للكاتب العمل بها.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة لمعالجة مهام النقد.
        """
        chapter_content = context.get("chapter_content")
        if not chapter_content:
            return {"status": "error", "message": "Chapter content is required for critique."}
        
        report = await self.review_chapter(chapter_content)
        
        if report:
            return {
                "status": "success",
                "content": {"critique_report": report.dict()},
                "summary": f"Critique generated with a score of {report.overall_score}."
            }
        else:
            return {
                "status": "error",
                "message": "Could not generate critique report."
            }

# إنشاء مثيل وحيد
literary_critic_agent = LiteraryCriticAgent()
