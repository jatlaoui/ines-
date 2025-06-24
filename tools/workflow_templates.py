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
self.templates[e# في ملف workflow_templates.py داخل فئة AdvancedWorkflowTemplates

# ----------------------------------------------------------------------
# 6. قالب إنتاج أغنية راب ببروتوكول "الروح العامية"
# ----------------------------------------------------------------------
vernacular_soul_rap = WorkflowTemplate(
    id="vernacular_soul_rap_v5",
    name="إنتاج أغنية راب (بروتوكول الروح العامية)",
    description="سير عمل نهائي ينتج أغنية راب أصيلة عبر فصل التعبير الخام عن الهندسة الموسيقية.",
    category="music_composition",
    tasks=[
        # المرحلة 1: التحليل الشامل
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
            input_data={"agent_id": "rhythm_flow_analyzer_agent", "audio_source": "{artist_audio_sample.mp3}"}
        ),
        # المرحلة 2: بناء عالم الأغنية
        WorkflowTask(
            id="task_3_sensory_library",
            name="بناء المكتبة الحسية للأغنية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "sensory_engine", "concept": "حومة النسيان"},
            dependencies=["task_1_soul_profile"]
        ),
        # المرحلة 3: الكتابة الخام
        WorkflowTask(
            id="task_4_raw_composition",
            name="كتابة تيار الوعي الخام",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={
                "agent_id": "poem_composer_agent",
                "embodiment_prompt": "أنت شاب تونسي عمره 22 عاماً، تعيش في 'حومة النسيان'. والدتك هي كل ما تملك. صديقك المقرب 'علي' مات في البحر. أنت تشعر بالغضب من الظلم، وبالحزن على صديقك. اكتب أفكارك الآن."
            },
            dependencies=["task_1_soul_profile", "task_3_sensory_library"]
        ),
        # المرحلة 4: الهندسة الموسيقية
        WorkflowTask(
            id="task_5_flow_engineering",
            name="هندسة التدفق والقافية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "lyrical_flow_master_agent"},
            dependencies=["task_2_rhythmic_profile", "task_4_raw_composition"]
        ),
        # المرحلة 5: إضافة الأداء
        WorkflowTask(
            id="task_6_performance_direction",
            name="إضافة توجيهات الأداء الصوتي",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "vocal_performance_director_agent"},
            dependencies=["task_2_rhythmic_profile", "task_5_flow_engineering"]
        ),
        # المرحلة 6: النقد النهائي
        WorkflowTask(
            id="task_7_final_critique",
            name="المراجعة الجمالية والأدائية النهائية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "aesthetic_critic_agent"},
            dependencies=["task_6_performance_direction"]
        ),
    ]
)
# تسجيل القالب
self.templates[vernacular_soul_rap.id] = vernacular_soul_rapmotional_rap_composition.id] = emotional_rap_composition
# في ملف workflow_templates.py داخل فئة AdvancedWorkflowTemplates

# ----------------------------------------------------------------------
# 6. قالب بناء منهج تعليمي متكامل
# ----------------------------------------------------------------------
curriculum_build_v1 = WorkflowTemplate(
    id="curriculum_build_v1",
    name="بناء منهج تعليمي متكامل من PDF",
    description="يأخذ كتابًا مدرسيًا (PDF) ويحوله إلى محتوى تعليمي تفاعلي.",
    category="educational_content",
    tasks=[
        WorkflowTask(
            id="task_1_ingest",
            name="استيعاب وتحليل المنهج",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "ingestion_engine", "input_type": "PDF_FILE", "source": "{file_content_base64}"}
        ),
        WorkflowTask(
            id="task_2_design_map",
            name="تصميم خريطة المنهج",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "instructional_designer", "mode": "academic"},
            dependencies=["task_1_ingest"]
        ),
        WorkflowTask(
            id="task_3_critique_map",
            name="نقد وتدقيق خريطة المنهج",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "educational_content_critic"},
            dependencies=["task_2_design_map"]
        ),
        # هذه المهمة ستكون حلقة تكرارية في التنفيذ الفعلي
        WorkflowTask(
            id="task_4_generate_lesson_content",
            name="توليد محتوى الدروس (ملخصات وتمارين)",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            # سيتم استدعاء هذا الوكيل عدة مرات مع سياق مختلف لكل درس
            input_data={"agent_id": "chapter_composer", "mode": "academic", "exercise_generator_agent_id": "exercises_generator"},
            dependencies=["task_3_critique_map"]
        ),
        WorkflowTask(
            id="task_5_build_knowledge_graph",
            name="بناء الشبكة المعرفية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "advanced_context_engine"},
            dependencies=["task_4_generate_lesson_content"]
        ),
        WorkflowTask(
            id="task_6_design_learning_paths",
            name="تصميم مسارات المراجعة",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "learning_path_architect", "path_types": ["quick_review", "deep_dive"]},
            dependencies=["task_5_build_knowledge_graph"]
        ),
    ]
)

