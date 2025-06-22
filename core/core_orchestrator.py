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

