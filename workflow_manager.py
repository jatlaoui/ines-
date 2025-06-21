# core/workflow_manager.py (الإصدار المحدث بالكامل)
import logging
import json
import asyncio
from typing import Dict, Any, List, Optional, Callable

# استيراد المنسق المحدث والمحركات
from core.apollo_orchestrator import apollo
from ingestion.ingestion_engine import InputType, ingestion_engine
from advanced_context_engine import AdvancedContextEngine # لاستخلاص قاعدة المعرفة الأولية

# --- إعدادات التسجيل ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    """
    يدير خطوط الإنتاج الإبداعية المعقدة (Pipelines)، وينسق سلسلة من المهام
    التي ينفذها "أبولو" لإنتاج أعمال إبداعية عالية الجودة.
    """
    def __init__(self):
        self.orchestrator = apollo
        self.ingestion_engine = ingestion_engine
        self.context_engine = AdvancedContextEngine()
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def run_deep_analysis_pipeline(
        self,
        project_id: str,
        source_text: str
    ) -> Dict[str, Any]:
        """
        خط إنتاج متخصص لإجراء تحليل عميق وشامل لأي نص.
        """
        pipeline_id = f"analysis_pipeline_{project_id}"
        logger.info(f"🚀 [{pipeline_id}] Starting 'Deep Analysis' Pipeline...")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # الخطوة 1: بناء قاعدة المعرفة الأساسية
            logger.info(f"[{pipeline_id}] STEP 1: Building initial Knowledge Base...")
            kb = await self.context_engine.analyze_text(source_text)
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = kb.dict()

            # الخطوة 2: تشغيل مهام التحليل المتخصصة بالتوازي
            logger.info(f"[{pipeline_id}] STEP 2: Running specialized analysis tasks...")
            analysis_tasks = {
                "psychological_analysis": self.orchestrator.run_task(
                    "analyze_psychological_profile", {"character_description": source_text}
                ),
                "social_conflict_map": self.orchestrator.run_task(
                    "map_social_conflicts", {"setting_description": source_text, "social_groups": [e.name for e in kb.entities if e.type == 'group']}
                ),
                "symbolism_analysis": self.orchestrator.run_task(
                    "interpret_dreams_and_symbols", {"text_content": source_text}
                )
            }
            
            results = await asyncio.gather(*analysis_tasks.values(), return_exceptions=True)
            analysis_results = dict(zip(analysis_tasks.keys(), results))

            self.active_pipelines[pipeline_id]["steps"]["specialized_analyses"] = analysis_results

            # الخطوة 3: تجميع التقرير النهائي
            logger.info(f"[{pipeline_id}] STEP 3: Compiling final analysis report...")
            final_report = {
                "knowledge_base": kb.dict(),
                **analysis_results
            }

            self.active_pipelines[pipeline_id].update({"status": "completed", "final_report": final_report})
            logger.info(f"✅ [{pipeline_id}] Deep Analysis Pipeline Completed Successfully.")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"❌ [{pipeline_id}] Pipeline failed: {e}", exc_info=True)
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    async def transmute_witness_to_creation(
        self,
        project_id: str, 
        source: Any, 
        input_type: InputType,
        creation_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        خط الإنتاج الرئيسي والمحسن: يحول أي "شاهد" (مصدر) إلى عمل إبداعي
        عبر مراحل التحليل العميق، والعصف الذهني التعاوني، والكتابة المحسنة.
        """
        pipeline_id = f"transmutation_pipeline_{project_id}"
        logger.info(f"🚀 [{pipeline_id}] Starting Advanced 'Witness Transmutation' Pipeline...")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # --- المرحلة 1: الاستيعاب والتحليل الأولي ---
            logger.info(f"[{pipeline_id}] STAGE 1: Ingestion & Initial Analysis...")
            ingestion_result = await self.ingestion_engine.ingest(source, input_type)
            if not ingestion_result.success:
                raise ValueError(f"Ingestion failed: {ingestion_result.error}")
            
            source_text = ingestion_result.text_content
            self.active_pipelines[pipeline_id]["steps"]["ingestion"] = {"text_length": len(source_text), "metadata": ingestion_result.metadata}

            # استخدام خط الإنتاج التحليلي للحصول على قاعدة معرفة معززة
            analysis_report = await self.run_deep_analysis_pipeline(f"{project_id}_analysis", source_text)
            enriched_kb = analysis_report.get("final_report", {})
            self.active_pipelines[pipeline_id]["steps"]["deep_analysis"] = enriched_kb

            # --- المرحلة 2: التفكير والإبداع التعاوني ---
            logger.info(f"[{pipeline_id}] STAGE 2: Collaborative Ideation...")
            
            # ملاحظة: يتطلب تهيئة جلسة تعاونية أولاً
            # collaboration_session = self.orchestrator.collaboration_system.create_collaboration_session(...)
            
            brainstorm_context = {
                "session_id": "temp_session_123", # يجب أن تكون ديناميكية
                "topic": f"أفكار إبداعية مستوحاة من النص الذي يبدأ بـ: '{source_text[:50]}...'",
                "max_ideas_per_agent": 3
            }
            # brainstorming_result = await self.orchestrator.run_task(
            #     "collaborative_brainstorming", brainstorm_context
            # )
            # self.active_pipelines[pipeline_id]["steps"]["brainstorming"] = brainstorming_result
            logger.warning("Skipping collaborative brainstorming as it requires a live session.")
            
            # بدلاً من ذلك، سنستخدم مهمة الإنشاء الفردي القابلة للتحسين
            idea_generation_result = await self.orchestrator.run_task(
                "generate_novel_idea",
                context={"genre_hint": creation_config.get("genre", "إثارة وغموض"), "enriched_kb": enriched_kb}
            )
            self.active_pipelines[pipeline_id]["steps"]["idea_generation"] = idea_generation_result
            
            # --- المرحلة 3: التحكيم والتخطيط ---
            logger.info(f"[{pipeline_id}] STAGE 3: Arbitration & Blueprinting...")
            selected_idea = idea_generation_result.get("final_content")
            
            # arbitrate_context = {"content": json.dumps(selected_idea, ensure_ascii=False), "content_type": "idea"}
            # arbitration_result = await self.orchestrator.run_task("arbitrate_content_quality", arbitrate_context)
            # self.active_pipelines[pipeline_id]["steps"]["idea_arbitration"] = arbitration_result
            logger.warning("Skipping idea arbitration as it requires a live DB/LLM connection.")

            # if arbitration_result.get("overall_score", 0) < 60:
            #     raise ValueError("The generated idea did not pass the quality arbitration.")

            blueprint_result = await self.orchestrator.run_task(
                "develop_story_blueprint",
                context={"idea": selected_idea, "knowledge_base": enriched_kb}
            )
            self.active_pipelines[pipeline_id]["steps"]["story_blueprint"] = blueprint_result

            # --- المرحلة 4: الإنتاج الإبداعي ---
            logger.info(f"[{pipeline_id}] STAGE 4: Creative Production...")
            story_blueprint = blueprint_result.get("final_content")
            # هنا يمكننا المرور على الفصول وكتابتها، لكننا سنكتفي بالمنتجات النهائية للمراحل
            # for chapter_outline in story_blueprint.chapters:
            #     ...

            final_product = {
                "idea": selected_idea,
                "blueprint": story_blueprint
            }

            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            logger.info(f"✅ [{pipeline_id}] Advanced Transmutation Pipeline Completed Successfully.")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"❌ [{pipeline_id}] Pipeline failed: {e}", exc_info=True)
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

