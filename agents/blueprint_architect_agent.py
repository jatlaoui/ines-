"""
وكيل بناء المخططات - متخصص في تصميم وبناء الهيكل الشامل للروايات
يقوم بتطوير المخططات التفصيلية والهيكل السردي للأعمال الأدبية
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from .base_agent import BaseAgent, AgentState, MessageType
from ..llm_service import call_llm, create_blueprint_prompt, get_best_model_for_task
from ..tools.text_processing_tools import TextProcessor
from ..tools.analysis_tools import StructureAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class NovelStructure:
    """هيكل الرواية"""
    acts: List[Dict[str, Any]]
    chapters: List[Dict[str, Any]]
    scenes: List[Dict[str, Any]]
    pacing: Dict[str, Any]
    word_count_targets: Dict[str, int]

@dataclass
class CharacterArc:
    """قوس تطور الشخصية"""
    character_name: str
    starting_point: str
    development_stages: List[str]
    climax_moment: str
    resolution: str
    motivation: str
    obstacles: List[str]

class BlueprintArchitectAgent(BaseAgent):
    """وكيل بناء المخططات والهياكل الأدبية"""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            name="مهندس المخططات الأدبية",
            persona="""أنا مهندس معماري للنصوص الأدبية، متخصص في تصميم وبناء الهياكل السردية المعقدة.
            أفهم بعمق كيفية بناء الروايات من الأساس، وأتقن تصميم الأقواس السردية المتداخلة.
            أركز على التوازن بين عناصر القصة المختلفة وضمان التماسك الهيكلي للعمل الأدبي.
            أستطيع تحويل الأفكار المتناثرة إلى مخطط شامل ومتماسك.""",
            goals=[
                "تصميم هياكل سردية محكمة ومتماسكة",
                "بناء مخططات تفصيلية للروايات",
                "تطوير أقواس الشخصيات والأحداث",
                "ضمان التوازن في إيقاع السرد",
                "تنظيم العناصر الأدبية بشكل متناغم"
            ],
            tools=[
                "structure_design",
                "blueprint_creation",
                "pacing_analysis",
                "arc_development",
                "scene_planning",
                "tension_mapping",
                "narrative_architecture"
            ],
            agent_id=agent_id
        )
        
        # أدوات متخصصة
        self.text_processor = TextProcessor()
        self.structure_analyzer = StructureAnalyzer()
        
        # قوالب الهياكل السردية
        self.structure_templates = {
            "three_act": {
                "name": "الهيكل ثلاثي الفصول",
                "acts": ["التأسيس", "المواجهة", "الحل"],
                "proportions": [0.25, 0.5, 0.25],
                "key_points": ["نقطة البداية", "نقطة التحول الأولى", "نقطة الوسط", "نقطة التحول الثانية", "الذروة", "النهاية"]
            },
            "hero_journey": {
                "name": "رحلة البطل",
                "stages": ["العالم العادي", "النداء للمغامرة", "رفض النداء", "مقابلة المرشد", "عبور العتبة", 
                          "الاختبارات والحلفاء", "الاقتراب من المغارة", "المحنة", "المكافأة", "طريق العودة", 
                          "القيامة", "العودة بالإكسير"],
                "arc_type": "transformation"
            },
            "five_act": {
                "name": "الهيكل خماسي الفصول",
                "acts": ["المقدمة", "الصعود", "الذروة", "الهبوط", "الكارثة/الحل"],
                "proportions": [0.15, 0.25, 0.2, 0.25, 0.15]
            },
            "episodic": {
                "name": "الهيكل المتسلسل",
                "structure": "مجموعة من الحلقات المترابطة",
                "connection_types": ["sequential", "thematic", "character_based"]
            }
        }
        
        # أنواع الصراعات
        self.conflict_types = {
            "internal": "صراع داخلي مع الذات",
            "interpersonal": "صراع بين شخصيتين",
            "social": "صراع مع المجتمع",
            "environmental": "صراع مع البيئة/الطبيعة",
            "supernatural": "صراع مع قوى خارقة",
            "technological": "صراع مع التكنولوجيا",
            "temporal": "صراع عبر الزمن"
        }
        
        # نماذج التوتر والإيقاع
        self.tension_patterns = {
            "escalating": "تصاعد مستمر للتوتر",
            "wave": "موجات من التوتر والاسترخاء",
            "plateau": "مستوى ثابت من التوتر",
            "explosive": "انفجارات مفاجئة للتوتر",
            "gradual": "تراكم تدريجي للتوتر"
        }
        
        logger.info("تم إنشاء وكيل بناء المخططات بنجاح")
    
    def get_capabilities(self) -> List[str]:
        """إرجاع قدرات الوكيل"""
        return [
            "novel_structure_design",
            "blueprint_creation",
            "chapter_planning",
            "scene_architecture",
            "character_arc_development",
            "pacing_design",
            "tension_mapping",
            "plot_orchestration",
            "narrative_flow_design",
            "structural_analysis"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة مهمة بناء المخطط"""
        try:
            self.update_state(AgentState.WORKING)
            start_time = datetime.now()
            
            task_type = task.get("type", "complete_blueprint")
            source_material = task.get("source", {})
            blueprint_options = task.get("options", {})
            
            # حفظ السياق
            self.memory.add_to_context({
                "task_type": task_type,
                "source_material": source_material,
                "blueprint_options": blueprint_options
            })
            
            result = {}
            
            if task_type == "complete_blueprint":
                result = await self._create_complete_blueprint(source_material, blueprint_options)
            elif task_type == "structure_design":
                result = await self._design_structure(source_material, blueprint_options)
            elif task_type == "chapter_outline":
                result = await self._create_chapter_outline(source_material, blueprint_options)
            elif task_type == "character_arcs":
                result = await self._develop_character_arcs(source_material, blueprint_options)
            elif task_type == "pacing_plan":
                result = await self._design_pacing_plan(source_material, blueprint_options)
            elif task_type == "scene_breakdown":
                result = await self._create_scene_breakdown(source_material, blueprint_options)
            elif task_type == "tension_mapping":
                result = await self._map_tension_flow(source_material, blueprint_options)
            elif task_type == "structure_analysis":
                result = await self._analyze_existing_structure(source_material, blueprint_options)
            else:
                raise ValueError(f"نوع المهمة غير مدعوم: {task_type}")
            
            # حساب الوقت المستغرق
            processing_time = (datetime.now() - start_time).total_seconds()
            result["processing_time"] = processing_time
            result["blueprint_timestamp"] = datetime.now().isoformat()
            result["architect_version"] = "1.0"
            
            # تقييم جودة المخطط
            quality_assessment = await self._assess_blueprint_quality(result)
            result["quality_assessment"] = quality_assessment
            
            # تحديث المقاييس
            self.learn_from_interaction({
                "task_type": task_type,
                "response_time": processing_time,
                "quality_score": quality_assessment.get("overall_score", 0),
                "success": True
            })
            
            self.update_state(AgentState.COMPLETED)
            logger.info(f"تم إكمال بناء المخطط في {processing_time:.2f} ثانية")
            
            return result
            
        except Exception as e:
            self.update_state(AgentState.ERROR)
            logger.error(f"خطأ في بناء المخطط: {str(e)}")
            return {
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _create_complete_blueprint(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء مخطط شامل للرواية"""
        logger.info("بدء إنشاء المخطط الشامل")
        
        # استخراج العناصر الأساسية
        story_idea = source.get("story_idea", "")
        characters = source.get("characters", [])
        themes = source.get("themes", [])
        setting = source.get("setting", "")
        genre = source.get("genre", "عام")
        target_length = options.get("target_length", 80000)  # كلمة
        
        # اختيار الهيكل المناسب
        structure_type = await self._select_optimal_structure(source, options)
        
        # تطوير الهيكل التفصيلي
        detailed_structure = await self._develop_detailed_structure(
            structure_type, source, target_length
        )
        
        # تطوير أقواس الشخصيات
        character_arcs = await self._develop_all_character_arcs(characters, detailed_structure)
        
        # تخطيط الفصول والمشاهد
        chapter_plan = await self._create_detailed_chapter_plan(detailed_structure, character_arcs)
        
        # تصميم خريطة التوتر
        tension_map = await self._create_comprehensive_tension_map(detailed_structure, chapter_plan)
        
        # تطوير خطة الإيقاع
        pacing_strategy = await self._develop_pacing_strategy(detailed_structure, tension_map)
        
        # إنشاء timeline للأحداث
        event_timeline = await self._create_event_timeline(chapter_plan)
        
        return {
            "status": "success",
            "blueprint_type": "complete",
            "structure": {
                "type": structure_type,
                "details": detailed_structure,
                "word_count_distribution": await self._calculate_word_distribution(detailed_structure, target_length)
            },
            "chapters": chapter_plan,
            "character_arcs": character_arcs,
            "tension_map": tension_map,
            "pacing_strategy": pacing_strategy,
            "event_timeline": event_timeline,
            "writing_guidelines": await self._generate_writing_guidelines(detailed_structure),
            "milestones": await self._define_writing_milestones(chapter_plan),
            "consistency_checklist": await self._create_consistency_checklist(source)
        }
    
    async def _design_structure(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """تصميم الهيكل السردي"""
        logger.info("بدء تصميم الهيكل السردي")
        
        structure_preference = options.get("structure_type", "auto")
        complexity_level = options.get("complexity", "medium")
        
        if structure_preference == "auto":
            structure_type = await self._select_optimal_structure(source, options)
        else:
            structure_type = structure_preference
        
        # بناء الهيكل المختار
        structure_details = await self._build_structure_details(structure_type, source, complexity_level)
        
        # تحليل نقاط القوة والضعف
        structure_analysis = await self._analyze_structure_strengths_weaknesses(structure_details)
        
        return {
            "status": "success",
            "structure_type": structure_type,
            "structure_details": structure_details,
            "analysis": structure_analysis,
            "alternative_structures": await self._suggest_alternative_structures(source),
            "implementation_notes": await self._generate_implementation_notes(structure_details)
        }
    
    async def _create_chapter_outline(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء مخطط الفصول"""
        logger.info("بدء إنشاء مخطط الفصول")
        
        chapter_count = options.get("chapter_count", 20)
        detail_level = options.get("detail_level", "medium")
        
        chapters = []
        story_progression = await self._calculate_story_progression(chapter_count)
        
        for i in range(chapter_count):
            chapter = await self._design_chapter(
                i + 1, 
                story_progression[i], 
                source, 
                detail_level
            )
            chapters.append(chapter)
        
        # تحليل التدفق بين الفصول
        flow_analysis = await self._analyze_chapter_flow(chapters)
        
        # إضافة hooks وconnections
        enhanced_chapters = await self._enhance_chapters_with_connections(chapters)
        
        return {
            "status": "success",
            "chapters": enhanced_chapters,
            "flow_analysis": flow_analysis,
            "chapter_statistics": await self._calculate_chapter_statistics(enhanced_chapters),
            "balance_assessment": await self._assess_chapter_balance(enhanced_chapters)
        }
    
    async def _develop_character_arcs(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """تطوير أقواس الشخصيات"""
        logger.info("بدء تطوير أقواس الشخصيات")
        
        characters = source.get("characters", [])
        story_structure = source.get("structure", {})
        arc_depth = options.get("arc_depth", "detailed")
        
        character_arcs = {}
        
        for character in characters:
            arc = await self._create_character_arc(character, story_structure, arc_depth)
            character_arcs[character.get("name", "Unknown")] = arc
        
        # تحليل التفاعلات بين الأقواس
        arc_interactions = await self._analyze_arc_interactions(character_arcs)
        
        # التحقق من التماسك
        consistency_check = await self._check_arc_consistency(character_arcs, story_structure)
        
        return {
            "status": "success",
            "character_arcs": character_arcs,
            "arc_interactions": arc_interactions,
            "consistency_check": consistency_check,
            "development_timeline": await self._create_character_development_timeline(character_arcs)
        }
    
    async def _design_pacing_plan(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """تصميم خطة الإيقاع"""
        logger.info("بدء تصميم خطة الإيقاع")
        
        pacing_style = options.get("pacing_style", "balanced")
        genre = source.get("genre", "عام")
        target_audience = source.get("target_audience", "عام")
        
        # تحليل متطلبات الإيقاع
        pacing_requirements = await self._analyze_pacing_requirements(genre, target_audience)
        
        # تصميم منحنى الإيقاع
        pacing_curve = await self._design_pacing_curve(pacing_style, pacing_requirements)
        
        # تحديد نقاط التسارع والإبطاء
        tempo_points = await self._identify_tempo_change_points(pacing_curve, source)
        
        return {
            "status": "success",
            "pacing_style": pacing_style,
            "pacing_curve": pacing_curve,
            "tempo_points": tempo_points,
            "pacing_guidelines": await self._generate_pacing_guidelines(pacing_curve),
            "rhythm_analysis": await self._analyze_narrative_rhythm(pacing_curve)
        }
    
    async def _create_scene_breakdown(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء تفصيل المشاهد"""
        logger.info("بدء إنشاء تفصيل المشاهد")
        
        chapters = source.get("chapters", [])
        scene_detail = options.get("scene_detail", "medium")
        
        scene_breakdown = {}
        
        for chapter in chapters:
            chapter_scenes = await self._break_down_chapter_into_scenes(chapter, scene_detail)
            scene_breakdown[f"chapter_{chapter.get('number', 'unknown')}"] = chapter_scenes
        
        # تحليل توزيع المشاهد
        scene_distribution = await self._analyze_scene_distribution(scene_breakdown)
        
        return {
            "status": "success",
            "scene_breakdown": scene_breakdown,
            "scene_distribution": scene_distribution,
            "scene_types": await self._categorize_scene_types(scene_breakdown),
            "transition_analysis": await self._analyze_scene_transitions(scene_breakdown)
        }
    
    async def _map_tension_flow(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """رسم خريطة تدفق التوتر"""
        logger.info("بدء رسم خريطة التوتر")
        
        structure = source.get("structure", {})
        chapters = source.get("chapters", [])
        tension_style = options.get("tension_style", "wave")
        
        # تحديد نقاط التوتر الرئيسية
        tension_points = await self._identify_major_tension_points(structure, chapters)
        
        # رسم منحنى التوتر
        tension_curve = await self._create_tension_curve(tension_points, tension_style)
        
        # تحليل ديناميكيات التوتر
        tension_dynamics = await self._analyze_tension_dynamics(tension_curve)
        
        return {
            "status": "success",
            "tension_curve": tension_curve,
            "tension_points": tension_points,
            "tension_dynamics": tension_dynamics,
            "optimization_suggestions": await self._suggest_tension_optimizations(tension_curve)
        }
    
    async def _analyze_existing_structure(self, source: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """تحليل هيكل موجود"""
        logger.info("بدء تحليل الهيكل الموجود")
        
        existing_text = source.get("text", "")
        analysis_depth = options.get("analysis_depth", "comprehensive")
        
        # تحليل الهيكل الحالي
        current_structure = await self.structure_analyzer.analyze_structure(existing_text)
        
        # تحديد نقاط القوة والضعف
        strengths_weaknesses = await self._evaluate_structure_quality(current_structure)
        
        # اقتراح تحسينات
        improvement_suggestions = await self._suggest_structural_improvements(current_structure)
        
        return {
            "status": "success",
            "current_structure": current_structure,
            "evaluation": strengths_weaknesses,
            "improvement_suggestions": improvement_suggestions,
            "restructuring_options": await self._propose_restructuring_options(current_structure)
        }
    
    # دوال مساعدة متخصصة
    
    async def _select_optimal_structure(self, source: Dict[str, Any], options: Dict[str, Any]) -> str:
        """اختيار الهيكل الأمثل"""
        genre = source.get("genre", "عام")
        story_type = source.get("story_type", "linear")
        complexity = options.get("complexity", "medium")
        
        # منطق اختيار الهيكل (مبسط)
        if genre in ["مغامرة", "فانتازيا"]:
            return "hero_journey"
        elif story_type == "episodic":
            return "episodic"
        elif complexity == "high":
            return "five_act"
        else:
            return "three_act"
    
    async def _develop_detailed_structure(self, structure_type: str, source: Dict[str, Any], target_length: int) -> Dict[str, Any]:
        """تطوير الهيكل التفصيلي"""
        template = self.structure_templates.get(structure_type, self.structure_templates["three_act"])
        
        detailed_structure = {
            "template": template,
            "word_count_target": target_length,
            "estimated_chapters": max(15, target_length // 4000),  # تقدير الفصول
            "key_plot_points": await self._define_key_plot_points(template, source),
            "act_breakdown": await self._create_act_breakdown(template, target_length)
        }
        
        return detailed_structure
    
    async def _develop_all_character_arcs(self, characters: List[Dict], structure: Dict[str, Any]) -> Dict[str, Any]:
        """تطوير جميع أقواس الشخصيات"""
        arcs = {}
        
        for character in characters:
            arc = CharacterArc(
                character_name=character.get("name", "Unknown"),
                starting_point=character.get("starting_state", "غير محدد"),
                development_stages=["البداية", "التطور", "الاختبار", "النمو", "التحول"],
                climax_moment="لحظة الحقيقة",
                resolution="الحالة النهائية",
                motivation=character.get("motivation", "غير محدد"),
                obstacles=character.get("obstacles", ["تحدي شخصي", "تحدي خارجي"])
            )
            arcs[character.get("name", "Unknown")] = arc
        
        return arcs
    
    async def _create_detailed_chapter_plan(self, structure: Dict[str, Any], character_arcs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """إنشاء خطة الفصول التفصيلية"""
        chapter_count = structure.get("estimated_chapters", 20)
        chapters = []
        
        for i in range(chapter_count):
            chapter = {
                "number": i + 1,
                "title": f"الفصل {i + 1}",
                "purpose": await self._determine_chapter_purpose(i, chapter_count, structure),
                "key_events": [f"حدث رئيسي {i + 1}"],
                "character_focus": await self._determine_chapter_character_focus(i, character_arcs),
                "estimated_word_count": structure.get("word_count_target", 80000) // chapter_count,
                "tension_level": await self._calculate_chapter_tension_level(i, chapter_count),
                "connections": {
                    "previous": f"ربط مع الفصل {i}" if i > 0 else None,
                    "next": f"تمهيد للفصل {i + 2}" if i < chapter_count - 1 else None
                }
            }
            chapters.append(chapter)
        
        return chapters
    
    async def _assess_blueprint_quality(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """تقييم جودة المخطط"""
        quality_metrics = {
            "structural_coherence": await self._assess_structural_coherence(blueprint),
            "character_development": await self._assess_character_development_quality(blueprint),
            "pacing_balance": await self._assess_pacing_balance(blueprint),
            "narrative_flow": await self._assess_narrative_flow(blueprint),
            "tension_management": await self._assess_tension_management(blueprint)
        }
        
        overall_score = sum(quality_metrics.values()) / len(quality_metrics)
        
        return {
            "overall_score": overall_score,
            "metrics": quality_metrics,
            "grade": "ممتاز" if overall_score > 8.5 else "جيد جداً" if overall_score > 7 else "جيد" if overall_score > 6 else "مقبول",
            "recommendations": await self._generate_quality_improvement_recommendations(quality_metrics)
        }
    
    # المزيد من الدوال المساعدة (مبسطة)
    
    async def _calculate_word_distribution(self, structure: Dict[str, Any], target_length: int) -> Dict[str, int]:
        """حساب توزيع الكلمات"""
        return {"act_1": int(target_length * 0.25), "act_2": int(target_length * 0.5), "act_3": int(target_length * 0.25)}
    
    async def _generate_writing_guidelines(self, structure: Dict[str, Any]) -> List[str]:
        """توليد إرشادات الكتابة"""
        return ["حافظ على التماسك السردي", "طور الشخصيات تدريجياً", "اعتن بالإيقاع"]
    
    async def _define_writing_milestones(self, chapters: List[Dict]) -> List[Dict[str, Any]]:
        """تحديد معالم الكتابة"""
        milestones = []
        for i, chapter in enumerate(chapters):
            if (i + 1) % 5 == 0:  # معلم كل 5 فصول
                milestones.append({
                    "chapter": i + 1,
                    "milestone": f"إنجاز {i + 1} فصول",
                    "review_points": ["مراجعة التماسك", "تقييم التطور"]
                })
        return milestones
    
    async def _create_consistency_checklist(self, source: Dict[str, Any]) -> List[str]:
        """إنشاء قائمة فحص التماسك"""
        return [
            "تماسك الشخصيات عبر الفصول",
            "استمرارية الزمان والمكان", 
            "تطور منطقي للأحداث",
            "ثبات الأسلوب السردي"
        ]
    
    # دوال تقييم الجودة (مبسطة)
    
    async def _assess_structural_coherence(self, blueprint: Dict[str, Any]) -> float:
        """تقييم التماسك الهيكلي"""
        return 8.5  # نتيجة مبسطة
    
    async def _assess_character_development_quality(self, blueprint: Dict[str, Any]) -> float:
        """تقييم جودة تطوير الشخصيات"""
        return 8.0
    
    async def _assess_pacing_balance(self, blueprint: Dict[str, Any]) -> float:
        """تقييم توازن الإيقاع"""
        return 7.5
    
    async def _assess_narrative_flow(self, blueprint: Dict[str, Any]) -> float:
        """تقييم تدفق السرد"""
        return 8.2
    
    async def _assess_tension_management(self, blueprint: Dict[str, Any]) -> float:
        """تقييم إدارة التوتر"""
        return 7.8
    
    def get_structure_templates(self) -> Dict[str, Any]:
        """الحصول على قوالب الهياكل المتاحة"""
        return self.structure_templates
    
    def add_custom_structure(self, name: str, structure: Dict[str, Any]):
        """إضافة هيكل مخصص"""
        self.structure_templates[name] = structure
        logger.info(f"تم إضافة هيكل مخصص: {name}")
    
    def get_blueprint_history(self) -> List[Dict[str, Any]]:
        """الحصول على تاريخ المخططات"""
        return self.memory.conversation_history
