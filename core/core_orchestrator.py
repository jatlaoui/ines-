# core/core_orchestrator.py (V5 - The Creative Partner)
# ... (كل الاستيرادات والتهيئة من النسخة السابقة) ...

class CoreOrchestrator:
    # ... (دوال التهيئة وتسجيل الوكلاء كما هي) ...

    async def _execute_dynamic_workflow(self, execution_id: str):
        """
        التنفيذ الفعلي لسير العمل مع منطق التقييم المقارن وحقن الطفرات.
        """
        # ... (نفس منطق بدء التنفيذ والحلقة الرئيسية) ...

        # --- داخل حلقة تنفيذ المهام ---
        for task_data in tasks_to_run:
            if task_data["id"] in completed_tasks:
                continue

            if all(dep in completed_tasks for dep in task_data.get("dependencies", [])):
                
                # --- [منطق جديد] التعامل مع دورات التخطيط الديناميكي المحسّنة ---
                if TaskType(task_data["task_type"]) == TaskType.DYNAMIC_REPLAN:
                    logger.info(">>>--- DYNAMIC RE-PLANNING CYCLE (with Chaos Injection) ---<<<")
                    # استدعاء وكيل الفوضى الإبداعية
                    chaos_context = {"story_context": self._get_story_summary(execution), "established_rules": list(narrative_guardian.fact_database.keys())}
                    mutation = await self.agents["creative_chaos_agent"].process_task(chaos_context)
                    
                    # استدعاء مهندس المخططات مع "الطفرة" المقترحة
                    replan_context = {"initial_blueprint": execution["context_data"].get("current_blueprint"), "mutation_suggestion": mutation.get("content")}
                    updated_blueprint = await self.agents["blueprint_architect"].process_task(replan_context)
                    
                    execution["context_data"]["current_blueprint"] = updated_blueprint.get("blueprint")
                    result = {"status": "success", "message": "Blueprint updated with creative mutation."}

                # --- [منطق جديد] التعامل مع النقد المقارن ---
                elif task_data["input_data"].get("critique_type") == "comparative":
                    logger.info(f">>>--- COMPARATIVE CRITIQUE CYCLE for task '{task_data['name']}' ---<<<")
                    # استدعاء الناقد المقارن
                    critique_report = await self.agents["literary_critic"].process_task(input_payload)
                    
                    # استدعاء مهندس التجربة التفاعلية لتقديم الخيارات للمستخدم
                    decision_context = {
                        "decision_context": {
                            "character": "Unknown", # يجب تحديدها من السياق
                            "options": [
                                {"id": "sensory", "summary": critique_report["content"]["critique_report"]["creative_alternatives"]["sensory_version"]},
                                {"id": "psychological", "summary": critique_report["content"]["critique_report"]["creative_alternatives"]["psychological_version"]},
                                {"id": "action", "summary": critique_report["content"]["critique_report"]["creative_alternatives"]["action_oriented_version"]},
                            ]
                        }
                    }
                    result = await self.agents["interactive_architect"].process_task(decision_context)
                    # في نظام حقيقي، سينتظر المنسق هنا رد المستخدم
                
                else:
                    # تنفيذ المهمة العادية
                    # ... (نفس منطق التنفيذ السابق) ...

                # ... (بقية منطق الحلقة) ...


    def _get_story_summary(self, execution: Dict) -> str:
        """يجمع ملخصًا للقصة من الذاكرة السردية."""
        entries = narrative_memory.get_full_chronology()
        return "\n".join([entry.content for entry in entries])
        
# ... (بقية الملف) ...# في core/core_orchestrator.py

# ... (استيرادات أخرى) ...
from ..agents.fusion_synthesizer_agent import fusion_synthesizer_agent

class CoreOrchestrator:
    def _register_agents(self) -> Dict[str, BaseAgent]:
        # ... (تسجيل كل الوكلاء الآخرين) ...
        agents = super()._register_agents()
        agents["fusion_synthesizer"] = fusion_synthesizer_agent
        return agents

    def _initialize_task_handlers(self) -> Dict[TaskType, Any]:
        handlers = super()._initialize_task_handlers()
        # إضافة معالجات لمهام الاندماج
        handlers[TaskType.FUSION_ANALYZE_COMPATIBILITY] = self._handle_fusion_task
        handlers[TaskType.FUSION_SYNTHESIZE_NARRATIVE] = self._handle_fusion_task
        return handlers

    async def _handle_fusion_task(self, task_data: Dict, context: Dict) -> Dict:
        """معالج عام لمهام الاندماج السردي."""
        agent = self.agents["fusion_synthesizer"]
        # تمرير نوع المهمة الفرعية إلى الوكيل
        context["fusion_task_type"] = task_data["task_type"].value.replace("fusion_", "")
        return await agent.process_task(context)

