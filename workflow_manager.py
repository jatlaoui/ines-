# core/workflow_manager.py (النسخة النهائية والمفعّلة)

import logging
import json
import asyncio
from typing import Dict, Any, List

from core.apollo_orchestrator import apollo
# نفترض أن ingestion و context engine موجودان في مجلد engines
from engines.advanced_context_engine import AdvancedContextEngine
# استيراد نماذج البيانات
from agents.blueprint_architect_agent import StoryBlueprint, ChapterOutline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    """
    يدير خطوط الإنتاج الإبداعية الكاملة (Pipelines) من البداية إلى النهاية.
    """
    def __init__(self):
        self.orchestrator = apollo
        self.context_engine = AdvancedContextEngine()
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def create_narrative_from_text(
        self,
        project_id: str,
        source_text: str,
        genre_hint: str = "دراما تاريخية",
        num_chapters: int = 3
    ) -> Dict[str, Any]:
        """
        خط الإنتاج الرئيسي: يأخذ نصًا خامًا ويحوله إلى قصة قصيرة متكاملة.
        """
        pipeline_id = f"narrative_{project_id}"
        logger.info(f"🚀 [{pipeline_id}] Starting 'Text-to-Narrative' Pipeline...")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}
        
        try:
            # --- المرحلة 1: الفهم والتحليل العميق ---
            logger.info(f"[{pipeline_id}] STAGE 1: Deep analysis of the source text...")
            knowledge_base = await self.context_engine.analyze_text(source_text)
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base.dict()
            logger.info(f"[{pipeline_id}] ✅ KnowledgeBase created.")

            # --- المرحلة 2: بناء المخطط السردي ---
            logger.info(f"[{pipeline_id}] STAGE 2: Developing a narrative blueprint...")
            blueprint_context = {"knowledge_base": knowledge_base.dict()}
            blueprint_result = await self.orchestrator.run_task("develop_blueprint", blueprint_context)
            if blueprint_result.get("status") != "success":
                raise RuntimeError(f"Blueprint creation failed: {blueprint_result.get('message')}")

            final_blueprint_dict = blueprint_result.get("final_content").get("blueprint")
            final_blueprint = StoryBlueprint.parse_obj(final_blueprint_dict)
            self.active_pipelines[pipeline_id]["steps"]["blueprint_creation"] = final_blueprint.dict()
            logger.info(f"[{pipeline_id}] ✅ Blueprint developed successfully.")

            # --- المرحلة 3: كتابة الفصول ---
            logger.info(f"[{pipeline_id}] STAGE 3: Composing chapters...")
            composed_chapters = []
            for i, chapter_outline_data in enumerate(final_blueprint.chapters):
                # التأكد من أن chapter_outline_data هو كائن ChapterOutline
                chapter_outline = ChapterOutline.parse_obj(chapter_outline_data)
                logger.info(f"  -> Composing Chapter {i+1}: '{chapter_outline.title}'")
                chapter_context = {"chapter_outline": chapter_outline}
                chapter_result = await self.orchestrator.run_task("compose_chapter", chapter_context)
                
                if chapter_result.get("status") == "success":
                    composed_chapters.append(chapter_result.get("final_content"))
            
            self.active_pipelines[pipeline_id]["steps"]["chapter_composition"] = composed_chapters
            logger.info(f"[{pipeline_id}] ✅ Chapters composed.")
            
            # --- المرحلة 4: تجميع المنتج النهائي ---
            final_product = {
                "title": f"رواية مستوحاة من: {source_text[:20]}...",
                "knowledge_base_summary": {
                    "entities": len(knowledge_base.entities),
                    "relationships": len(knowledge_base.relationship_graph)
                },
                "blueprint": final_blueprint.dict(),
                "chapters": composed_chapters
            }
            
            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            logger.info(f"🏁 [{pipeline_id}] Pipeline Completed Successfully!")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"❌ [{pipeline_id}] Pipeline failed: {e}", exc_info=True)
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

# --- قسم الاختبار النهائي ---
async def main_test():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود.")
        return

    logger.info("\n" + "="*80)
    logger.info("🔧 WorkflowManager - FULL End-to-End Test 🔧")
    logger.info("="*80)
    
    manager = WorkflowManager()
    
    # نص تاريخي عن صالح بن يوسف كمصدر
    source_text = """
    كان صالح بن يوسف زعيماً وطنياً تونسياً، اختلف مع الحبيب بورقيبة حول استراتيجية الاستقلال.
    آمن بن يوسف بضرورة الكفاح المسلح والاستقلال التام والفوري عن فرنسا، بينما فضل بورقيبة نهج المراحل والتفاوض.
    أدى هذا الخلاف إلى انقسام حاد في الحزب الدستوري الجديد وفي الشارع التونسي. 
    في مؤتمر صفاقس عام 1955، تم تجريد بن يوسف من مناصبه. شعر بالخذلان والمرارة.
    لاحقاً، تم اغتياله في ألمانيا عام 1961 في ظروف غامضة، مما ترك جرحاً عميقاً في تاريخ تونس الحديث.
    """

    try:
        pipeline_result = await manager.create_narrative_from_text(
            project_id="salah_ben_youssef_story",
            source_text=source_text,
            num_chapters=2 # للاختبار السريع
        )
        
        print("\n--- ✅ Pipeline Completed! Final Product Summary: ---")
        final_product = pipeline_result.get('final_product', {})
        
        print(f"\n**Title:** {final_product.get('title')}")
        print("\n**Generated Blueprint Summary:**")
        blueprint = final_product.get('blueprint', {})
        print(f"  - Main Conflict: {blueprint.get('main_conflict')}")
        print(f"  - Themes: {blueprint.get('themes')}")
        print(f"  - Chapters: {len(blueprint.get('chapters', []))}")
        
        print("\n**Generated Chapters:**")
        for i, chapter in enumerate(final_product.get('chapters', [])):
            print(f"  --- Chapter {i+1}: {chapter.get('title')} ---")
            print(f"  Content snippet: {chapter.get('chapter_content', '')[:100]}...")
            print(f"  Quality Score: {chapter.get('quality_score')}")

    except Exception as e:
        logger.error(f"❌ Workflow test failed at the highest level: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main_test())
