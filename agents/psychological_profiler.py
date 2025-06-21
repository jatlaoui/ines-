"""
محاكي الشخصيات النفسية
Psychological Profiler - Professional tool for authentic psychological character development

أداة متخصصة لإنشاء شخصيات ذات عمق نفسي واقعي:
- تحليل الأنماط النفسية والدوافع العميقة
- تطوير الشخصية عبر الأحداث
- كشف التناقضات النفسية في السلوك
- اقتراح ردود فعل نفسية واقعية
"""

import asyncio
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class PersonalityType(Enum):
    """أنواع الشخصية (المايرز-بريجز المبسط)"""
    EXTROVERT = "extrovert"  # منفتح
    INTROVERT = "introvert"  # منطوي
    THINKING = "thinking"  # عقلاني
    FEELING = "feeling"  # عاطفي
    JUDGING = "judging"  # منظم
    PERCEIVING = "perceiving"  # مرن

class PsychologicalDisorder(Enum):
    """الاضطرابات النفسية الشائعة"""
    ANXIETY = "anxiety"  # القلق
    DEPRESSION = "depression"  # الاكتئاب
    PTSD = "ptsd"  # اضطراب ما بعد الصدمة
    OCD = "ocd"  # الوسواس القهري
    BIPOLAR = "bipolar"  # ثنائي القطب
    NARCISSISM = "narcissism"  # النرجسية
    NONE = "none"  # لا يوجد

class EmotionalState(Enum):
    """الحالات العاطفية"""
    HAPPINESS = "happiness"  # سعادة
    SADNESS = "sadness"  # حزن
    ANGER = "anger"  # غضب
    FEAR = "fear"  # خوف
    ANXIETY = "anxiety"  # قلق
    LOVE = "love"  # حب
    HATE = "hate"  # كراهية
    NEUTRAL = "neutral"  # محايد

class CopingMechanism(Enum):
    """آليات التأقلم"""
    DENIAL = "denial"  # الإنكار
    PROJECTION = "projection"  # الإسقاط
    RATIONALIZATION = "rationalization"  # التبرير العقلي
    SUBLIMATION = "sublimation"  # التسامي
    REGRESSION = "regression"  # النكوص
    DISPLACEMENT = "displacement"  # الإزاحة

@dataclass
class PsychologicalProfile:
    """الملف النفسي للشخصية"""
    character_name: str
    personality_traits: List[PersonalityType]
    core_motivations: List[str]
    fears_and_phobias: List[str]
    emotional_patterns: Dict[str, float]
    coping_mechanisms: List[CopingMechanism]
    psychological_wounds: List[str]
    mental_health_status: PsychologicalDisorder
    behavioral_tendencies: List[str]
    relationship_patterns: List[str]
    growth_potential: float

@dataclass
class PsychologicalResponse:
    """الاستجابة النفسية لحدث"""
    trigger_event: str
    immediate_reaction: str
    emotional_impact: EmotionalState
    thought_process: List[str]
    behavioral_response: str
    long_term_effects: List[str]
    coping_strategy: CopingMechanism

@dataclass
class CharacterDevelopment:
    """تطور الشخصية النفسي"""
    starting_state: Dict[str, Any]
    key_events: List[Dict[str, Any]]
    psychological_changes: List[str]
    growth_milestones: List[str]
    final_state: Dict[str, Any]