# ----------------------------------------------------------------------
# 7. قالب التوصية التكيفية
# ----------------------------------------------------------------------
adaptive_recommendation_v1 = WorkflowTemplate(
    id="adaptive_recommendation_v1",
    name="توليد توصية تعلم تكيفية",
    description="يحلل أداء الطالب ويقترح الخطوة التالية.",
    category="adaptive_learning",
    tasks=[
        WorkflowTask(
            id="task_1_adapt_path",
            name="تحليل الأداء وتكييف المسار",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "interactive_curriculum_designer"}
        )
    ]
)

# ... تسجيل القوالب الجديدة
self.templates[curriculum_build_v1.id] = curriculum_build_v1
self.templates[adaptive_recommendation_v1.id] = adaptive_recommendation_v1
# في tools/workflow_templates.py داخل فئة AdvancedWorkflowTemplates

# ----------------------------------------------------------------------
# 8. قالب الاندماج السردي الفائق
# ----------------------------------------------------------------------
hyper_narrative_fusion_v1 = WorkflowTemplate(
    id="hyper_narrative_fusion_v1",
    name="الاندماج السردي الفائق",
    description="يدمج بين عملين أو أكثر لإنتاج عمل هجين ومبتكر.",
    category="experimental_writing",
    tasks=[
        WorkflowTask(
            id="task_1_analyze",
            name="تحليل التوافق بين المصادر",
            task_type=TaskType.FUSION_ANALYZE_COMPATIBILITY,
            # سيتم تمرير المصادر في سياق التنفيذ الأولي
            input_data={"sources": "{initial_sources}"}
        ),
        WorkflowTask(
            id="task_2_create_blueprint",
            name="إنشاء مخطط الاندماج",
            task_type=TaskType.BUILD_BLUEPRINT,
            # سيتم استخدام مخرجات التحليل هنا
            input_data={"agent_id": "blueprint_architect", "mode": "fusion"},
            dependencies=["task_1_analyze"]
        ),
        WorkflowTask(
            id="task_3_synthesize",
            name="تخليق السرد الهجين",
            task_type=TaskType.FUSION_SYNTHESIZE_NARRATIVE,
            # سيتم استخدام مخرجات المهمتين السابقتين
            dependencies=["task_1_analyze", "task_2_create_blueprint"]
        ),
        WorkflowTask(
            id="task_4_arbitrate",
            name="التحكيم في جودة الاندماج",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "fusion_arbitrator_agent"},
            dependencies=["task_3_synthesize"]
        ),
    ]
)

# ... تسجيل القالب الجديد
self.templates[hyper_narrative_fusion_v1.id] = hyper_narrative_fusion_v1
# في ملف tools/workflow_templates.py

# ... (داخل تعريف قالب long_form_social_play_v1)
# بعد مهمة المراجعة النهائية
        WorkflowTask(
            id="task_13_final_review",
            name="المراجعة النقدية النهائية",
            # ...
        ),
        # --- [مهمة جديدة] ---
        WorkflowTask(
            id="task_14_generate_story_bible",
            name="إنشاء الكتاب المقدس للقصة",
            task_type=TaskType.CUSTOM_AGENT_TASK, # يمكن إنشاء نوع مهمة مخصص
            input_data={"agent_id": "lore_master", "format": "markdown"},
            dependencies=["task_13_final_review"] # تعتمد على اكتمال كل شيء
        )
# ...# في ملف tools/workflow_templates.py

# ... (في TaskType Enum)
class TaskType(Enum):
    # ... (كل الأنواع السابقة)
    NARRATIVE_FORECAST = "narrative_forecast"

