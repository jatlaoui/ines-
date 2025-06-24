# core/refinement_service.py (V2 - Functional & Agent-Driven)

import logging
from typing import Any, Dict, Optional
import asyncio

# استيراد الوكلاء الذين تم تفعيلهم
from agents.chapter_composer_agent import chapter_composer_agent, ChapterOutline
from agents.literary_critic_agent import literary_critic_agent, CritiqueReport

logger = logging.getLogger("RefinementService")

class RefinementService:
    """
    خدمة عامة لإدارة دورة التحسين التكرارية (Create -> Critique -> Refine).
    V2: مصممة للعمل مع وكلاء INES الذين تم تفعيلهم.
    """
    def __init__(
        self,
        quality_threshold: float = 8.0,
        max_refinement_cycles: int = 2
    ):
        # لم نعد بحاجة لتمرير الدوال، فالخدمة ستعرف الوكلاء الذين يجب استدعاؤهم
        self.composer = chapter_composer_agent
        self.critic = literary_critic_agent
        self.quality_threshold = quality_threshold
        self.max_refinement_cycles = max_refinement_cycles
        logger.info("✅ RefinementService (V2) initialized.")

    async def refine_chapter(self, chapter_outline: ChapterOutline, prev_chapter_summary: Optional[str] = None) -> Dict[str, Any]:
        """
        يشغّل دورة تحسين تكرارية لكتابة فصل واحد.
        """
        logger.info(f"🚀 [Refinement] Starting iterative process for chapter: '{chapter_outline.title}'. Target score: {self.quality_threshold}")

        final_content: Optional[str] = None
        feedback_for_next_cycle: Optional[List[str]] = None
        final_critique: Optional[CritiqueReport] = None
        
        for cycle in range(self.max_refinement_cycles + 1):
            logger.info(f"--- 🔄 Refinement Cycle {cycle + 1}/{self.max_refinement_cycles + 1} ---")

            # --- الخطوة 1: الإنشاء أو التحسين ---
            logger.info("  Step 1: Calling ChapterComposerAgent to generate content...")
            current_content = await self.composer.write_chapter(
                chapter_outline=chapter_outline,
                previous_chapter_summary=prev_chapter_summary,
                feedback=feedback_for_next_cycle
            )
            
            if not current_content:
                error_message = "ChapterComposerAgent failed to generate content."
                logger.error(f"  ❌ Generation failed in cycle {cycle + 1}.")
                return {"status": "error", "message": error_message}
            
            final_content = current_content
            
            # --- الخطوة 2: النقد والتقييم ---
            logger.info("  Step 2: Calling LiteraryCriticAgent to critique content...")
            critique_report = await self.critic.review_chapter(current_content)
            
            if not critique_report:
                logger.error(f"  ❌ Critique function failed or returned invalid format.")
                break # الخروج من الحلقة والرضا بآخر نسخة مكتوبة

            final_critique = critique_report
            current_score = critique_report.overall_score
            feedback_for_next_cycle = critique_report.issues

            logger.info(f"  📊 Critique Result: Score = {current_score:.2f}/10.0")
            if feedback_for_next_cycle:
                logger.info(f"  📝 Feedback for next cycle: {feedback_for_next_cycle}")

            # --- الخطوة 3: اتخاذ القرار ---
            if current_score >= self.quality_threshold:
                logger.info(f"  ✅ Quality threshold met. Finalizing.")
                break
            
            if cycle >= self.max_refinement_cycles:
                logger.warning(f"  ⚠️ Max refinement cycles reached. Accepting current version with score {current_score:.2f}.")
                break
            
            logger.info("  ⏳ Quality below threshold. Preparing for next refinement cycle...")

        final_result = {
            "status": "success",
            "final_content": final_content,
            "final_critique": final_critique.dict() if final_critique else None,
            "refinement_cycles_used": cycle + 1
        }

        logger.info(f"🏁 [Refinement] Process finished. Final score: {final_critique.overall_score if final_critique else 'N/A'}")
        return final_result

# إنشاء مثيل وحيد
refinement_service = RefinementService()
