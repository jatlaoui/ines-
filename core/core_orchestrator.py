# core/core_orchestrator.py (V2 - The Autonomous Engine)
import logging
import asyncio
import uuid
from typing import Any, Dict, List, Optional

# --- استيراد جميع مكونات INES التي تم تفعيلها ---
from .core_narrative_memory import narrative_memory
from .refinement_service import refinement_service
from .workflow_templates_models import WorkflowTemplate, WorkflowTask, TaskType
from .workflow_templates import workflow_template_manager

# --- استيراد الوكلاء ---
from agents.idea_generator_agent import idea_generator_agent
from agents.blueprint_architect_agent import blueprint_architect_agent
from agents.chapter_composer_agent import chapter_composer_agent
from agents.literary_critic_agent import literary_critic_agent
from agents.psychological_profiler_agent import psychological_profiler_agent
# ... إضافة بقية الوكلاء عند الحاجة ...

# --- استيراد المنسق الاستراتيجي ---
from orchestrators.athena_strategic_orchestrator import athena_orchestrator, StrategicDecision

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CoreOrchestrator] - %(levelname)s - %(message)s')
logger = logging.getLogger("CoreOrchestrator")

class CoreOrchestrator:
    """
    المنسق الأساسي (V2) - المحرك المستقل لنظام INES.
    يدير سير العمل الديناميكي الموجه بقرارات "أثينا" الاستراتيجية.
    """
    def __init__(self):
        self.running_workflows: Dict[str, Dict[str, Any]] = {}
        self.completed_workflows: Dict[str, Dict[str, Any]] = {}
        
        # [جديد] تسجيل جميع الوكلاء المتاحين في النظام
        self.agents = {
            "idea_generator": idea_generator_agent,
            "blueprint_architect": blueprint_architect_agent,
            "chapter_composer": chapter_composer_agent,
            "literary_critic": literary_critic_agent,
            "psychological_profiler": psychological_profiler_agent,
            "athena_orchestrator": athena_orchestrator
            # ... إضافة بقية الوكلاء هنا ...
        }
        logger.info(f"✅ CoreOrchestrator (V2) initialized with {len(self.agents)} registered agents.")

    async def start_autonomous_workflow(self, project_goal: str, initial_context: Dict[str, Any]) -> str:
        """
        يبدأ سير عمل مستقل وديناميكي موجه بواسطة أثينا.
        """
        execution_id = f"exec_{uuid.uuid4().hex[:12]}"
        logger.info(f"🚀 Starting AUTONOMOUS workflow '{execution_id}' with goal: '{project_goal}'")

        # إعادة تعيين الذاكرة لمشروع جديد
        narrative_memory.clear()
        
        # إعداد حالة المشروع
        project_state = {
            "goal": project_goal,
            "initial_context": initial_context,
            "task_history": [],
            "last_task_output": {"summary": "Workflow initiated."},
            "latest_critique": None,
        }
        
        self.running_workflows[execution_id] = project_state
        
        # تشغيل سير العمل في الخلفية
        asyncio.create_task(self._execute_autonomous_workflow(execution_id, project_state))
        
        return execution_id

    async def _execute_autonomous_workflow(self, execution_id: str, project_state: Dict[str, Any]):
        """
        التنفيذ الفعلي لسير العمل المستقل.
        """
        try:
            for cycle in range(20): # الحد الأقصى للدورات لمنع الحلقات اللانهائية
                logger.info(f"--- 🔄 Workflow Cycle {cycle + 1} for exec_id: {execution_id} ---")

                # 1. أثينا تقرر المهمة التالية
                decision_obj = await athena_orchestrator.decide_next_task(
                    project_goal=project_state["goal"],
                    project_state=project_state
                )
                
                if not decision_obj:
                    raise RuntimeError("Athena failed to make a decision. Halting workflow.")
                
                decision = StrategicDecision.parse_obj(decision_obj)
                
                # التحقق من شرط التوقف
                if decision.next_task_type == TaskType.FINISH_WORKFLOW:
                    logger.info(f"🏁 Athena decided to finish the workflow. Reason: {decision.justification}")
                    break

                # 2. تنفيذ المهمة التي قررتها أثينا
                target_agent_id = decision.input_data.get("agent_id")
                target_agent = self.agents.get(target_agent_id)
                
                if not target_agent:
                    raise ValueError(f"Agent '{target_agent_id}' decided by Athena is not registered.")

                logger.info(f"Executing task '{decision.next_task_type.value}' on agent '{target_agent_id}'...")
                
                # تمرير السياق اللازم للمهمة
                task_context = decision.input_data
                
                # دمج المخرجات السابقة إذا لزم الأمر
                # (يمكن لأثينا تحديد ذلك في input_data)
                if task_context.get("use_last_output"):
                    task_context.update(project_state["last_task_output"].get("content", {}))

                task_output = await target_agent.process_task(task_context)

                # 3. تحديث حالة المشروع والذاكرة
                self._update_project_state(project_state, decision, task_output)
                
                # إضافة المخرجات الرئيسية إلى الذاكرة السردية
                if task_output.get("status") == "success" and "content" in task_output:
                     # نحول المحتوى إلى نص قبل إضافته للذاكرة
                    content_to_embed = json.dumps(task_output["content"], ensure_ascii=False)
                    narrative_memory.add_entry(
                        entry_type=decision.next_task_type.value,
                        content=content_to_embed,
                        metadata={"agent_id": target_agent_id}
                    )
            else:
                 logger.warning(f"Workflow {execution_id} reached max cycles (20). Terminating.")

            project_state["status"] = "completed"
        except Exception as e:
            logger.error(f"❌ Workflow {execution_id} failed: {e}", exc_info=True)
            project_state["status"] = "failed"
            project_state["error"] = str(e)
        
        self.completed_workflows[execution_id] = project_state
        del self.running_workflows[execution_id]

    def _update_project_state(self, state: Dict, decision: StrategicDecision, output: Dict):
        """
        تحديث كائن حالة المشروع بعد كل مهمة.
        """
        state["task_history"].append({
            "task": decision.next_task_type.value,
            "justification": decision.justification,
            "output_summary": output.get("summary", "No summary provided.")
        })
        state["last_task_output"] = output
        state["last_task_type"] = decision.next_task_type.value
        
        # إذا كانت المهمة نقدًا، نحفظ التقييم
        if "critique" in decision.next_task_type.value:
            state["latest_critique"] = output.get("content", {}).get("critique_report")
            
    def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """
        الحصول على حالة سير عمل معين.
        """
        if execution_id in self.running_workflows:
            state = self.running_workflows[execution_id]
            return {
                "status": "running",
                "goal": state["goal"],
                "progress": f"{len(state['task_history'])} steps completed.",
                "last_task": state.get("last_task_type")
            }
        elif execution_id in self.completed_workflows:
            state = self.completed_workflows[execution_id]
            return {
                "status": state["status"],
                "goal": state["goal"],
                "final_output": state.get("last_task_output", {}).get("content"),
                "error": state.get("error")
            }
        else:
            return {"status": "not_found"}

# إنشاء مثيل وحيد
core_orchestrator = CoreOrchestrator()
