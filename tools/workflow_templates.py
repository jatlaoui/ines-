# tools/workflow_templates.py (النسخة النهائية V3)
from typing import Dict, List, Optional
from core.core_orchestrator import WorkflowTemplate, WorkflowTask, TaskType, TaskPriority

class AdvancedWorkflowTemplates:
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        self._create_advanced_templates()

    def _create_advanced_templates(self):
        # ----------------------------------------------------------------------
        # القالب النهائي لكتابة مسرحية اجتماعية طويلة
        # ----------------------------------------------------------------------
        long_form_social_play = WorkflowTemplate(
            id="long_form_social_play_v1",
            name="إنتاج مسرحية اجتماعية نقدية (كاملة)",
            description="سير عمل متكامل لإنتاج مسرحية طويلة، مع تطوير الشخصيات، ودورات تخطيط ديناميكية، وفحص للاتساق.",
            category="playwriting",
            tasks=[
                # --- الإعداد والتحليل الأولي ---
                WorkflowTask(
                    id="task_1_concept_analysis",
                    name="تحليل الفكرة والمفهوم الأساسي",
                    task_type=TaskType.ANALYZE_NOVEL,
                    input_data={"agent_id": "dramaturg_agent", "text_content": "{initial_idea}"}
                ),
                WorkflowTask(
                    id="task_2_profiling",
                    name="بناء الملف النفسي للبطل (مبروك)",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={"agent_id": "psychological_profiler", "character_name": "مبروك", "character_context": "مواطن بسيط يعلق كل آماله على شهادة تقدير."},
                    dependencies=["task_1_concept_analysis"]
                ),
                WorkflowTask(
                    id="task_3_dramaturgy",
                    name="بناء الهيكل الدرامي الأولي",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={"agent_id": "dramaturg_agent"},
                    dependencies=["task_2_profiling"]
                ),
                
                # --- كتابة الفصل الأول ---
                WorkflowTask(
                    id="task_4_act1_scene1",
                    name="كتابة المشهد 1.1 (البيت)",
                    task_type=TaskType.GENERATE_CHAPTER, # استخدام المهمة العامة للكتابة
                    input_data={"agent_id": "narrative_constructor_agent", "prompt_id": "act1_scene1_prompt"},
                    dependencies=["task_3_dramaturgy"]
                ),
                WorkflowTask(
                    id="task_5_act1_scene2",
                    name="كتابة المشهد 1.2 (الإدارة)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"agent_id": "narrative_constructor_agent", "prompt_id": "act1_scene2_prompt"},
                    dependencies=["task_4_act1_scene1"]
                ),

                # --- دورة التخطيط الديناميكي الأولى ---
                WorkflowTask(
                    id="task_6_dynamic_replan_1",
                    name="دورة التخطيط الديناميكي الأولى",
                    task_type=TaskType.DYNAMIC_REPLAN,
                    dependencies=["task_5_act1_scene2"]
                ),
                
                # --- كتابة الفصل الثاني ---
                WorkflowTask(
                    id="task_7_act2_scene1",
                    name="كتابة المشهد 2.1 (المقهى)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"agent_id": "narrative_constructor_agent", "prompt_id": "act2_scene1_prompt"},
                    dependencies=["task_6_dynamic_replan_1"]
                ),
                WorkflowTask(
                    id="task_8_act2_scene2",
                    name="كتابة المشهد 2.2 (المونولوج)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"agent_id": "chapter_composer", "prompt_id": "monologue_prompt"},
                    dependencies=["task_7_act2_scene1"]
                ),

                # --- دورة التخطيط الديناميكي الثانية ---
                WorkflowTask(
                    id="task_9_dynamic_replan_2",
                    name="دورة التخطيط الديناميكي الثانية",
                    task_type=TaskType.DYNAMIC_REPLAN,
                    dependencies=["task_8_act2_scene2"]
                ),

                # --- كتابة الفصل الثالث ---
                WorkflowTask(
                    id="task_10_act3_scene1",
                    name="كتابة المشهد 3.1 (الذروة)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"agent_id": "narrative_constructor_agent", "prompt_id": "act3_scene1_prompt"},
                    dependencies=["task_9_dynamic_replan_2"]
                ),
                 WorkflowTask(
                    id="task_11_act3_scene2",
                    name="كتابة المشهد 3.2 (الخاتمة)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"agent_id": "narrative_constructor_agent", "prompt_id": "act3_scene2_prompt"},
                    dependencies=["task_10_act3_scene1"]
                ),
                
                # --- التجميع والمراجعة النهائية ---
                WorkflowTask(
                    id="task_12_assembly",
                    name="تجميع المسرحية الكاملة",
                    task_type=TaskType.MERGE_DATA,
                    input_data={"source_tasks": ["task_4_act1_scene1", "task_5_act1_scene2", "task_7_act2_scene1", "task_8_act2_scene2", "task_10_act3_scene1", "task_11_act3_scene2"]},
                    dependencies=["task_11_act3_scene2"]
                ),
                WorkflowTask(
                    id="task_13_final_review",
                    name="المراجعة النقدية النهائية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={"agent_id": "literary_critic"},
                    dependencies=["task_12_assembly"]
                ),
            ]
        )
        self.templates[long_form_social_play.id] = long_form_social_play

    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        return self.templates.get(template_id)

workflow_template_manager = AdvancedWorkflowTemplates()
# في ملف workflow_templates.py داخل فئة AdvancedWorkflowTemplates

# ----------------------------------------------------------------------
# 5. قالب كتابة أغنية راب مع تقمص وجداني وصوتي
# ----------------------------------------------------------------------
emotional_rap_composition = WorkflowTemplate(
    id="emotional_rap_v2",
    name="إنتاج أغنية راب (مع الروح الموسيقية)",
    description="سير عمل متقدم لإنتاج أغنية راب، مع تحليل صوتي وأدائي للفنان المستهدف.",
    category="music_composition",
    tasks=[
        WorkflowTask(
            id="task_1_soul_profile",
            name="تحليل الملف الروحي (النصي)",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "soul_profiler_agent", "text_content": "{artist_lyrics_corpus}"}
        ),
        WorkflowTask(
            id="task_2_rhythmic_profile",
            name="تحليل البصمة الإيقاعية (الصوتي)",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "rhythm_flow_analyzer", "audio_source": "{artist_audio_sample.mp3}"}
        ),
        WorkflowTask(
            id="task_3_idea_generation",
            name="توليد فكرة الأغنية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "idea_generator", "context_prompt": "Generate a contemporary social theme suitable for the artist's profile."},
            dependencies=["task_1_soul_profile", "task_2_rhythmic_profile"]
        ),
        WorkflowTask(
            id="task_4_lyric_composition",
            name="كتابة المسودة الأولى للكلمات",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "poem_composer_agent", "prompt_id": "balti_embodiment_prompt"},
            dependencies=["task_3_idea_generation"]
        ),
        WorkflowTask(
            id="task_5_performance_direction",
            name="إضافة توجيهات الأداء الصوتي",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            # سيتم تمرير مخرجات المهمتين 2 و 4 تلقائيًا
            input_data={"agent_id": "vocal_performance_director"},
            dependencies=["task_2_rhythmic_profile", "task_4_lyric_composition"]
        ),
        WorkflowTask(
            id="task_6_final_critique",
            name="المراجعة الجمالية النهائية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "aesthetic_critic_agent", "critique_focus": "authenticity_and_impact"},
            dependencies=["task_5_performance_direction"]
        ),
    ]
)
# ... تسجيل القالب الجديد
self.templates[emotional_rap_composition.id] = emotional_rap_composition
