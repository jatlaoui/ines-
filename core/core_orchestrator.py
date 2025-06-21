# core/core_orchestrator.py (النسخة النهائية V3 - Dynamic & Adaptive)
import asyncio
import logging
import uuid
from typing import Dict, Any, List, Type
from dataclasses import asdict

# --- استيراد المكونات الأساسية والمحسّنة ---
from .core_database import core_db, WorkflowStatus, TaskStatus
from .core_auth import core_auth, UserSession, require_auth
from .core_narrative_memory import narrative_memory
from .workflow_templates import workflow_template_manager, WorkflowTemplate, WorkflowTask, TaskType
from ..agents.base_agent import BaseAgent
from ..agents import * # استيراد جميع الوكلاء من الحزمة

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CoreOrchestrator] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoreOrchestrator:
    """
    المنسق الأساسي الديناميكي (V3).
    يدير سير عمل عضوي وتفاعلي، مع تفعيل الذاكرة، حارس الاتساق، والتخطيط المتكيف.
    """
    def __init__(self):
        self.running_workflows: Dict[str, Any] = {}
        self.agents: Dict[str, BaseAgent] = self._register_agents()
        self.task_handlers: Dict[TaskType, Any] = self._initialize_task_handlers()
        logger.info("✅ CoreOrchestrator V3 (Dynamic & Adaptive) Initialized.")

    def _register_agents(self) -> Dict[str, BaseAgent]:
        """تسجيل جميع وكلاء النظام المتاحين ديناميكيًا."""
        return {
            "idea_generator": idea_generator,
            "blueprint_architect": blueprint_architect,
            "chapter_composer": chapter_composer,
            "literary_critic": literary_critic,
            "narrative_constructor": narrative_constructor,
            "psychological_profiler": psychological_profiler,
            "dramaturg_agent": dramaturg_agent,
            "narrative_guardian": narrative_guardian,
            "adaptive_learner": adaptive_learner,
            "creative_chaos_agent": creative_chaos_agent,
            "style_mimic_agent": style_mimic_agent,
        }
        
    def _initialize_task_handlers(self) -> Dict[TaskType, Any]:
        """ربط أنواع المهام بالدوال المعالجة لها."""
        return {
            # المهام التي تستدعي وكيلاً واحداً بشكل مباشر
            TaskType.ANALYZE_NOVEL: self._handle_direct_agent_task,
            TaskType.GENERATE_IDEAS: self._handle_direct_agent_task,
            TaskType.BUILD_BLUEPRINT: self._handle_direct_agent_task,
            TaskType.CUSTOM_AGENT_TASK: self._handle_direct_agent_task,
            
            # المهام التي تتطلب منطقاً خاصاً من المنسق
            TaskType.GENERATE_CHAPTER: self._handle_intelligent_composition,
            TaskType.VALIDATE_CONSISTENCY: self._handle_direct_agent_task, # حارس السرد وكيل مباشر
            TaskType.DYNAMIC_REPLAN: self._handle_dynamic_replan,
            TaskType.MERGE_DATA: self._handle_merge_data,
        }

    @require_auth
    async def start_workflow(self, template_id: str, context_data: Dict[str, Any], user_session: UserSession) -> str:
        """بدء تنفيذ سير عمل من قالب."""
        logger.info(f"Orchestrator: Attempting to start workflow '{template_id}' for user '{user_session.user_id}'.")
        template = workflow_template_manager.get_template(template_id)
        if not template:
            raise ValueError(f"Workflow template '{template_id}' not found.")

        execution_id = f"exec_{uuid.uuid4().hex[:12]}"
        
        # إعادة تعيين الذاكرة والحارس لمشروع جديد
        narrative_memory.clear()
        narrative_guardian.reset()
        logger.info(f"Memory and Guardian reset for new execution: {execution_id}")
        
        execution = {
            "id": execution_id,
            "template_id": template_id,
            "user_id": user_session.user_id,
            "name": f"Execution: {template.name}",
            "status": WorkflowStatus.PENDING.value,
            "tasks": [asdict(task) for task in template.tasks],
            "context_data": context_data,
            "task_outputs": {},
            "created_at": datetime.now().isoformat(),
        }
        
        self.running_workflows[execution_id] = execution
        logger.info(f"Workflow '{execution['name']}' ({execution_id}) successfully started.")
        
        asyncio.create_task(self._execute_dynamic_workflow(execution_id))
        return execution_id

    async def _execute_dynamic_workflow(self, execution_id: str):
        """التنفيذ الفعلي لسير العمل بمنطق ديناميكي."""
        execution = self.running_workflows[execution_id]
        execution["status"] = WorkflowStatus.RUNNING.value
        execution["started_at"] = datetime.now().isoformat()
        logger.info(f"🚀 DYNAMIC WORKFLOW EXECUTION STARTED: {execution['name']}")

        completed_tasks = set()
        
        try:
            tasks_to_run = execution["tasks"]
            while len(completed_tasks) < len(tasks_to_run):
                task_executed_in_cycle = False
                for task_data in tasks_to_run:
                    if task_data["id"] in completed_tasks:
                        continue

                    if all(dep in completed_tasks for dep in task_data.get("dependencies", [])):
                        handler = self.task_handlers.get(TaskType(task_data["task_type"]))
                        if not handler:
                            raise NotImplementedError(f"No handler for task type '{task_data['task_type']}'")
                        
                        input_payload = self._prepare_task_input(task_data, execution["task_outputs"])
                        context = {**execution["context_data"], **input_payload}

                        result = await handler(task_data, context)
                        
                        if result.get("status") == "failure":
                            raise RuntimeError(f"Task '{task_data['name']}' failed: {result.get('message')}")
                        
                        await self._process_task_output(task_data, result, execution_id)
                        
                        completed_tasks.add(task_data["id"])
                        task_executed_in_cycle = True

                if not task_executed_in_cycle:
                    raise RuntimeError("Workflow stalled. Check for circular dependencies or unmet conditions.")

            execution["status"] = WorkflowStatus.COMPLETED.value
            logger.info(f"✅ Workflow '{execution['name']}' completed successfully.")

        except Exception as e:
            execution["status"] = WorkflowStatus.FAILED.value
            execution["error_message"] = str(e)
            logger.error(f"❌ Workflow '{execution['name']}' failed. Reason: {e}", exc_info=True)
        
        execution["completed_at"] = datetime.now().isoformat()

    async def _process_task_output(self, task_data: Dict, result: Dict, execution_id: str):
        """يعالج مخرجات المهمة، ويحدث الذاكرة، ويقوم بالتحقق من الاتساق."""
        execution = self.running_workflows[execution_id]
        execution["task_outputs"][task_data["id"]] = result

        content_to_process = self._extract_content_from_result(result)
        
        if content_to_process:
            logger.info(f"Guardian is checking output of '{task_data['name']}'...")
            inconsistencies = await narrative_guardian.check_consistency(content_to_process)
            if inconsistencies:
                logger.error(f"CONSISTENCY VIOLATION in '{task_data['name']}': {inconsistencies}")

            narrative_memory.add_entry(
                entry_type=task_data.get("task_type"),
                content=content_to_process[:500], # تخزين ملخص للمحتوى
                metadata={"task_id": task_data["id"], "source_content": content_to_process}
            )

    def _extract_content_from_result(self, result: Dict) -> str:
        """يستخلص المحتوى النصي الرئيسي من نتيجة مهمة."""
        if 'content' in result:
            content_dict = result['content']
            if isinstance(content_dict, dict):
                # البحث عن مفاتيح محتملة للمحتوى
                for key in ['final_script', 'chapter_content', 'merged_content', 'text_content']:
                    if key in content_dict and isinstance(content_dict[key], str):
                        return content_dict[key]
        return ""


    def _prepare_task_input(self, task_data: Dict, all_outputs: Dict) -> Dict:
        """يجمع المدخلات اللازمة لمهمة ما."""
        input_payload = task_data.get("input_data", {}).copy()
        for dep_id in task_data.get("dependencies", []):
            if dep_id in all_outputs:
                input_payload.update(all_outputs[dep_id])
        return input_payload

    # --- معالجات المهام المحسّنة ---

    async def _handle_direct_agent_task(self, task_data: Dict, context: Dict) -> Dict:
        """معالج عام يستدعي الوكيل المحدد في المهمة."""
        agent_id = task_data["input_data"]["agent_id"]
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found.")
        
        # استخلاص الـ prompt من القالب إذا كان موجودًا
        prompt_id = task_data.get("input_data", {}).get("prompt_id")
        if prompt_id:
            context["prompt"] = self._get_prompt_content(prompt_id)

        scene_prompt_id = task_data.get("input_data", {}).get("scene_outline_prompt_id")
        if scene_prompt_id:
            context["scene_outline"] = self._get_prompt_content(scene_prompt_id)

        return await agent.process_task(context)

    async def _handle_intelligent_composition(self, task_data: Dict, context: Dict) -> Dict[str, Any]:
        """معالج ذكي لكتابة المحتوى (فصل أو مشهد) باستخدام الذاكرة والتعلم."""
        user_id = context.get("user_id")
        logger.info(f"Initiating intelligent composition for user '{user_id}'.")
        
        # 1. جلب توجيهات الأسلوب المخصصة للمستخدم
        style_directives = await adaptive_learner.get_style_directives(user_id)
        
        # 2. الاستعلام من الذاكرة عن السياق ذي الصلة
        query = f"Context for chapter {context.get('chapter_number', 'next')}: {context.get('synopsis', 'general progress')}"
        relevant_memories = narrative_memory.query(query)
        
        # 3. تجميع السياق الكامل
        composition_context = {
            **context,
            "style_directives": style_directives,
            "memory_context": [mem.content for mem in relevant_memories],
        }

        # 4. استدعاء وكيل الكتابة المناسب
        agent_id = task_data.get("input_data", {}).get("agent_id", "chapter_composer")
        composer_agent = self.agents[agent_id]
        
        return await composer_agent.process_task(composition_context)

    async def _handle_dynamic_replan(self, task_data: Dict, context: Dict) -> Dict:
        """يعيد تقييم القصة ويحدث المخطط."""
        logger.info(">>>--- DYNAMIC RE-PLANNING CYCLE ---<<<")
        query = "Latest major plot points, character changes, and unresolved tensions."
        recent_memories = narrative_memory.query(query, top_k=7)
        
        disruptive_ideas = await self.agents["creative_chaos_agent"].process_task(context)

        replan_context = {
            "initial_blueprint": context.get("current_blueprint"),
            "recent_developments": [mem.content for mem in recent_memories],
            "disruptive_ideas": disruptive_ideas.get("content", []),
        }
        
        # استخدام وكيل بناء المخططات لتحديث الخطة
        updated_blueprint = await self.agents["blueprint_architect"].process_task(replan_context)
        context["current_blueprint"] = updated_blueprint.get("blueprint")
        logger.info("ORCHESTRATOR: Blueprint has been dynamically updated.")
        return {"status": "success", "message": "Blueprint updated successfully."}

    def _get_prompt_content(self, prompt_id: str) -> Any:
        # ... (نفس دالة جلب الموجهات من الرد السابق)
        return {}
        
core_orchestrator = CoreOrchestrator()