# ... (في فئة AdvancedWorkflowTemplates)
# ----------------------------------------------------------------------
# 9. قالب استشارة المنبئ السردي
# ----------------------------------------------------------------------
narrative_forecasting_v1 = WorkflowTemplate(
    id="narrative_forecasting_v1",
    name="استشارة المنبئ السردي",
    description="يحلل القصة الحالية ويقدم تقريراً بالمسارات المستقبلية المحتملة.",
    category="strategic_planning",
    tasks=[
        WorkflowTask(
            id="task_1_forecast",
            name="توليد التنبؤات السردية",
            task_type=TaskType.NARRATIVE_FORECAST,
            # سيتم تمرير السياق (ملفات الشخصيات، الصراعات) من حالة المشروع الحالية
        ),
    ]
)
# ... تسجيل القالب الجديد
self.templates[narrative_forecasting_v1.id] = narrative_forecasting_v1
# في ملف tools/workflow_templates.py

# ----------------------------------------------------------------------
# 10. قالب المنتج الفني المستقل (يعالج المواضيع المجردة)
# ----------------------------------------------------------------------
autonomous_artistic_producer = WorkflowTemplate(
    id="autonomous_artistic_producer_v1",
    name="المنتج الفني المستقل",
    description="يحول موضوعًا مجردًا إلى عمل فني كامل (أغنية) مع تحليل وتقمص عميق.",
    category="advanced_creation",
    tasks=[
        # المرحلة 1: التحليل والبناء الحسي
        WorkflowTask(id="task_1_soul_profile", name="تحليل روح الفنان", ...),
        WorkflowTask(id="task_2_sectional_rhythm", name="التحليل الأدائي المقطعي", ...),
        WorkflowTask(
            id="task_3_build_scenario",
            name="بناء السيناريو الحسي",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "scenario_builder_agent", "topic": "{initial_topic}"},
            dependencies=["task_1_soul_profile"]
        ),
        # المرحلة 2: الإنتاج الإبداعي (لاحظ أن كل خطوة تعتمد على ما قبلها)
        WorkflowTask(
            id="task_4_raw_composition",
            name="كتابة تيار الوعي الخام",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "content_generator_agent", "mode": "poetry"},
            dependencies=["task_3_build_scenario"]
        ),
        WorkflowTask(
            id="task_5_flow_engineering",
            name="هندسة التدفق والقافية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "lyrical_flow_master_agent"},
            dependencies=["task_4_raw_composition"]
        ),
        WorkflowTask(
            id="task_6_performance_direction",
            name="إضافة توجيهات الأداء المقطعية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "vocal_performance_director_agent"},
            dependencies=["task_2_sectional_rhythm", "task_5_flow_engineering"]
        ),
        # المرحلة 3: النقد النهائي
        WorkflowTask(
            id="task_7_final_critique",
            name="المراجعة الجمالية والأدائية النهائية",
            # ...
        ),
    ]
)
# ... تسجيل القالب
# في ملف tools/workflow_templates.py

# ----------------------------------------------------------------------
# 11. قالب إنتاج حزمة المشروع الجاهز للتمويل
# ----------------------------------------------------------------------
generate_funding_package_v1 = WorkflowTemplate(
    id="generate_funding_package_v1",
    name="إنشاء حزمة المشروع الجاهز للتمويل",
    description="ينتج مجموعة كاملة من المستندات الاحترافية لتقديم المشروع للمنتجين والجهات الداعمة.",
    category="production",
    tasks=[
        # تفترض هذه المهمة أن السيناريو (raw_script) موجود بالفعل في سياق التنفيذ
        WorkflowTask(
            id="task_1_format_script",
            name="تنسيق السيناريو بالصيغة الاحترافية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "screenplay_formatter"}
        ),
        WorkflowTask(
            id="task_2_generate_prod_bible",
            name="إنشاء ملف المشروع الشامل",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "lore_master", "task_type": "generate_production_bible"}
        ),
        WorkflowTask(
            id="task_3_generate_cultural_cert",
            name="إنشاء شهادة الأصالة الثقافية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "lore_master", "task_type": "generate_cultural_certificate"}
        ),
        WorkflowTask(
            id="task_4_feasibility_report",
            name="إنشاء تقرير الجدوى الإنتاجية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "production_analyst"},
            dependencies=["task_1_format_script"] # يعتمد على السيناريو المنسق
        ),
        # المهمة النهائية هي تجميع كل هذه المخرجات في حزمة واحدة
        WorkflowTask(
            id="task_5_package_assembly",
            name="تجميع حزمة التمويل النهائية",
            task_type=TaskType.MERGE_DATA,
            input_data={"output_name": "Funding_Ready_Package"},
            dependencies=[
                "task_1_format_script",
                "task_2_generate_prod_bible",
                "task_3_generate_cultural_cert",
                "task_4_feasibility_report"
            ]
        ),
    ]
)
# ... تسجيل القالب الجديد
# في ملف tools/workflow_templates.py

