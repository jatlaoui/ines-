# core/workflow_manager.py (النسخة الإبداعية)

import logging
import json
import asyncio
from typing import Dict, Any

from core.apollo_orchestrator import apollo
from services.web_search_service import web_inspiration_service # الخدمة الجديدة

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    def __init__(self):
        self.orchestrator = apollo
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def create_poem_in_style_of(
        self,
        project_id: str,
        artist_name: str,
        inspiration_source: str, # يمكن أن يكون رابط ويب أو نصًا
        poem_topic: str
    ) -> Dict[str, Any]:
        """
        خط إنتاج كامل لمحاكاة روح شاعر وكتابة قصيدة بأسلوبه.
        """
        pipeline_id = f"poem_creation_{project_id}"
        logger.info(f"🎨 [{pipeline_id}] Starting 'Poet Soul Emulation' Pipeline for {artist_name}...")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}
        
        try:
            # --- المرحلة 1: الاستلهام - فهم روح الشاعر ---
            logger.info(f"[{pipeline_id}] STAGE 1: Seeking inspiration and building Soul Profile...")
            
            # جلب المحتوى الملهم
            inspiration = await web_inspiration_service.get_inspiration_from_url(inspiration_source)
            if inspiration.get("status") != "success":
                raise RuntimeError(f"Inspiration fetching failed: {inspiration.get('message')}")
            
            source_text = inspiration["data"]["full_text_for_analysis"]
            
            # بناء الملف الروحي
            profile_context = {"text_content": source_text, "artist_name": artist_name}
            profile_result = await self.orchestrator.run_task("create_soul_profile", profile_context)
            if profile_result.get("status") != "success":
                raise RuntimeError(f"Soul profiling failed: {profile_result.get('message')}")
            
            soul_profile = profile_result["profile"]
            self.active_pipelines[pipeline_id]["steps"]["soul_profiling"] = soul_profile
            logger.info(f"[{pipeline_id}] ✅ Soul Profile for {artist_name} created successfully.")
            
            # --- المرحلة 2: المخاض الإبداعي - كتابة القصيدة ---
            logger.info(f"[{pipeline_id}] STAGE 2: Composing the poem with refinement cycle...")
            poem_context = {
                "topic": poem_topic,
                "soul_profile": soul_profile
            }
            
            # استدعاء مهمة كتابة الشعر القابلة للتحسين
            poem_result = await self.orchestrator.run_refinable_task("compose_poem", poem_context)

            if poem_result.get("status") != "success":
                raise RuntimeError(f"Poem composition failed: {poem_result.get('message')}")

            self.active_pipelines[pipeline_id]["steps"]["poem_composition"] = poem_result
            logger.info(f"[{pipeline_id}] ✅ Poem composed successfully!")

            # --- المرحلة 3: تجميع المنتج النهائي ---
            final_product = {
                "artist_inspiration": artist_name,
                "poem_topic": poem_topic,
                "soul_profile_summary": {
                    "themes": soul_profile.get('core_themes'),
                    "emotions": soul_profile.get('dominant_emotions')
                },
                "final_poem": poem_result.get("final_content"),
                "final_score": poem_result.get("final_score"),
            }
            
            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            logger.info(f"🏁 [{pipeline_id}] Pipeline Completed!")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"❌ [{pipeline_id}] Pipeline failed: {e}", exc_info=True)
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

# --- قسم الاختبار المحدث ---
async def main_test():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY is not set.")
        return

    manager = WorkflowManager()
    
    # تهيئة أبولو (مهم جدًا لأنها أصبحت async)
    await apollo.initialize()

    url = "https://blidetnet.fr.gd/%26%231576%3B%26%231604%3B%26%231602%3B%26%231575%3B%26%231587%3B%231605%3B-%26%231576%3B%26%231608%3B%26%231602%3B%26%231606%3B%26%231577%3B.htm"
    topic = "رسالة إلى الديار القديمة من مغترب طال به السفر"

    try:
        pipeline_result = await manager.create_poem_in_style_of(
            project_id="belaid_poem_creative_02",
            artist_name="بلقاسم بوقنة",
            inspiration_source=url,
            poem_topic=topic
        )
        
        print("\n" + "="*50)
        print("🎉🎉🎉 الـقـصـيـدة الـنـهـائـيـة 🎉🎉🎉")
        print("="*50)
        final_poem_data = pipeline_result.get('final_product', {}).get('final_poem', {}).get('content', {})
        
        print(f"\n**العنوان:** {final_poem_data.get('title')}\n")
        print(final_poem_data.get('poem_text').replace('\n', '\n'))
        
        print("\n" + "-"*50)
        print(f"**ملاحظات الشاعر (الوكيل):** {final_poem_data.get('inspiration_notes')}")
        print(f"**التقييم النهائي للجودة:** {pipeline_result.get('final_product', {}).get('final_score'):.2f} / 10.0")
        print("="*50)

    except Exception as e:
        logger.error(f"❌ Workflow test failed: {e}", exc_info=True)

    # لا تنس إغلاق اتصال httpx
    await web_inspiration_service.close()

if __name__ == "__main__":
    # تأكد من أن apollo_orchestrator الآن يحتوي على المهمة الجديدة
    # سأقوم بتحديثه ليشملها
    from agents.soul_profiler_agent import SoulProfilerAgent
    apollo.agents["soul_profiler"] = SoulProfilerAgent()
    apollo._task_registry["create_soul_profile"] = {
        "task_type": "analysis",
        "handler": apollo.agents["soul_profiler"].create_soul_profile
    }

    asyncio.run(main_test())