class PsychologicalProfiler:
    """محاكي الشخصيات النفسية المتقدم"""
    
    def __init__(self):
        self.personality_indicators = self._load_personality_indicators()
        self.psychological_patterns = self._load_psychological_patterns()
        self.cultural_psychology = self._load_cultural_psychology()
        self.trauma_responses = self._load_trauma_responses()
        self.therapy_techniques = self._load_therapy_techniques()
    
    def get_name(self) -> str:
        return "محاكي الشخصيات النفسية"
    
    def get_description(self) -> str:
        return "أداة متخصصة لتطوير شخصيات أدبية بعمق نفسي وواقعية سلوكية"
    
    def get_features(self) -> List[str]:
        return [
            "تحليل الأنماط النفسية",
            "بناء الدوافع العميقة",
            "محاكاة ردود الأفعال",
            "تتبع التطور النفسي",
            "كشف التناقضات السلوكية"
        ]
    
    def get_supported_formats(self) -> List[str]:
        return ["text", "character_analysis", "psychological_profile"]
    
    def get_output_types(self) -> List[str]:
        return ["analysis", "profiles", "responses", "development_arc"]
    
    async def analyze(self, content: str, context: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """التحليل النفسي الشامل للشخصيات"""
        try:
            # تحديد الشخصيات وخصائصها النفسية
            character_profiles = await self._analyze_character_psychology(content)
            
            # تحليل الأنماط العاطفية
            emotional_patterns = await self._analyze_emotional_patterns(content)
            
            # تحديد الصدمات والجروح النفسية
            psychological_wounds = await self._identify_psychological_wounds(content)
            
            # تحليل آليات التأقلم
            coping_mechanisms = await self._analyze_coping_mechanisms(content)
            
            # تحليل ديناميكيات العلاقات
            relationship_dynamics = await self._analyze_relationship_dynamics(content, character_profiles)
            
            # تطوير قوس التطور النفسي
            development_arcs = await self._develop_psychological_arcs(content, character_profiles)
            
            # اقتراح ردود أفعال واقعية
            realistic_responses = await self._suggest_realistic_responses(character_profiles, content)
            
            # كشف التناقضات النفسية
            psychological_inconsistencies = await self._detect_psychological_inconsistencies(content, character_profiles)
            
            # إنتاج التوصيات
            recommendations = await self._generate_psychological_recommendations(
                character_profiles, emotional_patterns, psychological_wounds, psychological_inconsistencies
            )
            
            # حساب درجة الثقة
            confidence_score = self._calculate_confidence_score(
                character_profiles, emotional_patterns, psychological_wounds
            )
            
            # إنشاء البيانات المرئية
            visual_data = await self._generate_visual_data(
                character_profiles, emotional_patterns, development_arcs
            )
            
            return {
                "analysis": {
                    "characters_analyzed": len(character_profiles),
                    "emotional_patterns_detected": len(emotional_patterns),
                    "psychological_wounds_identified": len(psychological_wounds),
                    "coping_mechanisms_found": len(coping_mechanisms),
                    "relationship_dynamics": len(relationship_dynamics),
                    "inconsistencies_detected": len(psychological_inconsistencies)
                },
                "character_profiles": [self._profile_to_dict(profile) for profile in character_profiles],
                "emotional_patterns": emotional_patterns,
                "psychological_wounds": psychological_wounds,
                "coping_mechanisms": coping_mechanisms,
                "relationship_dynamics": relationship_dynamics,
                "development_arcs": [self._development_to_dict(arc) for arc in development_arcs],
                "realistic_responses": realistic_responses,
                "psychological_inconsistencies": psychological_inconsistencies,
                "recommendations": recommendations,
                "confidence_score": confidence_score,
                "visual_data": visual_data,
                "metadata": {
                    "analysis_type": "psychological_profiling",
                    "processing_time": datetime.now().isoformat(),
                    "psychological_framework": "integrative_approach"
                }
            }
            
        except Exception as e:
            raise Exception(f"خطأ في التحليل النفسي: {str(e)}")
    
    async def _analyze_character_psychology(self, content: str) -> List[PsychologicalProfile]:
        """تحليل علم النفس للشخصيات"""
        profiles = []
        
        # استخراج أسماء الشخصيات
        character_names = await self._extract_character_names(content)
        
        for name in character_names[:5]:  # تحليل أول 5 شخصيات
            profile = await self._create_psychological_profile(name, content)
            profiles.append(profile)
        
        return profiles
    
    async def _extract_character_names(self, content: str) -> List[str]:
        """استخراج أسماء الشخصيات من النص"""
        # أنماط الأسماء العربية
        name_patterns = [
            r'([أ-ي]{3,})\s+(?:قال|قالت|فعل|فعلت|شعر|شعرت)',
            r'الشخصية\s+([أ-ي]{3,})',
            r'([أ-ي]{3,})\s+(?:البطل|البطلة|الشخص)',
            r'(?:اسمه|اسمها)\s+([أ-ي]{3,})'
        ]
        
        names = set()
        for pattern in name_patterns:
            matches = re.findall(pattern, content)
            names.update(matches)
        
        # إزالة الكلمات الشائعة غير المناسبة للأسماء
        common_words = {'هذا', 'هذه', 'ذلك', 'تلك', 'كان', 'كانت', 'الذي', 'التي'}
        names = names - common_words
        
        return list(names)
    
    async def _create_psychological_profile(self, name: str, content: str) -> PsychologicalProfile:
        """إنشاء ملف نفسي للشخصية"""
        
        # تحليل السمات الشخصية
        personality_traits = await self._analyze_personality_traits(name, content)
        
        # تحديد الدوافع الأساسية
        core_motivations = await self._identify_core_motivations(name, content)
        
        # تحديد المخاوف والرهاب
        fears_and_phobias = await self._identify_fears(name, content)
        
        # تحليل الأنماط العاطفية
        emotional_patterns = await self._analyze_character_emotions(name, content)
        
        # تحديد آليات التأقلم
        coping_mechanisms = await self._identify_character_coping(name, content)
        
        # تحديد الجروح النفسية
        psychological_wounds = await self._identify_character_wounds(name, content)
        
        # تقييم الصحة النفسية
        mental_health_status = await self._assess_mental_health(name, content)
        
        # تحليل الميول السلوكية
        behavioral_tendencies = await self._analyze_behavioral_patterns(name, content)
        
        # تحليل أنماط العلاقات
        relationship_patterns = await self._analyze_relationship_patterns(name, content)
        
        # تقدير إمكانية النمو
        growth_potential = await self._assess_growth_potential(name, content)
        
        return PsychologicalProfile(
            character_name=name,
            personality_traits=personality_traits,
            core_motivations=core_motivations,
            fears_and_phobias=fears_and_phobias,
            emotional_patterns=emotional_patterns,
            coping_mechanisms=coping_mechanisms,
            psychological_wounds=psychological_wounds,
            mental_health_status=mental_health_status,
            behavioral_tendencies=behavioral_tendencies,
            relationship_patterns=relationship_patterns,
            growth_potential=growth_potential
        )
    
    async def _analyze_personality_traits(self, name: str, content: str) -> List[PersonalityType]:
        """تحليل السمات الشخصية"""
        traits = []
        
        # البحث عن مؤشرات الانطواء/الانفتاح
        extrovert_indicators = ["يحب الناس", "اجتماعي", "يتكلم كثيراً", "نشيط", "منفتح"]
        introvert_indicators = ["هادئ", "يفضل الوحدة", "متحفظ", "يفكر كثيراً", "منطوي"]
        
        extrovert_score = sum(1 for indicator in extrovert_indicators if indicator in content and name in content)
        introvert_score = sum(1 for indicator in introvert_indicators if indicator in content and name in content)
        
        if extrovert_score > introvert_score:
            traits.append(PersonalityType.EXTROVERT)
        elif introvert_score > extrovert_score:
            traits.append(PersonalityType.INTROVERT)
        
        # البحث عن مؤشرات العقلانية/العاطفية
        thinking_indicators = ["يفكر", "منطقي", "عقلاني", "يحلل", "واقعي"]
        feeling_indicators = ["يشعر", "عاطفي", "حساس", "رحيم", "متعاطف"]
        
        thinking_score = sum(1 for indicator in thinking_indicators if indicator in content and name in content)
        feeling_score = sum(1 for indicator in feeling_indicators if indicator in content and name in content)
        
        if thinking_score > feeling_score:
            traits.append(PersonalityType.THINKING)
        elif feeling_score > thinking_score:
            traits.append(PersonalityType.FEELING)
        
        # البحث عن مؤشرات التنظيم/المرونة
        judging_indicators = ["منظم", "مخطط", "دقيق", "ملتزم", "جدي"]
        perceiving_indicators = ["مرن", "عفوي", "متكيف", "مغامر", "متسامح"]
        
        judging_score = sum(1 for indicator in judging_indicators if indicator in content and name in content)
        perceiving_score = sum(1 for indicator in perceiving_indicators if indicator in content and name in content)
        
        if judging_score > perceiving_score:
            traits.append(PersonalityType.JUDGING)
        elif perceiving_score > judging_score:
            traits.append(PersonalityType.PERCEIVING)
        
        return traits
    
    async def _identify_core_motivations(self, name: str, content: str) -> List[str]:
        """تحديد الدوافع الأساسية"""
        motivations = []
        
        motivation_patterns = {
            "السلطة": ["يريد السيطرة", "يحب القيادة", "يسعى للنفوذ"],
            "الحب": ["يبحث عن الحب", "يريد القبول", "يحتاج المودة"],
            "الأمان": ["يخاف من", "يحتاج الأمان", "يسعى للاستقرار"],
            "التقدير": ["يريد الاحترام", "يسعى للتميز", "يحب الإعجاب"],
            "المعرفة": ["يحب التعلم", "فضولي", "يبحث عن الحقيقة"],
            "العدالة": ["يحارب الظلم", "يسعى للعدل", "يدافع عن الحق"]
        }
        
        for motivation, indicators in motivation_patterns.items():
            if any(indicator in content and name in content for indicator in indicators):
                motivations.append(motivation)
        
        return motivations
    
    async def _identify_fears(self, name: str, content: str) -> List[str]:
        """تحديد المخاوف والرهاب"""
        fears = []
        
        fear_patterns = {
            "الموت": ["يخاف من الموت", "رهاب الموت", "قلق الموت"],
            "الوحدة": ["يخاف من الوحدة", "رهاب الوحدة", "يكره العزلة"],
            "الفشل": ["يخاف من الفشل", "قلق الأداء", "رهاب النجاح"],
            "الرفض": ["يخاف من الرفض", "قلق الانفصال", "رهاب التخلي"],
            "الظلام": ["يخاف من الظلام", "رهاب الظلام", "يفضل النور"],
            "المرتفعات": ["يخاف من المرتفعات", "رهاب المرتفعات", "دوار المرتفعات"]
        }
        
        for fear, indicators in fear_patterns.items():
            if any(indicator in content and name in content for indicator in indicators):
                fears.append(fear)
        
        return fears
    
    async def _analyze_character_emotions(self, name: str, content: str) -> Dict[str, float]:
        """تحليل الأنماط العاطفية للشخصية"""
        emotions = {
            "happiness": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "anxiety": 0.0,
            "love": 0.0
        }
        
        emotion_indicators = {
            "happiness": ["سعيد", "فرح", "مبتهج", "مسرور", "يضحك", "يبتسم"],
            "sadness": ["حزين", "كئيب", "مكتئب", "يبكي", "يئس", "محبط"],
            "anger": ["غاضب", "ثائر", "منفعل", "يصرخ", "غيظ", "حنق"],
            "fear": ["خائف", "مذعور", "مرعوب", "قلق", "خوف", "رعب"],
            "anxiety": ["قلق", "متوتر", "عصبي", "مضطرب", "يرتجف"],
            "love": ["يحب", "عاشق", "متيم", "مغرم", "حنان", "عطف"]
        }
        
        # حساب تكرار كل عاطفة
        for emotion, indicators in emotion_indicators.items():
            count = sum(1 for indicator in indicators if indicator in content and name in content)
            emotions[emotion] = min(1.0, count * 0.2)  # تطبيع النتيجة
        
        return emotions
    
    async def _identify_character_coping(self, name: str, content: str) -> List[CopingMechanism]:
        """تحديد آليات التأقلم للشخصية"""
        mechanisms = []
        
        coping_indicators = {
            CopingMechanism.DENIAL: ["ينكر", "يرفض الاعتراف", "لا يقبل الواقع"],
            CopingMechanism.PROJECTION: ["يلوم الآخرين", "يسقط على", "مسؤولية الآخرين"],
            CopingMechanism.RATIONALIZATION: ["يبرر", "يجد أعذار", "منطق مقنع"],
            CopingMechanism.SUBLIMATION: ["يحول طاقته", "يبدع", "ينتج فن"],
            CopingMechanism.REGRESSION: ["يتصرف كطفل", "يعود لسلوك قديم", "سلوك طفولي"],
            CopingMechanism.DISPLACEMENT: ["يحول غضبه", "يصب جامه على", "يوجه مشاعره"]
        }
        
        for mechanism, indicators in coping_indicators.items():
            if any(indicator in content and name in content for indicator in indicators):
                mechanisms.append(mechanism)
        
        return mechanisms
    
    async def _identify_character_wounds(self, name: str, content: str) -> List[str]:
        """تحديد الجروح النفسية للشخصية"""
        wounds = []
        
        wound_patterns = {
            "فقدان الوالدين": ["مات والده", "فقد أمه", "يتيم", "بلا أهل"],
            "الخيانة": ["خانه", "غدر به", "فقد الثقة", "خذلوه"],
            "الرفض": ["رفضوه", "لم يقبلوه", "نبذوه", "أهانوه"],
            "العنف": ["تعرض للضرب", "عنف", "اعتداء", "أذى جسدي"],
            "الإهمال": ["أهملوه", "تجاهلوه", "لم يهتموا", "ترك وحيداً"],
            "الفقر": ["عاش فقيراً", "حرمان", "عوز", "بؤس"]
        }
        
        for wound, indicators in wound_patterns.items():
            if any(indicator in content and name in content for indicator in indicators):
                wounds.append(wound)
        
        return wounds
    
    async def _assess_mental_health(self, name: str, content: str) -> PsychologicalDisorder:
        """تقييم الصحة النفسية"""
        disorder_indicators = {
            PsychologicalDisorder.ANXIETY: ["قلق مستمر", "يخاف دائماً", "توتر شديد", "نوبات هلع"],
            PsychologicalDisorder.DEPRESSION: ["اكتئاب", "حزن عميق", "يأس", "فقدان الأمل", "لا يستمتع"],
            PsychologicalDisorder.PTSD: ["صدمة", "كوابيس", "ذكريات مؤلمة", "تجنب", "فرط يقظة"],
            PsychologicalDisorder.OCD: ["وسواس", "أفكار متكررة", "طقوس", "نظافة مفرطة"],
            PsychologicalDisorder.BIPOLAR: ["تقلبات مزاجية", "نشاط مفرط", "اكتئاب متناوب"],
            PsychologicalDisorder.NARCISSISM: ["غرور", "يعتقد أنه أفضل", "حب الذات", "يستغل الآخرين"]
        }
        
        for disorder, indicators in disorder_indicators.items():
            if any(indicator in content and name in content for indicator in indicators):
                return disorder
        
        return PsychologicalDisorder.NONE
    
    async def _analyze_behavioral_patterns(self, name: str, content: str) -> List[str]:
        """تحليل الأنماط السلوكية"""
        patterns = []
        
        behavioral_indicators = [
            "يكرر نفس السلوك",
            "عادات ثابتة",
            "سلوك قهري",
            "تجنب معين",
            "ردود فعل متوقعة",
            "سلوك دفاعي"
        ]
        
        for indicator in behavioral_indicators:
            if indicator in content and name in content:
                patterns.append(indicator)
        
        return patterns
    
    async def _analyze_relationship_patterns(self, name: str, content: str) -> List[str]:
        """تحليل أنماط العلاقات"""
        patterns = []
        
        relationship_indicators = [
            "يتجنب العلاقات",
            "يرتبط بسرعة",
            "صعوبة في الثقة",
            "يسيطر على الآخرين",
            "يعتمد على الآخرين",
            "يضحي من أجل الآخرين"
        ]
        
        for indicator in relationship_indicators:
            if indicator in content and name in content:
                patterns.append(indicator)
        
        return patterns
    
    async def _assess_growth_potential(self, name: str, content: str) -> float:
        """تقدير إمكانية النمو النفسي"""
        growth_indicators = [
            "يتعلم من أخطائه",
            "يريد التغيير",
            "مرن في التفكير",
            "يطلب المساعدة",
            "واعي بمشاكله",
            "يحاول التطوير"
        ]
        
        growth_score = sum(1 for indicator in growth_indicators if indicator in content and name in content)
        return min(1.0, growth_score * 0.15)
    
    async def _analyze_emotional_patterns(self, content: str) -> List[Dict[str, Any]]:
        """تحليل الأنماط العاطفية في النص"""
        patterns = []
        
        # البحث عن التقلبات العاطفية
        emotion_transitions = [
            "من الفرح إلى الحزن",
            "تحول مزاجه",
            "انقلبت مشاعره",
            "تقلب عاطفي"
        ]
        
        for transition in emotion_transitions:
            if transition in content:
                patterns.append({
                    "type": "emotional_transition",
                    "description": transition,
                    "stability": "منخفضة"
                })
        
        return patterns
    
    async def _identify_psychological_wounds(self, content: str) -> List[Dict[str, Any]]:
        """تحديد الجروح النفسية في النص"""
        wounds = []
        
        trauma_indicators = [
            "صدمة نفسية",
            "تجربة مؤلمة",
            "ذكرى أليمة",
            "جرح عميق",
            "أثر نفسي"
        ]
        
        for indicator in trauma_indicators:
            if indicator in content:
                wounds.append({
                    "type": "psychological_trauma",
                    "description": indicator,
                    "severity": "متوسط إلى عالي"
                })
        
        return wounds
    
    async def _analyze_coping_mechanisms(self, content: str) -> List[Dict[str, Any]]:
        """تحليل آليات التأقلم في النص"""
        mechanisms = []
        
        coping_patterns = [
            "يهرب من المشكلة",
            "يواجه التحدي",
            "يطلب المساعدة",
            "يلجأ للعزلة",
            "يبحث عن الدعم"
        ]
        
        for pattern in coping_patterns:
            if pattern in content:
                mechanisms.append({
                    "strategy": pattern,
                    "effectiveness": "متغيرة حسب السياق"
                })
        
        return mechanisms
    
    async def _analyze_relationship_dynamics(self, content: str, profiles: List[PsychologicalProfile]) -> List[Dict[str, Any]]:
        """تحليل ديناميكيات العلاقات"""
        dynamics = []
        
        if len(profiles) >= 2:
            for i, profile1 in enumerate(profiles):
                for profile2 in profiles[i+1:]:
                    compatibility = self._assess_compatibility(profile1, profile2)
                    dynamics.append({
                        "character1": profile1.character_name,
                        "character2": profile2.character_name,
                        "compatibility_score": compatibility,
                        "potential_conflicts": self._predict_conflicts(profile1, profile2),
                        "relationship_type": self._determine_relationship_type(compatibility)
                    })
        
        return dynamics
    
    def _assess_compatibility(self, profile1: PsychologicalProfile, profile2: PsychologicalProfile) -> float:
        """تقييم التوافق بين شخصيتين"""
        compatibility = 0.5  # قيمة أساسية
        
        # التوافق في الشخصية
        if PersonalityType.EXTROVERT in profile1.personality_traits and PersonalityType.INTROVERT in profile2.personality_traits:
            compatibility += 0.1  # التكامل إيجابي
        
        # التوافق في الدوافع
        shared_motivations = len(set(profile1.core_motivations).intersection(set(profile2.core_motivations)))
        compatibility += shared_motivations * 0.1
        
        # التعارض في المخاوف
        shared_fears = len(set(profile1.fears_and_phobias).intersection(set(profile2.fears_and_phobias)))
        compatibility -= shared_fears * 0.05
        
        return max(0.0, min(1.0, compatibility))
    
    def _predict_conflicts(self, profile1: PsychologicalProfile, profile2: PsychologicalProfile) -> List[str]:
        """التنبؤ بالصراعات المحتملة"""
        conflicts = []
        
        # صراعات الشخصية
        if PersonalityType.THINKING in profile1.personality_traits and PersonalityType.FEELING in profile2.personality_traits:
            conflicts.append("تضارب في أسلوب اتخاذ القرارات")
        
        # صراعات الدوافع
        if "السلطة" in profile1.core_motivations and "السلطة" in profile2.core_motivations:
            conflicts.append("تنافس على السيطرة والقيادة")
        
        return conflicts
    
    def _determine_relationship_type(self, compatibility: float) -> str:
        """تحديد نوع العلاقة بناءً على التوافق"""
        if compatibility >= 0.8:
            return "علاقة متناغمة"
        elif compatibility >= 0.6:
            return "علاقة متوازنة"
        elif compatibility >= 0.4:
            return "علاقة متوترة"
        else:
            return "علاقة متصارعة"
    
    async def _develop_psychological_arcs(self, content: str, profiles: List[PsychologicalProfile]) -> List[CharacterDevelopment]:
        """تطوير أقواس التطور النفسي"""
        development_arcs = []
        
        for profile in profiles:
            arc = CharacterDevelopment(
                starting_state={
                    "psychological_wounds": profile.psychological_wounds,
                    "coping_mechanisms": [m.value for m in profile.coping_mechanisms],
                    "mental_health": profile.mental_health_status.value
                },
                key_events=self._identify_transformative_events(profile.character_name, content),
                psychological_changes=self._predict_psychological_changes(profile),
                growth_milestones=self._define_growth_milestones(profile),
                final_state=self._project_final_state(profile)
            )
            development_arcs.append(arc)
        
        return development_arcs
    
    def _identify_transformative_events(self, character_name: str, content: str) -> List[Dict[str, Any]]:
        """تحديد الأحداث المحورية"""
        events = []
        
        transformative_patterns = [
            "تغير جذري",
            "نقطة تحول",
            "إدراك مهم",
            "قرار مصيري",
            "تجربة محورية"
        ]
        
        for pattern in transformative_patterns:
            if pattern in content and character_name in content:
                events.append({
                    "event": pattern,
                    "impact": "عالي",
                    "timing": "منتصف الحكاية"
                })
        
        return events
    
    def _predict_psychological_changes(self, profile: PsychologicalProfile) -> List[str]:
        """التنبؤ بالتغيرات النفسية"""
        changes = []
        
        if profile.growth_potential > 0.6:
            changes.append("تطوير آليات تأقلم أكثر صحة")
            changes.append("زيادة الوعي الذاتي")
        
        if profile.mental_health_status != PsychologicalDisorder.NONE:
            changes.append("تحسن تدريجي في الصحة النفسية")
        
        if profile.psychological_wounds:
            changes.append("شفاء جزئي من الجروح النفسية")
        
        return changes
    
    def _define_growth_milestones(self, profile: PsychologicalProfile) -> List[str]:
        """تحديد معالم النمو"""
        milestones = [
            "الاعتراف بالمشكلة",
            "البحث عن المساعدة",
            "تطبيق استراتيجيات جديدة",
            "تحقيق تقدم ملموس",
            "الوصول لحالة أفضل"
        ]
        
        return milestones[:3]  # أهم 3 معالم
    
    def _project_final_state(self, profile: PsychologicalProfile) -> Dict[str, Any]:
        """توقع الحالة النهائية"""
        improvement_factor = profile.growth_potential
        
        return {
            "psychological_wounds": len(profile.psychological_wounds) * (1 - improvement_factor * 0.5),
            "mental_health_improvement": improvement_factor * 0.7,
            "relationship_skills": "محسّنة" if improvement_factor > 0.5 else "مستقرة",
            "overall_wellbeing": improvement_factor * 0.8
        }
    
    async def _suggest_realistic_responses(self, profiles: List[PsychologicalProfile], content: str) -> List[Dict[str, Any]]:
        """اقتراح ردود أفعال واقعية"""
        responses = []
        
        for profile in profiles:
            # ردود فعل للضغط
            if profile.mental_health_status == PsychologicalDisorder.ANXIETY:
                responses.append({
                    "character": profile.character_name,
                    "situation": "موقف ضاغط",
                    "realistic_response": "تسارع في النبض، تعرق، تجنب الموقف",
                    "coping_strategy": "تمارين التنفس أو الهروب"
                })
            
            # ردود فعل للصراع
            if PersonalityType.THINKING in profile.personality_traits:
                responses.append({
                    "character": profile.character_name,
                    "situation": "صراع عاطفي",
                    "realistic_response": "تحليل منطقي للموقف قبل التفاعل العاطفي",
                    "coping_strategy": "وضع قائمة إيجابيات وسلبيات"
                })
        
        return responses
    
    async def _detect_psychological_inconsistencies(self, content: str, profiles: List[PsychologicalProfile]) -> List[str]:
        """كشف التناقضات النفسية"""
        inconsistencies = []
        
        for profile in profiles:
            # تناقض بين الشخصية والسلوك
            if PersonalityType.INTROVERT in profile.personality_traits and "يحب الحفلات" in content:
                inconsistencies.append(f"{profile.character_name}: تناقض بين الانطوائية وحب الحفلات")
            
            # تناقض في آليات التأقلم
            if CopingMechanism.DENIAL in profile.coping_mechanisms and "يواجه المشاكل" in content:
                inconsistencies.append(f"{profile.character_name}: تناقض بين الإنكار ومواجهة المشاكل")
            
            # تغير مفاجئ غير مبرر
            if profile.mental_health_status == PsychologicalDisorder.DEPRESSION and "أصبح سعيداً فجأة" in content:
                inconsistencies.append(f"{profile.character_name}: تعافي سريع غير واقعي من الاكتئاب")
        
        return inconsistencies
    
    async def _generate_psychological_recommendations(self, profiles: List[PsychologicalProfile], 
                                                    emotional_patterns: List[Dict[str, Any]],
                                                    psychological_wounds: List[Dict[str, Any]],
                                                    inconsistencies: List[str]) -> List[str]:
        """إنتاج التوصيات النفسية"""
        recommendations = []
        
        # توصيات للشخصيات
        if not profiles:
            recommendations.append("تطوير ملفات نفسية أعمق للشخصيات")
        
        # توصيات للتناقضات
        if inconsistencies:
            recommendations.append("حل التناقضات النفسية في سلوك الشخصيات")
        
        # توصيات للنمو
        low_growth_characters = [p for p in profiles if p.growth_potential < 0.3]
        if low_growth_characters:
            recommendations.append("إضافة فرص نمو وتطور للشخصيات الجامدة")
        
        # توصيات عامة
        recommendations.extend([
            "تعميق الدوافع النفسية للشخصيات",
            "إضافة ردود أفعال عاطفية واقعية",
            "تطوير تدرجي ومنطقي للتغيرات النفسية"
        ])
        
        return recommendations[:5]
    
    def _calculate_confidence_score(self, profiles: List[PsychologicalProfile], 
                                   emotional_patterns: List[Dict[str, Any]],
                                   psychological_wounds: List[Dict[str, Any]]) -> float:
        """حساب درجة الثقة في التحليل"""
        base_score = 0.7
        
        # زيادة الثقة بناءً على عدد الشخصيات المحللة
        characters_bonus = min(0.2, len(profiles) * 0.05)
        
        # زيادة الثقة بناءً على وجود أنماط عاطفية
        patterns_bonus = min(0.1, len(emotional_patterns) * 0.02)
        
        # زيادة الثقة بناءً على تحديد الجروح النفسية
        wounds_bonus = min(0.1, len(psychological_wounds) * 0.02)
        
        final_score = base_score + characters_bonus + patterns_bonus + wounds_bonus
        return round(max(0.0, min(1.0, final_score)), 2)
    
    async def _generate_visual_data(self, profiles: List[PsychologicalProfile], 
                                   emotional_patterns: List[Dict[str, Any]],
                                   development_arcs: List[CharacterDevelopment]) -> Dict[str, Any]:
        """إنتاج البيانات المرئية للتحليل"""
        return {
            "personality_radar": {
                "type": "radar",
                "data": [
                    {
                        "character": profile.character_name,
                        "traits": {trait.value: 1 for trait in profile.personality_traits}
                    }
                    for profile in profiles
                ]
            },
            "emotional_timeline": {
                "type": "timeline",
                "data": emotional_patterns
            },
            "growth_trajectory": {
                "type": "line",
                "data": [
                    {
                        "character": profile.character_name,
                        "growth_potential": profile.growth_potential
                    }
                    for profile in profiles
                ]
            },
            "mental_health_distribution": {
                "type": "pie",
                "data": [
                    {"status": profile.mental_health_status.value, "count": 1}
                    for profile in profiles
                ]
            }
        }
    
    def _profile_to_dict(self, profile: PsychologicalProfile) -> Dict[str, Any]:
        """تحويل الملف النفسي إلى قاموس"""
        return {
            "character_name": profile.character_name,
            "personality_traits": [trait.value for trait in profile.personality_traits],
            "core_motivations": profile.core_motivations,
            "fears_and_phobias": profile.fears_and_phobias,
            "emotional_patterns": profile.emotional_patterns,
            "coping_mechanisms": [mechanism.value for mechanism in profile.coping_mechanisms],
            "psychological_wounds": profile.psychological_wounds,
            "mental_health_status": profile.mental_health_status.value,
            "behavioral_tendencies": profile.behavioral_tendencies,
            "relationship_patterns": profile.relationship_patterns,
            "growth_potential": profile.growth_potential
        }
    
    def _development_to_dict(self, development: CharacterDevelopment) -> Dict[str, Any]:
        """تحويل التطور النفسي إلى قاموس"""
        return {
            "starting_state": development.starting_state,
            "key_events": development.key_events,
            "psychological_changes": development.psychological_changes,
            "growth_milestones": development.growth_milestones,
            "final_state": development.final_state
        }
    
    def _load_personality_indicators(self) -> Dict[str, List[str]]:
        """تحميل مؤشرات الشخصية"""
        return {
            "extroversion": ["اجتماعي", "نشيط", "متكلم", "منفتح", "يحب الناس"],
            "introversion": ["هادئ", "متحفظ", "يفضل الوحدة", "يفكر كثيراً"],
            "thinking": ["منطقي", "عقلاني", "موضوعي", "يحلل"],
            "feeling": ["عاطفي", "حساس", "متعاطف", "يهتم بالآخرين"],
            "judging": ["منظم", "مخطط", "دقيق", "ملتزم"],
            "perceiving": ["مرن", "عفوي", "متكيف", "مفتوح الذهن"]
        }
    
    def _load_psychological_patterns(self) -> Dict[str, List[str]]:
        """تحميل الأنماط النفسية"""
        return {
            "defense_mechanisms": ["الإنكار", "الإسقاط", "التبرير", "الإزاحة"],
            "attachment_styles": ["آمن", "قلق", "تجنبي", "مضطرب"],
            "trauma_responses": ["فرط يقظة", "تجنب", "خدر عاطفي", "كوابيس"]
        }
    
    def _load_cultural_psychology(self) -> Dict[str, Any]:
        """تحميل علم النفس الثقافي العربي"""
        return {
            "collectivist_values": ["الأسرة أولاً", "احترام الكبار", "التضامن الاجتماعي"],
            "honor_concepts": ["الكرامة", "الشرف", "ماء الوجه", "السمعة"],
            "religious_coping": ["الصبر", "التوكل على الله", "الدعاء", "الاستغفار"],
            "emotional_expression": ["الكتمان", "التعبير غير المباشر", "الشعر والحكم"]
        }
    
    def _load_trauma_responses(self) -> Dict[str, List[str]]:
        """تحميل استجابات الصدمة"""
        return {
            "acute_stress": ["ذهول", "إنكار", "فرط نشاط", "تجمد"],
            "chronic_trauma": ["اكتئاب", "قلق", "اضطرابات نوم", "مشاكل تركيز"],
            "ptsd_symptoms": ["ذكريات تطفلية", "كوابيس", "تجنب المحفزات", "فرط يقظة"]
        }
    
    def _load_therapy_techniques(self) -> Dict[str, List[str]]:
        """تحميل تقنيات العلاج النفسي"""
        return {
            "cognitive_behavioral": ["إعادة هيكلة المعرفة", "تقنيات التأقلم", "حل المشكلات"],
            "psychodynamic": ["الاستبصار", "نقل المشاعر", "تحليل الأحلام"],
            "humanistic": ["القبول غير المشروط", "التعاطف", "الأصالة"],
            "cultural_methods": ["العلاج بالقرآن", "الإرشاد الديني", "العلاج الجماعي"]
        }
