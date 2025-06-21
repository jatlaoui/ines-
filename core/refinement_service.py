async def refine(self, context: Any) -> Dict[str, Any]:
    """
    يشغّل دورة تحسين تكرارية لأي كيان قابل للإنشاء والنقد.
    """
    logger.info("[Refinement] Starting iterative refinement process...")

    final_content = None
    feedback = None
    final_score = 0.0
    final_critique_report = {}

    for cycle in range(self.max_refinement_cycles + 1): # +1 for the initial attempt
        logger.info(f"[Refinement] --- Cycle {cycle + 1} ---")

        # 1. توليد المحتوى أو تحسينه
        generation_result = await self.creator_fn(context, feedback)
        
        # استخلاص المحتوى الفعلي من النتيجة
        current_content = generation_result.get("content")
        if not current_content:
            raise RuntimeError("Content generation failed or returned an empty result.")
        
        final_content = current_content # تحديث المحتوى النهائي في كل دورة
        
        # 2. مراجعة المحتوى
        critique_report = self.critique_fn(final_content)
        final_critique_report = critique_report # حفظ آخر تقرير نقد
        
        feedback = critique_report.get("issues")
        final_score = critique_report.get("overall_score", 0)

        logger.info(f"[Refinement] Score: {final_score:.1f}/10 | Feedback issues: {feedback}")

        # 3. اتخاذ القرار
        if final_score >= self.quality_threshold:
            logger.info(f"[Refinement] Quality threshold met ({final_score} >= {self.quality_threshold}). Finalizing.")
            break
        elif cycle >= self.max_refinement_cycles -1: # -1 because we loop one extra time
            logger.warning(f"[Refinement] Max refinement cycles ({self.max_refinement_cycles}) reached. Accepting current version with score {final_score:.1f}.")
            break
        else:
            logger.info("[Refinement] Quality below threshold. Retrying with new feedback.")

    return {
        "final_content": final_content,
        "final_score": final_score,
        "final_critique": final_critique_report,
        "refinement_cycles_used": cycle + 1
    }
