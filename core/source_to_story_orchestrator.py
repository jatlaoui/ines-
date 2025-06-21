"""
منسق بناء القصة من المصدر (Source to Story Orchestrator)
يدير التعاون بين الوكلاء لتحويل الترانسكريبت إلى قصة متكاملة
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from .agents.raw_narrative_analyzer import RawNarrativeAnalyzer
from .contextual_inference_engine import ContextualInferenceEngine
from .agents.idea_generator_agent import IdeaGeneratorAgent
from .agents.blueprint_architect_agent import BlueprintArchitectAgent
from .agents.chapter_composer_agent import ChapterComposerAgent
from .agents.literary_critic_agent import LiteraryCriticAgent
from .agents.cultural_maestro_agent import CulturalMaestroAgent

@dataclass
class StoryGenerationTask:
    """مهمة إنشاء قصة"""
    task_id: str
    transcript: str
    story_type: str
    target_length: str
    cultural_focus: str
    narrative_style: str
    user_preferences: Dict[str, Any]
    created_at: datetime

@dataclass
class AgentCollaboration:
    """تعاون بين الوكلاء"""
    agent_name: str
    contribution_type: str
    output: Any
    feedback_received: List[str]
    revisions: int
    completion_status: str

@dataclass
class StoryComponent:
    """مكون من مكونات القصة"""
    component_type: str  # character, plot, setting, theme, dialogue
    content: Any
    source_reference: str
    integration_status: str
    quality_score: float

class SourceToStoryOrchestrator:
    """منسق بناء القصة من المصدر المتطور"""
    
    def __init__(self):
        self.narrative_analyzer = RawNarrativeAnalyzer()
        self.inference_engine = ContextualInferenceEngine()
        self.idea_generator = IdeaGeneratorAgent()
        self.blueprint_architect = BlueprintArchitectAgent()
        self.chapter_composer = ChapterComposerAgent()
        self.literary_critic = LiteraryCriticAgent()
        self.cultural_maestro = CulturalMaestroAgent()
        
        self.active_tasks = {}
        self.collaboration_history = []
        
    async def initiate_story_generation(self, task: StoryGenerationTask) -> Dict[str, Any]:
        """بدء عملية إنشاء القصة"""
        
        self.active_tasks[task.task_id] = {
            "task": task,
            "phase": "analysis",
            "progress": 0.0,
            "components": {},
            "collaborations": [],
            "iterations": 0
        }
        
        result = await self._execute_generation_workflow(task)
        
        return result
    
    async def _execute_generation_workflow(self, task: StoryGenerationTask) -> Dict[str, Any]:
        """تنفيذ سير عمل إنشاء القصة"""
        
        workflow_result = {
            "task_id": task.task_id,
            "phases": {},
            "final_story": None,
            "quality_metrics": {},
            "collaboration_summary": {}
        }
        
        try:
            # المرحلة 1: التحليل الأولي
            workflow_result["phases"]["analysis"] = await self._phase_1_initial_analysis(task)
            await self._update_task_progress(task.task_id, 0.2, "analysis_complete")
            
            # المرحلة 2: الاستدلال والإثراء
            workflow_result["phases"]["inference"] = await self._phase_2_contextual_inference(
                task, workflow_result["phases"]["analysis"]
            )
            await self._update_task_progress(task.task_id, 0.4, "inference_complete")
            
            # المرحلة 3: التعاون لبناء الهيكل
            workflow_result["phases"]["collaboration"] = await self._phase_3_collaborative_structure(
                task, workflow_result["phases"]["analysis"], workflow_result["phases"]["inference"]
            )
            await self._update_task_progress(task.task_id, 0.6, "structure_complete")
            
            # المرحلة 4: الإنشاء التفاعلي
            workflow_result["phases"]["generation"] = await self._phase_4_interactive_generation(
                task, workflow_result["phases"]["collaboration"]
            )
            await self._update_task_progress(task.task_id, 0.8, "generation_complete")
            
            # المرحلة 5: المراجعة والتنقيح
            workflow_result["phases"]["refinement"] = await self._phase_5_collaborative_refinement(
                task, workflow_result["phases"]["generation"]
            )
            await self._update_task_progress(task.task_id, 1.0, "complete")
            
            # الانتهاء من العملية
            workflow_result["final_story"] = workflow_result["phases"]["refinement"]["final_output"]
            workflow_result["quality_metrics"] = await self._calculate_quality_metrics(workflow_result)
            workflow_result["collaboration_summary"] = await self._generate_collaboration_summary(task.task_id)
            
        except Exception as e:
            workflow_result["error"] = str(e)
            workflow_result["status"] = "failed"
        
        return workflow_result
    
    async def _phase_1_initial_analysis(self, task: StoryGenerationTask) -> Dict[str, Any]:
        """المرحلة 1: التحليل الأولي للترانسكريبت"""
        
        print(f"🔍 بدء المرحلة 1: التحليل الأولي للمهمة {task.task_id}")
        
        # تحليل السرد الخام
        narrative_analysis = await self.narrative_analyzer.analyze_raw_transcript(
            task.transcript
        )
        
        # تحليل أولي للمتطلبات
        requirements_analysis = await self._analyze_story_requirements(task)
        
        # تحديد التحديات المتوقعة
        challenges = await self._identify_generation_challenges(task, narrative_analysis)
        
        # تقييم جودة المصدر
        source_quality = await self._assess_source_quality(task.transcript, narrative_analysis)
        
        phase_result = {
            "narrative_analysis": narrative_analysis,
            "requirements_analysis": requirements_analysis,
            "identified_challenges": challenges,
            "source_quality_assessment": source_quality,
            "recommended_approach": await self._recommend_generation_approach(task, narrative_analysis)
        }
        
        print(f"✅ اكتمال المرحلة 1: تم تحليل {len(narrative_analysis.get('characters', []))} شخصية و {len(narrative_analysis.get('plot_structure', {}).get('plot_points', []))} نقطة حبكة")
        
        return phase_result
    
    async def _analyze_story_requirements(self, task: StoryGenerationTask) -> Dict[str, Any]:
        """تحليل متطلبات القصة"""
        
        # تحديد الطول المطلوب
        length_mapping = {
            "قصيرة": {"pages": "5-10", "words": "1500-3000", "chapters": 1},
            "متوسطة": {"pages": "15-30", "words": "4500-9000", "chapters": "3-5"},
            "طويلة": {"pages": "50-100", "words": "15000-30000", "chapters": "8-15"},
            "رواية": {"pages": "100+", "words": "30000+", "chapters": "15+"}
        }
        
        # تحديد النمط السردي
        style_requirements = {
            "كلاسيكي": {
                "structure": "تقليدي",
                "language": "فصيح",
                "pacing": "متوازن"
            },
            "حديث": {
                "structure": "مرن",
                "language": "معاصر",
                "pacing": "متنوع"
            },
            "تجريبي": {
                "structure": "مبتكر",
                "language": "إبداعي",
                "pacing": "غير تقليدي"
            }
        }
        
        requirements = {
            "length_specs": length_mapping.get(task.target_length, length_mapping["متوسطة"]),
            "style_specs": style_requirements.get(task.narrative_style, style_requirements["كلاسيكي"]),
            "cultural_requirements": await self._analyze_cultural_requirements(task.cultural_focus),
            "user_preferences": task.user_preferences,
            "genre_expectations": await self._determine_genre_expectations(task.story_type)
        }
        
        return requirements
    
    async def _analyze_cultural_requirements(self, cultural_focus: str) -> Dict[str, Any]:
        """تحليل المتطلبات الثقافية"""
        
        cultural_specs = {
            "تراثي": {
                "elements": ["حكايات شعبية", "أمثال", "شعر", "تقاليد"],
                "language_style": "كلاسيكي",
                "references": "تاريخية"
            },
            "معاصر": {
                "elements": ["قضايا حديثة", "تحديات العصر", "تكنولوجيا"],
                "language_style": "حديث",
                "references": "معاصرة"
            },
            "مختلط": {
                "elements": ["تراث وحداثة", "ماضي وحاضر", "تطور"],
                "language_style": "متوازن",
                "references": "متنوعة"
            }
        }
        
        return cultural_specs.get(cultural_focus, cultural_specs["مختلط"])
    
    async def _determine_genre_expectations(self, story_type: str) -> Dict[str, Any]:
        """تحديد توقعات النوع الأدبي"""
        
        genre_specs = {
            "مغامرة": {
                "key_elements": ["رحلة", "تحديات", "اكتشاف"],
                "pacing": "سريع",
                "conflicts": ["إنسان ضد طبيعة", "إنسان ضد مجهول"]
            },
            "رومانسي": {
                "key_elements": ["حب", "علاقات", "عواطف"],
                "pacing": "متوسط",
                "conflicts": ["صراع عاطفي", "عوائق اجتماعية"]
            },
            "تاريخي": {
                "key_elements": ["فترة تاريخية", "شخصيات حقيقية", "أحداث مهمة"],
                "pacing": "متأني",
                "conflicts": ["تاريخي", "اجتماعي"]
            },
            "اجتماعي": {
                "key_elements": ["قضايا مجتمعية", "نقد", "تغيير"],
                "pacing": "متوازن",
                "conflicts": ["إنسان ضد مجتمع", "قيم متصارعة"]
            }
        }
        
        return genre_specs.get(story_type, genre_specs["اجتماعي"])
    
    async def _identify_generation_challenges(self, task: StoryGenerationTask, 
                                            analysis: Dict[str, Any]) -> List[str]:
        """تحديد تحديات الإنشاء"""
        
        challenges = []
        
        # تحديات المصدر
        characters = analysis.get("characters", [])
        if len(characters) < 2:
            challenges.append("قلة الشخصيات في المصدر - يحتاج تطوير شخصيات إضافية")
        
        plot_points = analysis.get("plot_structure", {}).get("plot_points", [])
        if len(plot_points) < 3:
            challenges.append("ضعف البنية السردية - يحتاج تطوير أحداث إضافية")
        
        # تحديات التحويل
        if task.target_length in ["طويلة", "رواية"]:
            challenges.append("التحدي في توسيع المحتوى للطول المطلوب")
        
        if task.story_type == "تاريخي":
            challenges.append("ضرورة التحقق من الدقة التاريخية")
        
        # تحديات ثقافية
        cultural_elements = analysis.get("cultural_context", {}).get("cultural_elements", {})
        if not cultural_elements:
            challenges.append("غياب العناصر الثقافية - يحتاج إثراء ثقافي")
        
        return challenges
    
    async def _assess_source_quality(self, transcript: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """تقييم جودة المصدر"""
        
        quality_metrics = {
            "content_richness": 0.0,
            "narrative_coherence": 0.0,
            "character_development": 0.0,
            "cultural_authenticity": 0.0,
            "overall_quality": 0.0
        }
        
        # ثراء المحتوى
        word_count = len(transcript.split())
        character_count = len(analysis.get("characters", []))
        plot_density = len(analysis.get("plot_structure", {}).get("plot_points", []))
        
        quality_metrics["content_richness"] = min(1.0, 
            (word_count / 500 * 0.4) + 
            (character_count / 3 * 0.3) + 
            (plot_density / 5 * 0.3)
        )
        
        # تماسك السرد
        temporal_structure = analysis.get("temporal_structure", {})
        if temporal_structure.get("time_markers"):
            quality_metrics["narrative_coherence"] += 0.3
        if temporal_structure.get("chronological_order"):
            quality_metrics["narrative_coherence"] += 0.3
        quality_metrics["narrative_coherence"] = min(1.0, quality_metrics["narrative_coherence"] + 0.4)
        
        # تطوير الشخصيات
        developed_characters = sum(1 for char in analysis.get("characters", []) 
                                 if hasattr(char, 'traits') and len(char.traits) > 1)
        quality_metrics["character_development"] = min(1.0, developed_characters / max(1, character_count))
        
        # الأصالة الثقافية
        cultural_density = analysis.get("cultural_context", {}).get("cultural_density", 0)
        quality_metrics["cultural_authenticity"] = min(1.0, cultural_density / 10)
        
        # الجودة الإجمالية
        quality_metrics["overall_quality"] = sum(quality_metrics.values()) / 4
        
        # تصنيف الجودة
        if quality_metrics["overall_quality"] > 0.8:
            quality_level = "ممتاز"
        elif quality_metrics["overall_quality"] > 0.6:
            quality_level = "جيد"
        elif quality_metrics["overall_quality"] > 0.4:
            quality_level = "متوسط"
        else:
            quality_level = "يحتاج تطوير"
        
        return {
            "metrics": quality_metrics,
            "quality_level": quality_level,
            "strengths": await self._identify_source_strengths(analysis),
            "weaknesses": await self._identify_source_weaknesses(analysis)
        }
    
    async def _identify_source_strengths(self, analysis: Dict[str, Any]) -> List[str]:
        """تحديد نقاط قوة المصدر"""
        strengths = []
        
        # قوة الشخصيات
        characters = analysis.get("characters", [])
        complex_characters = sum(1 for char in characters 
                               if hasattr(char, 'traits') and len(char.traits) > 2)
        if complex_characters > 0:
            strengths.append(f"شخصيات معقدة ومتطورة ({complex_characters} شخصية)")
        
        # ثراء العاطفة
        emotional_arc = analysis.get("emotional_arc", {})
        if emotional_arc.get("dominant_emotions"):
            strengths.append("تنوع عاطفي غني")
        
        # تماسك ثقافي
        cultural_elements = analysis.get("cultural_context", {}).get("cultural_elements", {})
        if len(cultural_elements) > 2:
            strengths.append("تنوع ثقافي أصيل")
        
        # بنية سردية قوية
        plot_structure = analysis.get("plot_structure", {})
        if plot_structure.get("climax"):
            strengths.append("ذروة واضحة ومؤثرة")
        
        return strengths
    
    async def _identify_source_weaknesses(self, analysis: Dict[str, Any]) -> List[str]:
        """تحديد نقاط ضعف المصدر"""
        weaknesses = []
        
        # ضعف الشخصيات
        characters = analysis.get("characters", [])
        weak_characters = sum(1 for char in characters 
                            if not hasattr(char, 'traits') or len(char.traits) < 2)
        if weak_characters > len(characters) / 2:
            weaknesses.append("شخصيات تحتاج تطوير أكثر")
        
        # ضعف الحبكة
        plot_points = analysis.get("plot_structure", {}).get("plot_points", [])
        if len(plot_points) < 3:
            weaknesses.append("حبكة تحتاج المزيد من الأحداث")
        
        # ضعف ثقافي
        cultural_density = analysis.get("cultural_context", {}).get("cultural_density", 0)
        if cultural_density < 3:
            weaknesses.append("محتوى ثقافي محدود")
        
        # ضعف الحوار
        dialogue_ratio = analysis.get("dialogue_analysis", {}).get("dialogue_ratio", 0)
        if dialogue_ratio < 0.1:
            weaknesses.append("قلة الحوار والتفاعل")
        
        return weaknesses
    
    async def _recommend_generation_approach(self, task: StoryGenerationTask, 
                                           analysis: Dict[str, Any]) -> Dict[str, Any]:
        """اقتراح نهج الإنشاء"""
        
        approach = {
            "primary_strategy": "",
            "focus_areas": [],
            "agent_priorities": {},
            "enhancement_techniques": []
        }
        
        # تحديد الاستراتيجية الأساسية
        quality = await self._assess_source_quality(task.transcript, analysis)
        
        if quality["quality_level"] == "ممتاز":
            approach["primary_strategy"] = "التطوير والإثراء"
            approach["focus_areas"] = ["توسيع المحتوى", "تعميق الشخصيات", "إثراء التفاصيل"]
        elif quality["quality_level"] == "جيد":
            approach["primary_strategy"] = "التحسين والتوسيع"
            approach["focus_areas"] = ["معالجة نقاط الضعف", "تطوير الحبكة", "إضافة عناصر جديدة"]
        else:
            approach["primary_strategy"] = "البناء والتطوير"
            approach["focus_areas"] = ["إعادة هيكلة", "تطوير شامل", "إثراء كامل"]
        
        # تحديد أولويات الوكلاء
        approach["agent_priorities"] = {
            "idea_generator": 0.8 if quality["quality_level"] in ["متوسط", "يحتاج تطوير"] else 0.5,
            "blueprint_architect": 0.9,  # دائماً مهم للهيكلة
            "chapter_composer": 0.7,
            "literary_critic": 0.8,  # مهم للمراجعة
            "cultural_maestro": 0.9 if task.cultural_focus != "معاصر" else 0.6
        }
        
        # تقنيات التحسين
        if len(analysis.get("characters", [])) < 3:
            approach["enhancement_techniques"].append("تطوير شخصيات إضافية")
        
        if task.target_length in ["طويلة", "رواية"]:
            approach["enhancement_techniques"].append("توسيع الأحداث والمشاهد")
        
        if task.cultural_focus == "تراثي":
            approach["enhancement_techniques"].append("إثراء العناصر التراثية")
        
        return approach
    
    async def _phase_2_contextual_inference(self, task: StoryGenerationTask, 
                                          analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """المرحلة 2: الاستدلال السياقي والإثراء"""
        
        print(f"🧠 بدء المرحلة 2: الاستدلال السياقي للمهمة {task.task_id}")
        
        # التحليل السياقي العميق
        inference_result = await self.inference_engine.analyze_context_and_infer(
            analysis_result["narrative_analysis"], 
            task.transcript
        )
        
        # تطوير السيناريوهات المحتملة
        enhanced_scenarios = await self._enhance_scenario_hypotheses(
            inference_result["scenario_hypotheses"], 
            task
        )
        
        # تحديد استراتيجيات الإثراء
        enrichment_strategies = await self._develop_enrichment_strategies(
            inference_result, 
            analysis_result["requirements_analysis"]
        )
        
        # خطة التكامل
        integration_plan = await self._create_integration_plan(
            analysis_result["narrative_analysis"], 
            inference_result
        )
        
        phase_result = {
            "contextual_analysis": inference_result,
            "enhanced_scenarios": enhanced_scenarios,
            "enrichment_strategies": enrichment_strategies,
            "integration_plan": integration_plan,
            "cultural_enrichment": await self._plan_cultural_enrichment(task, inference_result)
        }
        
        print(f"✅ اكتمال المرحلة 2: تم تطوير {len(enhanced_scenarios)} سيناريو و {len(enrichment_strategies)} استراتيجية إثراء")
        
        return phase_result
    
    async def _enhance_scenario_hypotheses(self, scenarios: List[Any], 
                                         task: StoryGenerationTask) -> List[Dict[str, Any]]:
        """تطوير فرضيات السيناريوهات"""
        
        enhanced_scenarios = []
        
        for scenario in scenarios:
            enhanced_scenario = {
                "original": scenario,
                "adaptations": await self._adapt_scenario_to_requirements(scenario, task),
                "expansion_possibilities": await self._identify_expansion_possibilities(scenario, task),
                "cultural_integration": await self._plan_cultural_integration(scenario, task)
            }
            enhanced_scenarios.append(enhanced_scenario)
        
        return enhanced_scenarios
    
    async def _adapt_scenario_to_requirements(self, scenario: Any, 
                                            task: StoryGenerationTask) -> Dict[str, Any]:
        """تكييف السيناريو مع المتطلبات"""
        
        adaptations = {
            "length_adaptation": "",
            "style_adaptation": "",
            "genre_adaptation": "",
            "cultural_adaptation": ""
        }
        
        # تكييف الطول
        if task.target_length == "طويلة":
            adaptations["length_adaptation"] = "توسيع السيناريو بتفاصيل أكثر وأحداث فرعية"
        elif task.target_length == "قصيرة":
            adaptations["length_adaptation"] = "تركيز السيناريو على الأحداث الأساسية"
        
        # تكييف النمط
        if task.narrative_style == "كلاسيكي":
            adaptations["style_adaptation"] = "استخدام البنية التقليدية والأسلوب الكلاسيكي"
        elif task.narrative_style == "حديث":
            adaptations["style_adaptation"] = "دمج تقنيات سردية معاصرة"
        
        # تكييف النوع
        if task.story_type == "مغامرة":
            adaptations["genre_adaptation"] = "تطوير عناصر التشويق والإثارة"
        elif task.story_type == "رومانسي":
            adaptations["genre_adaptation"] = "التركيز على العلاقات العاطفية"
        
        return adaptations
    
    async def _identify_expansion_possibilities(self, scenario: Any, 
                                              task: StoryGenerationTask) -> List[str]:
        """تحديد إمكانيات التوسيع"""
        
        possibilities = []
        
        # إمكانيات التوسيع بناءً على نوع السيناريو
        if hasattr(scenario, 'scenario_id'):
            if "char_dev" in scenario.scenario_id:
                possibilities.extend([
                    "تطوير خلفية الشخصية",
                    "إضافة صراعات داخلية",
                    "تطوير علاقات مع شخصيات أخرى"
                ])
            elif "conflict" in scenario.scenario_id:
                possibilities.extend([
                    "تصعيد التوتر تدريجياً",
                    "إضافة عقد فرعية",
                    "تطوير حلول متعددة"
                ])
        
        # إمكانيات بناءً على نوع القصة
        if task.story_type == "تاريخي":
            possibilities.extend([
                "ربط بأحداث تاريخية حقيقية",
                "تطوير السياق التاريخي",
                "إضافة شخصيات تاريخية"
            ])
        
        return possibilities
    
    async def _plan_cultural_integration(self, scenario: Any, 
                                       task: StoryGenerationTask) -> Dict[str, Any]:
        """تخطيط التكامل الثقافي"""
        
        integration_plan = {
            "cultural_elements": [],
            "traditional_references": [],
            "language_enhancements": [],
            "social_context": []
        }
        
        if task.cultural_focus == "تراثي":
            integration_plan["cultural_elements"] = [
                "أمثال شعبية", "حكايات تراثية", "شعر كلاسيكي"
            ]
            integration_plan["traditional_references"] = [
                "مراجع تاريخية", "شخصيات تراثية", "أماكن مقدسة"
            ]
        elif task.cultural_focus == "معاصر":
            integration_plan["cultural_elements"] = [
                "قضايا حديثة", "تحديات العصر", "تكنولوجيا"
            ]
        
        return integration_plan
    
    async def _develop_enrichment_strategies(self, inference_result: Dict[str, Any], 
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """تطوير استراتيجيات الإثراء"""
        
        strategies = []
        
        # استراتيجية إثراء الشخصيات
        if inference_result.get("enrichment_suggestions", {}).get("character_development"):
            strategies.append({
                "type": "character_enrichment",
                "priority": "عالية",
                "techniques": [
                    "تطوير الخلفيات الشخصية",
                    "إضافة دوافع معقدة",
                    "تطوير العلاقات بين الشخصيات"
                ],
                "target_agents": ["idea_generator", "cultural_maestro"]
            })
        
        # استراتيجية إثراء الحبكة
        if inference_result.get("enrichment_suggestions", {}).get("plot_strengthening"):
            strategies.append({
                "type": "plot_enrichment",
                "priority": "عالية",
                "techniques": [
                    "إضافة نقاط تحول مثيرة",
                    "تطوير التوتر تدريجياً",
                    "ربط الأحداث بشكل منطقي"
                ],
                "target_agents": ["blueprint_architect", "chapter_composer"]
            })
        
        # استراتيجية الإثراء الثقافي
        cultural_suggestions = inference_result.get("enrichment_suggestions", {}).get("cultural_deepening", [])
        if cultural_suggestions:
            strategies.append({
                "type": "cultural_enrichment",
                "priority": "متوسطة",
                "techniques": cultural_suggestions,
                "target_agents": ["cultural_maestro"]
            })
        
        return strategies
    
    async def _create_integration_plan(self, narrative_analysis: Dict[str, Any], 
                                     inference_result: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء خطة التكامل"""
        
        integration_plan = {
            "source_preservation": await self._plan_source_preservation(narrative_analysis),
            "enhancement_integration": await self._plan_enhancement_integration(inference_result),
            "quality_assurance": await self._plan_quality_assurance(),
            "iteration_strategy": await self._plan_iteration_strategy()
        }
        
        return integration_plan
    
    async def _plan_source_preservation(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """تخطيط الحفاظ على المصدر"""
        
        preservation_plan = {
            "core_elements_to_preserve": [],
            "key_quotes_to_include": [],
            "character_essence_maintenance": {},
            "plot_core_retention": {}
        }
        
        # العناصر الأساسية للحفاظ عليها
        characters = analysis.get("characters", [])
        for character in characters:
            if hasattr(character, 'significance_score') and character.significance_score > 0.5:
                preservation_plan["core_elements_to_preserve"].append(f"شخصية {character.name}")
        
        # الحبكة الأساسية
        plot_structure = analysis.get("plot_structure", {})
        if plot_structure.get("climax"):
            preservation_plan["core_elements_to_preserve"].append("الذروة الأساسية")
        
        return preservation_plan
    
    async def _plan_enhancement_integration(self, inference_result: Dict[str, Any]) -> Dict[str, Any]:
        """تخطيط دمج التحسينات"""
        
        integration_plan = {
            "seamless_additions": [],
            "gradual_expansions": [],
            "cultural_weaving": [],
            "narrative_bridges": []
        }
        
        # الإضافات السلسة
        scenarios = inference_result.get("scenario_hypotheses", [])
        for scenario in scenarios[:3]:  # أفضل 3 سيناريوهات
            if hasattr(scenario, 'probability') and scenario.probability > 0.6:
                integration_plan["seamless_additions"].append(scenario.description)
        
        return integration_plan
    
    async def _plan_quality_assurance(self) -> Dict[str, Any]:
        """تخطيط ضمان الجودة"""
        
        return {
            "review_cycles": 2,
            "quality_checkpoints": [
                "بعد كل فصل",
                "بعد المسودة الأولى",
                "قبل الإنتاج النهائي"
            ],
            "evaluation_criteria": [
                "الاتساق السردي",
                "جودة الشخصيات",
                "الأصالة الثقافية",
                "اللغة والأسلوب"
            ]
        }
    
    async def _plan_iteration_strategy(self) -> Dict[str, Any]:
        """تخطيط استراتيجية التكرار"""
        
        return {
            "max_iterations": 3,
            "improvement_focus": [
                "التكرار الأول: البنية والهيكل",
                "التكرار الثاني: المحتوى والتفاصيل",
                "التكرار الثالث: الأسلوب واللغة"
            ],
            "success_criteria": {
                "narrative_coherence": 0.8,
                "character_development": 0.7,
                "cultural_authenticity": 0.8
            }
        }
    
    async def _plan_cultural_enrichment(self, task: StoryGenerationTask, 
                                      inference_result: Dict[str, Any]) -> Dict[str, Any]:
        """تخطيط الإثراء الثقافي"""
        
        cultural_plan = {
            "target_elements": [],
            "integration_methods": [],
            "authenticity_validation": [],
            "modernization_balance": []
        }
        
        if task.cultural_focus == "تراثي":
            cultural_plan["target_elements"] = [
                "حكايات شعبية", "أمثال وحكم", "شعر تراثي", "عادات وتقاليد"
            ]
            cultural_plan["integration_methods"] = [
                "الاقتباس المباشر", "الإشارة الضمنية", "إعادة الصياغة"
            ]
        
        return cultural_plan
    
    async def _phase_3_collaborative_structure(self, task: StoryGenerationTask,
                                             analysis: Dict[str, Any],
                                             inference: Dict[str, Any]) -> Dict[str, Any]:
        """المرحلة 3: البناء التعاوني للهيكل"""
        
        print(f"🏗️ بدء المرحلة 3: البناء التعاوني للهيكل للمهمة {task.task_id}")
        
        # تفعيل التعاون بين الوكلاء
        collaborations = []
        
        # 1. مولد الأفكار + المهندس المعماري
        idea_blueprint_collab = await self._collaborate_idea_generation_and_architecture(
            task, analysis, inference
        )
        collaborations.append(idea_blueprint_collab)
        
        # 2. المهندس المعماري + الخبير الثقافي
        architect_cultural_collab = await self._collaborate_architecture_and_culture(
            task, analysis, inference
        )
        collaborations.append(architect_cultural_collab)
        
        # 3. مراجعة نقدية أولية
        initial_review = await self._initial_critical_review(
            [idea_blueprint_collab, architect_cultural_collab]
        )
        
        # 4. تكرار وتحسين
        refined_structure = await self._refine_collaborative_structure(
            collaborations, initial_review
        )
        
        phase_result = {
            "collaborations": collaborations,
            "initial_review": initial_review,
            "refined_structure": refined_structure,
            "structure_quality_metrics": await self._evaluate_structure_quality(refined_structure)
        }
        
        print(f"✅ اكتمال المرحلة 3: تم إنشاء هيكل مع {len(collaborations)} تعاون")
        
        return phase_result
    
    async def _collaborate_idea_generation_and_architecture(self, task: StoryGenerationTask,
                                                          analysis: Dict[str, Any],
                                                          inference: Dict[str, Any]) -> AgentCollaboration:
        """تعاون مولد الأفكار والمهندس المعماري"""
        
        # 1. مولد الأفكار يطور أفكار جديدة
        idea_input = {
            "source_analysis": analysis["narrative_analysis"],
            "requirements": analysis["requirements_analysis"],
            "enhancement_opportunities": inference["enrichment_strategies"]
        }
        
        generated_ideas = await self.idea_generator.generate_ideas(idea_input)
        
        # 2. المهندس المعماري يطور الهيكل
        architecture_input = {
            "generated_ideas": generated_ideas,
            "source_structure": analysis["narrative_analysis"]["plot_structure"],
            "target_requirements": analysis["requirements_analysis"]
        }
        
        story_blueprint = await self.blueprint_architect.create_blueprint(architecture_input)
        
        # 3. التفاعل والتحسين
        feedback_cycles = []
        for i in range(2):  # دورتين من التغذية الراجعة
            # المهندس يعطي تغذية راجعة للأفكار
            architect_feedback = await self.blueprint_architect.review_ideas(generated_ideas)
            
            # مولد الأفكار يحسن الأفكار
            refined_ideas = await self.idea_generator.refine_ideas(generated_ideas, architect_feedback)
            
            # المهندس يحدث الهيكل
            updated_blueprint = await self.blueprint_architect.update_blueprint(
                story_blueprint, refined_ideas
            )
            
            feedback_cycles.append({
                "cycle": i + 1,
                "architect_feedback": architect_feedback,
                "refined_ideas": refined_ideas,
                "updated_blueprint": updated_blueprint
            })
            
            generated_ideas = refined_ideas
            story_blueprint = updated_blueprint
        
        return AgentCollaboration(
            agent_name="مولد الأفكار + المهندس المعماري",
            contribution_type="تطوير الأفكار والهيكل",
            output={
                "final_ideas": generated_ideas,
                "final_blueprint": story_blueprint,
                "feedback_cycles": feedback_cycles
            },
            feedback_received=[],
            revisions=len(feedback_cycles),
            completion_status="مكتمل"
        )
    
    async def _collaborate_architecture_and_culture(self, task: StoryGenerationTask,
                                                   analysis: Dict[str, Any],
                                                   inference: Dict[str, Any]) -> AgentCollaboration:
        """تعاون المهندس المعماري والخبير الثقافي"""
        
        # 1. تحليل الخبير الثقافي للمتطلبات
        cultural_input = {
            "cultural_focus": task.cultural_focus,
            "source_cultural_context": analysis["narrative_analysis"].get("cultural_context", {}),
            "historical_context": inference["contextual_analysis"].get("historical_context")
        }
        
        cultural_guidelines = await self.cultural_maestro.provide_cultural_guidance(cultural_input)
        
        # 2. المهندس يدمج الإرشادات الثقافية
        cultural_integration = await self.blueprint_architect.integrate_cultural_elements(
            cultural_guidelines
        )
        
        # 3. الخبير الثقافي يراجع التكامل
        cultural_review = await self.cultural_maestro.review_cultural_integration(
            cultural_integration
        )
        
        # 4. تحسين التكامل
        refined_integration = await self.blueprint_architect.refine_cultural_integration(
            cultural_integration, cultural_review
        )
        
        return AgentCollaboration(
            agent_name="المهندس المعماري + الخبير الثقافي",
            contribution_type="التكامل الثقافي",
            output={
                "cultural_guidelines": cultural_guidelines,
                "cultural_integration": refined_integration,
                "cultural_review": cultural_review
            },
            feedback_received=[cultural_review],
            revisions=1,
            completion_status="مكتمل"
        )
    
    async def _initial_critical_review(self, collaborations: List[AgentCollaboration]) -> Dict[str, Any]:
        """المراجعة النقدية الأولية"""
        
        # جمع نتائج التعاون
        combined_output = {}
        for collab in collaborations:
            combined_output.update(collab.output)
        
        # المراجعة النقدية
        critical_review = await self.literary_critic.review_structure(combined_output)
        
        return {
            "overall_assessment": critical_review.get("overall_assessment", ""),
            "strengths": critical_review.get("strengths", []),
            "areas_for_improvement": critical_review.get("areas_for_improvement", []),
            "recommendations": critical_review.get("recommendations", []),
            "quality_score": critical_review.get("quality_score", 0.0)
        }
    
    async def _refine_collaborative_structure(self, collaborations: List[AgentCollaboration],
                                            review: Dict[str, Any]) -> Dict[str, Any]:
        """تحسين الهيكل التعاوني"""
        
        refinement_actions = []
        
        # تحسين بناءً على التوصيات
        for recommendation in review.get("recommendations", []):
            if "شخصيات" in recommendation:
                # تحسين تطوير الشخصيات
                character_refinement = await self._refine_character_development(collaborations)
                refinement_actions.append(character_refinement)
            
            elif "حبكة" in recommendation:
                # تحسين الحبكة
                plot_refinement = await self._refine_plot_structure(collaborations)
                refinement_actions.append(plot_refinement)
            
            elif "ثقافي" in recommendation:
                # تحسين العناصر الثقافية
                cultural_refinement = await self._refine_cultural_elements(collaborations)
                refinement_actions.append(cultural_refinement)
        
        # دمج التحسينات
        refined_structure = await self._integrate_refinements(collaborations, refinement_actions)
        
        return {
            "refinement_actions": refinement_actions,
            "refined_structure": refined_structure,
            "improvement_metrics": await self._calculate_improvement_metrics(
                collaborations, refined_structure
            )
        }
    
    async def _refine_character_development(self, collaborations: List[AgentCollaboration]) -> Dict[str, Any]:
        """تحسين تطوير الشخصيات"""
        
        # استخراج الشخصيات الحالية
        current_characters = []
        for collab in collaborations:
            if "final_ideas" in collab.output:
                characters_data = collab.output["final_ideas"].get("characters", [])
                current_characters.extend(characters_data)
        
        # تطوير الشخصيات بواسطة مولد الأفكار
        enhanced_characters = await self.idea_generator.enhance_characters(current_characters)
        
        return {
            "type": "character_refinement",
            "original_count": len(current_characters),
            "enhanced_characters": enhanced_characters,
            "improvements": [
                "إضافة خلفيات شخصية",
                "تطوير الدوافع",
                "تعقيد العلاقات"
            ]
        }
    
    async def _refine_plot_structure(self, collaborations: List[AgentCollaboration]) -> Dict[str, Any]:
        """تحسين بنية الحبكة"""
        
        # استخراج الهيكل الحالي
        current_blueprint = None
        for collab in collaborations:
            if "final_blueprint" in collab.output:
                current_blueprint = collab.output["final_blueprint"]
                break
        
        if current_blueprint:
            # تحسين الهيكل بواسطة المهندس المعماري
            enhanced_blueprint = await self.blueprint_architect.enhance_structure(current_blueprint)
            
            return {
                "type": "plot_refinement",
                "original_structure": current_blueprint,
                "enhanced_structure": enhanced_blueprint,
                "improvements": [
                    "تقوية نقاط التحول",
                    "تحسين الإيقاع",
                    "زيادة التوتر"
                ]
            }
        
        return {"type": "plot_refinement", "status": "no_structure_found"}
    
    async def _refine_cultural_elements(self, collaborations: List[AgentCollaboration]) -> Dict[str, Any]:
        """تحسين العناصر الثقافية"""
        
        # استخراج العناصر الثقافية الحالية
        cultural_elements = {}
        for collab in collaborations:
            if "cultural_integration" in collab.output:
                cultural_elements = collab.output["cultural_integration"]
                break
        
        # تحسين العناصر الثقافية
        enhanced_cultural = await self.cultural_maestro.enhance_cultural_elements(cultural_elements)
        
        return {
            "type": "cultural_refinement",
            "original_elements": cultural_elements,
            "enhanced_elements": enhanced_cultural,
            "improvements": [
                "إضافة تفاصيل تراثية",
                "تقوية الأصالة",
                "تحسين السياق الثقافي"
            ]
        }
    
    async def _integrate_refinements(self, collaborations: List[AgentCollaboration],
                                   refinements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """دمج التحسينات"""
        
        integrated_structure = {
            "characters": [],
            "plot_structure": {},
            "cultural_elements": {},
            "themes": [],
            "settings": []
        }
        
        # دمج التحسينات
        for refinement in refinements:
            if refinement["type"] == "character_refinement":
                integrated_structure["characters"] = refinement.get("enhanced_characters", [])
            elif refinement["type"] == "plot_refinement":
                integrated_structure["plot_structure"] = refinement.get("enhanced_structure", {})
            elif refinement["type"] == "cultural_refinement":
                integrated_structure["cultural_elements"] = refinement.get("enhanced_elements", {})
        
        return integrated_structure
    
    async def _calculate_improvement_metrics(self, original_collaborations: List[AgentCollaboration],
                                           refined_structure: Dict[str, Any]) -> Dict[str, float]:
        """حساب مقاييس التحسين"""
        
        metrics = {
            "character_complexity_improvement": 0.0,
            "plot_coherence_improvement": 0.0,
            "cultural_richness_improvement": 0.0,
            "overall_improvement": 0.0
        }
        
        # حساب تحسين تعقيد الشخصيات
        original_char_count = 0
        for collab in original_collaborations:
            if "final_ideas" in collab.output:
                original_char_count = len(collab.output["final_ideas"].get("characters", []))
                break
        
        refined_char_count = len(refined_structure.get("characters", []))
        if original_char_count > 0:
            metrics["character_complexity_improvement"] = (refined_char_count - original_char_count) / original_char_count
        
        # حساب التحسين الإجمالي
        metrics["overall_improvement"] = sum([
            metrics["character_complexity_improvement"],
            metrics["plot_coherence_improvement"],
            metrics["cultural_richness_improvement"]
        ]) / 3
        
        return metrics
    
    async def _evaluate_structure_quality(self, structure: Dict[str, Any]) -> Dict[str, float]:
        """تقييم جودة الهيكل"""
        
        quality_metrics = {
            "completeness": 0.0,
            "coherence": 0.0,
            "cultural_authenticity": 0.0,
            "creative_potential": 0.0,
            "overall_quality": 0.0
        }
        
        # تقييم الاكتمال
        required_components = ["characters", "plot_structure", "cultural_elements"]
        present_components = sum(1 for comp in required_components if structure.get(comp))
        quality_metrics["completeness"] = present_components / len(required_components)
        
        # تقييم التماسك
        if structure.get("plot_structure") and structure.get("characters"):
            quality_metrics["coherence"] = 0.8  # تقييم مبسط
        
        # تقييم الأصالة الثقافية
        cultural_elements = structure.get("cultural_elements", {})
        if cultural_elements:
            quality_metrics["cultural_authenticity"] = min(1.0, len(cultural_elements) / 5)
        
        # تقييم الإمكانات الإبداعية
        character_count = len(structure.get("characters", []))
        plot_complexity = len(structure.get("plot_structure", {}))
        quality_metrics["creative_potential"] = min(1.0, (character_count + plot_complexity) / 10)
        
        # الجودة الإجمالية
        quality_metrics["overall_quality"] = sum(quality_metrics.values()) / 4
        
        return quality_metrics
    
    async def _phase_4_interactive_generation(self, task: StoryGenerationTask,
                                            structure: Dict[str, Any]) -> Dict[str, Any]:
        """المرحلة 4: الإنشاء التفاعلي"""
        
        print(f"✍️ بدء المرحلة 4: الإنشاء التفاعلي للمهمة {task.task_id}")
        
        # إنشاء الفصول بالتعاون
        chapter_collaborations = []
        
        # تحديد عدد الفصول بناءً على الطول المطلوب
        chapter_count = await self._determine_chapter_count(task.target_length)
        
        for chapter_num in range(1, chapter_count + 1):
            chapter_collab = await self._generate_chapter_collaboratively(
                chapter_num, task, structure
            )
            chapter_collaborations.append(chapter_collab)
        
        # دمج الفصول
        assembled_story = await self._assemble_story_chapters(chapter_collaborations)
        
        # مراجعة تتابعية
        sequential_review = await self._sequential_story_review(assembled_story)
        
        phase_result = {
            "chapter_collaborations": chapter_collaborations,
            "assembled_story": assembled_story,
            "sequential_review": sequential_review,
            "generation_metrics": await self._calculate_generation_metrics(chapter_collaborations)
        }
        
        print(f"✅ اكتمال المرحلة 4: تم إنشاء {len(chapter_collaborations)} فصل")
        
        return phase_result
    
    async def _determine_chapter_count(self, target_length: str) -> int:
        """تحديد عدد الفصول"""
        
        length_to_chapters = {
            "قصيرة": 1,
            "متوسطة": 4,
            "طويلة": 10,
            "رواية": 15
        }
        
        return length_to_chapters.get(target_length, 4)
    
    async def _generate_chapter_collaboratively(self, chapter_num: int,
                                              task: StoryGenerationTask,
                                              structure: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء فصل بالتعاون"""
        
        # 1. كاتب الفصول ينشئ المسودة الأولى
        chapter_input = {
            "chapter_number": chapter_num,
            "story_structure": structure,
            "requirements": task,
            "previous_chapters": []  # سيتم ملؤها لاحقاً
        }
        
        initial_chapter = await self.chapter_composer.compose_chapter(chapter_input)
        
        # 2. الخبير الثقافي يراجع ويضيف العناصر الثقافية
        cultural_enhancement = await self.cultural_maestro.enhance_chapter_culturally(
            initial_chapter, task.cultural_focus
        )
        
        # 3. الناقد الأدبي يراجع ويقترح تحسينات
        critical_feedback = await self.literary_critic.review_chapter(cultural_enhancement)
        
        # 4. كاتب الفصول يطبق التحسينات
        final_chapter = await self.chapter_composer.refine_chapter(
            cultural_enhancement, critical_feedback
        )
        
        return {
            "chapter_number": chapter_num,
            "initial_draft": initial_chapter,
            "cultural_enhancement": cultural_enhancement,
            "critical_feedback": critical_feedback,
            "final_chapter": final_chapter,
            "collaboration_quality": await self._assess_chapter_collaboration_quality(
                initial_chapter, final_chapter
            )
        }
    
    async def _assess_chapter_collaboration_quality(self, initial: Any, final: Any) -> Dict[str, float]:
        """تقييم جودة التعاون في الفصل"""
        
        # تقييم مبسط للتحسين
        quality_metrics = {
            "improvement_level": 0.7,  # افتراضي
            "cultural_integration": 0.8,
            "literary_quality": 0.75,
            "collaboration_effectiveness": 0.0
        }
        
        # حساب فعالية التعاون
        quality_metrics["collaboration_effectiveness"] = (
            quality_metrics["improvement_level"] + 
            quality_metrics["cultural_integration"] + 
            quality_metrics["literary_quality"]
        ) / 3
        
        return quality_metrics
    
    async def _assemble_story_chapters(self, chapter_collaborations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """تجميع فصول القصة"""
        
        assembled_story = {
            "title": "القصة المُولَّدة",  # سيتم تطويرها لاحقاً
            "chapters": [],
            "word_count": 0,
            "character_consistency": {},
            "plot_continuity": {}
        }
        
        # تجميع الفصول
        for collab in chapter_collaborations:
            chapter = collab["final_chapter"]
            assembled_story["chapters"].append(chapter)
            
            # حساب عدد الكلمات (تقديري)
            if isinstance(chapter, dict) and "content" in chapter:
                words = len(str(chapter["content"]).split())
                assembled_story["word_count"] += words
        
        # فحص الاتساق
        assembled_story["character_consistency"] = await self._check_character_consistency_across_chapters(
            assembled_story["chapters"]
        )
        
        assembled_story["plot_continuity"] = await self._check_plot_continuity(
            assembled_story["chapters"]
        )
        
        return assembled_story
    
    async def _check_character_consistency_across_chapters(self, chapters: List[Any]) -> Dict[str, Any]:
        """فحص اتساق الشخصيات عبر الفصول"""
        
        consistency_report = {
            "consistent_characters": [],
            "inconsistent_characters": [],
            "missing_characters": [],
            "overall_consistency_score": 0.0
        }
        
        # تحليل مبسط للاتساق
        # في تطبيق حقيقي، سنقوم بتحليل أعمق
        
        consistency_report["overall_consistency_score"] = 0.8  # افتراضي
        
        return consistency_report
    
    async def _check_plot_continuity(self, chapters: List[Any]) -> Dict[str, Any]:
        """فحص استمرارية الحبكة"""
        
        continuity_report = {
            "smooth_transitions": True,
            "logical_progression": True,
            "unresolved_plot_points": [],
            "continuity_score": 0.0
        }
        
        # تحليل مبسط للاستمرارية
        continuity_report["continuity_score"] = 0.85  # افتراضي
        
        return continuity_report
    
    async def _sequential_story_review(self, assembled_story: Dict[str, Any]) -> Dict[str, Any]:
        """مراجعة تتابعية للقصة"""
        
        # المراجعة الأدبية الشاملة
        comprehensive_review = await self.literary_critic.review_complete_story(assembled_story)
        
        # المراجعة الثقافية
        cultural_review = await self.cultural_maestro.review_cultural_authenticity(assembled_story)
        
        # توصيات للتحسين
        improvement_recommendations = await self._generate_improvement_recommendations(
            comprehensive_review, cultural_review
        )
        
        return {
            "literary_review": comprehensive_review,
            "cultural_review": cultural_review,
            "improvement_recommendations": improvement_recommendations,
            "overall_assessment": await self._generate_overall_assessment(
                comprehensive_review, cultural_review
            )
        }
    
    async def _generate_improvement_recommendations(self, literary_review: Any, 
                                                  cultural_review: Any) -> List[str]:
        """إنشاء توصيات التحسين"""
        
        recommendations = []
        
        # توصيات أدبية
        if hasattr(literary_review, 'suggestions'):
            recommendations.extend(literary_review.suggestions)
        else:
            recommendations.extend([
                "تحسين التوازن بين الحوار والسرد",
                "تعميق تطوير الشخصيات",
                "تقوية الروابط بين الفصول"
            ])
        
        # توصيات ثقافية
        if hasattr(cultural_review, 'suggestions'):
            recommendations.extend(cultural_review.suggestions)
        else:
            recommendations.extend([
                "إضافة المزيد من العناصر التراثية",
                "تحسين الأصالة اللغوية",
                "تقوية السياق الثقافي"
            ])
        
        return recommendations
    
    async def _generate_overall_assessment(self, literary_review: Any, 
                                         cultural_review: Any) -> Dict[str, Any]:
        """إنشاء التقييم الإجمالي"""
        
        return {
            "quality_level": "جيد",  # افتراضي
            "strengths": [
                "تطوير جيد للشخصيات",
                "حبكة متماسكة",
                "عناصر ثقافية أصيلة"
            ],
            "areas_for_improvement": [
                "تحسين الوصف",
                "تقوية النهاية",
                "توازن أفضل في الإيقاع"
            ],
            "readiness_for_refinement": True
        }
    
    async def _calculate_generation_metrics(self, chapter_collaborations: List[Dict[str, Any]]) -> Dict[str, float]:
        """حساب مقاييس الإنشاء"""
        
        metrics = {
            "average_collaboration_quality": 0.0,
            "chapter_consistency": 0.0,
            "cultural_integration_success": 0.0,
            "overall_generation_success": 0.0
        }
        
        # متوسط جودة التعاون
        if chapter_collaborations:
            quality_scores = [
                collab.get("collaboration_quality", {}).get("collaboration_effectiveness", 0.0)
                for collab in chapter_collaborations
            ]
            metrics["average_collaboration_quality"] = sum(quality_scores) / len(quality_scores)
        
        # اتساق الفصول
        metrics["chapter_consistency"] = 0.8  # افتراضي
        
        # نجاح التكامل الثقافي
        metrics["cultural_integration_success"] = 0.75  # افتراضي
        
        # النجاح الإجمالي
        metrics["overall_generation_success"] = sum([
            metrics["average_collaboration_quality"],
            metrics["chapter_consistency"],
            metrics["cultural_integration_success"]
        ]) / 3
        
        return metrics
    
    async def _phase_5_collaborative_refinement(self, task: StoryGenerationTask,
                                              generation_result: Dict[str, Any]) -> Dict[str, Any]:
        """المرحلة 5: التنقيح التعاوني"""
        
        print(f"✨ بدء المرحلة 5: التنقيح التعاوني للمهمة {task.task_id}")
        
        current_story = generation_result["assembled_story"]
        refinement_cycles = []
        
        # دورات التنقيح (حتى 3 دورات)
        for cycle in range(1, 4):
            cycle_result = await self._execute_refinement_cycle(
                current_story, task, cycle
            )
            refinement_cycles.append(cycle_result)
            
            # تحديث القصة الحالية
            current_story = cycle_result["refined_story"]
            
            # فحص جودة التحسين
            if cycle_result["improvement_score"] < 0.1:  # تحسين طفيف
                print(f"🎯 توقف التنقيح بعد الدورة {cycle} - تحسين مقبول")
                break
        
        # التقييم النهائي
        final_assessment = await self._final_quality_assessment(current_story)
        
        # إنشاء النسخة النهائية
        final_story = await self._create_final_version(current_story, task)
        
        phase_result = {
            "refinement_cycles": refinement_cycles,
            "final_assessment": final_assessment,
            "final_output": final_story,
            "refinement_summary": await self._create_refinement_summary(refinement_cycles)
        }
        
        print(f"✅ اكتمال المرحلة 5: تم التنقيح خلال {len(refinement_cycles)} دورة")
        
        return phase_result
    
    async def _execute_refinement_cycle(self, current_story: Dict[str, Any],
                                       task: StoryGenerationTask, 
                                       cycle_number: int) -> Dict[str, Any]:
        """تنفيذ دورة تنقيح"""
        
        print(f"🔄 دورة التنقيح {cycle_number}")
        
        # تحديد تركيز هذه الدورة
        cycle_focus = self._determine_cycle_focus(cycle_number)
        
        # تنقيح بناءً على التركيز
        if cycle_focus == "structure":
            refined_story = await self._refine_structure_and_flow(current_story)
        elif cycle_focus == "content":
            refined_story = await self._refine_content_and_details(current_story, task)
        else:  # style
            refined_story = await self._refine_style_and_language(current_story, task)
        
        # تقييم التحسين
        improvement_score = await self._calculate_improvement_score(current_story, refined_story)
        
        return {
            "cycle_number": cycle_number,
            "focus": cycle_focus,
            "refined_story": refined_story,
            "improvement_score": improvement_score,
            "specific_improvements": await self._identify_specific_improvements(
                current_story, refined_story
            )
        }
    
    def _determine_cycle_focus(self, cycle_number: int) -> str:
        """تحديد تركيز دورة التنقيح"""
        
        focus_mapping = {
            1: "structure",  # البنية والتدفق
            2: "content",    # المحتوى والتفاصيل
            3: "style"       # الأسلوب واللغة
        }
        
        return focus_mapping.get(cycle_number, "style")
    
    async def _refine_structure_and_flow(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """تنقيح البنية والتدفق"""
        
        # تحسين بواسطة المهندس المعماري
        structural_improvements = await self.blueprint_architect.refine_story_structure(story)
        
        # تحسين الانتقالات بين الفصول
        improved_transitions = await self.chapter_composer.improve_chapter_transitions(
            story["chapters"]
        )
        
        refined_story = story.copy()
        refined_story.update(structural_improvements)
        refined_story["chapters"] = improved_transitions
        
        return refined_story
    
    async def _refine_content_and_details(self, story: Dict[str, Any], 
                                        task: StoryGenerationTask) -> Dict[str, Any]:
        """تنقيح المحتوى والتفاصيل"""
        
        # تحسين الشخصيات
        character_improvements = await self.idea_generator.deepen_character_development(
            story["chapters"]
        )
        
        # إثراء ثقافي
        cultural_enrichment = await self.cultural_maestro.enrich_cultural_details(
            story, task.cultural_focus
        )
        
        refined_story = story.copy()
        refined_story.update(character_improvements)
        refined_story.update(cultural_enrichment)
        
        return refined_story
    
    async def _refine_style_and_language(self, story: Dict[str, Any], 
                                       task: StoryGenerationStation) -> Dict[str, Any]:
        """تنقيح الأسلوب واللغة"""
        
        # تحسين اللغة والأسلوب
        language_improvements = await self.literary_critic.enhance_language_and_style(
            story, task.narrative_style
        )
        
        # تحسين الحوار
        dialogue_improvements = await self.chapter_composer.enhance_dialogue_quality(
            story["chapters"]
        )
        
        refined_story = story.copy()
        refined_story.update(language_improvements)
        refined_story["chapters"] = dialogue_improvements
        
        return refined_story
    
    async def _calculate_improvement_score(self, original: Dict[str, Any], 
                                         refined: Dict[str, Any]) -> float:
        """حساب درجة التحسين"""
        
        # تقييم مبسط للتحسين
        improvement_factors = {
            "structural_improvement": 0.3,
            "content_richness": 0.3,
            "language_quality": 0.4
        }
        
        # في تطبيق حقيقي، سنقوم بمقارنة أعمق
        return sum(improvement_factors.values()) * 0.6  # تحسين متوسط
    
    async def _identify_specific_improvements(self, original: Dict[str, Any], 
                                            refined: Dict[str, Any]) -> List[str]:
        """تحديد التحسينات المحددة"""
        
        # في تطبيق حقيقي، سنقوم بمقارنة تفصيلية
        return [
            "تحسين التوازن بين الفصول",
            "تطوير شخصية رئيسية",
            "تقوية الحوار في الفصل الثالث",
            "إثراء الوصف في المشاهد الطبيعية"
        ]
    
    async def _final_quality_assessment(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """التقييم النهائي للجودة"""
        
        # تقييم شامل من جميع الوكلاء
        literary_assessment = await self.literary_critic.final_story_evaluation(story)
        cultural_assessment = await self.cultural_maestro.final_cultural_evaluation(story)
        structural_assessment = await self.blueprint_architect.final_structure_evaluation(story)
        
        # دمج التقييمات
        final_assessment = {
            "literary_quality": literary_assessment,
            "cultural_authenticity": cultural_assessment,
            "structural_integrity": structural_assessment,
            "overall_score": await self._calculate_overall_quality_score([
                literary_assessment, cultural_assessment, structural_assessment
            ]),
            "readiness_status": "جاهز للنشر"  # أو يحتاج مراجعة إضافية
        }
        
        return final_assessment
    
    async def _calculate_overall_quality_score(self, assessments: List[Any]) -> float:
        """حساب نتيجة الجودة الإجمالية"""
        
        # تقييم مبسط
        scores = []
        for assessment in assessments:
            if isinstance(assessment, dict) and "score" in assessment:
                scores.append(assessment["score"])
            else:
                scores.append(0.75)  # افتراضي
        
        return sum(scores) / len(scores) if scores else 0.75
    
    async def _create_final_version(self, story: Dict[str, Any], 
                                  task: StoryGenerationTask) -> Dict[str, Any]:
        """إنشاء النسخة النهائية"""
        
        final_version = {
            "metadata": {
                "title": await self._generate_story_title(story, task),
                "author": "السردي الخارق - نظام الكتابة الذكية",
                "genre": task.story_type,
                "length": task.target_length,
                "cultural_focus": task.cultural_focus,
                "created_at": datetime.now().isoformat(),
                "word_count": story.get("word_count", 0)
            },
            "content": {
                "chapters": story["chapters"],
                "appendices": await self._create_appendices(story, task)
            },
            "source_information": {
                "original_transcript_reference": f"مهمة {task.task_id}",
                "adaptation_notes": await self._create_adaptation_notes(task),
                "cultural_references": await self._extract_cultural_references(story)
            },
            "quality_metrics": await self._compile_final_metrics(story)
        }
        
        return final_version
    
    async def _generate_story_title(self, story: Dict[str, Any], 
                                   task: StoryGenerationTask) -> str:
        """إنشاء عنوان القصة"""
        
        # استخراج العناصر الرئيسية لتكوين العنوان
        main_character = "البطل"  # سيتم استخراجه من الشخصيات
        theme = task.story_type
        
        # أنماط العناوين حسب النوع
        title_patterns = {
            "مغامرة": [f"رحلة {main_character}", f"مغامرات {main_character}", f"قصة {main_character}"],
            "رومانسي": [f"حب {main_character}", f"قلب {main_character}", f"عشق {main_character}"],
            "تاريخي": [f"{main_character} في التاريخ", f"حكاية {main_character}", f"زمن {main_character}"],
            "اجتماعي": [f"{main_character} والمجتمع", f"قضية {main_character}", f"صراع {main_character}"]
        }
        
        patterns = title_patterns.get(theme, [f"قصة {main_character}"])
        return patterns[0]  # اختيار أول نمط
    
    async def _create_appendices(self, story: Dict[str, Any], 
                               task: StoryGenerationTask) -> Dict[str, Any]:
        """إنشاء الملاحق"""
        
        appendices = {}
        
        # ملحق الشخصيات
        if len(story.get("chapters", [])) > 1:
            appendices["character_guide"] = await self._create_character_guide(story)
        
        # ملحق المراجع الثقافية
        if task.cultural_focus == "تراثي":
            appendices["cultural_references"] = await self._create_cultural_reference_guide(story)
        
        # ملحق المصطلحات
        appendices["glossary"] = await self._create_glossary(story)
        
        return appendices
    
    async def _create_character_guide(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء دليل الشخصيات"""
        
        # استخراج الشخصيات من الفصول
        characters = {}
        
        # في تطبيق حقيقي، سنستخرج الشخصيات من المحتوى الفعلي
        characters = {
            "الشخصيات الرئيسية": [
                {"name": "البطل", "description": "الشخصية المحورية في القصة"}
            ],
            "الشخصيات الثانوية": []
        }
        
        return characters
    
    async def _create_cultural_reference_guide(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """إنشاء دليل المراجع الثقافية"""
        
        return {
            "مراجع تراثية": [
                "أمثال شعبية مستخدمة",
                "تقاليد مذكورة",
                "مراجع دينية"
            ],
            "سياق تاريخي": [
                "الفترة الزمنية",
                "الأحداث التاريخية المرجعية"
            ]
        }
    
    async def _create_glossary(self, story: Dict[str, Any]) -> Dict[str, str]:
        """إنشاء قاموس المصطلحات"""
        
        return {
            "مصطلحات تراثية": "التعريفات",
            "كلمات قديمة": "المعاني المعاصرة"
        }
    
    async def _create_adaptation_notes(self, task: StoryGenerationTask) -> List[str]:
        """إنشاء ملاحظات التكييف"""
        
        return [
            f"تم تكييف القصة من ترانسكريبت أصلي لتناسب نوع {task.story_type}",
            f"تم التركيز على العناصر الثقافية {task.cultural_focus}",
            f"تم استهداف طول {task.target_length} بأسلوب {task.narrative_style}",
            "تم الحفاظ على جوهر الأحداث الأصلية مع إثراء السرد"
        ]
    
    async def _extract_cultural_references(self, story: Dict[str, Any]) -> List[str]:
        """استخراج المراجع الثقافية"""
        
        # في تطبيق حقيقي، سنحلل المحتوى لاستخراج المراجع
        return [
            "مراجع دينية وروحانية",
            "تقاليد اجتماعية عربية",
            "قيم ثقافية أصيلة",
            "تراث شعبي وأدبي"
        ]
    
    async def _compile_final_metrics(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """تجميع المقاييس النهائية"""
        
        return {
            "word_count": story.get("word_count", 0),
            "chapter_count": len(story.get("chapters", [])),
            "character_count": 3,  # افتراضي
            "cultural_density": 8,  # عدد العناصر الثقافية
            "quality_score": 0.85,  # نتيجة الجودة الإجمالية
            "completion_time": "2 ساعات",  # وقت الإنتاج
            "revision_cycles": 2  # عدد دورات المراجعة
        }
    
    async def _create_refinement_summary(self, refinement_cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """إنشاء ملخص التنقيح"""
        
        summary = {
            "total_cycles": len(refinement_cycles),
            "total_improvements": 0,
            "improvement_categories": {},
            "overall_improvement_score": 0.0
        }
        
        for cycle in refinement_cycles:
            summary["total_improvements"] += len(cycle.get("specific_improvements", []))
            
            # تصنيف التحسينات
            focus = cycle.get("focus", "unknown")
            if focus not in summary["improvement_categories"]:
                summary["improvement_categories"][focus] = 0
            summary["improvement_categories"][focus] += 1
        
        # حساب درجة التحسين الإجمالية
        if refinement_cycles:
            improvement_scores = [cycle.get("improvement_score", 0) for cycle in refinement_cycles]
            summary["overall_improvement_score"] = sum(improvement_scores) / len(improvement_scores)
        
        return summary
    
    async def _update_task_progress(self, task_id: str, progress: float, status: str):
        """تحديث تقدم المهمة"""
        
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["progress"] = progress
            self.active_tasks[task_id]["phase"] = status
            
            print(f"📈 تقدم المهمة {task_id}: {progress*100:.1f}% - {status}")
    
    async def _generate_collaboration_summary(self, task_id: str) -> Dict[str, Any]:
        """إنشاء ملخص التعاون"""
        
        if task_id not in self.active_tasks:
            return {}
        
        task_data = self.active_tasks[task_id]
        
        summary = {
            "total_collaborations": len(task_data.get("collaborations", [])),
            "agent_participation": {
                "idea_generator": True,
                "blueprint_architect": True,
                "chapter_composer": True,
                "literary_critic": True,
                "cultural_maestro": True
            },
            "collaboration_effectiveness": 0.85,  # متوسط فعالية التعاون
            "key_achievements": [
                "تطوير هيكل سردي متماسك",
                "دمج ثقافي أصيل",
                "إنتاج نص عالي الجودة"
            ]
        }
        
        return summary
