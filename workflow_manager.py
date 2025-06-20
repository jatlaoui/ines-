# workflow_manager.py (النسخة الكاملة والمحدثة مع دعم التفاعل)
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

# استيراد المنسق الرئيسي الذي سيقوم بتشغيل المهام الفردية
from core.apollo_orchestrator import apollo # استيراد المثيل الوحيد

# إعداد التسجيل
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

    async def run_story_pipeline(
        self,
        user_id: str,
        project_id: str,
        user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable[[str, Any], Union[str, Dict[str, Any]]]] = None
    ) -> Dict[str, Any]:
        """
        يشغل خط إنتاج كامل للرواية: من الفكرة -> المخطط -> الفصل الأول.
        """
        pipeline_id = f"pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Story Pipeline' for project {project_id}")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}
        
        try:
            # --- STEP 1: Generate Idea ---
            logger.info(f"[{pipeline_id}] ==> STEP 1: Generating Idea...")
            idea_result = await self.orchestrator.run_refinable_task(
                task_name="generate_idea",
                initial_context=user_config,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["idea"] = idea_result
            if "error" in idea_result:
                raise RuntimeError(f"Idea generation failed: {idea_result['error']}")
            
            logger.info(f"[{pipeline_id}] Idea generated with score: {idea_result.get('final_score'):.1f}")
            
            # --- نقطة التوقف التفاعلية للفكرة ---
            if user_feedback_fn and "idea" in user_config.get("user_checkpoints", []):
                logger.info(f"[{pipeline_id}] Awaiting user feedback on idea...")
                user_action = await user_feedback_fn("idea", idea_result["final_content"])
                
                if isinstance(user_action, dict): # User provided a modified version
                    logger.info(f"[{pipeline_id}] User modified the idea.")
                    idea_result["final_content"] = user_action
                elif user_action == "regenerate":
                    logger.info("User requested idea regeneration. Restarting pipeline...")
                    # For simplicity, we restart the whole pipeline. A more complex system could restart just the step.
                    return await self.run_story_pipeline(user_id, project_id, user_config, user_feedback_fn)
                # If 'accept', we just continue

            # --- STEP 2: Generate Blueprint ---
            logger.info(f"[{pipeline_id}] ==> STEP 2: Generating Blueprint...")
            blueprint_result = await self.orchestrator.run_refinable_task(
                task_name="generate_blueprint",
                initial_context=idea_result.get("final_content"),
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
            if "error" in blueprint_result:
                 raise RuntimeError(f"Blueprint generation failed: {blueprint_result['error']}")
            
            logger.info(f"[{pipeline_id}] Blueprint generated with score: {blueprint_result.get('final_score'):.1f}")
            
            # --- نقطة التوقف التفاعلية للمخطط ---
            if user_feedback_fn and "blueprint" in user_config.get("user_checkpoints", []):
                logger.info(f"[{pipeline_id}] Awaiting user feedback on blueprint...")
                user_action = await user_feedback_fn("blueprint", blueprint_result["final_content"])
                
                if isinstance(user_action, dict): # User provided a modified version
                    logger.info(f"[{pipeline_id}] User modified the blueprint.")
                    blueprint_result["final_content"] = user_action
                elif user_action == "regenerate":
                    # In a real system, you'd want a more robust way to handle regeneration
                    # without restarting everything. For now, we show the concept.
                    logger.info("User requested blueprint regeneration. Re-running blueprint step...")
                    blueprint_result = await self.orchestrator.run_refinable_task(
                        task_name="generate_blueprint",
                        initial_context=idea_result.get("final_content"),
                        user_config=user_config
                    )
                    self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result

            # --- STEP 3: Generate Chapter 1 ---
            logger.info(f"[{pipeline_id}] ==> STEP 3: Generating Chapter 1...")
            first_chapter_outline = blueprint_result.get("final_content").chapters[0]
            
            chapter_result = await self.orchestrator.run_refinable_task(
                task_name="generate_chapter",
                initial_context=first_chapter_outline,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["chapter_1"] = chapter_result
            if "error" in chapter_result:
                 raise RuntimeError(f"Chapter generation failed: {chapter_result['error']}")

            logger.info(f"[{pipeline_id}] Chapter 1 generated with score: {chapter_result.get('final_score'):.1f}")

            # --- الانتهاء بنجاح ---
            self.active_pipelines[pipeline_id]["status"] = "completed"
            logger.info(f"[{pipeline_id}] 'Story Pipeline' completed successfully.")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"[{pipeline_id}] Pipeline failed: {e}")
            self.active_pipelines[pipeline_id]["status"] = "failed"
            self.active_pipelines[pipeline_id]["error"] = str(e)
            raise

    async def run_poem_pipeline(
        self, 
        user_id: str, 
        project_id: str, 
        user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable[[str, Any], Union[str, Dict[str, Any]]]] = None
    ) -> Dict[str, Any]:
        """
        يشغل خط إنتاج متخصص لكتابة قصيدة.
        """
        pipeline_id = f"poem_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Poem Pipeline' for project {project_id}")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # --- الخطوة 1: توليد القصيدة ---
            logger.info(f"[{pipeline_id}] ==> STEP 1: Generating Poem...")
            poem_result = await self.orchestrator.run_refinable_task(
                task_name="generate_poem",
                initial_context=user_config,
                user_config=user_config
            )
            self.active_pipelines[pipeline_id]["steps"]["poem"] = poem_result

            if "error" in poem_result:
                raise RuntimeError(f"Poem generation failed: {poem_result['error']}")

            logger.info(f"[{pipeline_id}] Poem generated successfully with score: {poem_result.get('final_score'):.1f}")
            
            # --- نقطة التوقف التفاعلية للقصيدة ---
            if user_feedback_fn and "poem" in user_config.get("user_checkpoints", []):
                logger.info(f"[{pipeline_id}] Awaiting user feedback on poem...")
                user_action = await user_feedback_fn("poem", poem_result["final_content"])
                if isinstance(user_action, dict): # User provided a modified version
                    logger.info(f"[{pipeline_id}] User modified the poem.")
                    poem_result["final_content"] = user_action

            self.active_pipelines[pipeline_id]["status"] = "completed"
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"[{pipeline_id}] Poem pipeline failed: {e}")
            self.active_pipelines[pipeline_id]["status"] = "failed"
            self.active_pipelines[pipeline_id]["error"] = str(e)
            raise

