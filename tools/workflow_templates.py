# tools/workflow_templates.py (النسخة الكاملة التي تم تقديمها سابقًا)
from typing import Dict, List
from core.core_orchestrator import WorkflowTemplate, WorkflowTask, TaskType, TaskPriority

class AdvancedWorkflowTemplates:
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        self._create_advanced_templates()

    def _create_advanced_templates(self):
        # ----------------------------------------------------------------------
        # 1. قالب كتابة رواية كاملة (معزز بالذاكرة والتحقق)
        # ----------------------------------------------------------------------
        complete_novel_enhanced = WorkflowTemplate(
            id="complete_novel_v2",
            name="رحلة الروائي الكاملة (معززة بالذكاء)",
            description="سير عمل شامل لكتابة رواية من الفكرة إلى المسودة النهائية، مع التحقق من الاتساق والتخطيط الديناميكي.",
            category="writing_process",
            tasks=[
                # ... (المهام كما تم تعريفها في الرد السابق) ...
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
                 # ... (بقية المهام) ...
            ]
        )
        
        # ----------------------------------------------------------------------
        # 2. قالب كتابة مسرحية اجتماعية نقدية طويلة (القالب الجديد)
        # ----------------------------------------------------------------------
        long_form_social_play = WorkflowTemplate(
            id="long_form_social_play_v1",
            name="مسرحية اجتماعية نقدية (نسخة مطولة)",
            description="سير عمل متكامل لإنتاج مسرحية طويلة من فصل واحد، مع تطوير الشخصيات والحبكات الفرعية.",
            category="playwriting",
            tasks=[
                WorkflowTask(id="task_1_concept_analysis", name="تحليل المفهوم الأساسي", task_type=TaskType.ANALYZE_NOVEL, input_data={"text_content": "{initial_idea}"}),
                WorkflowTask(id="task_2_profiling", name="بناء الملف النفسي للبطل (مبروك)", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "psychological_profiler", "prompt_id": "mabrouk_profile_prompt"}, dependencies=["task_1_concept_analysis"]),
                WorkflowTask(id="task_3_dramaturgy", name="بناء الهيكل الدرامي العام", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "dramaturg_agent"}, dependencies=["task_2_profiling"]),
                
                # الفصل الأول
                WorkflowTask(id="task_4_act1_scene1", name="كتابة المشهد الأول (البيت)", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "narrative_constructor_agent", "scene_outline_prompt_id": "act1_scene1_prompt"}, dependencies=["task_3_dramaturgy"]),
                WorkflowTask(id="task_5_act1_scene2", name="كتابة المشهد الثاني (الإدارة)", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "narrative_constructor_agent", "scene_outline_prompt_id": "act1_scene2_prompt"}, dependencies=["task_4_act1_scene1"]),
                
                # الفصل الثاني
                WorkflowTask(id="task_6_act2_scene1", name="كتابة المشهد الثالث (المقهى)", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "narrative_constructor_agent", "scene_outline_prompt_id": "act2_scene1_prompt"}, dependencies=["task_5_act1_scene2"]),
                WorkflowTask(id="task_7_act2_scene2", name="كتابة المشهد الرابع (المعتمد)", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "narrative_constructor_agent", "scene_outline_prompt_id": "act2_scene2_prompt"}, dependencies=["task_6_act2_scene1"]),
                WorkflowTask(id="task_8_act2_scene3", name="كتابة المونولوج (الشارع)", task_type=TaskType.GENERATE_CHAPTER, input_data={"prompt_id": "monologue_prompt"}, dependencies=["task_7_act2_scene2"]),

                # الفصل الثالث
                WorkflowTask(id="task_9_act3_scene1", name="كتابة مشهد الذروة (الحبل)", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "narrative_constructor_agent", "scene_outline_prompt_id": "act3_scene1_prompt"}, dependencies=["task_8_act2_scene3"]),
                WorkflowTask(id="task_10_act3_scene2", name="كتابة المشهد النهائي (التحرر)", task_type=TaskType.CUSTOM_AGENT_TASK, input_data={"agent_id": "narrative_constructor_agent", "scene_outline_prompt_id": "act3_scene2_prompt"}, dependencies=["task_9_act3_scene1"]),
                
                # التجميع والمراجعة
                WorkflowTask(id="task_11_assembly", name="تجميع المسرحية الكاملة", task_type=TaskType.MERGE_DATA, input_data={"source_tasks": ["task_4_act1_scene1", "task_5_act1_scene2", "task_6_act2_scene1", "task_7_act2_scene2", "task_8_act2_scene3", "task_9_act3_scene1", "task_10_act3_scene2"]}, dependencies=["task_10_act3_scene2"]),
                WorkflowTask(id="task_12_final_review", name="المراجعة النقدية النهائية", task_type=TaskType.CHECK_CONSISTENCY, dependencies=["task_11_assembly"]),
            ]
        )
        
        # تسجيل القوالب
        self.templates[complete_novel_enhanced.id] = complete_novel_enhanced
        self.templates[long_form_social_play.id] = long_form_social_play

# ... (بقية الملف كما هو)
workflow_template_manager = AdvancedWorkflowTemplates()
