# core/core_orchestrator.py (النسخة المحسّنة)
import asyncio
import logging
from typing import Dict, Any, List, Optional

# ... (بقية الاستيرادات كما هي) ...
# --- استيراد المكونات الجديدة ---
from .core_narrative_memory import narrative_memory
from ..agents.narrative_guardian_agent import narrative_guardian
from ..agents.adaptive_learning_agent import adaptive_learner

class CoreOrchestrator:
    def __init__(self):
        # ... (التهيئة الحالية كما هي) ...
        # --- إضافة الوكلاء الجدد إلى قائمة الوكلاء المتاحين ---
        self.agents["narrative_guardian"] = narrative_guardian
        self.agents["adaptive_learner"] = adaptive_learner
        
        # --- إضافة المهام الجديدة إلى السجل ---
        self._init_default_handlers() # إعادة تهيئة المعالجات
    
    def _init_default_handlers(self):
        super()._init_default_handlers() # استدعاء المعالجات الأصلية
        # إضافة المعالجات الجديدة
        self.task_handlers[TaskType.VALIDATE_CONSISTENCY] = self._handle_validate_consistency
        self.task_handlers[TaskType.ANALYZE_USER_EDIT] = self._handle_analyze_user_edit
        self.task_handlers[TaskType.DYNAMIC_REPLAN] = self._handle_dynamic_replan

    async def _execute_workflow(self, execution_id: str):
        """
        تنفيذ سير العمل الفعلي مع إضافة دورة التخطيط الديناميكي والتحقق.
        """
        try:
            execution = self.running_workflows[execution_id]
            # ... (بداية التنفيذ كما هي) ...

            total_tasks = len(execution.tasks)
            completed_tasks_ids = set()

            while len(completed_tasks_ids) < total_tasks:
                # --- [مُحسّن] إضافة دورة تخطيط ديناميكي كل 3 مهام مكتملة ---
                if len(completed_tasks_ids) > 0 and len(completed_tasks_ids) % 3 == 0:
                    # تحقق مما إذا كنا قد خططنا بالفعل لهذه المرحلة
                    planning_cycle_id = f"planning_cycle_{len(completed_tasks_ids)}"
                    if planning_cycle_id not in completed_tasks_ids:
                        logger.info(">>>-- Starting Dynamic Re-planning Cycle --<<<")
                        await self._execute_task(
                            WorkflowTask(id=planning_cycle_id, name="Dynamic Re-planning", task_type=TaskType.DYNAMIC_REPLAN),
                            execution
                        )
                        completed_tasks_ids.add(planning_cycle_id) # نضيفه كأنه مهمة مكتملة

                # البحث عن المهام الجاهزة للتنفيذ
                ready_tasks = [
                    task for task in execution.tasks
                    if task.status == TaskStatus.PENDING and
                       all(dep in completed_tasks_ids for dep in task.dependencies)
                ]

                # ... (بقية منطق حلقة التنفيذ كما هو) ...
                for task in ready_tasks:
                    await self._execute_task(task, execution)
                    # --- [مُحسّن] إضافة خطوة التحقق من الاتساق بعد الكتابة ---
                    if task.task_type == TaskType.GENERATE_CHAPTER and task.status == TaskStatus.COMPLETED:
                        logger.info(">>>-- Handing over to Narrative Guardian for consistency check --<<<")
                        validation_task = WorkflowTask(id=f"validation_{task.id}", name="Validate Chapter", task_type=TaskType.VALIDATE_CONSISTENCY)
                        validation_result = await self._execute_task(validation_task, execution, context_override=task.output_data)

                        if validation_result.get("status") == "failure":
                            # إعادة المهمة الأصلية إلى قائمة الانتظار مع ملاحظات
                            task.status = TaskStatus.PENDING
                            # حقن ملاحظات الحارس في المهمة التالية
                            task.input_data["guardian_feedback"] = validation_result["inconsistencies"]
                            logger.warning(f"Task '{task.name}' sent back for revision by the Guardian.")
                            continue # الانتقال إلى المهمة التالية بدلاً من اعتبار هذه مكتملة
                    
                    completed_tasks_ids.add(task.id)
                    # ... (تحديث التقدم، إلخ) ...
            
            # ... (نهاية تنفيذ سير العمل كما هي) ...

        except Exception as e:
            # ... (معالجة الأخطاء كما هي) ...

    # --- معالجات المهام الجديدة ---

    async def _handle_validate_consistency(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج مهمة التحقق من الاتساق."""
        return await self.agents["narrative_guardian"].process_task(input_data)

    async def _handle_analyze_user_edit(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج مهمة تحليل تعديلات المستخدم."""
        return await self.agents["adaptive_learner"].process_task(context={"type": "analyze_edit", **input_data})
        
    async def _handle_dynamic_replan(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        معالج دورة التخطيط الديناميكي.
        """
        logger.info("DRAMATURG: Re-assessing plot based on recent developments.")
        # 1. الاستعلام من الذاكرة عن آخر التطورات
        recent_developments = narrative_memory.query("latest major plot points and character changes", top_k=5)
        
        # 2. استدعاء مهندس المخططات لتحديث الخطة
        blueprint_agent = self.agents["blueprint_architect"]
        updated_blueprint = await blueprint_agent.create_blueprint(context={
            "knowledge_base": context.get("from_deep_analysis"), # استخدام التحليل الأولي
            "dynamic_updates": [entry.content for entry in recent_developments] # إضافة التطورات الجديدة
        })
        
        # 3. تحديث سياق التنفيذ بالمخطط الجديد
        context["current_blueprint"] = updated_blueprint
        logger.info("PLAN UPDATED: Workflow will now proceed with the revised blueprint.")
        return {"status": "success", "updated_blueprint": updated_blueprint}
        
    # --- تحوير في معالج كتابة الفصل ---
    async def _handle_generate_chapter(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        معالج توليد الفصل (محسّن ليدمج توجيهات الأسلوب وملاحظات الحارس).
        """
        user_id = context.get("user_id") # نفترض وجوده في سياق التنفيذ
        
        # جلب توجيهات الأسلوب المخصصة للمستخدم
        style_directives = await adaptive_learner.get_style_directives(user_id)
        
        # دمج التوجيهات وملاحظات الحارس (إن وجدت) في الـ prompt
        chapter_context = input_data.get("from_detailed_blueprint", {})
        chapter_context["style_directives"] = style_directives
        if "guardian_feedback" in input_data:
            chapter_context["feedback"] = input_data["guardian_feedback"]

        # استدعاء وكيل كتابة الفصول مع السياق المعزز
        chapter_composer = self.agents["chapter_composer"]
        result = await chapter_composer.write_chapter(context=chapter_context) # استخدام write_chapter
        
        # إضافة النص الناتج إلى الذاكرة السردية
        if result.get("status") == "success":
            narrative_memory.add_entry(
                entry_type="chapter_summary",
                content=result["content"].get("chapter_content", "")[:200], # ملخص بسيط
                metadata={"chapter": chapter_context.get("chapter_number")}
            )

        return result