# --- مثال اختبار جديد ---
if __name__ == "__main__":
    import sys
    sys.path.append('.') # Add current directory to path for imports
    
    from agents.blueprint_architect_agent import ChapterOutline # للتوافق

    async def cli_feedback_handler(stage: str, content: Optional[Any] = None) -> Union[str, Dict[str, Any]]:
        """دالة معالجة تفاعل المستخدم عبر CLI."""
        if stage == "modified_idea" or stage == "modified_blueprint":
            print(f"\n✍️ أدخل النسخة المعدلة من {stage.replace('modified_', '')} بصيغة JSON:")
            user_input = input("→ ")
            try:
                return json.loads(user_input)
            except json.JSONDecodeError:
                print("إدخال JSON غير صالح. سيتم استخدام النسخة الأصلية.")
                return "accept" # Fallback

        print(f"\n\n📍 نقطة مراجعة المستخدم: {stage.upper()}")
        
        # Dataclass handling for printing
        from dataclasses import is_dataclass, asdict
        if is_dataclass(content):
            print(json.dumps(asdict(content), indent=2, ensure_ascii=False))
        else:
            print(json.dumps(content, indent=2, ensure_ascii=False))
        
        while True:
            choice = input("\nهل تريد قبول (a)ccept، إعادة توليد (r)egenerate، أم تعديل (m)odify؟ [a/r/m]: ").strip().lower()
            if choice in ['a', 'accept']:
                return "accept"
            elif choice in ['r', 'regenerate']:
                return "regenerate"
            elif choice in ['m', 'modify']:
                return "modify" # This signals to the pipeline to call the handler again for input
            else:
                print("خيار غير صالح. الرجاء إدخال a, r, أو m.")

    async def test_all_workflows():
        """اختبار جميع خطوط الإنتاج المتاحة."""
        manager = WorkflowManager()
        
        # --- اختبار خط إنتاج الرواية ---
        print("\n" + "="*80)
        print("🎬🎬🎬  RUNNING STORY WORKFLOW TEST 🎬🎬🎬")
        print("="*80)
        story_config = {
            "genre_hint": "خيال علمي فلسفي",
            "theme_hint": "الوعي والهوية في عصر الذكاء الاصطناعي",
            "quality_threshold": 8.0,
            "user_checkpoints": ["idea", "blueprint"]
        }
        try:
            final_story_assets = await manager.run_story_pipeline(
                "cli_user", "project_story_001", story_config, cli_feedback_handler
            )
            print("\n--- ✅ النتيجة النهائية لخط إنتاج الرواية ---")
            
            # Custom encoder to handle dataclasses
            class DataclassEncoder(json.JSONEncoder):
                def default(self, o):
                    if is_dataclass(o):
                        return asdict(o)
                    return super().default(o)
            print(json.dumps(final_story_assets, ensure_ascii=False, indent=2, cls=DataclassEncoder))
        except Exception as e:
            print(f"--- ❌ فشل اختبار خط إنتاج الرواية --- \n {e}")


        # --- اختبار خط إنتاج الشعر ---
        print("\n" + "="*80)
        print("📜📜📜  RUNNING POEM WORKFLOW TEST 📜📜📜")
        print("="*80)
        poem_config = {
            "theme_hint": "الحنين إلى الماضي في عالم رقمي",
            "style_hint": "شعر حر",
            "quality_threshold": 7.0,
            "user_checkpoints": ["poem"]
        }
        try:
            final_poem_assets = await manager.run_poem_pipeline(
                "cli_user", "project_poem_001", poem_config, cli_feedback_handler
            )
            print("\n--- ✅ النتيجة النهائية لخط إنتاج الشعر ---")
            print(json.dumps(final_poem_assets, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"--- ❌ فشل اختبار خط إنتاج الشعر --- \n {e}")

    asyncio.run(test_all_workflows())
