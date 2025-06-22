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
        
# ... (بقية الملف) ...