# ----------------------------------------------------------------------
# تحديث قالب كتابة المسرحية ليشمل النقد والأسلوب
# ----------------------------------------------------------------------
interactive_playwriting_v2 = WorkflowTemplate(
    id="interactive_playwriting_v2",
    name="كتابة مشهد مسرحي (مع نقد وأسلوب فني)",
    description="سير عمل متقدم يكتب مسودة أولية، ثم ينقدها للكشف عن الكليشيهات، ثم يعيد صياغتها بأسلوب فني محدد.",
    category="playwriting",
    tasks=[
        # ... (نفس مهام الإعداد الأولية: بناء العالم، الملفات النفسية، إلخ)
        WorkflowTask(
            id="task_1_scene_setup", ...
        ),
        # الخطوة 1: كتابة المسودة الأولى
        WorkflowTask(
            id="task_2_draft_writing",
            name="كتابة المسودة الأولى للمشهد",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "playwright_agent"},
            dependencies=["task_1_scene_setup"]
        ),
        # [جديد] الخطوة 2: تحليل ونقد الكليشيهات
        WorkflowTask(
            id="task_3_trope_analysis",
            name="تحليل الكليشيهات الدرامية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "tunisian_media_tropes_analyzer"},
            dependencies=["task_2_draft_writing"]
        ),
        # [جديد] الخطوة 3: الصياغة الفنية النهائية
        WorkflowTask(
            id="task_4_artistic_refinement",
            name="إعادة الصياغة بأسلوب فني (الدوعاجي)",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "ali_douagi_dialogue_agent"},
            # تعتمد على المسودة الأولى واقتراحات كسر الكليشيه
            dependencies=["task_2_draft_writing", "task_3_trope_analysis"]
        ),
        # الخطوة 4: التفاعل مع المستخدم
        WorkflowTask(
            id="task_5_interactive_prompt",
            name="تقديم الخيارات للمستخدم",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "interactive_experience_architect"},
            dependencies=["task_4_artistic_refinement"]
        ),
    ]
)
# ... تسجيل القالب الجديد
self.templates[interactive_playwriting_v2.id] = interactive_playwriting_v2
# في ملف tools/workflow_templates.py

# ----------------------------------------------------------------------
# تحديث قالب كتابة المسرحية ليعكس "المراجعة المزدوجة"
# ----------------------------------------------------------------------
critical_playwriting_v2 = WorkflowTemplate(
    id="critical_playwriting_v2",
    name="كتابة مشهد مسرحي نقدي (مع مراجعة مزدوجة)",
    description="سير عمل يكتب مسودة بأسلوب فني، ثم يراجعها لضمان الأصالة اللهجية.",
    category="playwriting_advanced",
    tasks=[
        # --- الخطوة 1: الإعداد وبناء العالم (كما كانت) ---
        WorkflowTask(
            id="task_1_scene_setup",
            name="إعداد المشهد (شخصيات، صراع، مكان)",
            ...
        ),
        
        # --- الخطوة 2: الكتابة الأسلوبية (المسودة الأولى) ---
        WorkflowTask(
            id="task_2_artistic_draft",
            name="كتابة المسودة الأولى بأسلوب فني (الدوعاجي)",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "ali_douagi_dialogue_agent"},
            dependencies=["task_1_scene_setup"]
        ),

        # --- [جديد] الخطوة 3: التدقيق اللهجي الإلزامي ---
        WorkflowTask(
            id="task_3_dialect_review",
            name="مراجعة وتصحيح الأصالة اللهجية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={
                "agent_id": "dialect_authenticity_guardian",
                # سيتم تمرير النص من المهمة السابقة واللهجة من الإعداد
            },
            dependencies=["task_2_artistic_draft"]
        ),

        # --- [جديد] الخطوة 4: الدمج والصياغة النهائية ---
        WorkflowTask(
            id="task_4_final_drafting",
            name="دمج التصحيحات والصياغة النهائية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "final_draft_agent"}, # وكيل بسيط مهمته الدمج
            dependencies=["task_2_artistic_draft", "task_3_dialect_review"]
        ),
    ]
)
# ... تسجيل القالب الجديد
self.templates[critical_playwriting_v2.id] = critical_playwriting_v2
# ... (كل القوالب السابقة التي قمنا بإنشائها) ...

