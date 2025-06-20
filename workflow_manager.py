# workflow_manager.py (النسخة الكاملة والمحدثة مع خطوط إنتاج متخصصة)
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
    يدير خطوط الإنتاج الإبداعية (Pipelines) التي تتكون من عدة مهام متسلسلة،
    مع دعم نقاط التوقف التفاعلية للمستخدم.
    """
    def __init__(self):
        """
        تهيئة مدير سير العمل. يستخدم المثيل الوحيد من "أبولو".
        """
        self.orchestrator = apollo
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def _handle_user_feedback(
        self,
        pipeline_id: str,
        step_name: str,
        step_result: Dict[str, Any],
        user_feedback_fn: Callable,
        user_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """دالة مساعدة لإدارة تفاعل المستخدم."""
        if user_feedback_fn and step_name in user_config.get("user_checkpoints", []):
            logger.info(f"[{pipeline_id}] Awaiting user feedback on '{step_name}'...")
            user_action = await user_feedback_fn(step_name, step_result.get("final_content"))
            
            if isinstance(user_action, dict): # User provided a modified version
                logger.info(f"[{pipeline_id}] User modified the '{step_name}'.")
                step_result["final_content"] = user_action
            elif user_action == "regenerate":
                raise InterruptedError(f"User requested regeneration at step: {step_name}")
        return step_result

    async def run_story_pipeline(
        self,
        user_id: str, project_id: str, user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        يشغل خط إنتاج كامل للرواية: من الفكرة -> المخطط -> الفصل الأول.
        """
        pipeline_id = f"pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Story Pipeline' for project {project_id}")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}
        
        try:
            # STEP 1: Generate Idea
            idea_result = await self.orchestrator.run_refinable_task("generate_idea", user_config, user_config)
            self.active_pipelines[pipeline_id]["steps"]["idea"] = idea_result
            idea_result = await self._handle_user_feedback(pipeline_id, "idea", idea_result, user_feedback_fn, user_config)

            # STEP 2: Generate Blueprint
            blueprint_result = await self.orchestrator.run_refinable_task("generate_blueprint", idea_result["final_content"], user_config)
            self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
            blueprint_result = await self._handle_user_feedback(pipeline_id, "blueprint", blueprint_result, user_feedback_fn, user_config)

            # STEP 3: Generate Chapter 1
            first_chapter_outline = blueprint_result["final_content"].chapters[0]
            chapter_result = await self.orchestrator.run_refinable_task("generate_chapter", first_chapter_outline, user_config)
            self.active_pipelines[pipeline_id]["steps"]["chapter_1"] = chapter_result

            self.active_pipelines[pipeline_id]["status"] = "completed"
            logger.info(f"[{pipeline_id}] 'Story Pipeline' completed successfully.")
            return self.active_pipelines[pipeline_id]

        except InterruptedError as e:
            logger.info(f"[{pipeline_id}] Pipeline interrupted by user: {e}. Restarting...")
            return await self.run_story_pipeline(user_id, project_id, user_config, user_feedback_fn)
        except Exception as e:
            logger.error(f"[{pipeline_id}] Pipeline failed: {e}")
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    async def run_poem_pipeline(
        self,
        user_id: str, project_id: str, user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        يشغل خط إنتاج متخصص لكتابة قصيدة.
        """
        pipeline_id = f"poem_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Poem Pipeline'")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # STEP 1: Generate Poem
            poem_result = await self.orchestrator.run_refinable_task("generate_poem", user_config, user_config)
            self.active_pipelines[pipeline_id]["steps"]["poem"] = poem_result
            await self._handle_user_feedback(pipeline_id, "poem", poem_result, user_feedback_fn, user_config)

            self.active_pipelines[pipeline_id]["status"] = "completed"
            logger.info(f"[{pipeline_id}] 'Poem Pipeline' completed successfully.")
            return self.active_pipelines[pipeline_id]
        
        except InterruptedError as e:
            logger.info(f"[{pipeline_id}] Pipeline interrupted by user: {e}. Restarting...")
            return await self.run_poem_pipeline(user_id, project_id, user_config, user_feedback_fn)
        except Exception as e:
            logger.error(f"[{pipeline_id}] Poem pipeline failed: {e}")
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    async def run_crime_novel_pipeline(
        self,
        user_id: str, project_id: str, user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        خط إنتاج متخصص لكتابة رواية جريمة وغموض.
        """
        pipeline_id = f"crime_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Crime Novel Pipeline'")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # STEP 1: Generate Crime Idea
            crime_idea_context = {**user_config, "genre_hint": "جريمة وغموض"}
            idea_result = await self.orchestrator.run_refinable_task("generate_idea", crime_idea_context, user_config)
            self.active_pipelines[pipeline_id]["steps"]["idea"] = idea_result
            await self._handle_user_feedback(pipeline_id, "idea", idea_result, user_feedback_fn, user_config)
            
            # STEP 2: Forensic Analysis
            forensic_context = {"text_content": idea_result["final_content"]["premise"]}
            forensic_analysis = await self.orchestrator.run_refinable_task("analyze_crime_narrative", forensic_context, user_config)
            self.active_pipelines[pipeline_id]["steps"]["forensic_analysis"] = forensic_analysis

            # STEP 3: Build Blueprint
            blueprint_context = {"idea": idea_result["final_content"], "forensic_report": forensic_analysis["final_content"]}
            blueprint_result = await self.orchestrator.run_refinable_task("generate_blueprint", blueprint_context, user_config)
            self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
            
            self.active_pipelines[pipeline_id]["status"] = "completed"
            return self.active_pipelines[pipeline_id]
            
        except Exception as e:
            logger.error(f"[{pipeline_id}] Crime Novel Pipeline failed: {e}")
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise
