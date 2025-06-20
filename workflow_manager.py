# core/workflow_manager.py (النسخة النهائية مع خط إنتاج متقدم)
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

from core.apollo_orchestrator import apollo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    def __init__(self):
        self.orchestrator = apollo
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}
        
    # ... (دوال _handle_user_feedback, run_story_pipeline, run_poem_pipeline كما هي) ...

    # --- خط إنتاج جديد فائق التطور ---
    async def run_deep_narrative_pipeline(
        self,
        user_id: str, project_id: str,
        witness_content: str, # المدخل الرئيسي هو الشاهد
        user_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        خط إنتاج فائق يطبق عقيدة "الشاهد أولاً" ويستخدم الأدوات المتخصصة.
        """
        pipeline_id = f"deep_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Deep Narrative Pipeline'")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}
        
        try:
            # STEP 1: تحليل الشاهد وبناء قاعدة المعرفة (منطق مستقبلي)
            logger.info(f"[{pipeline_id}] ==> STEP 1: Analyzing Witness...")
            # knowledge_base = await apollo.run_task("analyze_witness", {"witness_content": witness_content})
            # محاكاة لقاعدة المعرفة الآن
            knowledge_base = {"entities": [{"name": "علي", "type": "character", "importance_score": 9.0}], "relationship_graph": []}
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base
            
            # STEP 2: توليد أفكار غير متوقعة
            logger.info(f"[{pipeline_id}] ==> STEP 2: Generating Disruptive Ideas...")
            disruptive_ideas = await self.orchestrator.run_refinable_task(
                task_name="generate_disruptive_ideas",
                initial_context={"knowledge_base": knowledge_base}
            )
            self.active_pipelines[pipeline_id]["steps"]["disruptive_ideas"] = disruptive_ideas

            # STEP 3: بناء مخطط مبني على فكرة "فوضوية"
            logger.info(f"[{pipeline_id}] ==> STEP 3: Building Blueprint...")
            selected_idea = disruptive_ideas.get("final_content")[0] # اختيار أول فكرة
            blueprint_result = await self.orchestrator.run_refinable_task(
                task_name="generate_blueprint",
                initial_context={"idea": selected_idea}
            )
            self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result

            # STEP 4: كتابة فصل
            logger.info(f"[{pipeline_id}] ==> STEP 4: Composing Chapter...")
            chapter_outline = blueprint_result["final_content"].chapters[0]
            chapter_result = await self.orchestrator.run_refinable_task(
                task_name="generate_chapter",
                initial_context=chapter_outline
            )
            self.active_pipelines[pipeline_id]["steps"]["chapter"] = chapter_result

            # STEP 5: إضافة لمسة الضعف الإنساني
            logger.info(f"[{pipeline_id}] ==> STEP 5: Humanizing Text...")
            humanized_result = await self.orchestrator.run_refinable_task(
                task_name="humanize_text",
                initial_context={"text_content": chapter_result["final_content"]["chapter_content"]}
            )
            self.active_pipelines[pipeline_id]["steps"]["humanized_chapter"] = humanized_result
            
            self.active_pipelines[pipeline_id]["status"] = "completed"
            return self.active_pipelines[pipeline_id]
            
        except Exception as e:
            # ... (معالجة الأخطاء) ...
            raise
