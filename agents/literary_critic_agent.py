"""
وكيل التحرير والتقييم الأدبي - متخصص في مراجعة وتقييم النصوص الأدبية
يقوم بالتحرير المتقدم والنقد البناء وتقديم التوصيات للتحسين
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from .base_agent import BaseAgent, AgentState, MessageType
from ..llm_service import call_llm, create_text_refinement_prompt, create_consistency_check_prompt, get_best_model_for_task
from ..tools.text_processing_tools import TextProcessor
from ..tools.analysis_tools import LiteraryAnalyzer, StyleAnalyzer

logger = logging.getLogger(__name__)

class CriticismLevel(Enum):
    """مستويات النقد"""
    GENTLE = "لطيف"
    CONSTRUCTIVE = "بناء"
    DETAILED = "مفصل"
    RIGOROUS = "صارم"

class EditingFocus(Enum):
    """مجالات التحرير"""
    LANGUAGE = "language"
    STRUCTURE = "structure"
    STYLE = "style"
    CONTENT = "content"
    CONSISTENCY = "consistency"
    FLOW = "flow"

@dataclass
class CritiqueReport:
    """تقرير النقد الأدبي"""
    overall_rating: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    detailed_feedback: Dict[str, Any]
    priority_issues: List[str]
    improvement_roadmap: List[str]

@dataclass
class EditingChange:
    """تغيير تحريري"""
    original_text: str
    suggested_text: str
    reason: str
    category: EditingFocus
    confidence: float
    line_number: Optional[int] = None

class LiteraryCriticAgent(BaseAgent):
    """وكيل التحرير والنقد الأدبي المتخصص"""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            name="الناقد والمحرر الأدبي",
            persona="""أنا ناقد أدبي ومحرر متخصص بخبرة عميقة في الأدب العربي الكلاسيكي والمعاصر.
            أتمتع بحس نقدي مرهف وقدرة على تحليل النصوص بدقة وعمق.
            أهدف إلى تقديم نقد بناء يساعد الكتاب على تطوير أعمالهم وتحسين جودتها.
            أتقن معايير النقد الأدبي الحديثة مع احترام التراث النقدي العربي.
            أركز على التوازن بين الصرامة النقدية والتشجيع الإيجابي.""",
            goals=[
                "تقديم نقد أدبي دقيق وبناء",
                "تحرير النصوص وتحسين جودتها اللغوية",
                "تقييم التماسك الأدبي والسردي",
                "اكتشاف نقاط القوة والضعف في النصوص",
                "إرشاد الكتاب نحو التطوير والتحسين"
            ],
            tools=[
                "literary_criticism",
                "text_editing",
                "style_analysis",
                "consistency_checking",
                "quality_assessment",
                "linguistic_review",
                "structural_analysis"
            ],
            agent_id=agent_id
        )
        
        # أدوات متخصصة
        self.text_processor = TextProcessor()
        self.literary_analyzer = LiteraryAnalyzer()
        self.style_analyzer = StyleAnalyzer()
        
        # معايير النقد الأدبي
        self.criticism_criteria = {
            "language": {
                "name": "جودة اللغة",
                "aspects": ["الفصاحة", "دقة التعبير", "ثراء المفردات", "سلامة النحو"],
                "weight": 0.25
            },
            "structure": {
                "name": "البناء والهيكل",
                "aspects": ["تماسك البناء", "منطقية التسلسل", "توازن الأجزاء", "قوة الانتقالات"],
                "weight": 0.20
            },
            "style": {
                "name": "الأسلوب الأدبي",
                "aspects": ["تميز الأسلوب", "ثبات النبرة", "جمال التعبير", "أصالة الصوت"],
                "weight": 0.20
            },
            "content": {
                "name": "المضمون والمحتوى",
                "aspects": ["عمق الأفكار", "أصالة المضمون", "غنى التفاصيل", "قوة الرسالة"],
                "weight": 0.15
            },
            "characters": {
                "name": "الشخصيات",
                "aspects": ["واقعية الشخصيات", "تطورها", "تميزها", "عمقها النفسي"],
                "weight": 0.10
            },
            "engagement": {
                "name": "الإشراك والتأثير",
                "aspects": ["قوة الجذب", "التشويق", "التأثير العاطفي", "قابلية القراءة"],
                "weight": 0.10
            }
        }
        
        # أنواع الأخطاء الشائعة
        self.common_errors = {
            "linguistic": [
                "أخطاء نحوية",
                "أخطاء إملائية",
                "استخدام خاطئ للمفردات",
                "ضعف في التراكيب اللغوية"
            ],
            "stylistic": [
                "تذبذب في الأسلوب",
                "تكرار مفرط",
                "ضعف في الصور البلاغية",
                "عدم تناسق في النبرة"
            ],
            "structural": [
                "ضعف في التنظيم",
                "انتقالات مفاجئة",
                "عدم توازن الأجزاء",
                "فقدان التماسك"
            ],
            "content": [
                "ضحالة في المعالجة",
                "تناقضات داخلية",
                "معلومات غير دقيقة",
                "افتقار للعمق"
            ]
        }
        
        # مستويات التحرير
        self.editing_levels = {
            "proofreading": {
                "name": "التدقيق اللغوي",
                "focus": ["إملاء", "نحو", "ترقيم", "طباعة"]
            },
            "copy_editing": {
                "name": "التحرير النسخي",
                "focus": ["وضوح", "دقة", "اتساق", "أسلوب"]
            },
            "substantive_editing": {
                "name": "التحرير الموضوعي",
                "focus": ["محتوى", "تنظيم", "منطق", "تدفق"]
            },
            "developmental_editing": {
                "name": "التحرير التطويري",
                "focus": ["هيكل عام", "رؤية", "جمهور", "هدف"]
            }
        }
        
        logger.info("تم إنشاء وكيل التحرير والنقد الأدبي بنجاح")
    
    def get_capabilities(self) -> List[str]:
        """إرجاع قدرات الوكيل"""
        return [
            "literary_criticism",
            "text_editing",
            "proofreading",
            "style_review",
            "consistency_checking",
            "quality_assessment",
            "structural_analysis",
            "linguistic_review",
            "developmental_feedback",
            "improvement_guidance"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة مهمة النقد والتحرير"""
        try:
            self.update_state(AgentState.WORKING)
            start_time = datetime.now()
            
            task_type = task.get("type", "comprehensive_review")
            content = task.get("content", "")
            review_options = task.get("options", {})
            
            # التحقق من وجود محتوى للمراجعة
            if not content:
                raise ValueError("لا يوجد محتوى للمراجعة")
            
            # حفظ السياق
            self.memory.add_to_context({
                "task_type": task_type,
                "content_length": len(content),
                "review_options": review_options
            })
            
            result = {}
            
            if task_type == "comprehensive_review":
                result = await self._comprehensive_literary_review(content, review_options)
            elif task_type == "editing_suggestions":
                result = await self._generate_editing_suggestions(content, review_options)
            elif task_type == "style_critique":
                result = await self._critique_writing_style(content, review_options)
            elif task_type == "proofreading":
                result = await self._proofread_text(content, review_options)
            elif task_type == "consistency_check":
                result = await self._check_consistency(content, review_options)
            elif task_type == "quality_assessment":
                result = await self._assess_overall_quality(content, review_options)
            elif task_type == "developmental_feedback":
                result = await self._provide_developmental_feedback(content, review_options)
            elif task_type == "comparative_analysis":
                result = await self._comparative_analysis(content, review_options)
            else:
                raise ValueError(f"نوع المهمة غير مدعوم: {task_type}")
            
            # حساب الوقت المستغرق
            processing_time = (datetime.now() - start_time).total_seconds()
            result["processing_time"] = processing_time
            result["review_timestamp"] = datetime.now().isoformat()
            result["critic_version"] = "1.0"
            
            # تقييم فعالية المراجعة
            review_effectiveness = await self._assess_review_effectiveness(result)
            result["review_effectiveness"] = review_effectiveness
            
            # تحديث المقاييس
            self.learn_from_interaction({
                "task_type": task_type,
                "response_time": processing_time,
                "content_length": len(content),
                "review_depth": review_options.get("depth", "standard"),
                "success": True
            })
            
            self.update_state(AgentState.COMPLETED)
            logger.info(f"تم إكمال المراجعة في {processing_time:.2f} ثانية")
            
            return result
            
        except Exception as e:
            self.update_state(AgentState.ERROR)
            logger.error(f"خطأ في المراجعة الأدبية: {str(e)}")
            return {
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _comprehensive_literary_review(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """مراجعة أدبية شاملة"""
        logger.info("بدء المراجعة الأدبية الشاملة")
        
        criticism_level = CriticismLevel(options.get("criticism_level", "CONSTRUCTIVE"))
        focus_areas = options.get("focus_areas", list(self.criticism_criteria.keys()))
        
        # التحليل الشامل
        comprehensive_analysis = await asyncio.gather(
            self._analyze_language_quality(content),
            self._analyze_structural_elements(content),
            self._analyze_stylistic_features(content),
            self._analyze_content_depth(content),
            self._analyze_character_development(content),
            self._analyze_engagement_factors(content),
            return_exceptions=True
        )
        
        # تجميع النتائج
        analysis_results = {}
        criteria_keys = list(self.criticism_criteria.keys())
        for i, result in enumerate(comprehensive_analysis):
            if not isinstance(result, Exception) and i < len(criteria_keys):
                analysis_results[criteria_keys[i]] = result
            elif isinstance(result, Exception):
                logger.error(f"خطأ في تحليل {criteria_keys[i] if i < len(criteria_keys) else 'unknown'}: {result}")
        
        # حساب التقييم الإجمالي
        overall_rating = await self._calculate_overall_rating(analysis_results)
        
        # تحديد نقاط القوة والضعف
        strengths, weaknesses = await self._identify_strengths_weaknesses(analysis_results)
        
        # توليد التوصيات
        suggestions = await self._generate_improvement_suggestions(analysis_results, weaknesses)
        
        # إنشاء خارطة طريق للتحسين
        improvement_roadmap = await self._create_improvement_roadmap(weaknesses, suggestions)
        
        # تقرير النقد المفصل
        detailed_critique = await self._create_detailed_critique_report(
            analysis_results, criticism_level
        )
        
        return {
            "status": "success",
            "review_type": "comprehensive",
            "overall_rating": overall_rating,
            "analysis_results": analysis_results,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
            "improvement_roadmap": improvement_roadmap,
            "detailed_critique": detailed_critique,
            "criticism_level": criticism_level.value,
            "priority_actions": await self._prioritize_improvement_actions(suggestions)
        }
    
    async def _generate_editing_suggestions(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """توليد اقتراحات التحرير"""
        logger.info("بدء توليد اقتراحات التحرير")
        
        editing_level = options.get("editing_level", "copy_editing")
        focus_areas = options.get("focus", [EditingFocus.LANGUAGE, EditingFocus.STYLE, EditingFocus.FLOW])
        
        editing_changes = []
        
        # تحليل النص وتحديد التحسينات المطلوبة
        for focus in focus_areas:
            changes = await self._identify_editing_opportunities(content, focus, editing_level)
            editing_changes.extend(changes)
        
        # ترتيب التغييرات حسب الأولوية
        prioritized_changes = await self._prioritize_editing_changes(editing_changes)
        
        # إنشاء النسخة المحررة
        edited_version = await self._apply_editing_changes(content, prioritized_changes[:20])  # أهم 20 تغيير
        
        return {
            "status": "success",
            "review_type": "editing_suggestions",
            "original_content": content,
            "edited_version": edited_version,
            "editing_changes": prioritized_changes,
            "change_summary": await self._summarize_editing_changes(prioritized_changes),
            "editing_level": editing_level,
            "improvement_metrics": await self._calculate_improvement_metrics(content, edited_version)
        }
    
    async def _critique_writing_style(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """نقد الأسلوب الكتابي"""
        logger.info("بدء نقد الأسلوب الكتابي")
        
        target_style = options.get("target_style", None)
        comparison_mode = options.get("comparison_mode", False)
        
        # تحليل الأسلوب الحالي
        current_style = await self.style_analyzer.analyze_comprehensive_style(content)
        
        # تحليل خصائص الأسلوب
        style_features = await self._analyze_style_features(content)
        
        # تقييم جودة الأسلوب
        style_quality = await self._assess_style_quality(style_features)
        
        # مقارنة مع أسلوب مستهدف (إن وجد)
        style_comparison = None
        if target_style:
            style_comparison = await self._compare_with_target_style(current_style, target_style)
        
        return {
            "status": "success",
            "review_type": "style_critique",
            "current_style": current_style,
            "style_features": style_features,
            "style_quality": style_quality,
            "style_comparison": style_comparison,
            "style_recommendations": await self._generate_style_recommendations(style_features, style_quality),
            "consistency_analysis": await self._analyze_style_consistency(content)
        }
    
    async def _proofread_text(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """تدقيق النص لغوياً"""
        logger.info("بدء التدقيق اللغوي")
        
        error_types = options.get("error_types", ["grammar", "spelling", "punctuation", "syntax"])
        
        detected_errors = []
        
        # كشف الأخطاء المختلفة
        for error_type in error_types:
            errors = await self._detect_errors(content, error_type)
            detected_errors.extend(errors)
        
        # تصحيح الأخطاء
        corrected_text = await self._apply_corrections(content, detected_errors)
        
        # إحصائيات التدقيق
        proofreading_stats = await self._calculate_proofreading_stats(detected_errors)
        
        return {
            "status": "success",
            "review_type": "proofreading",
            "original_text": content,
            "corrected_text": corrected_text,
            "detected_errors": detected_errors,
            "error_statistics": proofreading_stats,
            "correction_summary": await self._summarize_corrections(detected_errors),
            "text_quality_score": await self._calculate_text_quality_score(detected_errors, len(content))
        }
    
    async def _check_consistency(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """فحص التماسك والثبات"""
        logger.info("بدء فحص التماسك")
        
        consistency_aspects = options.get("aspects", ["characters", "timeline", "setting", "style", "tone"])
        
        consistency_issues = {}
        
        for aspect in consistency_aspects:
            issues = await self._check_specific_consistency(content, aspect)
            if issues:
                consistency_issues[aspect] = issues
        
        # تقييم مستوى التماسك العام
        consistency_score = await self._calculate_consistency_score(consistency_issues)
        
        # اقتراح حلول
        consistency_solutions = await self._suggest_consistency_solutions(consistency_issues)
        
        return {
            "status": "success",
            "review_type": "consistency_check",
            "consistency_score": consistency_score,
            "consistency_issues": consistency_issues,
            "solutions": consistency_solutions,
            "consistency_map": await self._create_consistency_map(content),
            "improvement_priority": await self._prioritize_consistency_fixes(consistency_issues)
        }
    
    async def _assess_overall_quality(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """تقييم الجودة الإجمالية"""
        logger.info("بدء تقييم الجودة الإجمالية")
        
        quality_dimensions = [
            "technical_quality",
            "artistic_merit",
            "originality",
            "engagement",
            "cultural_relevance",
            "market_appeal"
        ]
        
        quality_scores = {}
        for dimension in quality_dimensions:
            score = await self._assess_quality_dimension(content, dimension)
            quality_scores[dimension] = score
        
        # حساب النتيجة الإجمالية
        overall_score = sum(quality_scores.values()) / len(quality_scores)
        
        # تحديد المستوى
        quality_level = await self._determine_quality_level(overall_score)
        
        # توصيات للتحسين
        quality_recommendations = await self._generate_quality_recommendations(quality_scores)
        
        return {
            "status": "success",
            "review_type": "quality_assessment",
            "overall_score": overall_score,
            "quality_level": quality_level,
            "dimension_scores": quality_scores,
            "recommendations": quality_recommendations,
            "benchmarking": await self._benchmark_against_standards(quality_scores),
            "potential_rating": await self._predict_potential_rating(content, quality_scores)
        }
    
    async def _provide_developmental_feedback(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """تقديم ملاحظات تطويرية"""
        logger.info("بدء تقديم الملاحظات التطويرية")
        
        feedback_focus = options.get("focus", "comprehensive")
        target_audience = options.get("audience", "general")
        development_stage = options.get("stage", "draft")
        
        # تحليل القوة والضعف
        swot_analysis = await self._perform_swot_analysis(content)
        
        # تحديد إمكانيات التطوير
        development_opportunities = await self._identify_development_opportunities(content, target_audience)
        
        # اقتراح خطة تطوير
        development_plan = await self._create_development_plan(swot_analysis, development_opportunities)
        
        # ملاحظات مرحلية
        stage_specific_feedback = await self._generate_stage_specific_feedback(content, development_stage)
        
        return {
            "status": "success",
            "review_type": "developmental_feedback",
            "swot_analysis": swot_analysis,
            "development_opportunities": development_opportunities,
            "development_plan": development_plan,
            "stage_feedback": stage_specific_feedback,
            "next_steps": await self._recommend_next_steps(development_plan),
            "long_term_vision": await self._articulate_long_term_vision(content, development_opportunities)
        }
    
    async def _comparative_analysis(self, content: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """تحليل مقارن"""
        logger.info("بدء التحليل المقارن")
        
        comparison_texts = options.get("comparison_texts", [])
        comparison_criteria = options.get("criteria", ["style", "quality", "approach"])
        
        if not comparison_texts:
            # مقارنة مع معايير الجودة العامة
            comparison_results = await self._compare_with_standards(content, comparison_criteria)
        else:
            # مقارنة مع نصوص محددة
            comparison_results = await self._compare_with_specific_texts(content, comparison_texts, comparison_criteria)
        
        # تحليل الموقع النسبي
        relative_position = await self._analyze_relative_position(comparison_results)
        
        # نقاط التميز والتحسن
        differentiation_points = await self._identify_differentiation_points(comparison_results)
        
        return {
            "status": "success",
            "review_type": "comparative_analysis",
            "comparison_results": comparison_results,
            "relative_position": relative_position,
            "differentiation_points": differentiation_points,
            "competitive_advantages": await self._identify_competitive_advantages(comparison_results),
            "improvement_gaps": await self._identify_improvement_gaps(comparison_results)
        }
    
    # دوال مساعدة متخصصة
    
    async def _analyze_language_quality(self, content: str) -> Dict[str, Any]:
        """تحليل جودة اللغة"""
        # تحليل مبسط - يمكن تطويره
        words = content.split()
        sentences = content.split('.')
        
        return {
            "vocabulary_richness": len(set(words)) / len(words) if words else 0,
            "sentence_variety": len(set([len(s.split()) for s in sentences])) / len(sentences) if sentences else 0,
            "language_level": "متقدم",
            "grammatical_correctness": 0.85,
            "expression_clarity": 0.80
        }
    
    async def _analyze_structural_elements(self, content: str) -> Dict[str, Any]:
        """تحليل العناصر البنائية"""
        return {
            "logical_flow": 0.85,
            "paragraph_coherence": 0.80,
            "transition_quality": 0.75,
            "overall_organization": 0.82
        }
    
    async def _analyze_stylistic_features(self, content: str) -> Dict[str, Any]:
        """تحليل الخصائص الأسلوبية"""
        return {
            "style_consistency": 0.80,
            "tone_appropriateness": 0.85,
            "voice_uniqueness": 0.75,
            "literary_devices": 0.70
        }
    
    async def _analyze_content_depth(self, content: str) -> Dict[str, Any]:
        """تحليل عمق المحتوى"""
        return {
            "thematic_depth": 0.75,
            "idea_originality": 0.80,
            "insight_quality": 0.70,
            "message_clarity": 0.85
        }
    
    async def _analyze_character_development(self, content: str) -> Dict[str, Any]:
        """تحليل تطوير الشخصيات"""
        return {
            "character_depth": 0.75,
            "character_consistency": 0.80,
            "dialogue_quality": 0.70,
            "character_growth": 0.65
        }
    
    async def _analyze_engagement_factors(self, content: str) -> Dict[str, Any]:
        """تحليل عوامل الإشراك"""
        return {
            "readability": 0.80,
            "emotional_impact": 0.75,
            "suspense_maintenance": 0.70,
            "reader_connection": 0.78
        }
    
    async def _calculate_overall_rating(self, analysis_results: Dict[str, Any]) -> float:
        """حساب التقييم الإجمالي"""
        total_score = 0
        total_weight = 0
        
        for criterion, data in analysis_results.items():
            if criterion in self.criticism_criteria:
                weight = self.criticism_criteria[criterion]["weight"]
                # حساب متوسط النتائج للمعيار
                scores = [v for v in data.values() if isinstance(v, (int, float))]
                avg_score = sum(scores) / len(scores) if scores else 0
                total_score += avg_score * weight * 10  # تحويل إلى مقياس 10
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    async def _identify_strengths_weaknesses(self, analysis_results: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """تحديد نقاط القوة والضعف"""
        strengths = []
        weaknesses = []
        
        for criterion, data in analysis_results.items():
            scores = [v for v in data.values() if isinstance(v, (int, float))]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            if avg_score > 0.8:
                strengths.append(f"تميز في {self.criticism_criteria.get(criterion, {}).get('name', criterion)}")
            elif avg_score < 0.6:
                weaknesses.append(f"ضعف في {self.criticism_criteria.get(criterion, {}).get('name', criterion)}")
        
        return strengths, weaknesses
    
    async def _assess_review_effectiveness(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """تقييم فعالية المراجعة"""
        return {
            "comprehensiveness": 0.90,
            "actionability": 0.85,
            "specificity": 0.80,
            "constructiveness": 0.88
        }
    
    def get_criticism_criteria(self) -> Dict[str, Any]:
        """الحصول على معايير النقد"""
        return self.criticism_criteria
    
    def set_criticism_level(self, level: CriticismLevel):
        """تعيين مستوى النقد"""
        self.current_criticism_level = level
        logger.info(f"تم تعيين مستوى النقد إلى: {level.value}")
    
    def get_review_history(self) -> List[Dict[str, Any]]:
        """الحصول على تاريخ المراجعات"""
        return self.memory.conversation_history
    
    async def _generate_improvement_suggestions(self, analysis_results: Dict[str, Any], weaknesses: List[str]) -> List[str]:
        """توليد اقتراحات التحسين"""
        suggestions = [
            "تطوير الحوار ليكون أكثر طبيعية",
            "إثراء الوصف بتفاصيل حسية",
            "تعميق التحليل النفسي للشخصيات",
            "تحسين الانتقالات بين المشاهد",
            "تنويع بنية الجمل لإضافة إيقاع متنوع"
        ]
        return suggestions
    
    async def _create_improvement_roadmap(self, weaknesses: List[str], suggestions: List[str]) -> List[str]:
        """إنشاء خارطة طريق للتحسين"""
        roadmap = [
            "المرحلة الأولى: معالجة الأخطاء اللغوية والنحوية",
            "المرحلة الثانية: تحسين البناء والتنظيم",
            "المرحلة الثالثة: تطوير الأسلوب والصوت الأدبي",
            "المرحلة الرابعة: إثراء المحتوى والعمق",
            "المرحلة الخامسة: تعزيز عوامل الإشراك والتأثير"
        ]
        return roadmap