class AdvancedWorkflowTemplates:
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        # ... (استدعاء دوال إنشاء القوالب الأخرى) ...
        self._create_professional_playwriting_template()

    # ... (دوال إنشاء القوالب الأخرى) ...

    def _create_professional_playwriting_template(self):
        """
        [جديد] ينشئ قالب سير العمل الاحترافي لكتابة المسرحيات،
        بناءً على المنهجية الأكاديمية للكتابة الدرامية.
        """
        professional_playwriting_v1 = WorkflowTemplate(
            id="professional_playwriting_v1",
            name="إنشاء مسرحية احترافية (منهجية كاملة)",
            description="سير عمل متكامل يتبع الخطوات الأكاديمية لكتابة نص مسرحي، من الفكرة إلى المسودة الأولى.",
            category="playwriting_professional",
            tasks=[
                # --- المرحلة الأولى: التأسيس الفكري ---
                WorkflowTask(
                    id="task_1_generate_core_idea",
                    name="المرحلة 1: صياغة الفكرة الأساسية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={
                        "agent_id": "idea_generator",
                        "prompt_context": {
                            "request": "صغ فكرة مسرحية من سطر واحد حول موضوع '{initial_topic}'. يجب أن تكون الفكرة صراعًا دراميًا واضحًا.",
                            "examples": ["الطموح غير المشروع يؤدي للدمار.", "الغيرة المفرطة تدمر صاحبها."]
                        }
                    },
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    id="task_2_develop_synopsis",
                    name="المرحلة 1: تطوير الملخص العام",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={
                        "agent_id": "blueprint_architect", # يمكنه القيام بهذه المهمة
                        "prompt_context": {
                            "request": "طور هذه الفكرة '{core_idea}' إلى ملخص من فقرة واحدة يصف البنية الدرامية (بداية، وسط، نهاية)."
                        }
                    },
                    dependencies=["task_1_generate_core_idea"],
                    priority=TaskPriority.HIGH
                ),

                # --- المرحلة الثانية: خلق الشخصيات ---
                WorkflowTask(
                    id="task_3_design_characters",
                    name="المرحلة 2: تصميم الشخصيات الرئيسية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={
                        "agent_id": "psychological_profiler",
                        "prompt_context": {
                            "request": "بناءً على الملخص التالي، اقترح 3 شخصيات رئيسية. لكل شخصية، حدد أبعادها الثلاثة (المادي، الاجتماعي، النفسي) بالتفصيل.",
                            "synopsis": "{{task_2_develop_synopsis.output.content.synopsis}}"
                        }
                    },
                    dependencies=["task_2_develop_synopsis"],
                    priority=TaskPriority.HIGH
                ),

                # --- المرحلة الثالثة: بناء الحبكة الدرامية ---
                WorkflowTask(
                    id="task_4_design_dramatic_structure",
                    name="المرحلة 3: تصميم البناء الدرامي الكامل",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={
                        "agent_id": "dramaturg_agent",
                        "prompt_context": {
                            "request": "صمم هيكل الحبكة الكامل للمسرحية بناءً على الملخص والشخصيات، محددًا كل مرحلة: 1. البداية (المعلومات)، 2. نقطة انطلاق الحدث، 3. الوسط (الصراع، الأزمة، التعقيد، الذروة)، 4. الحل، 5. النهاية المقترحة (مفتوحة/مغلقة/دائرية)."
                        }
                    },
                    dependencies=["task_2_develop_synopsis", "task_3_design_characters"],
                    priority=TaskPriority.URGENT
                ),
                
                # --- المرحلة الرابعة: كتابة النص المسرحي ---
                # هذه المهمة ستكون حلقة تكرارية يديرها المنسق، لكل مشهد في المخطط
                WorkflowTask(
                    id="task_5_write_scenes",
                    name="المرحلة 4: كتابة مشاهد المسرحية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={
                        "agent_id": "playwright_agent",
                        "is_loop": True, # إشارة للمنسق بأن هذه مهمة تكرارية
                        "loop_over": "{{task_4_design_dramatic_structure.output.content.scenes}}"
                    },
                    dependencies=["task_4_design_dramatic_structure"]
                ),

                # --- المرحلة الخامسة: التدقيق والمراجعة ---
                 WorkflowTask(
                    id="task_6_dialect_and_critic_review",
                    name="المرحلة 5: المراجعة النقدية واللهجية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    input_data={
                        "agent_id": "dialect_authenticity_guardian", # يبدأ بالتدقيق اللهجي
                        "next_agent_id": "literary_critic" # ثم يمرر للنقد الأدبي
                    },
                    dependencies=["task_5_write_scenes"]
                ),

                # --- المرحلة السادسة: التجميع النهائي ---
                WorkflowTask(
                    id="task_7_final_assembly",
                    name="المرحلة 6: تجميع المسودة الأولى الكاملة",
                    task_type=TaskType.MERGE_DATA,
                    dependencies=["task_6_dialect_and_critic_review"]
                )
            ]
        )
        
        self.templates[professional_playwriting_v1.id] = professional_playwriting_v1

