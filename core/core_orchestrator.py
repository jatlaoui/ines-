# core/core_orchestrator.py (النسخة النهائية V3 - Dynamic & Adaptive)
import asyncio
import logging
from typing import Dict, Any, List
from dataclasses import asdict

# استيراد كافة المكونات الأساسية والوكلاء
from .core_database import core_db, WorkflowStatus, TaskStatus
from .core_auth import core_auth, UserSession, require_auth
from .core_narrative_memory import narrative_memory
from .workflow_templates import workflow_template_manager, WorkflowTemplate, WorkflowTask, TaskType
from ..agents.base_agent import BaseAgent
# ... (استيراد جميع الوكلاء كما في الملف السابق) ...
from ..agents.narrative_guardian_agent import narrative_guardian
from ..agents.adaptive_learning_agent import adaptive_learner
from ..agents.creative_chaos_agent import creative_chaos_agent
from ..agents.blueprint_architect_agent import blueprint_architect


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
        logger.info("✅ CoreOrchestrator V3 (Dynamic) Initialized.")

    def _register_agents(self) -> Dict[str, BaseAgent]:
        """تسجيل جميع وكلاء النظام."""
        # ... (نفس دالة تسجيل الوكلاء من الرد السابق)
        return { "narrative_guardian": narrative_guardian, "adaptive_learner": adaptive_learner, "creative_chaos_agent": creative_chaos_agent, "blueprint_architect": blueprint_architect}


    @require_auth
    async def start_workflow(self, template_id: str, context_data: Dict[str, Any], user_session: UserSession) -> str:
        """بدء تنفيذ سير عمل من قالب."""
        # ... (نفس دالة بدء سير العمل من الرد السابق)
        execution_id = "exec_id" # Placeholder
        asyncio.create_task(self._execute_dynamic_workflow(execution_id))
        return execution_id

    async def _execute_dynamic_workflow(self, execution_id: str):
        """
        [محسّن] التنفيذ الفعلي لسير العمل بمنطق ديناميكي.
        """
        execution = self.running_workflows[execution_id]
        execution["status"] = WorkflowStatus.RUNNING.value
        execution["started_at"] = datetime.now().isoformat()
        logger.info(f"🚀 Starting DYNAMIC workflow execution: {execution['name']}")

        # إعادة تعيين الذاكرة والحارس لمشروع جديد
        narrative_memory.clear()
        narrative_guardian.reset()

        execution["task_outputs"] = {}
        completed_tasks = set()
        
        try:
            tasks_to_run = execution["tasks"]
            while len(completed_tasks) < len(tasks_to_run):
                task_executed_in_cycle = False
                for task_data in tasks_to_run:
                    if task_data["id"] in completed_tasks:
                        continue

                    dependencies_met = all(dep in completed_tasks for dep in task_data.get("dependencies", []))
                    if dependencies_met:
                        
                        # --- [منطق جديد] التعامل مع دورات التخطيط الديناميكي ---
                        if TaskType(task_data["task_type"]) == TaskType.DYNAMIC_REPLAN:
                            logger.info(">>>--- DYNAMIC RE-PLANNING CYCLE ---<<<")
                            updated_blueprint = await self._handle_dynamic_replan(execution)
                            execution["context_data"]["current_blueprint"] = updated_blueprint.get("blueprint")
                            # لا يوجد مخرج مباشر، المهمة هي تحديث سياق التنفيذ
                            result = {"status": "success", "message": "Blueprint updated."}
                        else:
                            # --- تنفيذ المهمة العادية ---
                            logger.info(f"▶️ Executing task '{task_data['name']}'...")
                            input_payload = self._prepare_task_input(task_data, execution["task_outputs"])
                            
                            # حقن السياق المحدث (خاصة المخطط)
                            context = {**execution["context_data"], **input_payload}
                            
                            agent_id = task_data["input_data"].get("agent_id")
                            if not agent_id: raise ValueError(f"Task '{task_data['name']}' is missing an agent_id.")
                            agent = self.agents[agent_id]
                            
                            result = await agent.process_task(context)

                        if result.get("status") == "failure":
                            raise RuntimeError(f"Task '{task_data['name']}' failed: {result.get('message')}")
                        
                        # --- [منطق جديد] معالجة المخرجات بعد التنفيذ ---
                        await self._process_task_output(task_data, result, execution_id)
                        
                        completed_tasks.add(task_data["id"])
                        task_executed_in_cycle = True

                if not task_executed_in_cycle:
                    raise RuntimeError("Workflow stalled. Check dependencies.")

            execution["status"] = WorkflowStatus.COMPLETED.value
            logger.info(f"✅ Workflow '{execution['name']}' completed successfully.")

        except Exception as e:
            execution["status"] = WorkflowStatus.FAILED.value
            execution["error_message"] = str(e)
            logger.error(f"❌ Workflow '{execution['name']}' failed. Reason: {e}", exc_info=True)

    async def _process_task_output(self, task_data: Dict, result: Dict, execution_id: str):
        """
        [جديد] يعالج مخرجات المهمة، ويحدث الذاكرة، ويقوم بالتحقق من الاتساق.
        """
        execution = self.running_workflows[execution_id]
        execution["task_outputs"][task_data["id"]] = result

        content_to_check = ""
        entry_type = "generic_event"
        metadata = {"task_id": task_data["id"]}

        # استخلاص المحتوى والبيانات الوصفية لتحديث الذاكرة
        if task_data["task_type"] == TaskType.GENERATE_CHAPTER:
            content_to_check = result.get("content", {}).get("chapter_content", "")
            entry_type = "chapter_summary"
            metadata["chapter_title"] = result.get("content", {}).get("title")
        elif task_data["task_type"] == TaskType.CUSTOM_AGENT_TASK and task_data["input_data"]["agent_id"] == "narrative_constructor_agent":
            content_to_check = result.get("content", {}).get("final_script", "")
            entry_type = "scene"
            metadata["scene_title"] = result.get("summary", "")
        
        if content_to_check:
            # 1. التحقق من الاتساق بواسطة حارس السرد
            logger.info(f"Guardian is checking output of '{task_data['name']}'...")
            inconsistencies = await narrative_guardian.check_consistency(content_to_check)
            if inconsistencies:
                # في نظام حقيقي، يمكن إيقاف العمل أو وضع علامة للمراجعة
                logger.error(f"CONSISTENCY VIOLATION in '{task_data['name']}': {inconsistencies}")
                # هنا، سنكتفي بالتحذير ونكمل
            else:
                 logger.info("Guardian: Consistency check passed.")

            # 2. إضافة مدخل جديد إلى الذاكرة السردية
            narrative_memory.add_entry(entry_type, content_to_check, metadata)

    def _prepare_task_input(self, task_data: Dict, all_outputs: Dict) -> Dict:
        # ... (نفس دالة تحضير المدخلات من الرد السابق) ...
        return {}


    # [جديد] معالج دورة التخطيط الديناميكي
    async def _handle_dynamic_replan(self, execution: Dict) -> Dict:
        """
        يعيد تقييم القصة ويحدث المخطط.
        """
        logger.info("DRAMATURG: Re-assessing plot based on recent developments.")
        
        # 1. الاستعلام من الذاكرة عن آخر التطورات الهامة
        query_text = "What are the most recent character motivations, conflicts, and major plot turning points?"
        recent_memories = narrative_memory.query(query_text, top_k=5)
        recent_developments = [mem.content for mem in recent_memories]

        # 2. استدعاء وكيل الفوضى الإبداعية لاقتراح تحولات محتملة
        chaos_context = {"knowledge_base": execution["task_outputs"]["task_1_concept_analysis"]}
        disruptive_ideas = await creative_chaos_agent.generate_disruptive_ideas(chaos_context)

        # 3. استدعاء مهندس المخططات لتحديث الخطة
        replan_context = {
            "initial_blueprint": execution["context_data"].get("current_blueprint"),
            "recent_developments": recent_developments,
            "disruptive_ideas": [idea['idea'] for idea in disruptive_ideas['content']]
        }
        updated_blueprint_result = await blueprint_architect.refine_blueprint(replan_context)
        
        logger.info("ORCHESTRATOR: Blueprint has been dynamically updated.")
        return updated_blueprint_result.get("content", {})

# ... (بقية الملف كما هو، مع التأكد من أن وكيل `BlueprintArchitectAgent` لديه دالة `refine_blueprint`)

core_orchestrator = CoreOrchestrator()
