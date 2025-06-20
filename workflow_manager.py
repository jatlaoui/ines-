# core/workflow_manager.py (النسخة الكاملة مع خط الإنتاج المسرحي)
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

# استيراد المنسق الرئيسي الذي سيقوم بتشغيل المهام الفردية
from core.apollo_orchestrator import apollo
from ingestion.ingestion_engine import InputType, ingestion_engine
# استيراد نماذج البيانات اللازمة للتمرير بين المهام
from agents.blueprint_architect_agent import StoryBlueprint, ChapterOutline
from agents.dramaturg_agent import DramaticBlueprint # يفترض وجود هذا النموذج في الملف
from agents.character_arc_agent import CharacterArcMap # يفترض وجود هذا النموذج في الملف

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    """
    يدير خطوط الإنتاج الإبداعية (Pipelines) التي تتكون من عدة مهام متسلسلة،
    مع دعم نقاط التوقف التفاعلية للمستخدم والتعامل مع مدخلات متعددة.
    """
    def __init__(self):
        """
        تهيئة مدير سير العمل.
        """
        self.orchestrator = apollo
        self.ingestion_engine = ingestion_engine
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def _handle_user_feedback(
        self,
        pipeline_id: str,
        step_name: str,
        step_result: Dict[str, Any],
        user_feedback_fn: Optional[Callable],
        user_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """دالة مساعدة لإدارة تفاعل المستخدم."""
        if user_feedback_fn and step_name in user_config.get("user_checkpoints", []):
            logger.info(f"[{pipeline_id}] Awaiting user feedback on '{step_name}'...")
            user_action = await user_feedback_fn(step_name, step_result.get("final_content"))
            
            if isinstance(user_action, dict):
                logger.info(f"[{pipeline_id}] User modified the '{step_name}'.")
                step_result["final_content"] = user_action
            elif user_action == "regenerate":
                raise InterruptedError(f"User requested regeneration at step: {step_name}")
        return step_result

    async def transmute_witness(
        self,
        user_id: str, project_id: str, source: Any, input_type: InputType,
        creation_config: Dict[str, Any], user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        خط الإنتاج الموحد الجديد: يستوعب أي شاهد ويحوله إلى إبداع.
        """
        pipeline_id = f"transmute_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Witness Transmutation' Pipeline")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # STEP 0: استيعاب الشاهد
            ingestion_result = await self.ingestion_engine.ingest(source, input_type)
            if not ingestion_result.success:
                raise ValueError(f"فشل في استيعاب المصدر: {ingestion_result.error}")
            
            witness_content = ingestion_result.text_content
            witness_metadata = ingestion_result.metadata
            self.active_pipelines[pipeline_id]["steps"]["ingestion"] = {"success": True, "metadata": witness_metadata}
            
            # STEP 1: تحليل الشاهد
            # knowledge_base_result = await self.orchestrator.run_refinable_task(...)
            # محاكاة KnowledgeBase الآن
            knowledge_base = {"raw_text": witness_content, "entities": [], "relationship_graph": [], "emotional_arc": []}
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base

            # STEP 2: التوجيه إلى خط الإنتاج الفرعي
            creative_form = creation_config.get("creative_form", "novel")
            logger.info(f"[{pipeline_id}] ==> Routing to '{creative_form}' sub-pipeline...")

            sub_pipelines = {
                "novel": self._run_novel_sub_pipeline,
                "poem": self._run_poem_sub_pipeline,
                "play": self._run_play_sub_pipeline, # <-- خط الإنتاج المسرحي الجديد
            }
            
            sub_pipeline_fn = sub_pipelines.get(creative_form)
            if not sub_pipeline_fn:
                raise ValueError(f"Creative form '{creative_form}' is not supported.")
            
            final_product = await sub_pipeline_fn(pipeline_id, knowledge_base, creation_config, user_feedback_fn)

            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            logger.info(f"[{pipeline_id}] Pipeline completed successfully.")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"[{pipeline_id}] Pipeline failed: {e}")
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    # --- خطوط الإنتاج الفرعية ---

    async def _run_novel_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        # (الكود كما هو، لا تغيير هنا)
        logger.info(f"[{pipeline_id}] -> Engaging Novel Production Sub-Pipeline...")
        # ...
        return {"result": "Novel sub-pipeline executed."}

    async def _run_poem_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        # (الكود كما هو، لا تغيير هنا)
        logger.info(f"[{pipeline_id}] -> Engaging Poem Production Sub-Pipeline...")
        # ...
        return {"result": "Poem sub-pipeline executed."}

    # --- خط الإنتاج المسرحي الجديد ---
    async def _run_play_sub_pipeline(
        self,
        pipeline_id: str,
        knowledge_base: Dict[str, Any],
        user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        خط الإنتاج الفرعي لكتابة مسرحية كاملة بشكل آلي.
        """
        logger.info(f"[{pipeline_id}] -> Engaging Playwriting Sub-Pipeline...")

        # STEP 1: توليد الفكرة الدرامية
        logger.info(f"[{pipeline_id}] ==> STEP 1 (Play): Generating Dramatic Idea...")
        idea_context = {
            "genre_hint": "مسرحية",
            "knowledge_base": knowledge_base # نمرر قاعدة المعرفة كمصدر إلهام
        }
        idea_result = await self.orchestrator.run_refinable_task("generate_idea", idea_context, user_config)
        self.active_pipelines[pipeline_id]["steps"]["play_idea"] = idea_result
        idea_result = await self._handle_user_feedback(pipeline_id, "play_idea", idea_result, user_feedback_fn, user_config)
        
        # STEP 2: بناء المخطط الدرامي
        logger.info(f"[{pipeline_id}] ==> STEP 2 (Play): Building Dramatic Blueprint...")
        dramatic_blueprint_result = await self.orchestrator.run_refinable_task(
            task_name="generate_dramatic_blueprint",
            initial_context={"idea": idea_result["final_content"]},
            user_config=user_config
        )
        self.active_pipelines[pipeline_id]["steps"]["dramatic_blueprint"] = dramatic_blueprint_result
        await self._handle_user_feedback(pipeline_id, "dramatic_blueprint", dramatic_blueprint_result, user_feedback_fn, user_config)

        # STEP 3: بناء أقواس تطور الشخصيات
        logger.info(f"[{pipeline_id}] ==> STEP 3 (Play): Developing Character Arcs...")
        character_arcs_result = await self.orchestrator.run_refinable_task(
            task_name="develop_character_arcs",
            initial_context={"blueprint": dramatic_blueprint_result["final_content"]},
            user_config=user_config
        )
        self.active_pipelines[pipeline_id]["steps"]["character_arcs"] = character_arcs_result

        # STEP 4: كتابة فصول (مشاهد) المسرحية
        logger.info(f"[{pipeline_id}] ==> STEP 4 (Play): Composing Scenes...")
        full_play_script = ""
        blueprint_content = dramatic_blueprint_result["final_content"]
        arcs_content = character_arcs_result["final_content"]
        
        # حلقة لكتابة كل فصل/مشهد بناءً على المخطط
        for act in blueprint_content.get("acts", []):
            for chapter_outline in act.get("key_events", []): # نفترض أن الأحداث الرئيسية هي المشاهد
                logger.info(f"[{pipeline_id}]   -> Composing scene: {chapter_outline}")
                chapter_context = {
                    "chapter_outline": {"title": act.get("title"), "summary": chapter_outline, "emotional_focus": "متغير", "key_events": [chapter_outline], "character_arcs": {}},
                    "character_arcs": arcs_content
                }
                chapter_script_result = await self.orchestrator.run_refinable_task(
                    task_name="generate_play_chapter",
                    initial_context=chapter_context,
                    user_config=user_config
                )
                # استخلاص النص المكتوب
                script_content = chapter_script_result.get("final_content", {}).get("content", {}).get("chapter_content", "")
                full_play_script += script_content + "\n\n---\n\n"
        
        self.active_pipelines[pipeline_id]["steps"]["raw_script"] = {"content": full_play_script}

        # STEP 5: إضافة التوجيهات الإخراجية النهائية
        logger.info(f"[{pipeline_id}] ==> STEP 5 (Play): Adding Staging Directions...")
        final_script_result = await self.orchestrator.run_refinable_task(
            task_name="add_staging_directions",
            initial_context={"script": full_play_script},
            user_config=user_config
        )
        self.active_pipelines[pipeline_id]["steps"]["final_script"] = final_script_result

        logger.info(f"[{pipeline_id}] Playwriting pipeline completed successfully.")
        return final_script_result
