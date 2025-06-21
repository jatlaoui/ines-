# core/workflow_manager.py

import logging
import json
import asyncio
from typing import Dict, Any

from core.apollo_orchestrator import apollo
from engines.advanced_context_engine import AdvancedContextEngine
from services.web_search_service import web_search_service
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

    async def create_poem_from_url(self, project_id: str, style_inspiration_url: str, poem_topic: str) -> Dict[str, Any]:
        """
        خط إنتاج لكتابة شعر بأسلوب معين مستوحى من محتوى رابط ويب.
        """
        pipeline_id = f"poem_{project_id}"
        logger.info(f"🚀 [{pipeline_id}] Starting 'Poem from URL Inspiration' Pipeline...")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}
        
        try:
            # --- المرحلة 1: جلب وتحليل المصدر ---
            logger.info(f"[{pipeline_id}] STAGE 1: Fetching and analyzing inspiration from URL...")
            fetch_result = await web_search_service.fetch_direct_url_content(style_inspiration_url)
            if fetch_result.get("status") != "success":
                raise RuntimeError(f"Failed to fetch content from URL: {fetch_result.get('message')}")
            
            source_text = fetch_result["data"]["content"]
            
            knowledge_base = await self.context_engine.analyze_text(source_text)
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base.dict()
            logger.info(f"[{pipeline_id}] ✅ Inspiration KnowledgeBase created.")
            
            kb_for_prompt = {
                "themes": [rel.relation for rel in knowledge_base.relationship_graph if "يشعر" in rel.relation][:3],
                "vocabulary": [e.name for e in knowledge_base.entities if e.importance_score > 6][:5],
                "imagery": [e.name for e in knowledge_base.entities if e.type == 'مكان' or 'رمز' in e.type][:3]
            }

            # --- المرحلة 2: كتابة القصيدة مع التحسين ---
            logger.info(f"[{pipeline_id}] STAGE 2: Composing the poem with refinement...")
            poem_context = {"topic": poem_topic, "knowledge_base": kb_for_prompt}
            
            poem_result = await self.orchestrator.run_refinable_task("compose_poem", poem_context)

            if poem_result.get("status") != "success":
                raise RuntimeError(f"Poem composition failed: {poem_result.get('message')}")
            
            self.active_pipelines[pipeline_id]["steps"]["poem_composition"] = poem_result
            logger.info(f"[{pipeline_id}] ✅ Poem composed successfully!")

            # --- المرحلة 3: تجميع المنتج النهائي ---
            final_product = {
                "inspiration_url": style_inspiration_url,
                "poem_topic": poem_topic,
                "final_poem": poem_result.get("final_content"),
                "final_score": poem_result.get("final_score"),
                "cycles_used": poem_result.get("refinement_cycles_used")
            }
            
            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            logger.info(f"🏁 [{pipeline_id}] Pipeline Completed Successfully!")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"❌ [{pipeline_id}] Pipeline failed: {e}", exc_info=True)
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

# --- قسم الاختبار ---
async def main_test():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY environment variable is not set.")
        return

    manager = WorkflowManager()
    url = "https://blidetnet.fr.gd/%26%231576%3B%26%231604%3B%26%231602%3B%26%231575%3B%26%231587%3B%231605%3B-%26%231576%3B%26%231608%3B%26%231602%3B%26%231606%3B%26%231577%3B.htm"
    topic = "الحنين إلى الديار القديمة بعد طول غياب"

    try:
        pipeline_result = await manager.create_poem_from_url(
            project_id="belgassem_bouganna_poem_01",
            style_inspiration_url=url,
            poem_topic=topic
        )
        
        print("\n--- ✅ Poem Pipeline Completed! ---")
        final_poem_data = pipeline_result.get('final_product', {}).get('final_poem', {}).get('content', {})
        
        print(f"\n**العنوان:** {final_poem_data.get('title')}")
        print("-" * 20)
        print(final_poem_data.get('poem_text'))
        print("-" * 20)
        print(f"**ملاحظات الأسلوب:** {final_poem_data.get('style_notes')}")
        print(f"**التقييم النهائي:** {pipeline_result.get('final_product', {}).get('final_score')}")

    except Exception as e:
        logger.error(f"❌ Poem workflow test failed: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main_test())