# ...
# يجب التأكد من أن المنسق يعرف كيفية التعامل مع المهام التكرارية (`is_loop`)
# ويجب إنشاء ملف `workflow_templates_models.py` إذا لم يكن موجودًا

    

IGNORE_WHEN_COPYING_START
# في ملف tools/workflow_templates.py داخل فئة AdvancedWorkflowTemplates

# ----------------------------------------------------------------------
# 12. قالب المحاكاة العميقة لأسلوب رؤوف ماهر
# ----------------------------------------------------------------------
raouf_maher_deep_emulation_v1 = WorkflowTemplate(
    id="raouf_maher_deep_emulation_v1",
    name="إنتاج أغنية بأسلوب رؤوف ماهر (محاكاة عميقة)",
    description="سير عمل متكامل يحلل الأسلوب الموسيقي والأدائي، ثم ينتج كلمات ذات بنية وأداء مقطعي.",
    category="deep_artistic_emulation",
    tasks=[
        # --- المرحلة 1: التحليل الشامل (الأذن) ---
        WorkflowTask(
            id="task_1_soul_profile",
            name="تحليل الملف الروحي للنصوص",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "soul_profiler_agent", "text_content": "{artist_lyrics_corpus}"}
        ),
        WorkflowTask(
            id="task_2_sectional_rhythm_profile",
            name="تحليل البصمة الأدائية والموسيقية المقطعية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "rhythm_flow_analyzer_agent", "audio_source": "{artist_audio_sample}"}
        ),
        
        # --- المرحلة 2: بناء السيناريو والوعي الخام (القلب) ---
        WorkflowTask(
            id="task_3_build_scenario",
            name="بناء السيناريو الحسي للموضوع",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "scenario_builder_agent", "topic": "{song_topic}"},
            dependencies=["task_1_soul_profile"]
        ),
        WorkflowTask(
            id="task_4_raw_composition",
            name="كتابة تيار الوعي الخام (التقمص)",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "poem_composer_agent"}, # سيأخذ المخرجات من المهام السابقة
            dependencies=["task_1_soul_profile", "task_3_build_scenario"]
        ),
        
        # --- المرحلة 3: الهندسة والأداء (الصوت) ---
        WorkflowTask(
            id="task_5_flow_engineering",
            name="هندسة بنية الأغنية (مقاطع ولازمة)",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "lyrical_flow_master_agent"},
            dependencies=["task_2_sectional_rhythm_profile", "task_4_raw_composition"]
        ),
        WorkflowTask(
            id="task_6_performance_direction",
            name="إضافة توجيهات الأداء المقطعية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "vocal_performance_director_agent"},
            dependencies=["task_2_sectional_rhythm_profile", "task_5_flow_engineering"]
        ),
        
        # --- المرحلة 4: النقد النهائي (العقل) ---
        WorkflowTask(
            id="task_7_final_critique",
            name="المراجعة الجمالية النهائية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "aesthetic_critic_agent"},
            dependencies=["task_6_performance_direction"]
        )
    ]
)
# تسجيل القالب الجديد في __init__
# self.templates[raouf_maher_deep_emulation_v1.id] = raouf_maher_deep_emulation_v1
# في ملف tools/workflow_templates.py داخل فئة AdvancedWorkflowTemplates

