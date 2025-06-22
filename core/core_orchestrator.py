# core/core_orchestrator.py (النسخة النهائية V4 - كامل الصلاحيات)
import asyncio
import logging
import uuid
from typing import Dict, Any, List
from dataclasses import asdict

# ... (كل استيرادات الوكلاء والمكونات كما في الرد السابق) ...
from ..agents.audio_musical_producer_agent import audio_musical_producer_agent
from ..agents.interactive_experience_architect import interactive_architect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CoreOrchestrator-V4] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoreOrchestrator:
    """
    المنسق الأساسي النهائي (V4).
    يدير سير عمل ديناميكي بالكامل مع تفعيل سلطة الفيتو لحارس السرد.
    """
    def __init__(self):
        self.running_workflows: Dict[str, Any] = {}
        self.agents: Dict[str, BaseAgent] = self._register_agents()
        self.task_handlers: Dict[str, Any] = self._initialize_task_handlers()
        logger.info("✅ CoreOrchestrator V4 (Final) Initialized.")

    def _register_agents(self) -> Dict[str, BaseAgent]:
        """تسجيل جميع وكلاء النظام."""
        return {
            # ... (كل الوكلاء السابقين) ...
            "audio_musical_producer": audio_musical_producer_agent,
            "interactive_architect": interactive_architect,
        }

    def _initialize_task_handlers(self) -> Dict[str, Any]:
        # ... (نفس تعريف المعالجات من الرد السابق)
        return {}


    async def _execute_dynamic_workflow(self, execution_id: str):
        """
        التنفيذ الفعلي لسير العمل مع منطق الفيتو والتخطيط التفاعلي.
        """
        execution = self.running_workflows[execution_id]
        # ... (بداية التنفيذ كما هي) ...

        completed_tasks = set()
        
        try:
            while len(completed_tasks) < len(execution["tasks"]):
                task_executed_in_cycle = False
                for task_data in execution["tasks"]:
                    if task_data["id"] in completed_tasks:
                        continue

                    if all(dep in completed_tasks for dep in task_data.get("dependencies", [])):
                        max_retries = 2
                        current_retry = 0
                        task_successful = False

                        while current_retry <= max_retries and not task_successful:
                            # ... (نفس منطق استدعاء المعالج من الرد السابق) ...
                            result = await handler(task_data, context)
                            
                            # --- [منطق جديد] التحقق الإلزامي من حارس السرد ---
                            content_to_check = self._extract_content_from_result(result)
                            if content_to_check:
                                logger.info(f"Guardian is checking output of '{task_data['name']}'...")
                                inconsistencies = await narrative_guardian.check_consistency(content_to_check)
                                
                                if inconsistencies:
                                    current_retry += 1
                                    logger.warning(
                                        f"CONSISTENCY VIOLATION in '{task_data['name']}' (Attempt {current_retry}/{max_retries}): {inconsistencies}"
                                    )
                                    if current_retry > max_retries:
                                        raise RuntimeError(f"Task '{task_data['name']}' failed consistency check after {max_retries} retries.")
                                    
                                    # حقن ملاحظات الحارس لإعادة المحاولة
                                    context["guardian_feedback"] = inconsistencies
                                    logger.info(f"Retrying task '{task_data['name']}' with feedback from the Guardian.")
                                    continue # إعادة المحاولة في الحلقة الداخلية
                                else:
                                    logger.info("Guardian: Consistency check passed.")

                            # المهمة نجحت
                            task_successful = True
                            await self._process_task_output(task_data, result, execution_id)
                            completed_tasks.add(task_data["id"])
                            task_executed_in_cycle = True
                
                if not task_executed_in_cycle:
                    raise RuntimeError("Workflow stalled.")

            execution["status"] = WorkflowStatus.COMPLETED.value
            logger.info(f"✅ Workflow '{execution['name']}' completed successfully.")

        except Exception as e:
            # ... (معالجة الأخطاء كما هي) ...

    # ... (بقية الدوال المساعدة كما هي) ...

core_orchestrator = CoreOrchestrator()
