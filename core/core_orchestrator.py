# في core/core_orchestrator.py (V7 - State-Managed)

class CoreOrchestrator:
    # ...
    async def _execute_autonomous_workflow(self, execution_id: str):
        execution = self.running_workflows[execution_id]
        
        # [جديد] تعريف كائن الحالة الموحد
        project_state = {
            "goal": execution["project_goal"],
            "initial_context": execution["context_data"],
            "outputs": {}, # سيتم تخزين كل المخرجات هنا
            "critiques": [],
            "current_status_summary": "Starting..."
        }
        
        # ... (داخل الحلقة الرئيسية) ...
        # بدلاً من تمرير مخرجات المهمة الأخيرة فقط
        athena_context = {"project_state": project_state} # أثينا تحصل على كل شيء
        
        # ...
        # عند تنفيذ مهمة
        context_for_handler = project_state # الوكيل يحصل على كل شيء
        
        # ...
        # عند تحديث الحالة
        self._update_project_state(project_state, task_output, next_task_type)

    def _update_project_state(self, current_state: Dict, task_output: Dict, task_type: str):
        """[مُحسّن] يدمج المخرجات في كائن الحالة الموحد بطريقة منظمة."""
        # يضيف المخرجات إلى `current_state['outputs']`
        # ويقوم بتحديث `current_status_summary`
        # ...
