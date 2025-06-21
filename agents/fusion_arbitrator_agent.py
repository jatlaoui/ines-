"""
وكيل مُحكم الاندماج (Fusion Arbitrator Agent)
===============================================

وكيل متخصص في تقييم جودة الدمج السردي وضمان التماسك الفني
يعمل كمراقب جودة متقدم لعمليات التخليق السردي

المطور: فريق السردي الخارق
التاريخ: 2025
الإصدار: 1.0.0
"""

import asyncio
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import re
import statistics
from collections import Counter, defaultdict

from .base_agent import BaseAgent

# إعداد نظام السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """مقاييس الجودة الشاملة"""
    coherence_score: float  # التماسك السردي
    consistency_score: float  # الاتساق الداخلي
    authenticity_score: float  # الأصالة الأدبية
    creativity_score: float  # الإبداعية
    technical_score: float  # الجودة التقنية
    cultural_sensitivity: float  # الحساسية الثقافية
    readability_score: float  # سهولة القراءة
    emotional_resonance: float  # الرنين العاطفي
    overall_quality: float  # الجودة الإجمالية

@dataclass
class IssueReport:
    """تقرير المشاكل المكتشفة"""
    issue_id: str
    severity: str  # 'critical', 'major', 'minor', 'suggestion'
    category: str  # 'plot', 'character', 'style', 'language', 'structure'
    description: str
    location: str  # موقع المشكلة في النص
    suggested_fix: str
    impact_assessment: str
    priority: int  # 1-10

@dataclass
class ArbitrationResult:
    """نتيجة التحكيم الشاملة"""
    arbitration_id: str
    quality_metrics: QualityMetrics
    detected_issues: List[IssueReport]
    recommendations: List[str]
    improvement_suggestions: List[Dict[str, Any]]
    approval_status: str  # 'approved', 'needs_revision', 'major_revision'
    confidence_level: float
    processing_timestamp: str

