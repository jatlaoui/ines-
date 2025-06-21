# tools/workflow_templates.py (النسخة المحسّنة والموسّعة)
"""
قوالب سير العمل المتقدمة لنظام "إينيس"
يحتوي على مجموعة شاملة من "الوصفات الإبداعية" التي تستفيد من كامل قدرات النظام.
"""
from typing import Dict, List
from core.core_orchestrator import WorkflowTemplate, WorkflowTask, TaskType, TaskPriority

class AdvancedWorkflowTemplates:
    """
    مدير قوالب سير العمل المتقدمة.
    """
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        self._create_advanced_templates()

    def _create_advanced_templates(self):
        """إنشاء قوالب سير العمل المتقدمة والمحسّنة."""

        # ----------------------------------------------------------------------
        # 1. قالب كتابة رواية كاملة (معزز بالذاكرة والتحقق)
        # ----------------------------------------------------------------------
        complete_novel_enhanced = WorkflowTemplate(
            id="complete_novel_v2",
            name="رحلة الروائي الكاملة (معززة بالذكاء)",
            description="سير عمل شامل لكتابة رواية من الفكرة إلى المسودة النهائية، مع التحقق من الاتساق والتخطيط الديناميكي.",
            category="writing_process",
            tasks=[
                WorkflowTask(
                    id="task_1_initial_analysis",
                    name="التحليل العميق للفكرة المصدر",
                    task_type=TaskType.ANALYZE_NOVEL,
                    input_data={"analysis_depth": "deep"},
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_2_idea_generation",
                    name="توليد الأفكار المحورية",
                    task_type=TaskType.GENERATE_IDEAS,
                    input_data={"count": 5, "creativity_level": "high"},
                    dependencies=["task_1_initial_analysis"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_3_blueprint_creation",
                    name="بناء المخطط السردي الأولي",
                    task_type=TaskType.BUILD_BLUEPRINT,
                    input_data={"structure_type": "dynamic_three_act"},
                    dependencies=["task_2_idea_generation"]
                ),
                # --- بداية دورة كتابة الفصول مع التخطيط الدوري ---
                # يتم محاكاة التكرار هنا بتعريف المهام بشكل متسلسل
                # في التنفيذ الفعلي، سيقوم المنسق بتكرار هذه المجموعة من المهام
                
                # --- الكتلة الأولى (الفصول 1-5) ---
                WorkflowTask(
                    id="task_4_generate_chapters_1_5",
                    name="كتابة الفصول (1-5)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"chapter_count": 5},
                    dependencies=["task_3_blueprint_creation"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_5_consistency_check_1",
                    name="فحص الاتساق (بعد الفصل 5)",
                    task_type=TaskType.VALIDATE_CONSISTENCY,
                    dependencies=["task_4_generate_chapters_1_5"],
                ),
                WorkflowTask(
                    id="task_6_dynamic_replan_1",
                    name="دورة التخطيط الديناميكي (1)",
                    task_type=TaskType.DYNAMIC_REPLAN,
                    dependencies=["task_5_consistency_check_1"],
                    priority=TaskPriority.HIGH
                ),

                # --- الكتلة الثانية (الفصول 6-10) ---
                WorkflowTask(
                    id="task_7_generate_chapters_6_10",
                    name="كتابة الفصول (6-10)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"chapter_count": 5, "start_chapter": 6},
                    dependencies=["task_6_dynamic_replan_1"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_8_consistency_check_2",
                    name="فحص الاتساق (بعد الفصل 10)",
                    task_type=TaskType.VALIDATE_CONSISTENCY,
                    dependencies=["task_7_generate_chapters_6_10"],
                ),
                WorkflowTask(
                    id="task_9_dynamic_replan_2",
                    name="دورة التخطيط الديناميكي (2)",
                    task_type=TaskType.DYNAMIC_REPLAN,
                    dependencies=["task_8_consistency_check_2"],
                    priority=TaskPriority.HIGH
                ),

                # --- الكتلة النهائية ---
                 WorkflowTask(
                    id="task_10_generate_final_chapters",
                    name="كتابة الفصول النهائية",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"chapter_count": 5, "start_chapter": 11, "focus": "resolution"},
                    dependencies=["task_9_dynamic_replan_2"],
                    priority=TaskPriority.URGENT
                ),
                WorkflowTask(
                    id="task_11_final_consistency_check",
                    name="فحص الاتساق النهائي والشامل",
                    task_type=TaskType.CHECK_CONSISTENCY, # مهمة الناقد الشاملة
                    dependencies=["task_10_generate_final_chapters"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_12_final_report",
                    name="توليد تقرير الرواية النهائي",
                    task_type=TaskType.GENERATE_REPORT,
                    dependencies=["task_11_final_consistency_check"]
                ),
            ]
        )

        # ----------------------------------------------------------------------
        # 2. قالب "محاكاة الأسلوب" (للكتابة بأسلوب مؤلف معين)
        # ----------------------------------------------------------------------
        style_mimic_template = WorkflowTemplate(
            id="style_mimic_v1",
            name="الكتابة بأسلوب العمالقة",
            description="يحلل نصًا مرجعيًا لكاتب معين، ثم يكتب فصلاً جديدًا بنفس الأسلوب.",
            category="style_transfer",
            tasks=[
                WorkflowTask(
                    id="task_1_analyze_reference",
                    name="تحليل أسلوب النص المرجعي",
                    task_type=TaskType.ANALYZE_NOVEL,
                    input_data={"analysis_focus": "style"},
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_2_extract_style_directives",
                    name="استخلاص توجيهات الأسلوب",
                    task_type=TaskType.CUSTOM_AGENT_TASK, # يمكن استخدام وكيل متخصص هنا
                    input_data={"agent_id": "adaptive_learner", "type": "get_directives"},
                    dependencies=["task_1_analyze_reference"],
                ),
                WorkflowTask(
                    id="task_3_generate_chapter_with_style",
                    name="كتابة فصل بأسلوب الكاتب",
                    task_type=TaskType.GENERATE_CHAPTER,
                    # سيتم حقن `style_directives` من المهمة السابقة تلقائيًا
                    dependencies=["task_2_extract_style_directives"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_4_review_mimicked_style",
                    name="نقد الأسلوب المحاكى",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={"agent_id": "literary_critic", "critique_focus": "style_authenticity"},
                    dependencies=["task_3_generate_chapter_with_style"],
                ),
            ]
        )
        
        # ----------------------------------------------------------------------
        # 3. قالب تحويل شهادة إلى قصة قصيرة (باستخدام نظام الشاهد)
        # ----------------------------------------------------------------------
        witness_to_story_template = WorkflowTemplate(
            id="witness_to_story_v1",
            name="من الحقيقة إلى الخيال",
            description="يحول ترانسكريبت (شهادة) إلى قصة قصيرة مؤثرة مع الحفاظ على الأصالة.",
            category="documentary_fiction",
            tasks=[
                WorkflowTask(
                    id="task_1_ingest_witness",
                    name="استيعاب وتحليل شهادة الشاهد",
                    task_type=TaskType.WITNESS_ANALYZE, # مهمة جديدة من وكيل الشاهد
                    input_data={"analysis_depth": "deep"},
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_2_build_narrative_from_witness",
                    name="بناء مخطط سردي من الشهادة",
                    task_type=TaskType.BUILD_BLUEPRINT,
                    # سيتم تمرير مخرجات الشاهد تلقائيًا كسياق
                    dependencies=["task_1_ingest_witness"]
                ),
                WorkflowTask(
                    id="task_3_compose_story",
                    name="تأليف القصة القصيرة",
                    task_type=TaskType.GENERATE_CHAPTER, # يمكن استخدامه لكتابة قصة قصيرة
                    input_data={"chapter_count": 1, "target_length": 2000},
                    dependencies=["task_2_build_narrative_from_witness"]
                ),
                 WorkflowTask(
                    id="task_4_integrate_authentic_quotes",
                    name="دمج اقتباسات أصيلة",
                    task_type=TaskType.WITNESS_INTEGRATE, # مهمة جديدة من وكيل الشاهد
                    input_data={"integration_style": "seamless"},
                    dependencies=["task_3_compose_story"]
                ),
            ]
        )
        
        # تسجيل جميع القوالب
        self.templates = {
            complete_novel_enhanced.id: complete_novel_enhanced,
            style_mimic_template.id: style_mimic_template,
            witness_to_story_template.id: witness_to_story_template,
            # ... يمكن إضافة قوالب أخرى هنا ...
        }

    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """الحصول على قالب سير عمل محدد."""
        return self.templates.get(template_id)

    def list_templates(self) -> List[Dict[str, Any]]:
        """قائمة بجميع القوالب المتاحة."""
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "category": t.category,
                "task_count": len(t.tasks)
            }
            for t in self.templates.values()
        ]

# إنشاء مثيل وحيد لمدير القوالب
workflow_template_manager = AdvancedWorkflowTemplates()
