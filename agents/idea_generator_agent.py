"""
وكيل توليد الأفكار - متخصص في إبداع وتطوير الأفكار الأدبية
يقوم بتوليد أفكار إبداعية للروايات والقصص والشخصيات
"""

import asyncio
import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentState, MessageType
from ..llm_service import call_llm, create_idea_generation_prompt, get_best_model_for_task
from ..tools.text_processing_tools import TextProcessor
from ..tools.analysis_tools import CreativityAnalyzer

logger = logging.getLogger(__name__)

class IdeaGeneratorAgent(BaseAgent):
    """وكيل توليد الأفكار الإبداعية"""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            name="مولد الأفكار الإبداعي",
            persona="""أنا مفكر إبداعي متخصص في توليد الأفكار الأدبية المبتكرة.
            أتمتع بخيال واسع وقدرة على ربط المفاهيم المختلفة لإنتاج أفكار جديدة ومثيرة.
            أستطيع تطوير أفكار من نقطة بداية بسيطة إلى مفاهيم معقدة ومتماسكة.
            أركز على الأصالة والابتكار مع احترام التراث الأدبي العربي.""",
            goals=[
                "توليد أفكار إبداعية ومبتكرة للروايات",
                "تطوير مفاهيم الشخصيات والحبكات",
                "إنشاء عوالم خيالية مقنعة",
                "ربط الأفكار التراثية بالمعاصرة",
                "تقديم حلول إبداعية للتحديات الأدبية"
            ],
            tools=[
                "creative_thinking",
                "idea_generation",
                "concept_development",
                "brainstorming",
                "inspiration_synthesis",
                "creativity_assessment",
                "trend_analysis"
            ],
            agent_id=agent_id
        )
        
        # أدوات متخصصة
        self.text_processor = TextProcessor()
        self.creativity_analyzer = CreativityAnalyzer()
        
        # بنك الأفكار والإلهام
        self.inspiration_sources = {
            "cultural": ["التراث العربي", "الأساطير", "التاريخ الإسلامي", "الفولكلور"],
            "modern": ["التكنولوجيا", "القضايا المعاصرة", "العولمة", "وسائل التواصل"],
            "universal": ["الحب", "الصداقة", "البحث عن الذات", "الصراع بين الخير والشر"],
            "experimental": ["الواقعية السحرية", "الخيال العلمي", "التجريب السردي"]
        }
        
        # أنماط الأفكار
        self.idea_patterns = {
            "character_driven": "قصة تركز على تطور الشخصية",
            "plot_driven": "قصة تركز على الأحداث والمغامرة",
            "theme_driven": "قصة تركز على موضوع أو فكرة فلسفية",
            "setting_driven": "قصة تركز على العالم والبيئة",
            "hybrid": "مزيج من عدة أنماط"
        }
        
        # مستويات الإبداع
        self.creativity_levels = {
            "safe": "أفكار مألوفة ومقبولة",
            "moderate": "أفكار مبتكرة نسبياً",
            "bold": "أفكار جريئة ومختلفة",
            "experimental": "أفكار تجريبية متقدمة"
        }
        
        logger.info("تم إنشاء وكيل توليد الأفكار بنجاح")
    
    def get_capabilities(self) -> List[str]:
        """إرجاع قدرات الوكيل"""
        return [
            "story_idea_generation",
            "character_creation",
            "plot_development",
            "world_building",
            "theme_exploration",
            "conflict_design",
            "creative_brainstorming",
            "concept_refinement",
            "inspiration_synthesis",
            "trend_integration"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة مهمة توليد الأفكار"""
        try:
            self.update_state(AgentState.WORKING)
            start_time = datetime.now()
            
            task_type = task.get("type", "general_ideas")
            seed_content = task.get("seed", "")
            generation_options = task.get("options", {})
            
            # حفظ السياق
            self.memory.add_to_context({
                "task_type": task_type,
                "seed_content": seed_content,
                "generation_options": generation_options
            })
            
            result = {}
            
            if task_type == "story_ideas":
                result = await self._generate_story_ideas(seed_content, generation_options)
            elif task_type == "character_ideas":
                result = await self._generate_character_ideas(seed_content, generation_options)
            elif task_type == "plot_twists":
                result = await self._generate_plot_twists(seed_content, generation_options)
            elif task_type == "world_building":
                result = await self._generate_world_concepts(seed_content, generation_options)
            elif task_type == "theme_exploration":
                result = await self._explore_themes(seed_content, generation_options)
            elif task_type == "brainstorming":
                result = await self._creative_brainstorming(seed_content, generation_options)
            elif task_type == "idea_expansion":
                result = await self._expand_idea(seed_content, generation_options)
            elif task_type == "conflict_generation":
                result = await self._generate_conflicts(seed_content, generation_options)
            else:
                result = await self._generate_general_ideas(seed_content, generation_options)
            
            # حساب الوقت المستغرق
            processing_time = (datetime.now() - start_time).total_seconds()
            result["processing_time"] = processing_time
            result["generation_timestamp"] = datetime.now().isoformat()
            result["generator_version"] = "1.0"
            
            # تقييم الإبداع
            creativity_score = await self._assess_creativity(result)
            result["creativity_assessment"] = creativity_score
            
            # تحديث المقاييس
            self.learn_from_interaction({
                "task_type": task_type,
                "response_time": processing_time,
                "creativity_score": creativity_score.get("overall_score", 0),
                "success": True
            })
            
            self.update_state(AgentState.COMPLETED)
            logger.info(f"تم إكمال توليد الأفكار في {processing_time:.2f} ثانية")
            
            return result
            
        except Exception as e:
            self.update_state(AgentState.ERROR)
            logger.error(f"خطأ في توليد الأفكار: {str(e)}")
            return {
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _generate_story_ideas(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توليد أفكار القصص"""
        logger.info("بدء توليد أفكار القصص")
        
        count = options.get("count", 5)
        creativity_level = options.get("creativity", "moderate")
        genre = options.get("genre", "عام")
        target_audience = options.get("audience", "عام")
        
        # تحضير prompt متخصص
        generation_prompt = await self._create_story_generation_prompt(
            seed, creativity_level, genre, target_audience
        )
        
        # استخدام نموذج مناسب للإبداع
        model = get_best_model_for_task("creative_writing")
        llm_ideas = await call_llm(generation_prompt, model=model)
        
        # توليد أفكار إضافية بطرق مختلفة
        pattern_ideas = await self._generate_pattern_based_ideas(seed, count)
        hybrid_ideas = await self._generate_hybrid_ideas(seed, count)
        cultural_ideas = await self._generate_cultural_ideas(seed, count)
        
        # تنسيق وتنظيم الأفكار
        all_ideas = await self._organize_story_ideas([
            llm_ideas,
            pattern_ideas,
            hybrid_ideas,
            cultural_ideas
        ])
        
        return {
            "status": "success",
            "type": "story_ideas",
            "ideas": all_ideas[:count],
            "generation_method": "multi_approach",
            "creativity_level": creativity_level,
            "genre": genre,
            "additional_concepts": await self._generate_supporting_concepts(all_ideas[:count])
        }
    
    async def _generate_character_ideas(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توليد أفكار الشخصيات"""
        logger.info("بدء توليد أفكار الشخصيات")
        
        count = options.get("count", 3)
        character_type = options.get("type", "متنوع")
        depth_level = options.get("depth", "detailed")
        
        characters = []
        
        for i in range(count):
            character = await self._create_character_concept(seed, character_type, depth_level)
            characters.append(character)
        
        # تحليل التوافق بين الشخصيات
        compatibility = await self._analyze_character_compatibility(characters)
        
        return {
            "status": "success",
            "type": "character_ideas",
            "characters": characters,
            "character_dynamics": compatibility,
            "ensemble_potential": await self._assess_ensemble_potential(characters)
        }
    
    async def _generate_plot_twists(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توليد المفاجآت والانعطافات في الحبكة"""
        logger.info("بدء توليد المفاجآت في الحبكة")
        
        count = options.get("count", 5)
        intensity = options.get("intensity", "medium")
        
        twist_types = [
            "identity_revelation",
            "hidden_connection",
            "false_assumption",
            "time_manipulation",
            "moral_reversal",
            "power_shift",
            "sacrifice_twist"
        ]
        
        twists = []
        for twist_type in random.sample(twist_types, min(count, len(twist_types))):
            twist = await self._generate_specific_twist(seed, twist_type, intensity)
            twists.append(twist)
        
        return {
            "status": "success",
            "type": "plot_twists",
            "twists": twists,
            "implementation_tips": await self._generate_twist_implementation_tips(twists)
        }
    
    async def _generate_world_concepts(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توليد مفاهيم بناء العالم"""
        logger.info("بدء توليد مفاهيم العالم")
        
        scope = options.get("scope", "comprehensive")
        genre = options.get("genre", "realistic")
        
        world_elements = {
            "setting": await self._create_setting_concept(seed, genre),
            "society": await self._create_society_concept(seed, genre),
            "culture": await self._create_culture_concept(seed, genre),
            "history": await self._create_history_concept(seed, genre),
            "rules": await self._create_world_rules(seed, genre),
            "conflicts": await self._create_world_conflicts(seed, genre)
        }
        
        return {
            "status": "success",
            "type": "world_building",
            "world_elements": world_elements,
            "coherence_check": await self._check_world_coherence(world_elements),
            "expansion_opportunities": await self._identify_expansion_opportunities(world_elements)
        }
    
    async def _explore_themes(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """استكشاف الموضوعات والثيمات"""
        logger.info("بدء استكشاف الموضوعات")
        
        depth = options.get("depth", "moderate")
        perspective = options.get("perspective", "balanced")
        
        # استكشاف موضوعات متعددة المستويات
        themes = {
            "primary": await self._identify_primary_themes(seed),
            "secondary": await self._identify_secondary_themes(seed),
            "symbolic": await self._identify_symbolic_themes(seed),
            "universal": await self._identify_universal_themes(seed),
            "cultural": await self._identify_cultural_themes(seed)
        }
        
        # تطوير المعالجة الموضوعية
        thematic_treatment = await self._develop_thematic_treatment(themes, perspective)
        
        return {
            "status": "success",
            "type": "theme_exploration",
            "themes": themes,
            "thematic_treatment": thematic_treatment,
            "integration_strategies": await self._suggest_theme_integration(themes)
        }
    
    async def _creative_brainstorming(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """جلسة عصف ذهني إبداعي"""
        logger.info("بدء جلسة العصف الذهني الإبداعي")
        
        session_type = options.get("session_type", "open")
        time_limit = options.get("time_limit", 300)  # 5 دقائق
        
        # تقنيات العصف الذهني المختلفة
        brainstorm_results = await asyncio.gather(
            self._word_association_brainstorm(seed),
            self._perspective_shift_brainstorm(seed),
            self._random_stimulus_brainstorm(seed),
            self._constraint_based_brainstorm(seed),
            self._cultural_fusion_brainstorm(seed)
        )
        
        # تجميع وتنظيم النتائج
        organized_ideas = await self._organize_brainstorm_results(brainstorm_results)
        
        return {
            "status": "success",
            "type": "brainstorming",
            "session_results": organized_ideas,
            "breakthrough_ideas": await self._identify_breakthrough_ideas(organized_ideas),
            "development_priorities": await self._prioritize_ideas(organized_ideas)
        }
    
    async def _expand_idea(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توسيع وتطوير فكرة موجودة"""
        logger.info("بدء توسيع الفكرة")
        
        expansion_method = options.get("method", "comprehensive")
        detail_level = options.get("detail", "high")
        
        expansion = {
            "core_concept": await self._analyze_core_concept(seed),
            "extensions": await self._generate_extensions(seed),
            "variations": await self._create_variations(seed),
            "complications": await self._add_complications(seed),
            "subplots": await self._develop_subplots(seed),
            "implications": await self._explore_implications(seed)
        }
        
        return {
            "status": "success",
            "type": "idea_expansion",
            "expansion": expansion,
            "development_roadmap": await self._create_development_roadmap(expansion)
        }
    
    async def _generate_conflicts(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توليد الصراعات والتوترات"""
        logger.info("بدء توليد الصراعات")
        
        conflict_types = options.get("types", ["internal", "interpersonal", "social", "environmental"])
        intensity = options.get("intensity", "medium")
        
        conflicts = {}
        for conflict_type in conflict_types:
            conflicts[conflict_type] = await self._create_conflict(seed, conflict_type, intensity)
        
        # تحليل التفاعلات بين الصراعات
        conflict_dynamics = await self._analyze_conflict_dynamics(conflicts)
        
        return {
            "status": "success",
            "type": "conflict_generation",
            "conflicts": conflicts,
            "conflict_dynamics": conflict_dynamics,
            "resolution_possibilities": await self._suggest_conflict_resolutions(conflicts)
        }
    
    async def _generate_general_ideas(self, seed: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توليد أفكار عامة"""
        logger.info("بدء توليد الأفكار العامة")
        
        # مجموعة متنوعة من الأفكار
        ideas = {
            "story_concepts": await self._generate_quick_story_concepts(seed, 3),
            "character_seeds": await self._generate_character_seeds(seed, 3),
            "setting_ideas": await self._generate_setting_ideas(seed, 3),
            "theme_suggestions": await self._generate_theme_suggestions(seed, 3),
            "creative_exercises": await self._suggest_creative_exercises(seed)
        }
        
        return {
            "status": "success",
            "type": "general_ideas",
            "ideas": ideas,
            "inspiration_sources": await self._recommend_inspiration_sources(seed)
        }
    
    # دوال مساعدة متخصصة
    
    async def _create_story_generation_prompt(self, seed: str, creativity: str, genre: str, audience: str) -> str:
        """إنشاء prompt لتوليد القصص"""
        creativity_instructions = {
            "safe": "أفكار مألوفة ومقبولة اجتماعياً",
            "moderate": "أفكار مبتكرة مع احترام التقاليد",
            "bold": "أفكار جريئة ومختلفة",
            "experimental": "أفكار تجريبية ومتقدمة"
        }
        
        return f"""
        قم بتوليد أفكار إبداعية للقصص بناءً على: {seed}
        
        المتطلبات:
        - النوع الأدبي: {genre}
        - الجمهور المستهدف: {audience}
        - مستوى الإبداع: {creativity_instructions.get(creativity, 'متوسط')}
        - أن تكون الأفكار أصيلة ومبتكرة
        - أن تحترم الثقافة العربية والإسلامية
        - أن تكون قابلة للتطوير إلى رواية كاملة
        
        اقترح 5 أفكار متنوعة مع شرح موجز لكل فكرة.
        """
    
    async def _generate_pattern_based_ideas(self, seed: str, count: int) -> List[Dict[str, Any]]:
        """توليد أفكار مبنية على أنماط أدبية"""
        ideas = []
        patterns = list(self.idea_patterns.keys())
        
        for i in range(min(count, len(patterns))):
            pattern = patterns[i]
            idea = {
                "title": f"فكرة مبنية على نمط {pattern}",
                "pattern": self.idea_patterns[pattern],
                "concept": f"تطوير {seed} باستخدام {pattern}",
                "approach": pattern
            }
            ideas.append(idea)
        
        return ideas
    
    async def _generate_hybrid_ideas(self, seed: str, count: int) -> List[Dict[str, Any]]:
        """توليد أفكار مهجنة من مصادر متعددة"""
        ideas = []
        sources = list(self.inspiration_sources.keys())
        
        for i in range(count):
            # دمج مصدرين عشوائيين
            source1, source2 = random.sample(sources, 2)
            elements1 = random.choice(self.inspiration_sources[source1])
            elements2 = random.choice(self.inspiration_sources[source2])
            
            idea = {
                "title": f"فكرة مهجنة: {elements1} × {elements2}",
                "fusion": f"دمج {elements1} مع {elements2}",
                "seed_integration": f"تطبيق على {seed}",
                "innovation_potential": "عالي"
            }
            ideas.append(idea)
        
        return ideas
    
    async def _generate_cultural_ideas(self, seed: str, count: int) -> List[Dict[str, Any]]:
        """توليد أفكار مستوحاة من الثقافة العربية"""
        cultural_elements = self.inspiration_sources["cultural"]
        ideas = []
        
        for i in range(count):
            element = random.choice(cultural_elements)
            idea = {
                "title": f"فكرة مستوحاة من {element}",
                "cultural_root": element,
                "modern_adaptation": f"تحديث {element} في سياق {seed}",
                "authenticity_level": "عالي"
            }
            ideas.append(idea)
        
        return ideas
    
    async def _organize_story_ideas(self, idea_groups: List[Any]) -> List[Dict[str, Any]]:
        """تنظيم وتصنيف أفكار القصص"""
        organized = []
        
        # معالجة كل مجموعة أفكار
        for group in idea_groups:
            if isinstance(group, list):
                organized.extend(group)
            elif isinstance(group, str):
                # معالجة نتائج LLM
                organized.append({
                    "title": "فكرة من الذكاء الاصطناعي",
                    "content": group,
                    "source": "llm_generation"
                })
        
        return organized
    
    async def _assess_creativity(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """تقييم مستوى الإبداع في النتائج"""
        # تقييم مبسط - يمكن تطويره
        creativity_metrics = {
            "originality": random.uniform(6, 9),
            "feasibility": random.uniform(7, 9),
            "engagement": random.uniform(6, 9),
            "cultural_relevance": random.uniform(7, 10)
        }
        
        overall_score = sum(creativity_metrics.values()) / len(creativity_metrics)
        
        return {
            "overall_score": overall_score,
            "metrics": creativity_metrics,
            "assessment": "مبدع" if overall_score > 8 else "جيد" if overall_score > 6 else "متوسط"
        }
    
    # المزيد من الدوال المساعدة (مبسطة للمثال)
    
    async def _create_character_concept(self, seed: str, char_type: str, depth: str) -> Dict[str, Any]:
        """إنشاء مفهوم شخصية"""
        return {
            "name": "شخصية جديدة",
            "type": char_type,
            "background": f"خلفية مرتبطة بـ {seed}",
            "motivation": "دافع قوي للعمل",
            "conflict": "صراع داخلي أو خارجي",
            "depth_level": depth
        }
    
    async def _analyze_character_compatibility(self, characters: List[Dict]) -> Dict[str, Any]:
        """تحليل التوافق بين الشخصيات"""
        return {"compatibility_score": 8.5, "potential_conflicts": ["تضارب الأهداف"]}
    
    async def _generate_specific_twist(self, seed: str, twist_type: str, intensity: str) -> Dict[str, Any]:
        """توليد مفاجأة محددة"""
        return {
            "type": twist_type,
            "description": f"مفاجأة من نوع {twist_type}",
            "intensity": intensity,
            "timing_suggestions": ["الثلث الثاني", "قبل النهاية"]
        }
    
    # ... المزيد من الدوال المساعدة
    
    def get_idea_bank(self) -> Dict[str, Any]:
        """الحصول على بنك الأفكار المتاح"""
        return {
            "inspiration_sources": self.inspiration_sources,
            "idea_patterns": self.idea_patterns,
            "creativity_levels": self.creativity_levels,
            "generated_ideas_count": self.performance_metrics["tasks_completed"]
        }
    
    def add_inspiration_source(self, category: str, sources: List[str]):
        """إضافة مصادر إلهام جديدة"""
        if category not in self.inspiration_sources:
            self.inspiration_sources[category] = []
        self.inspiration_sources[category].extend(sources)
        logger.info(f"تم إضافة مصادر إلهام جديدة في فئة {category}")
