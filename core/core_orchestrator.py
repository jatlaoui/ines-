# core/core_orchestrator.py (النسخة المحسّنة والجاهزة للتنفيذ)
import asyncio
import logging
from typing import Dict, Any, List, Optional
from dataclasses import asdict

# --- استيراد المكونات الأساسية والمحسّنة ---
from .core_database import core_db, WorkflowStatus, TaskStatus
from .core_auth import core_auth, UserSession, require_auth
from .core_narrative_memory import narrative_memory
from .workflow_templates import workflow_template_manager, WorkflowTemplate, WorkflowTask, TaskType
from ..agents.base_agent import BaseAgent
from ..agents.idea_generator_agent import idea_generator
from ..agents.blueprint_architect_agent import blueprint_architect
from ..agents.chapter_composer_agent import chapter_composer
from ..agents.literary_critic_agent import literary_critic
from ..agents.narrative_constructor_agent import narrative_constructor
from ..agents.psychological_profiler_agent import psychological_profiler
from ..agents.dramaturg_agent import dramaturg_agent
from ..agents.narrative_guardian_agent import narrative_guardian
from ..agents.adaptive_learning_agent import adaptive_learner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CoreOrchestrator] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoreOrchestrator:
    """
    المنسق الأساسي المحسّن (V2).
    يدير سير العمل، وينسق بين الوكلاء، ويدمج القدرات الجديدة
    مثل الذاكرة السردية، حارس الاتساق، والتخطيط الديناميكي.
    """
    def __init__(self):
        self.running_workflows: Dict[str, Any] = {}
        self.agents: Dict[str, BaseAgent] = self._register_agents()
        self.task_handlers: Dict[TaskType, Any] = self._initialize_task_handlers()
        logger.info("✅ CoreOrchestrator V2 Initialized with Advanced Agents and Handlers.")

    def _register_agents(self) -> Dict[str, BaseAgent]:
        """تسجيل جميع وكلاء النظام المتاحين."""
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
        }
        
    def _initialize_task_handlers(self) -> Dict[TaskType, Any]:
        """ربط أنواع المهام بالدوال المعالجة لها."""
        return {
            TaskType.ANALYZE_NOVEL: self._handle_generic_agent_task,
            TaskType.GENERATE_IDEAS: self._handle_generic_agent_task,
            TaskType.BUILD_BLUEPRINT: self._handle_generic_agent_task,
            TaskType.GENERATE_CHAPTER: self._handle_generate_chapter,
            TaskType.CUSTOM_AGENT_TASK: self._handle_generic_agent_task,
            TaskType.VALIDATE_CONSISTENCY: self._handle_generic_agent_task,
            TaskType.DYNAMIC_REPLAN: self._handle_dynamic_replan,
            TaskType.MERGE_DATA: self._handle_merge_data,
            # ... إضافة بقية المعالجات
        }

    @require_auth
    async def start_workflow(self, template_id: str, context_data: Dict[str, Any], user_session: UserSession) -> str:
        """بدء تنفيذ سير عمل من قالب."""
        logger.info(f"Attempting to start workflow '{template_id}' for user '{user_session.user_id}'.")
        template = workflow_template_manager.get_template(template_id)
        if not template:
            raise ValueError(f"قالب سير العمل '{template_id}' غير موجود.")

        execution_id = f"exec_{uuid.uuid4().hex[:12]}"
        
        # تحضير المهام للتنفيذ
        execution_tasks = [asdict(task) for task in template.tasks]

        execution = {
            "id": execution_id,
            "template_id": template_id,
            "user_id": user_session.user_id,
            "name": f"تنفيذ: {template.name}",
            "status": WorkflowStatus.PENDING.value,
            "tasks": execution_tasks,
            "context_data": context_data, # السياق الأولي من المستخدم
            "task_outputs": {}, # لتخزين مخرجات كل مهمة
            "created_at": datetime.now().isoformat(),
        }
        
        self.running_workflows[execution_id] = execution
        # core_db.save_workflow_execution(execution) # يجب أن تكون هذه الدالة موجودة
        logger.info(f"Workflow '{execution['name']}' ({execution_id}) started.")
        
        asyncio.create_task(self._execute_workflow(execution_id))
        return execution_id

    async def _execute_workflow(self, execution_id: str):
        """التنفيذ الفعلي لسير العمل مع المنطق المحسّن."""
        execution = self.running_workflows[execution_id]
        execution["status"] = WorkflowStatus.RUNNING.value
        execution["started_at"] = datetime.now().isoformat()

        logger.info(f"Executing workflow: {execution['name']}")
        
        completed_tasks = set()
        
        try:
            while len(completed_tasks) < len(execution["tasks"]):
                task_executed_in_cycle = False
                for i, task_data in enumerate(execution["tasks"]):
                    if task_data["id"] in completed_tasks:
                        continue

                    dependencies_met = all(dep in completed_tasks for dep in task_data.get("dependencies", []))
                    if dependencies_met:
                        task_data["status"] = TaskStatus.RUNNING.value
                        
                        # --- [محسّن] حقن مخرجات المهام السابقة كمدخلات ---
                        input_payload = self._prepare_task_input(task_data, execution["task_outputs"])
                        
                        logger.info(f"Executing task '{task_data['name']}'...")
                        handler = self.task_handlers.get(TaskType(task_data["task_type"]))
                        if not handler:
                            raise NotImplementedError(f"No handler for task type '{task_data['task_type']}'")
                        
                        result = await handler(task_data, input_payload, execution["context_data"])

                        if result.get("status") == "failure":
                            raise RuntimeError(f"Task '{task_data['name']}' failed: {result.get('message')}")
                        
                        execution["task_outputs"][task_data["id"]] = result
                        task_data["status"] = TaskStatus.COMPLETED.value
                        task_data["output_data"] = result
                        completed_tasks.add(task_data["id"])
                        task_executed_in_cycle = True
                        
                        # --- [محسّن] التحقق من الاتساق بعد كل مهمة كتابة ---
                        if task_data["task_type"] in [TaskType.GENERATE_CHAPTER, TaskType.CUSTOM_AGENT_TASK]:
                            consistency_result = await self.agents["narrative_guardian"].check_consistency(result.get("content", {}).get("final_script", ""))
                            if consistency_result:
                                # في نظام حقيقي، يمكننا هنا إما إيقاف سير العمل أو إعادة المهمة
                                logger.warning(f"Consistency issues found after task '{task_data['name']}': {consistency_result}")


                if not task_executed_in_cycle:
                    # لا توجد مهام جاهزة، قد يكون هناك حلقة مفرغة أو خطأ في التبعيات
                    raise RuntimeError("Workflow stalled. Check for circular dependencies or unmet conditions.")

            execution["status"] = WorkflowStatus.COMPLETED.value
            logger.info(f"✅ Workflow '{execution['name']}' completed successfully.")

        except Exception as e:
            execution["status"] = WorkflowStatus.FAILED.value
            execution["error_message"] = str(e)
            logger.error(f"❌ Workflow '{execution['name']}' failed. Reason: {e}", exc_info=True)
        
        execution["completed_at"] = datetime.now().isoformat()
        # core_db.update_workflow_execution(execution)


    def _prepare_task_input(self, task_data: Dict, all_outputs: Dict) -> Dict:
        """يجمع المدخلات اللازمة لمهمة ما من مخرجات المهام السابقة."""
        input_payload = task_data.get("input_data", {}).copy()
        for dep_id in task_data.get("dependencies", []):
            if dep_id in all_outputs:
                # دمج مخرجات المهمة السابقة في مدخلات المهمة الحالية
                input_payload.update(all_outputs[dep_id])
        return input_payload

    # --- معالجات المهام ---

    async def _handle_generic_agent_task(self, task_data: Dict, input_payload: Dict, execution_context: Dict) -> Dict:
        """معالج عام يستدعي الوكيل المناسب بناءً على المهمة."""
        agent_id = task_data["input_data"]["agent_id"]
        agent = self.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found.")
        
        # تمرير prompt_id إلى الوكيل إذا كان موجوداً
        context = {**input_payload, **execution_context}
        prompt_id = task_data.get("input_data", {}).get("prompt_id")
        if prompt_id:
            context["prompt_id"] = prompt_id

        # تمرير scene_outline_prompt_id للوكيل
        scene_prompt_id = task_data.get("input_data", {}).get("scene_outline_prompt_id")
        if scene_prompt_id:
             context["scene_outline_prompt"] = self._get_prompt_content(scene_prompt_id)

        return await agent.process_task(context)

    async def _handle_generate_chapter(self, task_data: Dict, input_payload: Dict, execution_context: Dict) -> Dict[str, Any]:
        """معالج محسّن لكتابة فصل."""
        user_id = execution_context.get("user_id")
        
        # 1. جلب توجيهات الأسلوب المخصصة للمستخدم
        style_directives = await adaptive_learner.get_style_directives(user_id)
        
        # 2. الاستعلام من الذاكرة عن السياق ذي الصلة
        query = f"Relevant context for chapter {input_payload.get('start_chapter', 1)} which focuses on {input_payload.get('focus', 'general development')}"
        relevant_memories = narrative_memory.query(query)
        
        # 3. تجميع السياق الكامل
        full_context = {
            **input_payload,
            "style_directives": style_directives,
            "memory_context": [mem.content for mem in relevant_memories],
        }

        # 4. استدعاء وكيل كتابة الفصول
        result = await self.agents["chapter_composer"].process_task(full_context)
        
        # 5. إضافة ملخص الفصل إلى الذاكرة
        if result.get("status") == "success":
            chapter_content = result.get("content", {}).get("chapter_content", "")
            narrative_memory.add_entry(
                entry_type="chapter_summary",
                content=f"Summary of chapter {input_payload.get('start_chapter', 1)}: {chapter_content[:250]}...",
                metadata={"chapter": input_payload.get('start_chapter', 1)}
            )
        return result

    async def _handle_dynamic_replan(self, task_data: Dict, input_payload: Dict, execution_context: Dict) -> Dict[str, Any]:
        """معالج دورة التخطيط الديناميكي."""
        logger.info("ORCHESTRATOR: Initiating dynamic re-planning cycle...")
        recent_developments = narrative_memory.query("latest major plot points and character arc changes", top_k=5)
        
        # تحديث المخطط بناءً على التطورات
        updated_blueprint = await self.agents["blueprint_architect"].process_task({
            "knowledge_base": execution_context.get("initial_analysis"),
            "dynamic_updates": [mem.content for mem in recent_developments]
        })
        
        execution_context["current_blueprint"] = updated_blueprint.get("blueprint")
        logger.info("ORCHESTRATOR: Blueprint has been dynamically updated.")
        return {"status": "success", "updated_blueprint": updated_blueprint}

    async def _handle_merge_data(self, task_data: Dict, input_payload: Dict, execution_context: Dict) -> Dict[str, Any]:
        """معالج دمج مخرجات المهام المختلفة."""
        source_tasks_ids = task_data.get("input_data", {}).get("source_tasks", [])
        full_script = ""
        for task_id in source_tasks_ids:
            task_output = execution_context.get("task_outputs", {}).get(task_id, {})
            # افتراض أن المحتوى موجود في هذا المسار
            content = task_output.get("content", {}).get("final_script", "") or task_output.get("content", {}).get("chapter_content", "")
            full_script += content + "\n\n---\n\n"
            
        return {"status": "success", "merged_content": full_script.strip()}

    def _get_prompt_content(self, prompt_id: str) -> Dict:
        """(محاكاة) جلب محتوى الموجه من قاعدة بيانات أو ملف."""
        prompts = {
             "act1_scene1_prompt": {
                "title": "الفصل الأول، المشهد الأول: أحلام ورقية", "location": "منزل تونسي متواضع", "dialect": "tunisois",
                "sensory_focus": ["رائحة القهوة", "صوت التلفاز القديم"],
                "interactions": [
                    {"character_name": "مبروك", "character_archetype": "ammi_salah", "topic": "pride", "mood": "يتحدث بفخر وأمل."},
                    {"character_name": "زهرة", "character_archetype": "al_hajja", "topic": "reality_check", "mood": "تظهر فرحاً سطحياً مع قلق داخلي."}
                ]
            },
            # ... إضافة بقية الموجهات التي صممناها ...
        }
        return prompts.get(prompt_id, {})

# إنشاء مثيل وحيد
core_orchestrator = CoreOrchestrator()
