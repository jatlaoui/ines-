# core/refinement_service.py (النسخة المفعّلة والمحسنة)

import logging
from typing import Any, Callable, Dict, Optional, List, Awaitable

# إعداد التسجيل بشكل أفضل
logger = logging.getLogger("RefinementService")
# لا حاجة لـ basicConfig هنا إذا تم تعريفه في نقطة انطلاق المشروع

class RefinementService:
    """
    خدمة عامة لإدارة دورة التحسين التكرارية (Create -> Critique -> Refine).
    تعمل كحلقة تحكم لأي عملية تتطلب تحسينًا متكررًا للجودة.
    """
    def __init__(
        self,
        creator_fn: Callable[[Dict[str, Any], Optional[List[str]]], Awaitable[Dict[str, Any]]],
        critique_fn: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]],
        quality_threshold: float = 8.0,
        max_refinement_cycles: int = 2
    ):
        """
        تهيئة خدمة التحسين.
        :param creator_fn: دالة غير متزامنة لتوليد المحتوى (تأخذ السياق الأولي وملاحظات اختيارية).
        :param critique_fn: دالة غير متزامنة للنقد (تأخذ المحتوى الذي تم إنشاؤه).
        :param quality_threshold: عتبة الجودة المطلوبة لإيقاف التحسين.
        :param max_refinement_cycles: أقصى عدد من دورات التحسين.
        """
        self.creator_fn = creator_fn
        self.critique_fn = critique_fn
        self.quality_threshold = quality_threshold
        self.max_refinement_cycles = max_refinement_cycles

    async def refine(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        يشغّل دورة تحسين تكرارية لأي كيان قابل للإنشاء والنقد.
        """
        logger.info(f"🚀 [Refinement] Starting iterative process. Target score: {self.quality_threshold}, Max cycles: {self.max_refinement_cycles}")

        final_content = None
        feedback_for_next_cycle: Optional[List[str]] = None
        final_score = 0.0
        critique_report = {}
        
        # الحلقة ستعمل `max_refinement_cycles` + 1 مرة (المحاولة الأولى + دورات التحسين)
        for cycle in range(self.max_refinement_cycles + 1):
            logger.info(f"--- 🔄 Refinement Cycle {cycle + 1}/{self.max_refinement_cycles + 1} ---")

            # --- الخطوة 1: الإنشاء أو التحسين ---
            logger.info("  Step 1: Generating content...")
            generation_result = await self.creator_fn(context, feedback_for_next_cycle)
            
            # التحقق من نجاح عملية الإنشاء
            if generation_result.get("status") != "success" or "content" not in generation_result:
                error_message = generation_result.get("message", "Content generation failed or returned an empty result.")
                logger.error(f"  ❌ Generation failed in cycle {cycle + 1}. Reason: {error_message}")
                # إرجاع خطأ فوري إذا فشلت عملية الإنشاء
                return {"status": "error", "message": error_message, "details": generation_result}

            current_content = generation_result["content"]
            final_content = current_content  # تحديث المحتوى النهائي في كل دورة ناجحة
            
            # --- الخطوة 2: النقد والتقييم ---
            logger.info("  Step 2: Critiquing generated content...")
            critique_result = await self.critique_fn(current_content)
            
            # التحقق من نجاح عملية النقد
            if "overall_score" not in critique_result or "issues" not in critique_result:
                logger.error(f"  ❌ Critique function returned invalid format: {critique_result}")
                # يمكننا إما إيقاف العملية أو الاستمرار بالنتيجة الحالية
                break

            critique_report = critique_result
            current_score = critique_report.get("overall_score", 0.0)
            feedback_for_next_cycle = critique_report.get("issues")
            final_score = current_score

            logger.info(f"  📊 Critique Result: Score = {current_score:.2f}/10.0")
            if feedback_for_next_cycle:
                logger.info(f"  📝 Feedback for next cycle: {feedback_for_next_cycle}")

            # --- الخطوة 3: اتخاذ القرار ---
            if current_score >= self.quality_threshold:
                logger.info(f"  ✅ Quality threshold met ({current_score:.2f} >= {self.quality_threshold}). Finalizing.")
                break
            
            # التحقق مما إذا كانت هذه هي الدورة الأخيرة
            if cycle >= self.max_refinement_cycles:
                logger.warning(f"  ⚠️ Max refinement cycles ({self.max_refinement_cycles}) reached. Final score {current_score:.2f} is below threshold. Accepting current version.")
                break
            
            logger.info("  ⏳ Quality below threshold. Preparing for next refinement cycle...")

        final_result = {
            "status": "success",
            "final_content": final_content,
            "final_score": final_score,
            "final_critique": critique_report,
            "refinement_cycles_used": cycle + 1
        }

        logger.info(f"🏁 [Refinement] Process finished. Final score: {final_score:.2f} after {cycle + 1} cycle(s).")
        return final_result