class FusionArbitratorAgent(BaseAgent):
    """وكيل محكم الاندماج السردي المتقدم"""
    
    def __init__(self, agent_id: str = "fusion_arbitrator", **kwargs):
        super().__init__(agent_id, **kwargs)
        self.agent_type = "fusion_arbitrator"
        self.capabilities = [
            "quality_assessment",
            "coherence_analysis", 
            "consistency_checking",
            "authenticity_validation",
            "creativity_evaluation",
            "issue_detection",
            "improvement_recommendation"
        ]
        
        # معايير التقييم المتقدمة
        self.quality_thresholds = {
            'excellent': 0.9,
            'good': 0.75,
            'acceptable': 0.6,
            'needs_improvement': 0.45,
            'poor': 0.3
        }
        
        # أوزان التقييم
        self.evaluation_weights = {
            'coherence': 0.25,
            'consistency': 0.20,
            'authenticity': 0.15,
            'creativity': 0.15,
            'technical': 0.10,
            'cultural': 0.05,
            'readability': 0.05,
            'emotional': 0.05
        }
        
        # قوائم المراجعة
        self.coherence_checklist = [
            'logical_flow',
            'plot_consistency',
            'character_continuity',
            'temporal_coherence',
            'causal_relationships'
        ]
        
        self.style_checklist = [
            'tone_consistency',
            'voice_uniformity',
            'register_appropriateness',
            'narrative_perspective',
            'linguistic_harmony'
        ]

    async def arbitrate_fusion(self, synthesized_narrative: str, 
                             source_narratives: List[str],
                             fusion_metadata: Dict[str, Any]) -> ArbitrationResult:
        """
        التحكيم الشامل لعملية الدمج السردي
        
        Args:
            synthesized_narrative: النص المُخلق
            source_narratives: النصوص المصدر
            fusion_metadata: بيانات وصفية عن عملية الدمج
            
        Returns:
            ArbitrationResult: نتيجة التحكيم الشاملة
        """
        try:
            logger.info("بدء عملية التحكيم والتقييم الشامل")
            
            arbitration_id = f"arbitration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 1. تحليل الجودة الشاملة
            logger.info("تحليل الجودة الشاملة...")
            quality_metrics = await self._assess_comprehensive_quality(
                synthesized_narrative, source_narratives, fusion_metadata
            )
            
            # 2. كشف المشاكل والتناقضات
            logger.info("كشف المشاكل والتناقضات...")
            detected_issues = await self._detect_issues(
                synthesized_narrative, source_narratives, fusion_metadata
            )
            
            # 3. توليد التوصيات
            logger.info("توليد التوصيات...")
            recommendations = await self._generate_recommendations(
                quality_metrics, detected_issues, fusion_metadata
            )
            
            # 4. اقتراحات التحسين
            logger.info("تطوير اقتراحات التحسين...")
            improvement_suggestions = await self._develop_improvement_suggestions(
                synthesized_narrative, detected_issues, quality_metrics
            )
            
            # 5. تحديد حالة الموافقة
            approval_status = await self._determine_approval_status(quality_metrics, detected_issues)
            
            # 6. حساب مستوى الثقة
            confidence_level = await self._calculate_confidence_level(quality_metrics, detected_issues)
            
            result = ArbitrationResult(
                arbitration_id=arbitration_id,
                quality_metrics=quality_metrics,
                detected_issues=detected_issues,
                recommendations=recommendations,
                improvement_suggestions=improvement_suggestions,
                approval_status=approval_status,
                confidence_level=confidence_level,
                processing_timestamp=datetime.now().isoformat()
            )
            
            logger.info(f"تم إكمال التحكيم - الحالة: {approval_status}")
            return result
            
        except Exception as e:
            logger.error(f"خطأ في عملية التحكيم: {str(e)}")
            raise

    async def _assess_comprehensive_quality(self, narrative: str, sources: List[str],
                                          metadata: Dict[str, Any]) -> QualityMetrics:
        """تقييم الجودة الشاملة للنص المُخلق"""
        
        # 1. تقييم التماسك السردي
        coherence_score = await self._evaluate_coherence(narrative)
        
        # 2. تقييم الاتساق الداخلي
        consistency_score = await self._evaluate_consistency(narrative, sources)
        
        # 3. تقييم الأصالة الأدبية
        authenticity_score = await self._evaluate_authenticity(narrative)
        
        # 4. تقييم الإبداعية
        creativity_score = await self._evaluate_creativity(narrative, sources)
        
        # 5. تقييم الجودة التقنية
        technical_score = await self._evaluate_technical_quality(narrative)
        
        # 6. تقييم الحساسية الثقافية
        cultural_sensitivity = await self._evaluate_cultural_sensitivity(narrative)
        
        # 7. تقييم سهولة القراءة
        readability_score = await self._evaluate_readability(narrative)
        
        # 8. تقييم الرنين العاطفي
        emotional_resonance = await self._evaluate_emotional_resonance(narrative)
        
        # حساب الجودة الإجمالية
        overall_quality = (
            coherence_score * self.evaluation_weights['coherence'] +
            consistency_score * self.evaluation_weights['consistency'] +
            authenticity_score * self.evaluation_weights['authenticity'] +
            creativity_score * self.evaluation_weights['creativity'] +
            technical_score * self.evaluation_weights['technical'] +
            cultural_sensitivity * self.evaluation_weights['cultural'] +
            readability_score * self.evaluation_weights['readability'] +
            emotional_resonance * self.evaluation_weights['emotional']
        )
        
        return QualityMetrics(
            coherence_score=coherence_score,
            consistency_score=consistency_score,
            authenticity_score=authenticity_score,
            creativity_score=creativity_score,
            technical_score=technical_score,
            cultural_sensitivity=cultural_sensitivity,
            readability_score=readability_score,
            emotional_resonance=emotional_resonance,
            overall_quality=overall_quality
        )

    async def _evaluate_coherence(self, narrative: str) -> float:
        """تقييم التماسك السردي"""
        scores = []
        
        # فحص التدفق المنطقي
        logical_flow = await self._check_logical_flow(narrative)
        scores.append(logical_flow)
        
        # فحص ثبات الحبكة
        plot_consistency = await self._check_plot_consistency(narrative)
        scores.append(plot_consistency)
        
        # فحص استمرارية الشخصيات
        character_continuity = await self._check_character_continuity(narrative)
        scores.append(character_continuity)
        
        # فحص التماسك الزمني
        temporal_coherence = await self._check_temporal_coherence(narrative)
        scores.append(temporal_coherence)
        
        # فحص العلاقات السببية
        causal_relationships = await self._check_causal_relationships(narrative)
        scores.append(causal_relationships)
        
        return statistics.mean(scores)

    async def _evaluate_consistency(self, narrative: str, sources: List[str]) -> float:
        """تقييم الاتساق الداخلي"""
        scores = []
        
        # اتساق النبرة
        tone_consistency = await self._check_tone_consistency(narrative)
        scores.append(tone_consistency)
        
        # اتساق الأسلوب
        style_consistency = await self._check_style_consistency(narrative)
        scores.append(style_consistency)
        
        # اتساق المعلومات
        information_consistency = await self._check_information_consistency(narrative)
        scores.append(information_consistency)
        
        # اتساق وجهة النظر السردية
        perspective_consistency = await self._check_perspective_consistency(narrative)
        scores.append(perspective_consistency)
        
        return statistics.mean(scores)

    async def _evaluate_authenticity(self, narrative: str) -> float:
        """تقييم الأصالة الأدبية"""
        scores = []
        
        # أصالة اللغة
        language_authenticity = await self._check_language_authenticity(narrative)
        scores.append(language_authenticity)
        
        # أصالة الحوارات
        dialogue_authenticity = await self._check_dialogue_authenticity(narrative)
        scores.append(dialogue_authenticity)
        
        # أصالة الوصف
        description_authenticity = await self._check_description_authenticity(narrative)
        scores.append(description_authenticity)
        
        # أصالة السياق الثقافي
        cultural_authenticity = await self._check_cultural_context_authenticity(narrative)
        scores.append(cultural_authenticity)
        
        return statistics.mean(scores)

    async def _evaluate_creativity(self, narrative: str, sources: List[str]) -> float:
        """تقييم الإبداعية والابتكار"""
        scores = []
        
        # الابتكار في الحبكة
        plot_innovation = await self._assess_plot_innovation(narrative, sources)
        scores.append(plot_innovation)
        
        # الابتكار في الشخصيات
        character_innovation = await self._assess_character_innovation(narrative, sources)
        scores.append(character_innovation)
        
        # الابتكار في الأسلوب
        style_innovation = await self._assess_style_innovation(narrative, sources)
        scores.append(style_innovation)
        
        # الابتكار في المعالجة
        treatment_innovation = await self._assess_treatment_innovation(narrative, sources)
        scores.append(treatment_innovation)
        
        return statistics.mean(scores)

    async def _evaluate_technical_quality(self, narrative: str) -> float:
        """تقييم الجودة التقنية"""
        scores = []
        
        # الجودة النحوية
        grammar_quality = await self._assess_grammar_quality(narrative)
        scores.append(grammar_quality)
        
        # جودة الترقيم
        punctuation_quality = await self._assess_punctuation_quality(narrative)
        scores.append(punctuation_quality)
        
        # جودة البنية
        structure_quality = await self._assess_structure_quality(narrative)
        scores.append(structure_quality)
        
        # جودة المفردات
        vocabulary_quality = await self._assess_vocabulary_quality(narrative)
        scores.append(vocabulary_quality)
        
        return statistics.mean(scores)

    async def _detect_issues(self, narrative: str, sources: List[str],
                           metadata: Dict[str, Any]) -> List[IssueReport]:
        """كشف المشاكل والتناقضات في النص"""
        issues = []
        
        # كشف مشاكل الحبكة
        plot_issues = await self._detect_plot_issues(narrative)
        issues.extend(plot_issues)
        
        # كشف مشاكل الشخصيات
        character_issues = await self._detect_character_issues(narrative)
        issues.extend(character_issues)
        
        # كشف مشاكل الأسلوب
        style_issues = await self._detect_style_issues(narrative)
        issues.extend(style_issues)
        
        # كشف مشاكل اللغة
        language_issues = await self._detect_language_issues(narrative)
        issues.extend(language_issues)
        
        # كشف مشاكل البنية
        structure_issues = await self._detect_structure_issues(narrative)
        issues.extend(structure_issues)
        
        # ترتيب المشاكل حسب الأولوية
        issues.sort(key=lambda x: x.priority, reverse=True)
        
        return issues

    # وظائف مساعدة للفحص التفصيلي
    async def _check_logical_flow(self, narrative: str) -> float:
        """فحص التدفق المنطقي للأحداث"""
        sentences = re.split(r'[.!?]+', narrative)
        transitions = ['ثم', 'بعد ذلك', 'فجأة', 'في النهاية', 'أخيراً']
        
        transition_count = sum(any(trans in sentence for trans in transitions) 
                             for sentence in sentences)
        
        # نسبة وجود الروابط المنطقية
        return min(transition_count / len(sentences) * 5, 1.0)

    async def _check_plot_consistency(self, narrative: str) -> float:
        """فحص ثبات الحبكة"""
        # فحص بسيط لوجود عناصر الحبكة الأساسية
        plot_elements = ['بداية', 'مشكلة', 'صراع', 'حل', 'نهاية']
        found_elements = sum(1 for element in plot_elements 
                           if any(keyword in narrative.lower() 
                                for keyword in [element]))
        
        return found_elements / len(plot_elements)

    async def _check_character_continuity(self, narrative: str) -> float:
        """فحص استمرارية الشخصيات"""
        # استخلاص الأسماء المحتملة
        names = re.findall(r'\b[A-Za-zأ-ي]{3,}\b(?=\s+(?:قال|قالت|ذهب|ذهبت))', narrative)
        unique_names = set(names)
        
        if not unique_names:
            return 0.5
        
        # فحص استمرارية ظهور الشخصيات
        continuity_scores = []
        for name in unique_names:
            mentions = narrative.count(name)
            if mentions > 1:
                continuity_scores.append(min(mentions / 10, 1.0))
        
        return statistics.mean(continuity_scores) if continuity_scores else 0.5

    async def _check_temporal_coherence(self, narrative: str) -> float:
        """فحص التماسك الزمني"""
        time_indicators = ['صباح', 'مساء', 'ليل', 'نهار', 'أمس', 'اليوم', 'غداً']
        
        found_indicators = sum(narrative.lower().count(indicator) 
                             for indicator in time_indicators)
        
        sentences = len(re.split(r'[.!?]+', narrative))
        return min(found_indicators / sentences * 3, 1.0)

    async def _check_causal_relationships(self, narrative: str) -> float:
        """فحص العلاقات السببية"""
        causal_connectors = ['لأن', 'بسبب', 'نتيجة', 'لذلك', 'من أجل', 'كي']
        
        causal_count = sum(narrative.count(connector) for connector in causal_connectors)
        sentences = len(re.split(r'[.!?]+', narrative))
        
        return min(causal_count / sentences * 4, 1.0)

    async def _check_tone_consistency(self, narrative: str) -> float:
        """فحص اتساق النبرة"""
        formal_indicators = ['إن', 'حيث', 'إذ', 'بل', 'لكن']
        informal_indicators = ['يعني', 'طبعاً', 'أكيد', 'ممكن']
        
        formal_count = sum(narrative.count(word) for word in formal_indicators)
        informal_count = sum(narrative.count(word) for word in informal_indicators)
        
        total = formal_count + informal_count
        if total == 0:
            return 0.7  # نبرة محايدة
        
        # اتساق النبرة يعني هيمنة إحدى النبرتين
        dominant_ratio = max(formal_count, informal_count) / total
        return dominant_ratio

    async def _detect_plot_issues(self, narrative: str) -> List[IssueReport]:
        """كشف مشاكل الحبكة"""
        issues = []
        
        # فحص وجود صراع واضح
        conflict_indicators = ['صراع', 'مشكلة', 'تحدي', 'عقبة', 'صعوبة']
        has_conflict = any(indicator in narrative.lower() for indicator in conflict_indicators)
        
        if not has_conflict:
            issues.append(IssueReport(
                issue_id="plot_001",
                severity="major",
                category="plot",
                description="لا يوجد صراع واضح في القصة",
                location="النص بأكمله",
                suggested_fix="إضافة عنصر صراع واضح يحرك الأحداث",
                impact_assessment="يؤثر على جاذبية القصة",
                priority=8
            ))
        
        # فحص وجود نهاية
        ending_indicators = ['النهاية', 'أخيراً', 'انتهت', 'انتهى']
        has_ending = any(indicator in narrative.lower() for indicator in ending_indicators)
        
        if not has_ending:
            issues.append(IssueReport(
                issue_id="plot_002",
                severity="minor",
                category="plot",
                description="النهاية غير واضحة",
                location="نهاية النص",
                suggested_fix="إضافة خاتمة واضحة للقصة",
                impact_assessment="قد يترك القارئ محتاراً",
                priority=5
            ))
        
        return issues

    async def _detect_character_issues(self, narrative: str) -> List[IssueReport]:
        """كشف مشاكل الشخصيات"""
        issues = []
        
        # فحص وجود شخصيات
        character_indicators = re.findall(r'\b[A-Za-zأ-ي]{3,}\b(?=\s+(?:قال|قالت))', narrative)
        
        if len(character_indicators) < 1:
            issues.append(IssueReport(
                issue_id="char_001",
                severity="critical",
                category="character",
                description="لا توجد شخصيات واضحة في القصة",
                location="النص بأكمله",
                suggested_fix="إضافة شخصيات محددة بأسماء وحوارات",
                impact_assessment="القصة تحتاج شخصيات للتفاعل",
                priority=9
            ))
        
        return issues

    async def _detect_style_issues(self, narrative: str) -> List[IssueReport]:
        """كشف مشاكل الأسلوب"""
        issues = []
        
        # فحص طول الجمل
        sentences = re.split(r'[.!?]+', narrative)
        avg_length = statistics.mean(len(sentence.split()) for sentence in sentences if sentence.strip())
        
        if avg_length > 25:
            issues.append(IssueReport(
                issue_id="style_001",
                severity="minor",
                category="style",
                description="الجمل طويلة جداً",
                location="النص بأكمله",
                suggested_fix="تقسيم الجمل الطويلة إلى جمل أقصر",
                impact_assessment="قد يؤثر على سهولة القراءة",
                priority=4
            ))
        
        return issues

    async def _detect_language_issues(self, narrative: str) -> List[IssueReport]:
        """كشف مشاكل اللغة"""
        issues = []
        
        # فحص التكرار المفرط
        words = narrative.split()
        word_counts = Counter(words)
        
        for word, count in word_counts.most_common(5):
            if count > len(words) * 0.05 and len(word) > 3:  # أكثر من 5% من النص
                issues.append(IssueReport(
                    issue_id=f"lang_001_{word}",
                    severity="minor",
                    category="language",
                    description=f"تكرار مفرط للكلمة: {word}",
                    location="النص بأكمله",
                    suggested_fix=f"استخدام مرادفات للكلمة {word}",
                    impact_assessment="قد يؤثر على تنوع المفردات",
                    priority=3
                ))
        
        return issues

    async def _detect_structure_issues(self, narrative: str) -> List[IssueReport]:
        """كشف مشاكل البنية"""
        issues = []
        
        # فحص تقسيم الفقرات
        paragraphs = narrative.split('\n\n')
        
        if len(paragraphs) < 3:
            issues.append(IssueReport(
                issue_id="struct_001",
                severity="minor",
                category="structure",
                description="النص يحتاج لتقسيم أفضل إلى فقرات",
                location="النص بأكمله",
                suggested_fix="تقسيم النص إلى فقرات منطقية",
                impact_assessment="يحسن من تنظيم النص",
                priority=4
            ))
        
        return issues

    async def _generate_recommendations(self, quality_metrics: QualityMetrics,
                                      issues: List[IssueReport],
                                      metadata: Dict[str, Any]) -> List[str]:
        """توليد التوصيات بناء على التحليل"""
        recommendations = []
        
        # توصيات بناء على الجودة الإجمالية
        if quality_metrics.overall_quality < 0.6:
            recommendations.append("النص يحتاج لمراجعة شاملة لتحسين الجودة العامة")
        
        if quality_metrics.coherence_score < 0.7:
            recommendations.append("تحسين التماسك السردي من خلال ربط الأحداث بشكل أفضل")
        
        if quality_metrics.creativity_score < 0.6:
            recommendations.append("إضافة عناصر إبداعية أكثر لجعل القصة أكثر تميزاً")
        
        # توصيات بناء على المشاكل المكتشفة
        critical_issues = [issue for issue in issues if issue.severity == 'critical']
        if critical_issues:
            recommendations.append("معالجة المشاكل الحرجة المكتشفة كأولوية قصوى")
        
        major_issues = [issue for issue in issues if issue.severity == 'major']
        if len(major_issues) > 2:
            recommendations.append("مراجعة وإصلاح المشاكل الرئيسية المتعددة")
        
        if quality_metrics.readability_score < 0.7:
            recommendations.append("تحسين سهولة القراءة من خلال تبسيط التراكيب المعقدة")
        
        return recommendations

    async def _develop_improvement_suggestions(self, narrative: str, issues: List[IssueReport],
                                             quality_metrics: QualityMetrics) -> List[Dict[str, Any]]:
        """تطوير اقتراحات التحسين المفصلة"""
        suggestions = []
        
        # اقتراحات تحسين التماسك
        if quality_metrics.coherence_score < 0.8:
            suggestions.append({
                'category': 'coherence',
                'priority': 'high',
                'suggestion': 'إضافة روابط انتقالية بين الفقرات',
                'implementation': 'استخدام كلمات مثل "ثم"، "بعد ذلك"، "في النهاية"',
                'expected_impact': 'تحسين تدفق القراءة'
            })
        
        # اقتراحات تحسين الإبداعية
        if quality_metrics.creativity_score < 0.7:
            suggestions.append({
                'category': 'creativity',
                'priority': 'medium',
                'suggestion': 'إضافة تفاصيل وصفية أكثر إبداعاً',
                'implementation': 'استخدام الصور البيانية والاستعارات',
                'expected_impact': 'جعل النص أكثر حيوية وجاذبية'
            })
        
        # اقتراحات محددة بناء على المشاكل
        for issue in issues[:5]:  # أهم 5 مشاكل
            suggestions.append({
                'category': issue.category,
                'priority': 'high' if issue.severity in ['critical', 'major'] else 'medium',
                'suggestion': issue.suggested_fix,
                'implementation': f"في {issue.location}: {issue.description}",
                'expected_impact': issue.impact_assessment
            })
        
        return suggestions

    async def _determine_approval_status(self, quality_metrics: QualityMetrics,
                                       issues: List[IssueReport]) -> str:
        """تحديد حالة الموافقة على النص"""
        critical_issues = [i for i in issues if i.severity == 'critical']
        major_issues = [i for i in issues if i.severity == 'major']
        
        # رفض في حالة وجود مشاكل حرجة
        if critical_issues:
            return 'major_revision'
        
        # مراجعة في حالة جودة منخفضة أو مشاكل رئيسية متعددة
        if quality_metrics.overall_quality < 0.6 or len(major_issues) > 3:
            return 'needs_revision'
        
        # موافقة في حالة الجودة المقبولة
        if quality_metrics.overall_quality >= 0.75:
            return 'approved'
        
        return 'needs_revision'

    async def _calculate_confidence_level(self, quality_metrics: QualityMetrics,
                                        issues: List[IssueReport]) -> float:
        """حساب مستوى الثقة في التقييم"""
        base_confidence = 0.8
        
        # تقليل الثقة مع ازدياد المشاكل
        issue_penalty = len(issues) * 0.02
        
        # تقليل الثقة مع انخفاض الجودة
        quality_factor = quality_metrics.overall_quality
        
        confidence = base_confidence * quality_factor - issue_penalty
        return max(0.3, min(1.0, confidence))

    # وظائف مساعدة إضافية للتقييمات المتقدمة
    async def _assess_grammar_quality(self, narrative: str) -> float:
        """تقييم الجودة النحوية (محاكاة)"""
        # في التطبيق الفعلي، ستستخدم أدوات تحليل نحوي متقدمة
        return 0.85

    async def _assess_punctuation_quality(self, narrative: str) -> float:
        """تقييم جودة الترقيم"""
        sentences = re.split(r'[.!?]+', narrative)
        punctuated_sentences = len([s for s in sentences if s.strip()])
        return min(punctuated_sentences / len(sentences), 1.0) if sentences else 0.5

    async def _assess_structure_quality(self, narrative: str) -> float:
        """تقييم جودة البنية"""
        paragraphs = narrative.split('\n\n')
        return min(len(paragraphs) / 5, 1.0)

    async def _assess_vocabulary_quality(self, narrative: str) -> float:
        """تقييم جودة المفردات"""
        words = narrative.split()
        unique_words = set(words)
        return len(unique_words) / len(words) if words else 0

    async def _evaluate_cultural_sensitivity(self, narrative: str) -> float:
        """تقييم الحساسية الثقافية"""
        # فحص وجود عناصر ثقافية إيجابية
        positive_cultural = ['تراث', 'أصالة', 'كرم', 'ضيافة', 'شهامة']
        return min(sum(narrative.count(word) for word in positive_cultural) / 10, 1.0)

    async def _evaluate_readability(self, narrative: str) -> float:
        """تقييم سهولة القراءة"""
        sentences = re.split(r'[.!?]+', narrative)
        words = narrative.split()
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # كلما قل طول الجملة، زادت سهولة القراءة
        return max(0, 1 - (avg_sentence_length - 15) / 25) if avg_sentence_length > 15 else 1.0

    async def _evaluate_emotional_resonance(self, narrative: str) -> float:
        """تقييم الرنين العاطفي"""
        emotional_words = ['حب', 'حزن', 'فرح', 'خوف', 'أمل', 'يأس', 'سعادة']
        emotional_count = sum(narrative.lower().count(word) for word in emotional_words)
        return min(emotional_count / len(narrative.split()) * 10, 1.0)

    # باقي الوظائف المساعدة للتقييمات المتخصصة...
    async def _check_style_consistency(self, narrative: str) -> float:
        return 0.8  # محاكاة

    async def _check_information_consistency(self, narrative: str) -> float:
        return 0.85  # محاكاة

    async def _check_perspective_consistency(self, narrative: str) -> float:
        return 0.8  # محاكاة

    async def _check_language_authenticity(self, narrative: str) -> float:
        return 0.85  # محاكاة

    async def _check_dialogue_authenticity(self, narrative: str) -> float:
        return 0.8  # محاكاة

    async def _check_description_authenticity(self, narrative: str) -> float:
        return 0.85  # محاكاة

    async def _check_cultural_context_authenticity(self, narrative: str) -> float:
        return 0.9  # محاكاة

    async def _assess_plot_innovation(self, narrative: str, sources: List[str]) -> float:
        return 0.75  # محاكاة

    async def _assess_character_innovation(self, narrative: str, sources: List[str]) -> float:
        return 0.8  # محاكاة

    async def _assess_style_innovation(self, narrative: str, sources: List[str]) -> float:
        return 0.7  # محاكاة

    async def _assess_treatment_innovation(self, narrative: str, sources: List[str]) -> float:
        return 0.75  # محاكاة

# مثال على الاستخدام
async def main():
    """مثال على تشغيل وكيل المحكم"""
    arbitrator = FusionArbitratorAgent()
    
    sample_narrative = """
    كان أحمد شاباً طموحاً يعيش في المدينة. أحب فاطمة من أول نظرة.
    واجه صعوبات كثيرة في الحياة، لكنه لم يستسلم أبداً.
    في النهاية، تزوج من حبيبته وعاشا سعيدين.
    """
    
    result = await arbitrator.arbitrate_fusion(
        synthesized_narrative=sample_narrative,
        source_narratives=["مصدر 1", "مصدر 2"],
        fusion_metadata={"type": "character_merge"}
    )
    
    print(f"نتيجة التحكيم: {result.approval_status}")
    print(f"الجودة الإجمالية: {result.quality_metrics.overall_quality:.2f}")
    print(f"عدد المشاكل المكتشفة: {len(result.detected_issues)}")

if __name__ == "__main__":
    asyncio.run(main())
