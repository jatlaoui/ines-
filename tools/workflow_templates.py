"""
قوالب سير العمل للنظام الذكي للكتابة العربية
يحتوي على مجموعة شاملة من قوالب سير العمل المحددة مسبقاً
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from unified_orchestrator import WorkflowTemplate, WorkflowTask, TaskType, TaskPriority

class WorkflowTemplateManager:
    """مدير قوالب سير العمل"""
    
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        self._create_builtin_templates()
    
    def _create_builtin_templates(self):
        """إنشاء قوالب سير العمل المدمجة"""
        
        # === قوالب الكتابة الشاملة ===
        
        # قالب كتابة رواية كاملة محسن
        complete_novel_template = WorkflowTemplate(
            template_id="complete_novel_enhanced",
            name="كتابة رواية كاملة - محسن",
            description="سير عمل شامل ومحسن لكتابة رواية احترافية من البداية إلى النهاية",
            category="novel_writing",
            tasks=[
                WorkflowTask(
                    task_id="deep_analysis",
                    name="تحليل عميق للمصدر",
                    task_type=TaskType.ANALYZE_NOVEL,
                    config={
                        "analysis_depth": "comprehensive",
                        "include_style_analysis": True,
                        "include_character_analysis": True,
                        "include_plot_structure": True
                    },
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="creative_ideation",
                    name="توليد أفكار إبداعية متنوعة",
                    task_type=TaskType.GENERATE_IDEAS,
                    config={
                        "idea_count": 8,
                        "creativity_level": "high",
                        "genre_diversity": True,
                        "cultural_adaptation": True
                    },
                    dependencies=["deep_analysis"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="idea_evaluation",
                    name="تقييم وفلترة الأفكار",
                    task_type=TaskType.CONDITION,
                    config={
                        "condition": "len(ideas) >= 3",
                        "filter_criteria": ["originality", "feasibility", "cultural_relevance"]
                    },
                    dependencies=["creative_ideation"]
                ),
                WorkflowTask(
                    task_id="detailed_blueprint",
                    name="بناء مخطط تفصيلي",
                    task_type=TaskType.BUILD_BLUEPRINT,
                    config={
                        "detail_level": "comprehensive",
                        "include_character_arcs": True,
                        "include_subplot_mapping": True,
                        "include_pacing_guide": True,
                        "include_cultural_elements": True
                    },
                    dependencies=["idea_evaluation"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="character_development",
                    name="تطوير الشخصيات بالتفصيل",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    config={
                        "agent_id": "character_developer",
                        "depth_level": "comprehensive",
                        "psychological_profiles": True
                    },
                    dependencies=["detailed_blueprint"]
                ),
                WorkflowTask(
                    task_id="chapter_generation_batch1",
                    name="توليد الفصول (الدفعة الأولى)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    config={
                        "chapter_range": "1-5",
                        "quality_focus": "high",
                        "style_consistency": True
                    },
                    dependencies=["character_development"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="mid_consistency_check",
                    name="فحص الاتساق المتوسط",
                    task_type=TaskType.CHECK_CONSISTENCY,
                    config={
                        "check_scope": "chapters_1_5",
                        "check_character_consistency": True,
                        "check_plot_consistency": True
                    },
                    dependencies=["chapter_generation_batch1"]
                ),
                WorkflowTask(
                    task_id="chapter_generation_batch2",
                    name="توليد الفصول (الدفعة الثانية)",
                    task_type=TaskType.GENERATE_CHAPTER,
                    config={
                        "chapter_range": "6-10",
                        "build_on_previous": True,
                        "maintain_tension": True
                    },
                    dependencies=["mid_consistency_check"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="final_consistency_check",
                    name="فحص الاتساق النهائي",
                    task_type=TaskType.CHECK_CONSISTENCY,
                    config={
                        "check_scope": "all_chapters",
                        "comprehensive_review": True,
                        "style_uniformity": True
                    },
                    dependencies=["chapter_generation_batch2"]
                ),
                WorkflowTask(
                    task_id="text_refinement",
                    name="تنقيح وتحسين النص",
                    task_type=TaskType.REFINE_TEXT,
                    config={
                        "refinement_type": "comprehensive",
                        "focus_areas": ["language", "flow", "style", "cultural_accuracy"],
                        "quality_level": "professional"
                    },
                    dependencies=["final_consistency_check"],
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="comprehensive_report",
                    name="توليد تقرير شامل",
                    task_type=TaskType.GENERATE_REPORT,
                    config={
                        "report_type": "comprehensive",
                        "include_analytics": True,
                        "include_suggestions": True,
                        "include_metrics": True
                    },
                    dependencies=["text_refinement"],
                    priority=TaskPriority.NORMAL
                ),
                WorkflowTask(
                    task_id="save_final_project",
                    name="حفظ المشروع النهائي",
                    task_type=TaskType.SAVE_TO_PROJECT,
                    config={
                        "data_type": "final_novel",
                        "stage": 6,
                        "include_metadata": True
                    },
                    dependencies=["comprehensive_report"]
                )
            ],
            estimated_duration_minutes=75,
            is_public=True,
            created_by="system",
            version="2.0.0",
            tags=["novel", "comprehensive", "professional", "arabic"]
        )
        
        # === قوالب التطوير السريع ===
        
        # قالب تطوير فكرة سريع محسن
        quick_idea_enhanced_template = WorkflowTemplate(
            template_id="quick_idea_enhanced",
            name="تطوير فكرة سريع - محسن",
            description="سير عمل محسن لتطوير الأفكار بسرعة مع ضمان الجودة",
            category="ideation",
            tasks=[
                WorkflowTask(
                    task_id="rapid_analysis",
                    name="تحليل سريع",
                    task_type=TaskType.ANALYZE_NOVEL,
                    config={
                        "analysis_depth": "moderate",
                        "speed_mode": True,
                        "focus_areas": ["theme", "style", "potential"]
                    },
                    priority=TaskPriority.HIGH,
                    timeout_seconds=120
                ),
                WorkflowTask(
                    task_id="brainstorm_ideas",
                    name="عصف ذهني للأفكار",
                    task_type=TaskType.GENERATE_IDEAS,
                    config={
                        "idea_count": 5,
                        "speed_mode": True,
                        "creativity_boost": True,
                        "diverse_perspectives": True
                    },
                    dependencies=["rapid_analysis"],
                    priority=TaskPriority.HIGH,
                    timeout_seconds=180
                ),
                WorkflowTask(
                    task_id="quick_evaluation",
                    name="تقييم سريع للأفكار",
                    task_type=TaskType.CONDITION,
                    config={
                        "condition": "len(ideas) >= 2",
                        "quick_filter": True
                    },
                    dependencies=["brainstorm_ideas"]
                ),
                WorkflowTask(
                    task_id="basic_outline",
                    name="مخطط أساسي",
                    task_type=TaskType.BUILD_BLUEPRINT,
                    config={
                        "detail_level": "basic",
                        "speed_mode": True,
                        "essential_elements_only": True
                    },
                    dependencies=["quick_evaluation"],
                    priority=TaskPriority.HIGH,
                    timeout_seconds=240
                ),
                WorkflowTask(
                    task_id="save_quick_idea",
                    name="حفظ الفكرة السريعة",
                    task_type=TaskType.SAVE_TO_PROJECT,
                    config={
                        "data_type": "quick_idea",
                        "stage": 2
                    },
                    dependencies=["basic_outline"]
                )
            ],
            estimated_duration_minutes=12,
            is_public=True,
            created_by="system",
            version="2.0.0",
            tags=["quick", "ideation", "brainstorm"]
        )
        
        # === قوالب التحليل المتخصصة ===
        
        # قالب تحليل أسلوب الكتابة
        style_analysis_template = WorkflowTemplate(
            template_id="writing_style_analysis",
            name="تحليل أسلوب الكتابة",
            description="تحليل متخصص لأسلوب الكتابة والخصائص الأدبية",
            category="analysis",
            tasks=[
                WorkflowTask(
                    task_id="linguistic_analysis",
                    name="تحليل لغوي",
                    task_type=TaskType.ANALYZE_NOVEL,
                    config={
                        "analysis_type": "linguistic",
                        "focus_areas": ["vocabulary", "syntax", "style"],
                        "detailed_metrics": True
                    },
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="stylistic_patterns",
                    name="تحليل الأنماط الأسلوبية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    config={
                        "agent_id": "style_analyzer",
                        "pattern_recognition": True,
                        "comparative_analysis": True
                    },
                    dependencies=["linguistic_analysis"]
                ),
                WorkflowTask(
                    task_id="cultural_context_analysis",
                    name="تحليل السياق الثقافي",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    config={
                        "agent_id": "cultural_maestro",
                        "depth_level": "comprehensive",
                        "regional_variations": True
                    },
                    dependencies=["linguistic_analysis"]
                ),
                WorkflowTask(
                    task_id="merge_analysis_results",
                    name="دمج نتائج التحليل",
                    task_type=TaskType.MERGE_DATA,
                    config={
                        "merge_strategy": "comprehensive"
                    },
                    dependencies=["stylistic_patterns", "cultural_context_analysis"]
                ),
                WorkflowTask(
                    task_id="style_report",
                    name="تقرير تحليل الأسلوب",
                    task_type=TaskType.GENERATE_REPORT,
                    config={
                        "report_type": "style_analysis",
                        "include_recommendations": True,
                        "visualization_data": True
                    },
                    dependencies=["merge_analysis_results"]
                )
            ],
            estimated_duration_minutes=25,
            is_public=True,
            created_by="system",
            tags=["analysis", "style", "linguistic", "cultural"]
        )
        
        # === قوالب التحسين والتطوير ===
        
        # قالب تحسين النص المتقدم
        advanced_text_improvement_template = WorkflowTemplate(
            template_id="advanced_text_improvement",
            name="تحسين النص المتقدم",
            description="سير عمل متقدم لتحسين وتطوير النصوص الأدبية",
            category="improvement",
            tasks=[
                WorkflowTask(
                    task_id="initial_assessment",
                    name="تقييم أولي للنص",
                    task_type=TaskType.ANALYZE_NOVEL,
                    config={
                        "analysis_focus": "improvement_areas",
                        "identify_weaknesses": True,
                        "strength_analysis": True
                    }
                ),
                WorkflowTask(
                    task_id="language_enhancement",
                    name="تحسين اللغة",
                    task_type=TaskType.REFINE_TEXT,
                    config={
                        "refinement_type": "language",
                        "sophistication_level": "high",
                        "preserve_voice": True
                    },
                    dependencies=["initial_assessment"]
                ),
                WorkflowTask(
                    task_id="flow_optimization",
                    name="تحسين تدفق النص",
                    task_type=TaskType.REFINE_TEXT,
                    config={
                        "refinement_type": "flow",
                        "coherence_focus": True,
                        "transition_improvement": True
                    },
                    dependencies=["language_enhancement"]
                ),
                WorkflowTask(
                    task_id="style_consistency",
                    name="توحيد الأسلوب",
                    task_type=TaskType.CHECK_CONSISTENCY,
                    config={
                        "consistency_type": "style",
                        "tone_uniformity": True,
                        "voice_consistency": True
                    },
                    dependencies=["flow_optimization"]
                ),
                WorkflowTask(
                    task_id="cultural_appropriateness",
                    name="مراجعة الملاءمة الثقافية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    config={
                        "agent_id": "cultural_maestro",
                        "appropriateness_check": True,
                        "sensitivity_review": True
                    },
                    dependencies=["style_consistency"]
                ),
                WorkflowTask(
                    task_id="final_polish",
                    name="التلميع النهائي",
                    task_type=TaskType.REFINE_TEXT,
                    config={
                        "refinement_type": "comprehensive",
                        "final_quality_pass": True,
                        "professional_standard": True
                    },
                    dependencies=["cultural_appropriateness"]
                ),
                WorkflowTask(
                    task_id="improvement_report",
                    name="تقرير التحسينات",
                    task_type=TaskType.GENERATE_REPORT,
                    config={
                        "report_type": "improvement_summary",
                        "before_after_comparison": True,
                        "improvement_metrics": True
                    },
                    dependencies=["final_polish"]
                )
            ],
            estimated_duration_minutes=35,
            is_public=True,
            created_by="system",
            tags=["improvement", "refinement", "quality", "professional"]
        )
        
        # === قوالب التعاون والمراجعة ===
        
        # قالب المراجعة التعاونية
        collaborative_review_template = WorkflowTemplate(
            template_id="collaborative_review",
            name="المراجعة التعاونية",
            description="سير عمل للمراجعة التعاونية بين عدة وكلاء",
            category="review",
            tasks=[
                WorkflowTask(
                    task_id="literary_critic_review",
                    name="مراجعة الناقد الأدبي",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    config={
                        "agent_id": "literary_critic",
                        "review_depth": "comprehensive",
                        "critical_analysis": True
                    }
                ),
                WorkflowTask(
                    task_id="cultural_review",
                    name="المراجعة الثقافية",
                    task_type=TaskType.CUSTOM_AGENT_TASK,
                    config={
                        "agent_id": "cultural_maestro",
                        "cultural_authenticity": True,
                        "sensitivity_check": True
                    }
                ),
                WorkflowTask(
                    task_id="technical_review",
                    name="المراجعة التقنية",
                    task_type=TaskType.CHECK_CONSISTENCY,
                    config={
                        "technical_aspects": True,
                        "grammar_check": True,
                        "structure_analysis": True
                    }
                ),
                WorkflowTask(
                    task_id="consolidate_reviews",
                    name="دمج المراجعات",
                    task_type=TaskType.MERGE_DATA,
                    config={
                        "merge_strategy": "weighted_consensus",
                        "conflict_resolution": "expert_priority"
                    },
                    dependencies=["literary_critic_review", "cultural_review", "technical_review"]
                ),
                WorkflowTask(
                    task_id="collaborative_report",
                    name="تقرير المراجعة التعاونية",
                    task_type=TaskType.GENERATE_REPORT,
                    config={
                        "report_type": "collaborative_review",
                        "multi_perspective": True,
                        "actionable_recommendations": True
                    },
                    dependencies=["consolidate_reviews"]
                )
            ],
            estimated_duration_minutes=30,
            is_public=True,
            created_by="system",
            tags=["collaborative", "review", "multi-agent", "comprehensive"]
        )
        
        # === قوالب مخصصة للأنواع الأدبية ===
        
        # قالب كتابة القصة القصيرة
        short_story_template = WorkflowTemplate(
            template_id="short_story_creation",
            name="إنشاء قصة قصيرة",
            description="سير عمل مخصص لكتابة القصص القصيرة عالية الجودة",
            category="short_story",
            tasks=[
                WorkflowTask(
                    task_id="concept_development",
                    name="تطوير المفهوم",
                    task_type=TaskType.GENERATE_IDEAS,
                    config={
                        "story_type": "short_story",
                        "focus_single_concept": True,
                        "impact_oriented": True
                    }
                ),
                WorkflowTask(
                    task_id="tight_structure",
                    name="بناء هيكل محكم",
                    task_type=TaskType.BUILD_BLUEPRINT,
                    config={
                        "structure_type": "short_story",
                        "economy_of_language": True,
                        "single_effect": True
                    },
                    dependencies=["concept_development"]
                ),
                WorkflowTask(
                    task_id="concise_writing",
                    name="الكتابة المقتضبة",
                    task_type=TaskType.GENERATE_CHAPTER,
                    config={
                        "writing_style": "concise",
                        "every_word_counts": True,
                        "emotional_impact": True
                    },
                    dependencies=["tight_structure"]
                ),
                WorkflowTask(
                    task_id="intensity_check",
                    name="فحص الكثافة",
                    task_type=TaskType.CHECK_CONSISTENCY,
                    config={
                        "check_type": "intensity",
                        "pacing_analysis": True,
                        "impact_assessment": True
                    },
                    dependencies=["concise_writing"]
                ),
                WorkflowTask(
                    task_id="polish_for_impact",
                    name="التلميع للتأثير",
                    task_type=TaskType.REFINE_TEXT,
                    config={
                        "refinement_focus": "impact",
                        "word_economy": True,
                        "emotional_resonance": True
                    },
                    dependencies=["intensity_check"]
                )
            ],
            estimated_duration_minutes=20,
            is_public=True,
            created_by="system",
            tags=["short_story", "concise", "impact", "economy"]
        )
        
        # حفظ جميع القوالب
        templates_to_register = [
            complete_novel_template,
            quick_idea_enhanced_template,
            style_analysis_template,
            advanced_text_improvement_template,
            collaborative_review_template,
            short_story_template
        ]
        
        # === قوالب الشاهد ===
        
        # قالب شامل للشاهد والكتابة التوثيقية
        witness_documentary_template = WorkflowTemplate(
            template_id="witness_documentary_writing",
            name="الكتابة التوثيقية بالشاهد",
            description="سير عمل متكامل لإنتاج محتوى توثيقي باستخدام شهادات الشهود",
            category="documentary_writing",
            tasks=[
                WorkflowTask(
                    task_id="source_preparation",
                    name="إعداد مصادر الشاهد",
                    task_type=TaskType.WITNESS_UPLOAD,
                    config={
                        "max_sources": 5,
                        "required_metadata": ["location", "date", "interviewer"],
                        "quality_check": True,
                        "language_detection": True
                    },
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="comprehensive_extraction",
                    name="استخلاص شامل للعناصر",
                    task_type=TaskType.WITNESS_EXTRACT,
                    config={
                        "analysis_depth": "deep",
                        "extract_events": True,
                        "extract_characters": True,
                        "extract_dialogues": True,
                        "credibility_assessment": True,
                        "literary_elements_analysis": True
                    },
                    priority=TaskPriority.HIGH,
                    depends_on=["source_preparation"]
                ),
                WorkflowTask(
                    task_id="credibility_analysis",
                    name="تحليل المصداقية والتقييم",
                    task_type=TaskType.WITNESS_ANALYZE,
                    config={
                        "credibility_factors": ["consistency", "detail_level", "emotional_authenticity"],
                        "cross_reference_check": True,
                        "bias_detection": True,
                        "reliability_scoring": True
                    },
                    priority=TaskPriority.NORMAL,
                    depends_on=["comprehensive_extraction"]
                ),
                WorkflowTask(
                    task_id="content_structuring",
                    name="هيكلة المحتوى التوثيقي",
                    task_type=TaskType.BLUEPRINT_CHAPTER,
                    config={
                        "structure_type": "documentary",
                        "chronological_order": True,
                        "thematic_grouping": True,
                        "witness_integration_points": True
                    },
                    priority=TaskPriority.NORMAL,
                    depends_on=["credibility_analysis"]
                ),
                WorkflowTask(
                    task_id="narrative_integration",
                    name="دمج الشهادات في السرد",
                    task_type=TaskType.WITNESS_INTEGRATE,
                    config={
                        "integration_style": "narrative_flow",
                        "preserve_authenticity": True,
                        "smooth_transitions": True,
                        "context_preservation": True
                    },
                    priority=TaskPriority.HIGH,
                    depends_on=["content_structuring"]
                ),
                WorkflowTask(
                    task_id="final_review",
                    name="مراجعة نهائية وتدقيق",
                    task_type=TaskType.REVIEW_CHAPTER,
                    config={
                        "check_authenticity": True,
                        "verify_sources": True,
                        "ethical_review": True,
                        "factual_accuracy": True
                    },
                    priority=TaskPriority.HIGH,
                    depends_on=["narrative_integration"]
                )
            ]
        )
        
        # قالب سريع للاستشهاد بالشاهد
        quick_witness_citation_template = WorkflowTemplate(
            template_id="quick_witness_citation",
            name="الاستشهاد السريع بالشاهد",
            description="سير عمل سريع لإدراج اقتباسات من شهادات الشهود في النص",
            category="citation",
            tasks=[
                WorkflowTask(
                    task_id="witness_search",
                    name="البحث في مصادر الشاهد",
                    task_type=TaskType.WITNESS_EXTRACT,
                    config={
                        "search_mode": "quick",
                        "target_elements": ["dialogue", "key_statements"],
                        "credibility_threshold": 0.6,
                        "max_results": 10
                    },
                    priority=TaskPriority.NORMAL
                ),
                WorkflowTask(
                    task_id="context_integration",
                    name="دمج في السياق",
                    task_type=TaskType.WITNESS_INTEGRATE,
                    config={
                        "integration_method": "contextual",
                        "maintain_flow": True,
                        "add_attribution": True,
                        "format_quotes": True
                    },
                    priority=TaskPriority.NORMAL,
                    depends_on=["witness_search"]
                )
            ]
        )
        
        # قالب تحليل متقدم للشاهد
        advanced_witness_analysis_template = WorkflowTemplate(
            template_id="advanced_witness_analysis",
            name="التحليل المتقدم للشاهد",
            description="تحليل عميق وشامل لشهادات الشهود مع استخلاص رؤى معمقة",
            category="analysis",
            tasks=[
                WorkflowTask(
                    task_id="multi_source_extraction",
                    name="استخلاص متعدد المصادر",
                    task_type=TaskType.WITNESS_EXTRACT,
                    config={
                        "analysis_depth": "comprehensive",
                        "cross_source_analysis": True,
                        "pattern_detection": True,
                        "contradiction_identification": True
                    },
                    priority=TaskPriority.HIGH
                ),
                WorkflowTask(
                    task_id="reliability_assessment",
                    name="تقييم الموثوقية الشامل",
                    task_type=TaskType.WITNESS_ANALYZE,
                    config={
                        "multiple_reliability_metrics": True,
                        "psychological_indicators": True,
                        "consistency_analysis": True,
                        "external_validation": True
                    },
                    priority=TaskPriority.HIGH,
                    depends_on=["multi_source_extraction"]
                ),
                WorkflowTask(
                    task_id="narrative_coherence",
                    name="تحليل التماسك السردي",
                    task_type=TaskType.WITNESS_EVALUATE,
                    config={
                        "coherence_metrics": ["timeline", "character_consistency", "event_logic"],
                        "gap_identification": True,
                        "reliability_weighting": True
                    },
                    priority=TaskPriority.NORMAL,
                    depends_on=["reliability_assessment"]
                ),
                WorkflowTask(
                    task_id="synthesis_report",
                    name="تقرير التحليل المتكامل",
                    task_type=TaskType.GENERATE_REPORT,
                    config={
                        "report_type": "witness_analysis",
                        "include_visualizations": True,
                        "credibility_summary": True,
                        "recommendations": True
                    },
                    priority=TaskPriority.NORMAL,
                    depends_on=["narrative_coherence"]
                )
            ]
        )
        
        # إضافة قوالب الشاهد للقائمة
        templates_to_register.extend([
            witness_documentary_template,
            quick_witness_citation_template,
            advanced_witness_analysis_template
        ])
        
        for template in templates_to_register:
            self.templates[template.template_id] = template
    
    def get_template(self, template_id: str) -> WorkflowTemplate:
        """الحصول على قالب سير العمل"""
        return self.templates.get(template_id)
    
    def list_templates_by_category(self, category: str = None) -> List[WorkflowTemplate]:
        """قائمة بالقوالب حسب الفئة"""
        if category:
            return [t for t in self.templates.values() if t.category == category]
        return list(self.templates.values())
    
    def get_categories(self) -> List[str]:
        """الحصول على قائمة بجميع الفئات"""
        return list(set(t.category for t in self.templates.values()))
    
    def search_templates(self, query: str) -> List[WorkflowTemplate]:
        """البحث في القوالب"""
        query = query.lower()
        results = []
        
        for template in self.templates.values():
            if (query in template.name.lower() or 
                query in template.description.lower() or
                any(query in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results
    
    def get_template_info(self, template_id: str) -> Dict[str, Any]:
        """الحصول على معلومات مفصلة عن القالب"""
        template = self.get_template(template_id)
        if not template:
            return None
        
        return {
            'template_id': template.template_id,
            'name': template.name,
            'description': template.description,
            'category': template.category,
            'estimated_duration_minutes': template.estimated_duration_minutes,
            'task_count': len(template.tasks),
            'tasks': [
                {
                    'task_id': task.task_id,
                    'name': task.name,
                    'task_type': task.task_type.value,
                    'dependencies': task.dependencies,
                    'priority': task.priority.value
                }
                for task in template.tasks
            ],
            'tags': template.tags,
            'version': template.version,
            'is_public': template.is_public,
            'created_by': template.created_by
        }

# مثيل مدير القوالب العامة
template_manager = WorkflowTemplateManager()

# وظائف مساعدة للتوافق
def get_workflow_template(template_id: str) -> WorkflowTemplate:
    """الحصول على قالب سير العمل"""
    return template_manager.get_template(template_id)

def list_workflow_templates(category: str = None) -> List[Dict[str, Any]]:
    """قائمة بقوالب سير العمل"""
    templates = template_manager.list_templates_by_category(category)
    return [template_manager.get_template_info(t.template_id) for t in templates]

def search_workflow_templates(query: str) -> List[Dict[str, Any]]:
    """البحث في قوالب سير العمل"""
    templates = template_manager.search_templates(query)
    return [template_manager.get_template_info(t.template_id) for t in templates]

def get_workflow_categories() -> List[str]:
    """الحصول على فئات قوالب سير العمل"""
    return template_manager.get_categories()
