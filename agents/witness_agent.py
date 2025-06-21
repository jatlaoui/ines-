"""
وكيل الشاهد - أول وكيل عالمي متخصص في تحليل واستخلاص المعلومات من ترانسكريبت الفيديوهات
وتحويلها إلى مادة إبداعية قابلة للاستخدام في الكتابة الأدبية
"""

import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict

from .base_agent import BaseAgent, AgentCapabilities, AgentMessage, MessageType, AgentState
from ..tools.witness_extractor_tool import (
    WitnessExtractorTool, 
    WitnessExtractionResult,
    ExtractedEvent, 
    ExtractedCharacter, 
    ExtractedDialogue,
    CredibilityLevel,
    ContentType,
    serialize_extraction_result
)

# إعداد التسجيل
logger = logging.getLogger(__name__)

@dataclass
class WitnessAnalysisTask:
    """مهمة تحليل الشاهد"""
    task_id: str
    transcript: str
    source_info: Dict[str, Any]
    analysis_depth: str = "deep"  # shallow, medium, deep
    focus_areas: List[str] = None  # events, characters, dialogues, all
    credibility_threshold: float = 0.3
    literary_focus: bool = True
    context_requirements: Dict[str, Any] = None

@dataclass
class WitnessAnalysisResult:
    """نتيجة تحليل الشاهد"""
    task_id: str
    extraction_result: WitnessExtractionResult
    analysis_summary: Dict[str, Any]
    integration_suggestions: List[str]
    creative_opportunities: List[str]
    verification_needs: List[str]
    usage_guidelines: Dict[str, Any]
    metadata: Dict[str, Any]

