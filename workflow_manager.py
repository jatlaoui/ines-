# core/workflow_manager.py (النسخة المفعّلة والمبسطة)

import logging
import json
import asyncio
from typing import Dict, Any, List, Optional, Callable

# --- الاستيرادات المحدثة ---
from core.apollo_orchestrator import apollo
# استيراد نماذج البيانات اللازمة لمحاكاة المخطط
try:
    from agents.blueprint_architect_agent import StoryBlueprint, ChapterOutline
except ImportError:
    from ..agents.blueprint_architect_agent import StoryBlueprint, ChapterOutline

# --- إعدادات التسجيل ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    """
    يدير خطوط الإنتاج الإبداعية (Pipelines) التي تتكون من عدة مهام متسلسلة.
    يعمل كطبقة عليا لتنسيق العمليات المعقدة عبر ApolloOrchestrator.
    """
    def __init__(self):
        self.orchestrator = apollo
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def create_short_story_from_idea(
        self,
        project_id: str,
        initial_prompt: str,
        genre_hint: str = "دراما اجتماعية",
        num_chapters: int = 3 # قصة قصيرة
    ) -> Dict[str, Any]:
        """
        خط إنتاج كامل ومبسّط: يولد فكرة، ثم يبني مخططًا وهميًا، ثم يكتب الفصول.
        """
        pipeline_id = f"short_story_{project_id}"
        logger.info(f"🚀 [{pipeline_id}] Starting 'Short Story From Idea' Pipeline...")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}
        
        try:
            # --- المرحلة 1: توليد الفكرة الرئيسية ---
            logger.info(f"[{pipeline_id}] STAGE 1: Generating a compelling story idea...")
            idea_context = {"genre_hint": genre_hint, "theme_hint": initial_prompt}
            idea_result = await self.orchestrator.run_refinable_task("generate_idea", idea_context)
            
            if idea_result.get("status") != "success":
                raise RuntimeError(f"Idea generation failed: {idea_result.get('message')}")
            
            final_idea = idea_result.get("final_content", {}).get("content", {})
            self.active_pipelines[pipeline_id]["steps"]["idea_generation"] = idea_result
            logger.info(f"[{pipeline_id}] ✅ Idea generated: '{final_idea.get('premise')}'")

            # --- المرحلة 2: بناء المخطط السردي (محاكاة حاليًا) ---
            logger.info(f"[{pipeline_id}] STAGE 2: Building a narrative blueprint (Mocked)...")
            # هذه الخطوة سيتم استبدالها باستدعاء حقيقي لـ `develop_story_blueprint` بعد تفعيله
            story_blueprint = self._mock_blueprint_creation(final_idea, num_chapters)
            self.active_pipelines[pipeline_id]["steps"]["blueprint_creation"] = story_blueprint.dict()
            logger.info(f"[{pipeline_id}] ✅ Blueprint created with {len(story_blueprint.chapters)} chapters.")

            # --- المرحلة 3: كتابة الفصول بناءً على المخطط ---
            logger.info(f"[{pipeline_id}] STAGE 3: Composing chapters based on the blueprint...")
            composed_chapters = []
            for i, chapter_outline in enumerate(story_blueprint.chapters):
                logger.info(f"  -> Composing Chapter {i+1}: '{chapter_outline.title}'")
                chapter_context = {"chapter_outline": chapter_outline}
                
                chapter_result = await self.orchestrator.run_refinable_task("compose_chapter", chapter_context)
                
                if chapter_result.get("status") != "success":
                    logger.warning(f"    ⚠️ Could not compose chapter {i+1}. Skipping.")
                    continue
                
                composed_chapters.append(chapter_result.get("final_content"))
            
            self.active_pipelines[pipeline_id]["steps"]["chapter_composition"] = composed_chapters
            if not composed_chapters:
                raise RuntimeError("Failed to compose any chapters for the story.")
            
            logger.info(f"[{pipeline_id}] ✅ All chapters composed.")

            # --- المرحلة 4: تجميع المنتج النهائي ---
            logger.info(f"[{pipeline_id}] STAGE 4: Assembling the final product...")
            final_product = {
                "title": final_idea.get("title", "قصة بدون عنوان"),
                "idea": final_idea,
                "blueprint": story_blueprint.dict(),
                "full_text": "\n\n---\n\n".join([ch.get("chapter_content", "") for ch in composed_chapters])
            }
            
            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            logger.info(f"🏁 [{pipeline_id}] Pipeline Completed Successfully!")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"❌ [{pipeline_id}] Pipeline failed: {e}", exc_info=True)
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    def _mock_blueprint_creation(self, idea: Dict, num_chapters: int) -> StoryBlueprint:
        """
        دالة وهمية لإنشاء مخطط. سيتم استبدالها بوكيل حقيقي لاحقًا.
        """
        chapters = []
        emotional_arc = ["الأمل", "الصراع", "الندم", "القبول", "السلام"]
        for i in range(num_chapters):
            chapter_outline = ChapterOutline(
                title=f"الفصل {i+1}: مرحلة جديدة",
                summary=f"هذا الفصل يركز على تطور الشخصية الرئيسية في مواجهة التحديات المستوحاة من فكرة: {idea.get('premise')}",
                emotional_focus=emotional_arc[i % len(emotional_arc)],
                key_events=[f"حدث رئيسي {i+1}-1", f"حدث رئيسي {i+1}-2"],
                character_arcs={"البطل": "يخطو خطوة جديدة في رحلته."}
            )
            chapters.append(chapter_outline)
            
        return StoryBlueprint(
            introduction=f"مقدمة للقصة التي تدور حول: {idea.get('premise')}",
            chapters=chapters,
            conclusion="خاتمة تترك أثرًا عميقًا لدى القارئ."
        )

# --- قسم الاختبار المتكامل ---
async def main_test():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود.")
        return

    logger.info("\n" + "="*80)
    logger.info("🔧 WorkflowManager - Full Story Generation Pipeline Test 🔧")
    logger.info("="*80)
    
    manager = WorkflowManager()
    
    # تعريف متطلبات القصة
    project_id = "story_001"
    initial_prompt = "رجل يكتشف أن ذكرياته ليست ملكه."
    genre_hint = "خيال علمي نفسي"
    
    try:
        # تشغيل سير العمل الكامل
        pipeline_result = await manager.create_short_story_from_idea(
            project_id=project_id,
            initial_prompt=initial_prompt,
            genre_hint=genre_hint,
            num_chapters=2 # قصة قصيرة جدًا للاختبار السريع
        )
        
        # طباعة النتائج النهائية
        print("\n--- ✅ Pipeline Completed Successfully! ---")
        final_product = pipeline_result.get('final_product', {})
        
        print(f"\n**Title:** {final_product.get('title')}")
        print("\n**Generated Idea:**")
        print(json.dumps(final_product.get('idea'), indent=2, ensure_ascii=False))
        
        print("\n**Full Story Text:**")
        print("--------------------")
        print(final_product.get('full_text'))
        print("--------------------")

    except Exception as e:
        logger.error(f"❌ Workflow test failed at the highest level: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main_test())
