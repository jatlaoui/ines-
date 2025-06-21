# core/workflow_manager.py (النسخة الكاملة مع خط الإنتاج المسرحي التونسي)
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

from core.apollo_orchestrator import apollo
from ingestion.ingestion_engine import InputType, ingestion_engine
# ... (استيراد نماذج البيانات إذا لزم الأمر)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    """
    يدير خطوط الإنتاج الإبداعية (Pipelines) التي تتكون من عدة مهام متسلسلة.
    """
    def __init__(self):
        self.orchestrator = apollo
        self.ingestion_engine = ingestion_engine
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    # --- دالة مساعدة لإدارة التفاعل مع المستخدم ---
    async def _handle_user_feedback(self, pipeline_id, step_name, step_result, user_feedback_fn, config):
        # ... (الكود كما هو، لا تغيير هنا)
        pass

    # --- خط الإنتاج الموحد والأساسي ---
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
                raise ValueError(f"Ingestion failed: {ingestion_result.error}")
            
            # محاكاة KnowledgeBase الآن
            knowledge_base = {"raw_text": ingestion_result.text_content, "metadata": ingestion_result.metadata}
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base

            # STEP 1: التوجيه إلى خط الإنتاج الفرعي
            creative_form = creation_config.get("creative_form", "novel")
            logger.info(f"[{pipeline_id}] ==> Routing to '{creative_form}' sub-pipeline...")

            sub_pipelines = {
                "novel": self._run_novel_sub_pipeline,
                "poem": self._run_poem_sub_pipeline,
                "tunisian_play": self._run_tunisian_play_sub_pipeline, # <-- خط الإنتاج الجديد
            }
            
            sub_pipeline_fn = sub_pipelines.get(creative_form)
            if not sub_pipeline_fn:
                raise ValueError(f"Creative form '{creative_form}' is not supported.")
            
            final_product = await sub_pipeline_fn(pipeline_id, knowledge_base, creation_config, user_feedback_fn)

            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"[{pipeline_id}] Pipeline failed: {e}")
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    # --- خطوط الإنتاج الفرعية (Sub-Pipelines) ---

    async def _run_novel_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        logger.info(f"[{pipeline_id}] -> Engaging Novel Production Sub-Pipeline...")
        # ... (منطق كتابة الرواية)
        return {"result": "Novel sub-pipeline executed."}

    async def _run_poem_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        logger.info(f"[{pipeline_id}] -> Engaging Poem Production Sub-Pipeline...")
        # ... (منطق كتابة القصيدة)
        return {"result": "Poem sub-pipeline executed."}
        
    # --- خط الإنتاج المسرحي التونسي الجديد ---
    async def _run_tunisian_play_sub_pipeline(
        self,
        pipeline_id: str,
        knowledge_base: Dict[str, Any],
        user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        خط إنتاج فرعي متخصص لكتابة مسرحية تونسية.
        """
        logger.info(f"[{pipeline_id}] -> Engaging Tunisian Playwriting Sub-Pipeline...")
        
        # هنا، سنقوم بمحاكاة بناء مسرحية من عدة مشاهد
        scenes = user_config.get("scenes_outline", []) # يفترض أن المستخدم قدم مخططًا للمشاهد
        
        if not scenes:
             # إذا لم يقدم المستخدم مخططًا، ننشئ واحدًا افتراضيًا
            scenes = [
                {
                    "title": "مشهد 1: المقهى",
                    "location": "cafe",
                    "location_name": "مقهى شعبي في تونس العاصمة",
                    "interactions": [{"character_name": "الحاجة", "character_archetype": "al_hajja", "topic": "الزواج", "mood": "قلق"}]
                },
                {
                    "title": "مشهد 2: السوق",
                    "location": "souk",
                    "location_name": "سوق العطارين",
                    "interactions": [{"character_name": "الشابة", "character_archetype": "al_mothaqafa", "topic": "المستقبل", "mood": "طموح"}]
                }
            ]

        full_play_script = ""
        for i, scene_outline in enumerate(scenes):
            logger.info(f"[{pipeline_id}] ==> Composing Scene {i+1}: {scene_outline['title']}")
            
            scene_result = await self.orchestrator.run_refinable_task(
                task_name="construct_tunisian_play_scene",
                initial_context={"scene_outline": scene_outline},
                user_config=user_config
            )
            
            script_content = scene_result.get("final_content", {}).get("content", {}).get("scene_script", "")
            full_play_script += script_content + "\n\n"
        
        self.active_pipelines[pipeline_id]["steps"]["full_raw_script"] = full_play_script
        
        # يمكن إضافة خطوة إخراجية نهائية هنا إذا لزم الأمر
        
        logger.info(f"[{pipeline_id}] Tunisian Playwriting pipeline completed.")
        return {"final_script": full_play_script}
