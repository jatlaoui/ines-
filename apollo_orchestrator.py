# apollo_orchestrator.py
"""
ApolloOrchestrator with Iterative Write–Critique Loop
"""
import asyncio
import logging
from typing import Any, Dict, List, Optional

# استيراد الوكلاء
from blueprint_architect_agent import ChapterOutline
from chapter_composer_agent import ChapterComposerAgent
from literary_critic_agent import LiteraryCriticAgent, CritiqueReport

# logger setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    def __init__(self):
        # وكلاء
        self.chapter_composer = ChapterComposerAgent()
        self.literary_critic = LiteraryCriticAgent()
        # إعدادات تحسين الفصول
        self.refinement_settings = {
            "quality_threshold": 8.5,
            "max_refinement_cycles": 2
        }
        logger.info("ApolloOrchestrator initialized with iterative refinement support.")

    async def start_new_creation(self, project_id: str, chapter_outline: ChapterOutline) -> Dict[str, Any]:
        """
        بدء عملية إنشاء فصل مع حلقة كتابة-نقد تكرارية.
        """
        return await self._iterative_chapter_creation_process(project_id, chapter_outline)

    async def _iterative_chapter_creation_process(self, project_id: str, chapter_outline: ChapterOutline) -> Dict[str, Any]:
        """
        يدير عملية كتابة ومراجعة وتحسين فصل واحد بشكل تكراري.
        """
        logger.info(f"[{project_id}] Starting iterative process for chapter: '{chapter_outline.title}'")

        current_content = None
        critique_report: Optional[CritiqueReport] = None

        for cycle in range(self.refinement_settings["max_refinement_cycles"] + 1):
            logger.info(f"[{project_id}] --- Refinement Cycle {cycle + 1} ---")

            # خطوة الكتابة
            feedback = critique_report.improvement_suggestions if critique_report else None
            generation_result = await self.chapter_composer.write_chapter(
                chapter_outline=chapter_outline,
                previous_feedback=feedback
            )
            if generation_result.get("error"):
                logger.error(f"[{project_id}] ChapterComposerAgent error: {generation_result['error']}")
                raise RuntimeError(generation_result['error'])

            current_content = generation_result["chapter_content"]
            word_count = generation_result.get("word_count")
            logger.info(f"[{project_id}] Composer generated version {cycle + 1} ({word_count} words)")

            # خطوة النقد
            logger.info(f"[{project_id}] Submitting version to LiteraryCriticAgent for review...")
            critique_report = await self.literary_critic.review_chapter(
                chapter_content=current_content,
                chapter_outline=chapter_outline.__dict__
            )
            quality_score = critique_report.overall_score
            logger.info(f"[{project_id}] Critique score: {quality_score:.1f}/10")

            # اتخاذ القرار
            if quality_score >= self.refinement_settings["quality_threshold"]:
                logger.info(f"[{project_id}] Quality threshold met. Finalizing chapter.")
                break
            elif cycle >= self.refinement_settings["max_refinement_cycles"]:
                logger.info(f"[{project_id}] Max cycles reached. Accepting current version.")
                break
            else:
                logger.info(f"[{project_id}] Quality below threshold. Refining again.")

        # حفظ النسخة النهائية
        final_data = {
            "content": current_content,
            "final_score": critique_report.overall_score,
            "critique": critique_report.dict()
        }
        logger.info(f"[{project_id}] Chapter '{chapter_outline.title}' finalized with score {critique_report.overall_score:.1f}")
        return final_data

# --- مثال اختبار ---
if __name__ == "__main__":
    import asyncio
    # محاكاة مخطط فصل
    sample_outline = ChapterOutline(
        title="الفصل 1: الرسالة الغامضة",
        summary="يلتقي علي بقدر الغموض في رسالة جده.",
        emotional_focus="الانتقال من الأمل الحذر إلى الإثارة",
        key_events=["علي يجد الرسالة","علي يقرأها للعائلة"],
        character_arcs={"علي": "يبدأ رحلة البحث عن هويته"}
    )
    orchestrator = ApolloOrchestrator()
    result = asyncio.run(orchestrator.start_new_creation("proj1", sample_outline))
    print(json.dumps(result, ensure_ascii=False, indent=2))
