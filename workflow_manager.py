# workflow_manager.py (نسخة محدثة مع دعم نقاط التوقف التفاعلية)
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

from apollo_orchestrator import ApolloOrchestrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    def __init__(self, orchestrator: ApolloOrchestrator):
        self.orchestrator = orchestrator
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    async def run_story_pipeline(
        self,
        user_id: str,
        project_id: str,
        user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable[[str, Dict[str, Any]], Union[str, Dict[str, Any]]]] = None
    ) -> Dict[str, Any]:
        pipeline_id = f"pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Story Pipeline'")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # STEP 1: Generate Idea
            idea_result = await self.orchestrator.run_refinable_task(
                task_name="generate_idea",
                initial_context=user_config,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["idea"] = idea_result
            if "error" in idea_result:
                raise RuntimeError(f"Idea generation failed: {idea_result['error']}")
            logger.info(f"[{pipeline_id}] Idea score: {idea_result.get('final_score'):.1f}")

            if user_feedback_fn and "idea" in user_config.get("user_checkpoints", []):
                logger.info(f"[{pipeline_id}] Awaiting user feedback on idea...")
                action = await user_feedback_fn("idea", idea_result["final_content"])
                if action == "regenerate":
                    logger.info("User requested idea regeneration. Restarting pipeline...")
                    return await self.run_story_pipeline(user_id, project_id, user_config, user_feedback_fn)
                elif action == "modify":
                    modified = await user_feedback_fn("modified_idea")
                    idea_result["final_content"] = modified

            # STEP 2: Generate Blueprint
            blueprint_result = await self.orchestrator.run_refinable_task(
                task_name="generate_blueprint",
                initial_context=idea_result["final_content"],
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
            if "error" in blueprint_result:
                raise RuntimeError(f"Blueprint generation failed: {blueprint_result['error']}")
            logger.info(f"[{pipeline_id}] Blueprint score: {blueprint_result.get('final_score'):.1f}")

            if user_feedback_fn and "blueprint" in user_config.get("user_checkpoints", []):
                logger.info(f"[{pipeline_id}] Awaiting user feedback on blueprint...")
                action = await user_feedback_fn("blueprint", blueprint_result["final_content"])
                if action == "regenerate":
                    logger.info("User requested blueprint regeneration. Restarting pipeline...")
                    return await self.run_story_pipeline(user_id, project_id, user_config, user_feedback_fn)
                elif action == "modify":
                    modified = await user_feedback_fn("modified_blueprint")
                    blueprint_result["final_content"] = modified

            # STEP 3: Generate Chapter 1
            chapter_outline = blueprint_result["final_content"].chapters[0]
            chapter_result = await self.orchestrator.run_refinable_task(
                task_name="generate_chapter",
                initial_context=chapter_outline,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["chapter_1"] = chapter_result
            if "error" in chapter_result:
                raise RuntimeError(f"Chapter generation failed: {chapter_result['error']}")
            logger.info(f"[{pipeline_id}] Chapter score: {chapter_result.get('final_score'):.1f}")

            self.active_pipelines[pipeline_id]["status"] = "completed"
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"[{pipeline_id}] Pipeline failed: {e}")
            self.active_pipelines[pipeline_id]["status"] = "failed"
            self.active_pipelines[pipeline_id]["error"] = str(e)
            raise

# === CLI TEST ===

async def user_feedback_fn(stage, content=None):
    print(f"\n\n📍 نقطة مراجعة المستخدم: {stage.upper()}")
    print(json.dumps(content, indent=2, ensure_ascii=False))
    choice = input("\nهل تريد قبول (accept)، إعادة توليد (regenerate)، أم تعديل (modify)؟ ").strip().lower()
    if choice == "modify":
        print("أدخل المحتوى المعدل بصيغة JSON:")
        user_input = input("→ ")
        return json.loads(user_input)
    return choice

if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from apollo_orchestrator import ApolloOrchestrator

    async def test():
        orchestrator = ApolloOrchestrator()
        manager = WorkflowManager(orchestrator)
        config = {
            "genre_hint": "خيال علمي فلسفي",
            "theme_hint": "الوعي الصناعي والهوية",
            "quality_threshold": 7.5,
            "user_checkpoints": ["idea", "blueprint"]
        }
        result = await manager.run_story_pipeline("user_1", "proj_1", config, user_feedback_fn)
        print("\nالنتيجة النهائية:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    asyncio.run(test())
