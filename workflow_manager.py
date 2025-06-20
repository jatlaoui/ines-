# workflow_manager.py (الإصدار المحدث مع خطوط إنتاج متخصصة)
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

# استيراد المنسق الرئيسي الذي سيقوم بتشغيل المهام الفردية
from core.apollo_orchestrator import apollo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    """
    يدير خطوط الإنتاج الإبداعية (Pipelines) التي تتكون من عدة مهام متسلسلة.
    """
    def __init__(self):
        self.orchestrator = apollo
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def run_story_pipeline(
        # ... (الكود كما هو في الرد السابق، لا حاجة لتغييره)
    ):
        pass

    async def run_poem_pipeline(
        # ... (الكود كما هو في الرد السابق، لا حاجة لتغييره)
    ):
        pass

    # --- خط إنتاج جديد ومتخصص ---
    async def run_crime_novel_pipeline(
        self,
        user_id: str,
        project_id: str,
        user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        خط إنتاج متخصص لكتابة رواية جريمة وغموض.
        """
        pipeline_id = f"crime_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Crime Novel Pipeline'")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # --- الخطوة 1: توليد فكرة جريمة ---
            logger.info(f"[{pipeline_id}] ==> STEP 1: Generating Crime Idea...")
            # نمرر سياقًا متخصصًا لمولد الأفكار
            crime_idea_context = {**user_config, "genre_hint": "جريمة وغموض"}
            idea_result = await self.orchestrator.run_refinable_task(
                task_name="generate_idea",
                initial_context=crime_idea_context,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["idea"] = idea_result
            
            # --- الخطوة 2: تحليل منطق الجريمة المقترح ---
            logger.info(f"[{pipeline_id}] ==> STEP 2: Forensic Logic Analysis of the Premise...")
            forensic_context = {"text_content": idea_result.get("final_content", {}).get("premise", "")}
            forensic_analysis = await self.orchestrator.run_refinable_task(
                task_name="analyze_crime_narrative",
                initial_context=forensic_context,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["forensic_analysis"] = forensic_analysis

            # --- الخطوة 3: بناء مخطط مبني على التحليل الجنائي ---
            logger.info(f"[{pipeline_id}] ==> STEP 3: Building Forensic-Aware Blueprint...")
            blueprint_context = {
                "idea": idea_result.get("final_content"),
                "forensic_report": forensic_analysis.get("final_content") # نمرر تقرير التحليل
            }
            blueprint_result = await self.orchestrator.run_refinable_task(
                task_name="generate_blueprint",
                initial_context=blueprint_context,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result

            # --- يمكن إضافة خطوات أخرى مثل بناء ملفات نفسية للمشتبه بهم والضحية ---
            # ...

            self.active_pipelines[pipeline_id]["status"] = "completed"
            logger.info(f"[{pipeline_id}] 'Crime Novel Pipeline' completed successfully.")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            # ... (معالجة الأخطاء) ...
            raise

# ... (بقية الكود ودالة الاختبار `if __name__ == "__main__":`)