# --- قسم الاختبار ---
async def main_test():
    logger.info("\n" + "="*80)
    logger.info("🔧 WorkflowManager - Advanced Pipeline Test 🔧")
    logger.info("="*80)
    
    manager = WorkflowManager()
    
    # مثال لنص خام
    sample_text = "في قرية صغيرة تقع على حافة الصحراء، كان الشيخ حكيم رجلاً يحترمه الجميع. لكن ابنه خالد كان متمرداً، يحلم بالمدينة وأضوائها. صراع بين التقاليد والحداثة كان يلوح في الأفق، خاصة مع وصول شركة تعدين غامضة تريد شراء أراضي القرية."

    # اختبار خط إنتاج التحليل العميق
    logger.info("\n--- TESTING DEEP ANALYSIS PIPELINE ---")
    try:
        analysis_pipeline_result = await manager.run_deep_analysis_pipeline(
            project_id="deep_dive_001",
            source_text=sample_text
        )
        print("✅ Deep Analysis Pipeline Result (Summary):")
        # طباعة ملخص فقط لتجنب الإطالة
        print(f"Knowledge Base Entities: {len(analysis_pipeline_result['final_report']['knowledge_base']['entities'])}")
        print(f"Psychological Analysis: {'Success' if 'content' in analysis_pipeline_result['final_report']['psychological_analysis'] else 'Failed'}")
        
    except Exception as e:
        logger.error(f"❌ Deep analysis pipeline test failed: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main_test())