class WitnessAgent(BaseAgent):
    """
    وكيل الشاهد المتخصص في:
    - تحليل ترانسكريبت الفيديوهات
    - استخلاص الأحداث والشخصيات والحوارات
    - تقييم المصداقية والموثوقية
    - توليد توصيات للاستخدام الإبداعي
    - دمج المحتوى في النصوص الأدبية
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        # إعداد القدرات المتخصصة لوكيل الشاهد
        capabilities = AgentCapabilities(
            name="وكيل الشاهد",
            description="متخصص في تحليل ترانسكريبت الفيديوهات واستخلاص المحتوى الإبداعي",
            primary_functions=[
                "تحليل ترانسكريبت الفيديوهات",
                "استخلاص الأحداث والشخصيات", 
                "تقييم المصداقية",
                "توليد المحتوى الإبداعي",
                "دمج المحتوى في النصوص"
            ],
            supported_tasks=[
                "witness_transcript_analysis",
                "event_extraction", 
                "character_extraction",
                "dialogue_extraction",
                "credibility_assessment",
                "content_integration",
                "literary_adaptation"
            ],
            interaction_style="تحليلي-إبداعي",
            expertise_level="خبير",
            language_preferences=["ar", "en"],
            response_format="structured_creative"
        )
        
        super().__init__(
            agent_id=agent_id or f"witness_agent_{uuid.uuid4().hex[:8]}",
            capabilities=capabilities
        )
        
        # أدوات متخصصة
        self.witness_extractor = WitnessExtractorTool()
        
        # إعدادات التحليل
        self.default_analysis_settings = {
            'credibility_threshold': 0.4,
            'literary_focus': True,
            'extract_dialogue': True,
            'extract_events': True,
            'extract_characters': True,
            'assess_credibility': True,
            'generate_recommendations': True
        }
        
        # كاش النتائج للأداء
        self.analysis_cache = {}
        
        logger.info(f"تم تهيئة وكيل الشاهد: {self.agent_id}")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة مهام وكيل الشاهد"""
        try:
            task_type = task.get('type', '')
            
            if task_type == 'witness_transcript_analysis':
                return await self._analyze_witness_transcript(task)
            elif task_type == 'extract_events':
                return await self._extract_events_only(task)
            elif task_type == 'extract_characters':
                return await self._extract_characters_only(task)
            elif task_type == 'extract_dialogues':
                return await self._extract_dialogues_only(task)
            elif task_type == 'assess_credibility':
                return await self._assess_credibility_only(task)
            elif task_type == 'integrate_content':
                return await self._integrate_content_into_text(task)
            elif task_type == 'literary_adaptation':
                return await self._adapt_for_literary_use(task)
            else:
                raise ValueError(f"نوع مهمة غير مدعوم: {task_type}")
                
        except Exception as e:
            logger.error(f"خطأ في معالجة مهمة وكيل الشاهد: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'task_id': task.get('id', 'unknown')
            }
    
    async def _analyze_witness_transcript(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """تحليل شامل لترانسكريبت الشاهد"""
        try:
            # استخراج معطيات المهمة
            transcript = task.get('transcript', '')
            source_info = task.get('source_info', {})
            analysis_depth = task.get('analysis_depth', 'deep')
            
            if not transcript.strip():
                raise ValueError("الترانسكريبت فارغ أو غير صالح")
            
            # تحديث حالة الوكيل
            await self._update_state(AgentState.WORKING)
            
            # إجراء الاستخلاص الرئيسي
            extraction_result = await self.witness_extractor.extract_witness_information(
                transcript=transcript,
                source_info=source_info
            )
            
            # تحليل إضافي حسب عمق التحليل المطلوب
            analysis_summary = await self._create_analysis_summary(
                extraction_result, analysis_depth
            )
            
            # توليد اقتراحات التكامل
            integration_suggestions = await self._generate_integration_suggestions(
                extraction_result
            )
            
            # تحديد الفرص الإبداعية
            creative_opportunities = await self._identify_creative_opportunities(
                extraction_result
            )
            
            # تحديد احتياجات التحقق
            verification_needs = await self._identify_verification_needs(
                extraction_result
            )
            
            # إرشادات الاستخدام
            usage_guidelines = await self._create_usage_guidelines(
                extraction_result
            )
            
            # إنشاء النتيجة النهائية
            result = WitnessAnalysisResult(
                task_id=task.get('id', ''),
                extraction_result=extraction_result,
                analysis_summary=analysis_summary,
                integration_suggestions=integration_suggestions,
                creative_opportunities=creative_opportunities,
                verification_needs=verification_needs,
                usage_guidelines=usage_guidelines,
                metadata={
                    'analysis_depth': analysis_depth,
                    'processing_time': datetime.now().isoformat(),
                    'agent_id': self.agent_id,
                    'transcript_length': len(transcript),
                    'extracted_items': {
                        'events': len(extraction_result.events),
                        'characters': len(extraction_result.characters),
                        'dialogues': len(extraction_result.dialogues)
                    }
                }
            )
            
            # حفظ في الكاش
            self.analysis_cache[task.get('id', '')] = result
            
            # تحديث حالة الوكيل
            await self._update_state(AgentState.COMPLETED)
            
            return {
                'success': True,
                'result': asdict(result),
                'extraction_data': serialize_extraction_result(extraction_result),
                'task_id': task.get('id', ''),
                'agent_id': self.agent_id
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل ترانسكريبت الشاهد: {str(e)}")
            await self._update_state(AgentState.ERROR)
            raise
    
    async def _create_analysis_summary(self, extraction_result: WitnessExtractionResult, 
                                     depth: str) -> Dict[str, Any]:
        """إنشاء ملخص تحليلي للنتائج"""
        summary = {
            'overview': {
                'total_events': len(extraction_result.events),
                'total_characters': len(extraction_result.characters),
                'total_dialogues': len(extraction_result.dialogues),
                'overall_credibility': extraction_result.credibility_assessment.get('overall_credibility', 0.5),
                'extraction_timestamp': extraction_result.extracted_at.isoformat()
            },
            'key_findings': [],
            'credibility_analysis': extraction_result.credibility_assessment,
            'literary_potential': extraction_result.literary_elements
        }
        
        # تحليل متقدم حسب العمق المطلوب
        if depth in ['medium', 'deep']:
            summary['character_analysis'] = await self._analyze_characters_deeply(
                extraction_result.characters
            )
            summary['event_analysis'] = await self._analyze_events_deeply(
                extraction_result.events
            )
        
        if depth == 'deep':
            summary['narrative_structure'] = await self._analyze_narrative_structure(
                extraction_result
            )
            summary['thematic_analysis'] = await self._analyze_themes(
                extraction_result
            )
        
        return summary
    
    async def _generate_integration_suggestions(self, extraction_result: WitnessExtractionResult) -> List[str]:
        """توليد اقتراحات لدمج المحتوى في النصوص الأدبية"""
        suggestions = []
        
        # اقتراحات للأحداث
        high_credibility_events = [
            event for event in extraction_result.events 
            if event.credibility in [CredibilityLevel.HIGH, CredibilityLevel.VERY_HIGH]
        ]
        
        if high_credibility_events:
            suggestions.append(
                f"يمكن استخدام {len(high_credibility_events)} حدث عالي المصداقية كأساس للحبكة الرئيسية"
            )
        
        # اقتراحات للشخصيات
        well_developed_characters = [
            char for char in extraction_result.characters 
            if len(char.characteristics) >= 3 and len(char.quotes) >= 2
        ]
        
        if well_developed_characters:
            suggestions.append(
                f"يمكن تطوير {len(well_developed_characters)} شخصية كشخصيات رئيسية أو ثانوية في النص"
            )
        
        # اقتراحات للحوارات
        literary_dialogues = [
            dlg for dlg in extraction_result.dialogues 
            if dlg.literary_value >= 0.7
        ]
        
        if literary_dialogues:
            suggestions.append(
                f"يمكن استخدام {len(literary_dialogues)} حوار عالي القيمة الأدبية مباشرة في النص"
            )
        
        # اقتراحات إضافية بناءً على التحليل الأدبي
        if extraction_result.literary_elements.get('dramatic_moments'):
            suggestions.append(
                "يحتوي النص على لحظات درامية قوية يمكن استغلالها لبناء ذروة فعالة"
            )
        
        if extraction_result.literary_elements.get('symbolic_elements'):
            suggestions.append(
                "توجد عناصر رمزية يمكن تطويرها لإضافة عمق فلسفي للنص"
            )
        
        return suggestions
    
    async def _identify_creative_opportunities(self, extraction_result: WitnessExtractionResult) -> List[str]:
        """تحديد الفرص الإبداعية في المحتوى المستخرج"""
        opportunities = []
        
        # تحليل التنوع في المحتوى
        event_types = set(event.event_type for event in extraction_result.events)
        if len(event_types) >= 5:
            opportunities.append("تنوع كبير في أنواع الأحداث يسمح ببناء حبكة متعددة الطبقات")
        
        # تحليل الصراعات المحتملة
        characters_with_conflicts = []
        for char in extraction_result.characters:
            if any('صراع' in trait or 'تضارب' in trait for trait in char.characteristics):
                characters_with_conflicts.append(char)
        
        if characters_with_conflicts:
            opportunities.append(f"وجود صراعات شخصية في {len(characters_with_conflicts)} شخصية يمكن استغلالها للتوتر الدرامي")
        
        # تحليل العواطف
        emotional_range = set()
        for dialogue in extraction_result.dialogues:
            emotional_range.add(dialogue.emotional_tone)
        
        if len(emotional_range) >= 4:
            opportunities.append("تنوع عاطفي واسع يسمح ببناء رحلة عاطفية شاملة للقارئ")
        
        # فرص الرمزية
        if extraction_result.literary_elements.get('symbolic_elements'):
            opportunities.append("إمكانية بناء طبقات رمزية عميقة تضيف معنى فلسفي للنص")
        
        return opportunities
    
    async def _identify_verification_needs(self, extraction_result: WitnessExtractionResult) -> List[str]:
        """تحديد المعلومات التي تحتاج لتحقق إضافي"""
        verification_needs = []
        
        # الأحداث منخفضة المصداقية
        low_credibility_events = [
            event for event in extraction_result.events 
            if event.credibility in [CredibilityLevel.LOW, CredibilityLevel.QUESTIONABLE]
        ]
        
        if low_credibility_events:
            verification_needs.append(
                f"{len(low_credibility_events)} حدث يحتاج لتحقق إضافي قبل الاستخدام في النص"
            )
        
        # الشخصيات غير الموثقة جيداً
        poorly_documented_characters = [
            char for char in extraction_result.characters 
            if len(char.characteristics) < 2 or char.credibility == CredibilityLevel.LOW
        ]
        
        if poorly_documented_characters:
            verification_needs.append(
                f"{len(poorly_documented_characters)} شخصية تحتاج لمعلومات إضافية لتطويرها"
            )
        
        # المعلومات المتضاربة
        if extraction_result.credibility_assessment.get('red_flags'):
            verification_needs.append(
                "وجود إشارات تحذيرية تتطلب مراجعة دقيقة للمعلومات"
            )
        
        return verification_needs
    
    async def _create_usage_guidelines(self, extraction_result: WitnessExtractionResult) -> Dict[str, Any]:
        """إنشاء إرشادات لاستخدام المحتوى المستخرج"""
        return {
            'credibility_recommendations': {
                'high_confidence_content': [
                    event.id for event in extraction_result.events 
                    if event.credibility in [CredibilityLevel.HIGH, CredibilityLevel.VERY_HIGH]
                ],
                'use_with_caution': [
                    event.id for event in extraction_result.events 
                    if event.credibility == CredibilityLevel.MEDIUM
                ],
                'verify_before_use': [
                    event.id for event in extraction_result.events 
                    if event.credibility in [CredibilityLevel.LOW, CredibilityLevel.QUESTIONABLE]
                ]
            },
            'literary_usage': {
                'direct_quotation': [
                    dlg.id for dlg in extraction_result.dialogues 
                    if dlg.literary_value >= 0.8
                ],
                'adaptation_recommended': [
                    dlg.id for dlg in extraction_result.dialogues 
                    if 0.5 <= dlg.literary_value < 0.8
                ],
                'inspiration_only': [
                    dlg.id for dlg in extraction_result.dialogues 
                    if dlg.literary_value < 0.5
                ]
            },
            'ethical_considerations': [
                "الحصول على إذن من الشاهد قبل النشر",
                "حماية هوية الأشخاص المذكورين إذا لزم الأمر",
                "التحقق من صحة المعلومات الحساسة",
                "احترام الخصوصية والكرامة الإنسانية"
            ],
            'creative_techniques': extraction_result.literary_elements.get('style_recommendations', [])
        }
    
    # === وظائف مساعدة للتحليل المتقدم ===
    
    async def _analyze_characters_deeply(self, characters: List[ExtractedCharacter]) -> Dict[str, Any]:
        """تحليل متقدم للشخصيات"""
        analysis = {
            'character_archetypes': {},
            'development_potential': {},
            'relationship_matrix': {},
            'dialogue_patterns': {}
        }
        
        for character in characters:
            # تحديد النموذج الأولي للشخصية
            archetype = await self._determine_character_archetype(character)
            analysis['character_archetypes'][character.id] = archetype
            
            # تقييم إمكانية التطوير
            development_score = len(character.characteristics) * 0.3 + len(character.quotes) * 0.2
            analysis['development_potential'][character.id] = min(development_score, 1.0)
        
        return analysis
    
    async def _analyze_events_deeply(self, events: List[ExtractedEvent]) -> Dict[str, Any]:
        """تحليل متقدم للأحداث"""
        analysis = {
            'event_categories': {},
            'temporal_structure': [],
            'causal_relationships': [],
            'dramatic_intensity': {}
        }
        
        # تصنيف الأحداث
        for event in events:
            category = await self._categorize_event(event)
            if category not in analysis['event_categories']:
                analysis['event_categories'][category] = []
            analysis['event_categories'][category].append(event.id)
        
        return analysis
    
    async def _determine_character_archetype(self, character: ExtractedCharacter) -> str:
        """تحديد النموذج الأولي للشخصية"""
        # تحليل الخصائص لتحديد النموذج
        traits = ' '.join(character.characteristics).lower()
        
        if any(word in traits for word in ['قائد', 'زعيم', 'رئيس']):
            return 'القائد'
        elif any(word in traits for word in ['حكيم', 'عالم', 'معلم']):
            return 'الحكيم'
        elif any(word in traits for word in ['بطل', 'شجاع', 'محارب']):
            return 'البطل'
        elif any(word in traits for word in ['مساعد', 'صديق', 'مرافق']):
            return 'المساعد'
        else:
            return 'شخصية عادية'
    
    async def _categorize_event(self, event: ExtractedEvent) -> str:
        """تصنيف نوع الحدث"""
        event_text = event.description.lower()
        
        if any(word in event_text for word in ['قتال', 'حرب', 'معركة']):
            return 'صراع'
        elif any(word in event_text for word in ['لقاء', 'اجتماع', 'زيارة']):
            return 'تفاعل اجتماعي'
        elif any(word in event_text for word in ['اكتشاف', 'وجد', 'عثر']):
            return 'اكتشاف'
        else:
            return 'حدث عام'
    
    # === وظائف المهام المتخصصة ===
    
    async def _extract_events_only(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """استخلاص الأحداث فقط"""
        transcript = task.get('transcript', '')
        extraction_result = await self.witness_extractor.extract_witness_information(
            transcript, task.get('source_info', {})
        )
        
        return {
            'success': True,
            'events': [asdict(event) for event in extraction_result.events],
            'task_id': task.get('id', ''),
            'agent_id': self.agent_id
        }
    
    async def _extract_characters_only(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """استخلاص الشخصيات فقط"""
        transcript = task.get('transcript', '')
        extraction_result = await self.witness_extractor.extract_witness_information(
            transcript, task.get('source_info', {})
        )
        
        return {
            'success': True,
            'characters': [asdict(char) for char in extraction_result.characters],
            'task_id': task.get('id', ''),
            'agent_id': self.agent_id
        }
    
    async def _extract_dialogues_only(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """استخلاص الحوارات فقط"""
        transcript = task.get('transcript', '')
        extraction_result = await self.witness_extractor.extract_witness_information(
            transcript, task.get('source_info', {})
        )
        
        return {
            'success': True,
            'dialogues': [asdict(dlg) for dlg in extraction_result.dialogues],
            'task_id': task.get('id', ''),
            'agent_id': self.agent_id
        }
    
    async def _assess_credibility_only(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """تقييم المصداقية فقط"""
        transcript = task.get('transcript', '')
        extraction_result = await self.witness_extractor.extract_witness_information(
            transcript, task.get('source_info', {})
        )
        
        return {
            'success': True,
            'credibility_assessment': extraction_result.credibility_assessment,
            'task_id': task.get('id', ''),
            'agent_id': self.agent_id
        }
    
    async def _integrate_content_into_text(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """دمج المحتوى المستخرج في نص موجود"""
        # هذه الوظيفة ستحتاج تطوير متقدم لدمج المحتوى
        # سيتم تطويرها في مرحلة لاحقة
        
        return {
            'success': True,
            'message': 'وظيفة دمج المحتوى قيد التطوير',
            'task_id': task.get('id', ''),
            'agent_id': self.agent_id
        }
    
    async def _adapt_for_literary_use(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """تكييف المحتوى للاستخدام الأدبي"""
        # هذه الوظيفة ستحتاج تطوير متقدم للتكييف الأدبي
        # سيتم تطويرها في مرحلة لاحقة
        
        return {
            'success': True,
            'message': 'وظيفة التكييف الأدبي قيد التطوير',
            'task_id': task.get('id', ''),
            'agent_id': self.agent_id
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """الحصول على حالة وكيل الشاهد"""
        status = super().get_agent_status()
        status.update({
            'specialized_capabilities': [
                'تحليل ترانسكريبت الفيديوهات',
                'استخلاص الأحداث والشخصيات',
                'تقييم المصداقية',
                'التكييف الأدبي'
            ],
            'cache_size': len(self.analysis_cache),
            'tool_status': 'witness_extractor_ready'
        })
        return status

# === وظائف مساعدة لإنشاء الوكيل ===

def create_witness_agent(agent_id: Optional[str] = None) -> WitnessAgent:
    """إنشاء مثيل من وكيل الشاهد"""
    return WitnessAgent(agent_id)

def register_witness_agent() -> Dict[str, Any]:
    """تسجيل وكيل الشاهد في النظام"""
    return {
        'agent_type': 'witness_agent',
        'class': WitnessAgent,
        'capabilities': [
            'witness_transcript_analysis',
            'event_extraction',
            'character_extraction', 
            'dialogue_extraction',
            'credibility_assessment',
            'content_integration',
            'literary_adaptation'
        ],
        'description': 'وكيل متخصص في تحليل ترانسكريبت الفيديوهات وتحويلها لمحتوى إبداعي'
    }