# ... (بقية الملف)
# core/core_orchestrator.py (V6 - The Autonomous Core)
import logging
from typing import Dict, Any

# ... (كل الاستيرادات السابقة) ...
from ..orchestrators.athena_strategic_orchestrator import athena_orchestrator

logger = logging.getLogger("CoreOrchestrator-V6")

class CoreOrchestrator:
    """
    المنسق الأساسي المستقل (V6).
    يعمل تحت التوجيه الاستراتيجي لـ "أثينا"، مما يسمح بسير عمل
    ديناميكي ومستقل بالكامل.
    """
    def __init__(self):
        # ... (نفس التهيئة وتسجيل الوكلاء) ...
        self.agents["athena_orchestrator"] = athena_orchestrator
        logger.info("✅ Autonomous CoreOrchestrator V6 Initialized.")

    async def start_autonomous_workflow(self, project_goal: str, initial_context: Dict[str, Any], user_session: UserSession) -> str:
        """
        [جديد] بدء سير عمل مستقل وموجه بالهدف.
        """
        execution_id = f"exec_auto_{uuid.uuid4().hex[:10]}"
        logger.info(f"Starting AUTONOMOUS workflow for goal: '{project_goal}'")

        execution = {
            "id": execution_id,
            "user_id": user_session.user_id,
            "project_goal": project_goal,
            "status": WorkflowStatus.RUNNING.value,
            "project_state": {"initial_context": initial_context}, # الحالة المتراكمة للمشروع
            "task_history": [],
            "created_at": datetime.now().isoformat(),
        }
        
        self.running_workflows[execution_id] = execution
        asyncio.create_task(self._execute_autonomous_workflow(execution_id))
        return execution_id

    async def _execute_autonomous_workflow(self, execution_id: str):
        """
        التنفيذ الفعلي لسير العمل المستقل.
        الحلقة هنا لا تنتهي بانتهاء قائمة مهام، بل بتحقيق الهدف.
        """
        execution = self.running_workflows[execution_id]
        last_task_output = {}

        try:
            for i in range(20): # حد أقصى لعدد الخطوات لمنع الحلقات اللانهائية
                logger.info(f"--- Autonomous Cycle {i+1} for exec_id: {execution_id} ---")

                # 1. "أثينا" تقرر الخطوة التالية
                athena_context = {
                    "project_goal": execution["project_goal"],
                    "project_state": execution["project_state"],
                    "last_task_output": last_task_output
                }
                decision_result = await self.agents["athena_orchestrator"].process_task(athena_context)
                strategic_decision = decision_result.get("content", {}).get("strategic_decision")
                if not strategic_decision:
                    raise RuntimeError(f"Athena failed to provide a valid strategic decision. Last output: {decision_result}")

                next_task_type = strategic_decision.get("next_task_type")
                input_data = strategic_decision.get("input_data")
                logger.info(f"Athena's strategic decision: Execute '{next_task_type}' - Justification: {strategic_decision.get('justification')}")

                # التحقق من شرط التوقف
                if TaskType(next_task_type) == TaskType.FINISH_WORKFLOW:
                    logger.info("Athena decided to finish the workflow. Process complete.")
                    break

                # 2. المنسق ينفذ قرار "أثينا"
                task_data_for_handler = {"task_type": next_task_type, "input_data": input_data}
                context_for_handler = {**execution["project_state"], **input_data}
                handler = self.task_handlers.get(TaskType(next_task_type))
                
                last_task_output = await handler(task_data_for_handler, context_for_handler)
                
                # 3. تحديث حالة المشروع بالمخرجات الجديدة
                self._update_project_state(execution["project_state"], last_task_output)
                execution["task_history"].append({
                    "task": next_task_type,
                    "output_summary": str(last_task_output)[:200] # ملخص للمخرجات
                })

            execution["status"] = WorkflowStatus.COMPLETED.value
            logger.info(f"✅ Autonomous workflow '{execution_id}' completed successfully.")

        except Exception as e:
            execution["status"] = WorkflowStatus.FAILED.value
            execution["error_message"] = str(e)
            logger.error(f"❌ Autonomous workflow '{execution_id}' failed. Reason: {e}", exc_info=True)

    def _update_project_state(self, current_state: Dict, task_output: Dict):
        """يدمج مخرجات المهمة الأخيرة في الحالة العامة للمشروع."""
        # هذا منطق دمج ذكي، يمكن تطويره ليكون أكثر تعقيدًا
        for key, value in task_output.items():
            if key in ["status", "summary"]: continue
            if isinstance(value, dict) and "content" in value:
                # استخلاص المحتوى الرئيسي
                main_content = value["content"]
                # تحديد مفتاح مناسب للحالة
                state_key = key
                if "critique" in key:
                    state_key = "latest_critique"
                elif "chapter" in key:
                    state_key = "latest_chapter"
                current_state[state_key] = main_content

# ... بقية الملف والمنسق الأساسي
