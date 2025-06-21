# core/workflow_manager.py
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

from core.apollo_orchestrator import apollo
from ingestion.ingestion_engine import InputType, ingestion_engine
from agents.blueprint_architect_agent import StoryBlueprint, ChapterOutline
# ... (افتراض وجود نماذج بيانات للمسرحية والمحتوى التعليمي)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    def __init__(self):
        self.orchestrator = apollo
        self.ingestion_engine = ingestion_engine
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def _handle_user_feedback(self, pipeline_id, step_name, step_result, user_feedback_fn, config):
        if user_feedback_fn and step_name in config.get("user_checkpoints", []):
            logger.info(f"[{pipeline_id}] Awaiting user feedback on '{step_name}'...")
            action = await user_feedback_fn(step_name, step_result.get("final_content"))
            if isinstance(action, dict):
                logger.info(f"[{pipeline_id}] User modified the '{step_name}'.")
                step_result["final_content"] = action
            elif action == "regenerate":
                raise InterruptedError(f"User requested regeneration at step: {step_name}")
        return step_result

    async def transmute_witness(self, user_id, project_id, source, input_type, creation_config, user_feedback_fn=None):
        pipeline_id = f"transmute_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Witness Transmutation' Pipeline")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # Step 0: Ingestion
            ingestion_result = await self.ingestion_engine.ingest(source, input_type)
            if not ingestion_result.success:
                raise ValueError(f"Ingestion failed: {ingestion_result.error}")
            
            knowledge_base = {"raw_text": ingestion_result.text_content, "metadata": ingestion_result.metadata, "entities": [], "relationship_graph": [], "emotional_arc": []}
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base
            
            # Step 1: Routing
            creative_form = creation_config.get("creative_form", "novel")
            logger.info(f"[{pipeline_id}] ==> Routing to '{creative_form}' sub-pipeline...")

            sub_pipelines = {
                "novel": self._run_novel_sub_pipeline,
                "poem": self._run_poem_sub_pipeline,
                "play": self._run_play_sub_pipeline,
                "educational_book": self._run_educational_book_sub_pipeline
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

    async def _run_novel_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        blueprint_result = await self.orchestrator.run_refinable_task("generate_blueprint", kb, config)
        self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
        blueprint_result = await self._handle_user_feedback(pipeline_id, "blueprint", blueprint_result, feedback_fn, config)
        first_chapter_outline = blueprint_result["final_content"].chapters[0]
        chapter_result = await self.orchestrator.run_refinable_task("generate_chapter", {"chapter_outline": first_chapter_outline}, config)
        return chapter_result

    async def _run_poem_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        emotional_arc = kb.get("emotional_arc", [])
        themes = [entity['name'] for entity in kb.get("entities", []) if entity.get('type') == 'concept']
        poem_context = {"theme_hint": themes[0] if themes else "الحياة", "mood_hint": emotional_arc[0]['emotion'] if emotional_arc else "تأملي", **config}
        poem_result = await self.orchestrator.run_refinable_task("generate_poem", poem_context, config)
        return poem_result

    async def _run_play_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        idea_context = {"genre_hint": "مسرحية", "knowledge_base": kb}
        idea_result = await self.orchestrator.run_refinable_task("generate_idea", idea_context, config)
        dramatic_blueprint = await self.orchestrator.run_refinable_task("generate_dramatic_blueprint", {"idea": idea_result["final_content"]}, config)
        character_arcs = await self.orchestrator.run_refinable_task("develop_character_arcs", {"blueprint": dramatic_blueprint["final_content"]}, config)
        
        full_script = ""
        for act in dramatic_blueprint["final_content"].get("acts", []):
            for event in act.get("key_events", []):
                scene_script = await self.orchestrator.run_refinable_task("generate_play_chapter", {"chapter_outline": {"summary": event}, "character_arcs": character_arcs["final_content"]}, config)
                full_script += scene_script["final_content"]["content"]["chapter_content"] + "\n\n"
        
        final_script = await self.orchestrator.run_refinable_task("add_staging_directions", {"script": full_script}, config)
        return final_script

    async def _run_educational_book_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        map_context = {"knowledge_base": kb, "target_audience": config.get("target_audience", "طلاب")}
        curriculum_map = await self.orchestrator.run_refinable_task("design_curriculum_map", map_context, config)
        # Future: Loop through lessons and call a 'generate_lesson_content' task
        return curriculum_map