# ----------------------------------------------------------------------
# 13. قالب المحاكاة العميقة ببروتوكول الروح الشعرية
# ----------------------------------------------------------------------
deep_soul_protocol_v1 = WorkflowTemplate(
    id="deep_soul_protocol_v1",
    name="إنتاج أغنية ببروتوكول الروح الشعرية العميقة",
    description="سير عمل استراتيجي يبدأ من الرمز، ثم التقمص، ثم الهندسة، وأخيرًا الصقل اللهجي.",
    category="deep_artistic_emulation",
    tasks=[
        # --- المرحلة 1: التحليل والتأسيس الرمزي ---
        WorkflowTask(
            id="task_1_soul_profile",
            name="تحليل الملف الروحي للنصوص",
            # ... (كما هي)
        ),
        WorkflowTask(
            id="task_2_sectional_rhythm_profile",
            name="تحليل البصمة الأدائية المقطعية",
            # ... (كما هي)
        ),
        WorkflowTask(
            id="task_3_generate_metaphor",
            name="توليد الصورة الشعرية المركزية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "dream_symbol_interpreter_agent", "topic": "{song_topic}"},
            dependencies=["task_1_soul_profile"]
        ),
        
        # --- المرحلة 2: الكتابة الخام من الرمز ---
        WorkflowTask(
            id="task_4_raw_composition",
            name="كتابة تيار الوعي الخام من الرمز",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "poem_composer_agent"}, # سيأخذ المخرجات من المهام السابقة
            dependencies=["task_1_soul_profile", "task_3_generate_metaphor"]
        ),
        
        # --- المرحلة 3: الهندسة والصقل ---
        WorkflowTask(
            id="task_5_flow_engineering",
            name="هندسة بنية الأغنية حول الرمز",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "lyrical_flow_master_agent"},
            dependencies=["task_2_sectional_rhythm_profile", "task_4_raw_composition", "task_3_generate_metaphor"]
        ),
        WorkflowTask(
            id="task_6_dialect_review", # [مهمة جديدة]
            name="مراجعة وصقل الأصالة اللهجية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "dialect_authenticity_guardian_agent"},
            dependencies=["task_5_flow_engineering"]
        ),

        # --- المرحلة 4: الأداء والنقد النهائي ---
        WorkflowTask(
            id="task_7_performance_direction",
            name="إضافة توجيهات الأداء المقطعية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "vocal_performance_director_agent"},
            dependencies=["task_2_sectional_rhythm_profile", "task_6_dialect_review"] # يعتمد على النص المصقول
        ),
        WorkflowTask(
            id="task_8_final_critique",
            name="المراجعة الجمالية النهائية",
            # ... (كما هي، لكنها تعتمد على المخرج النهائي)
            dependencies=["task_7_performance_direction"]
        )
    ]
)
# تسجيل القالب الجديد في __init__
# self.templates[deep_soul_protocol_v1.id] = deep_soul_protocol_v1
# في ملف workflow_templates.py داخل قالب deep_soul_protocol_v1

# ...
    tasks=[
        # --- [مهمة جديدة/اختيارية] ---
        WorkflowTask(
            id="task_0_oral_analysis",
            name="تحليل البصمة الشفوية للمصادر الصوتية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={"agent_id": "oral_heritage_agent", "audio_source": "{artist_oral_sample.mp3}"},
            # هذه المهمة لا تعتمد على شيء وتعمل بالتوازي
        ),
        # --- بقية المهام ---
        WorkflowTask(
            id="task_1_soul_profile",
            # ...
        ),
        # ...
        WorkflowTask(
            id="task_6_dialect_review",
            name="مراجعة وصقل الأصالة اللهجية",
            task_type=TaskType.CUSTOM_AGENT_TASK,
            input_data={
                "agent_id": "dialect_authenticity_guardian_agent",
                # [جديد] يمكننا الآن تمرير البصمة الشفوية كمرجع
                "oral_fingerprint": "{{task_0_oral_analysis.output.content.oral_fingerprint}}"
            },
            dependencies=["task_5_flow_engineering"]
        ),
        # ...
    ]
# ...
