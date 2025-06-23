# core/core_orchestrator.py (V8 - MCP Enabled)
import logging
from typing import Dict, Any

# ... (كل الاستيرادات السابقة) ...
from ..agents.context_distiller_agent import context_distiller_agent

logger = logging.getLogger("CoreOrchestrator-V8")

class CoreOrchestrator:
    """
    المنسق الأساسي (V8).
    ينفذ بروتوكول ضغط السياق وتفويض المهام (MCP) لتحقيق أقصى
    قدر من الكفاءة والجودة.
    """
    def __init__(self):
        # ... (تسجيل الوكلاء، بما في ذلك context_distiller_agent) ...
        self.agents = {"context_distiller": context_distiller_agent} # كمثال
        logger.info("✅ MCP-Enabled CoreOrchestrator (V8) Initialized.")

    # ... (دالة start_autonomous_workflow كما هي) ...

    async def _execute_autonomous_workflow(self, execution_id: str):
        """
        التنفيذ الفعلي لسير العمل المستقل باستخدام بروتوكول MCP.
        """
        execution = self.running_workflows[execution_id]
        project_state = {"initial_context": execution["context_data"]} # كائن الحالة
        last_task_output = {}

        try:
            for i in range(20): # الحد الأقصى للخطوات
                logger.info(f"--- MCP-Enabled Cycle {i+1} for exec_id: {execution_id} ---")

                # 1. "أثينا" تقرر الخطوة التالية (الـ "ماذا")
                athena_context = {"project_state": project_state, "last_task_output": last_task_output}
                decision_result = await self.agents["athena_orchestrator"].process_task(athena_context)
                strategic_decision = decision_result.get("content", {}).get("strategic_decision")
                
                next_task_type = strategic_decision.get("next_task_type")
                target_agent_id = strategic_decision.get("input_data", {}).get("agent_id")
                task_description = strategic_decision.get("justification")
                
                # ... (منطق التحقق من الإنهاء) ...

                # 2. [جديد] "مُحضِّر السياق" يحضر المهمة (الـ "كيف")
                logger.info(f"MCP Step 1: Distilling context for agent '{target_agent_id}'...")
                distillation_context = {
                    "full_project_state": project_state,
                    "next_task_description": task_description,
                    "target_agent_id": target_agent_id
                }
                distill_result = await self.agents["context_distiller"].process_task(distillation_context)
                if distill_result["status"] == "error": raise RuntimeError("Context distillation failed.")
                distilled_context = distill_result["content"]["distilled_context"]
                
                # 3. المنسق ينفذ المهمة مع السياق المضغوط
                logger.info(f"MCP Step 2: Executing task '{next_task_type}' with distilled context...")
                target_agent = self.agents.get(target_agent_id)
                
                # تمرير السياق المضغوط فقط إلى الوكيل المستهدف
                last_task_output = await target_agent.process_task(distilled_context)
                
                # 4. تحديث حالة المشروع الكاملة بالنتائج
                self._update_project_state(project_state, last_task_output, next_task_type)
                execution["task_history"].append({"task": next_task_type, "summary": str(last_task_output)[:200]})

            # ... (نهاية سير العمل) ...

        except Exception as e:
            # ... (معالجة الأخطاء) ...
            
    # ... (بقية الدوال المساعدة)
# في core/core_orchestrator.py

class CoreOrchestrator:
    # ...
    async def _execute_dynamic_workflow(self, execution_id: str):
        # ...
        # داخل حلقة تنفيذ المهام
        
        if task_data.get("is_loop"):
            # [منطق جديد] التعامل مع المهام التكرارية
            loop_data_path = task_data.get("loop_over")
            # استخلاص قائمة العناصر للتكرار عليها من مخرجات مهمة سابقة
            items_to_loop = self._get_data_from_path(execution["task_outputs"], loop_data_path)
            
            sub_tasks_results = []
            for item in items_to_loop:
                # لكل عنصر، قم بتنفيذ المهمة مع تمرير العنصر كسياق
                item_context = {**context, "current_item": item}
                sub_task_result = await handler(task_data, item_context)
                sub_tasks_results.append(sub_task_result)
            
            result = {"status": "success", "content": {"loop_results": sub_tasks_results}}
        else:
            # تنفيذ المهمة العادية
            result = await handler(task_data, context)
            
        # ...
