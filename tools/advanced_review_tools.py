"""
أدوات المراجعة والتحرير المتقدمة - Advanced Review & Editing Tools
محرر بشري افتراضي متطور للكتابة العربية
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class ReviewLevel(Enum):
    """مستويات المراجعة"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"

class IssueType(Enum):
    """أنواع المشاكل"""
    GRAMMAR = "grammar"
    STYLE = "style"
    CONTENT = "content"
    STRUCTURE = "structure"
    CULTURAL = "cultural"
    NARRATIVE = "narrative"

class IssueSeverity(Enum):
    """درجة خطورة المشكلة"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ReviewIssue:
    """مشكلة في المراجعة"""
    id: str
    type: IssueType
    severity: IssueSeverity
    title: str
    description: str
    suggestion: str
    start_pos: int
    end_pos: int
    original_text: str
    suggested_text: str = ""
    confidence: float = 0.0
    auto_fixable: bool = False

@dataclass
class PlotEvent:
    """حدث في الحبكة"""
    id: str
    title: str
    description: str
    timestamp: str
    duration: Optional[str]
    location: str
    characters: List[str]
    importance: int  # 1-10
    event_type: str  # "action", "dialogue", "description", "conflict"
    dependencies: List[str]  # معرفات الأحداث التي تعتمد عليها

@dataclass
class Character:
    """شخصية في النص"""
    id: str
    name: str
    description: str
    role: str  # "main", "secondary", "minor"
    traits: List[str]
    arc: Dict[str, Any]  # تطور الشخصية
    appearances: List[Dict[str, Any]]  # مواضع ظهور الشخصية

class ArabicGrammarChecker:
    """مدقق النحو العربي المتقدم"""
    
    def __init__(self):
        self.grammar_rules = self._load_grammar_rules()
        self.morphology_patterns = self._load_morphology_patterns()
        self.rhetoric_patterns = self._load_rhetoric_patterns()
    
    def _load_grammar_rules(self) -> Dict[str, Any]:
        """تحميل قواعد النحو العربي"""
        return {
            "subject_verb_agreement": {
                "pattern": r"([\u0600-\u06FF]+)\s+([\u0600-\u06FF]+)",
                "description": "توافق الفعل مع الفاعل",
                "severity": IssueSeverity.ERROR
            },
            "article_usage": {
                "pattern": r"\s(ال[\u0600-\u06FF]+)\s+(ال[\u0600-\u06FF]+)",
                "description": "استخدام أداة التعريف",
                "severity": IssueSeverity.WARNING
            },
            "preposition_usage": {
                "pattern": r"(من|إلى|في|على|عن|مع)\s+(ال[\u0600-\u06FF]+)",
                "description": "استخدام حروف الجر",
                "severity": IssueSeverity.WARNING
            },
            "verb_tense_consistency": {
                "pattern": r"(كان|يكون|سيكون)",
                "description": "اتساق الأزمنة",
                "severity": IssueSeverity.ERROR
            }
        }
    
    def _load_morphology_patterns(self) -> Dict[str, Any]:
        """تحميل أنماط الصرف العربي"""
        return {
            "root_patterns": {
                "فعل": r"[\u0641][\u0639][\u0644]",
                "فاعل": r"[\u0641][\u0627][\u0639][\u0644]",
                "مفعول": r"[\u0645][\u0641][\u0639][\u0648][\u0644]"
            },
            "derived_forms": {
                "مصدر": ["تفعيل", "إفعال", "انفعال", "استفعال"],
                "صفة_مشبهة": ["فعيل", "فعال", "فعول"],
                "اسم_فاعل": ["فاعل", "مفعل", "فعال"],
                "اسم_مفعول": ["مفعول", "فعيل", "فعل"]
            }
        }
    
    def _load_rhetoric_patterns(self) -> Dict[str, Any]:
        """تحميل أنماط البلاغة العربية"""
        return {
            "سجع": {
                "pattern": r"([\u0600-\u06FF]+ان)\s+.*?([\u0600-\u06FF]+ان)",
                "description": "توافق فواصل الجمل",
                "enhancement": "يُحسن الإيقاع والجمالية"
            },
            "جناس": {
                "pattern": r"([\u0600-\u06FF]{3,})\s+.*?([\u0600-\u06FF]{3,})",
                "description": "تشابه في الأصوات مع اختلاف في المعنى",
                "enhancement": "يضفي موسيقية على النص"
            },
            "طباق": {
                "pattern": r"(الخير|النور|الحياة|السلام)\s+.*?(الشر|الظلام|الموت|الحرب)",
                "description": "الجمع بين المتضادات",
                "enhancement": "يبرز المعنى بالتضاد"
            },
            "استعارة": {
                "pattern": r"(بحر|نهر|جبل|شمس|قمر)\s+(من|في|على)\s+([\u0600-\u06FF]+)",
                "description": "استخدام مجازي للألفاظ",
                "enhancement": "يثري الخيال والصورة الأدبية"
            }
        }
    
    def check_grammar(self, text: str) -> List[ReviewIssue]:
        """فحص القواعد النحوية"""
        issues = []
        
        for rule_name, rule_data in self.grammar_rules.items():
            pattern = rule_data["pattern"]
            matches = list(re.finditer(pattern, text))
            
            for match in matches:
                # تحليل مبسط - في التطبيق الحقيقي نحتاج محلل نحوي متقدم
                issue = ReviewIssue(
                    id=f"grammar_{len(issues)}",
                    type=IssueType.GRAMMAR,
                    severity=rule_data["severity"],
                    title=f"مشكلة نحوية: {rule_name}",
                    description=rule_data["description"],
                    suggestion=f"راجع {rule_data['description']} في الموضع المحدد",
                    start_pos=match.start(),
                    end_pos=match.end(),
                    original_text=match.group(),
                    confidence=0.7,
                    auto_fixable=False
                )
                issues.append(issue)
        
        return issues
    
    def check_morphology(self, text: str) -> List[ReviewIssue]:
        """فحص الصرف"""
        issues = []
        words = text.split()
        
        for i, word in enumerate(words):
            # فحص الاشتقاق والتصريف
            if len(word) > 3:
                # فحص مبسط للجذور
                if not self._is_valid_arabic_word(word):
                    issue = ReviewIssue(
                        id=f"morphology_{i}",
                        type=IssueType.GRAMMAR,
                        severity=IssueSeverity.WARNING,
                        title="مشكلة صرفية محتملة",
                        description=f"الكلمة '{word}' قد تحتاج مراجعة صرفية",
                        suggestion="تأكد من صحة تصريف الكلمة",
                        start_pos=text.find(word),
                        end_pos=text.find(word) + len(word),
                        original_text=word,
                        confidence=0.5
                    )
                    issues.append(issue)
        
        return issues
    
    def _is_valid_arabic_word(self, word: str) -> bool:
        """فحص صحة الكلمة العربية (تحليل مبسط)"""
        # إزالة التشكيل والعلامات
        clean_word = re.sub(r'[\u064B-\u0652\u0670\u0640]', '', word)
        
        # فحص أن الكلمة تحتوي على أحرف عربية فقط
        arabic_pattern = r'^[\u0600-\u06FF]+$'
        return bool(re.match(arabic_pattern, clean_word))

class StyleAnalyzer:
    """محلل الأسلوب المتقدم"""
    
    def __init__(self):
        self.style_patterns = self._load_style_patterns()
        self.readability_metrics = self._load_readability_metrics()
    
    def _load_style_patterns(self) -> Dict[str, Any]:
        """تحميل أنماط الأسلوب"""
        return {
            "repetition": {
                "pattern": r"\b([\u0600-\u06FF]+)\b.*?\b\1\b",
                "description": "تكرار كلمات",
                "suggestion": "استخدم مرادفات لتجنب التكرار"
            },
            "long_sentences": {
                "max_words": 25,
                "description": "جمل طويلة جداً",
                "suggestion": "قسم الجملة لتحسين القراءة"
            },
            "short_sentences": {
                "min_words": 3,
                "description": "جمل قصيرة جداً",
                "suggestion": "أضف تفاصيل لإثراء المعنى"
            },
            "passive_voice": {
                "pattern": r"(تم|يتم|سيتم)\s+[\u0600-\u06FF]+",
                "description": "الإفراط في استخدام المبني للمجهول",
                "suggestion": "استخدم المبني للمعلوم لمزيد من الوضوح"
            }
        }
    
    def _load_readability_metrics(self) -> Dict[str, Any]:
        """تحميل مقاييس سهولة القراءة"""
        return {
            "avg_sentence_length": {"ideal_range": (10, 20)},
            "avg_word_length": {"ideal_range": (4, 7)},
            "vocabulary_diversity": {"min_ratio": 0.6},
            "paragraph_length": {"ideal_range": (3, 8)}
        }
    
    def analyze_style(self, text: str) -> List[ReviewIssue]:
        """تحليل الأسلوب"""
        issues = []
        
        # تحليل طول الجمل
        sentences = self._split_sentences(text)
        for i, sentence in enumerate(sentences):
            word_count = len(sentence.split())
            
            if word_count > self.style_patterns["long_sentences"]["max_words"]:
                issue = ReviewIssue(
                    id=f"style_long_sentence_{i}",
                    type=IssueType.STYLE,
                    severity=IssueSeverity.WARNING,
                    title="جملة طويلة",
                    description=self.style_patterns["long_sentences"]["description"],
                    suggestion=self.style_patterns["long_sentences"]["suggestion"],
                    start_pos=text.find(sentence),
                    end_pos=text.find(sentence) + len(sentence),
                    original_text=sentence,
                    confidence=0.8
                )
                issues.append(issue)
            
            elif word_count < self.style_patterns["short_sentences"]["min_words"]:
                issue = ReviewIssue(
                    id=f"style_short_sentence_{i}",
                    type=IssueType.STYLE,
                    severity=IssueSeverity.INFO,
                    title="جملة قصيرة",
                    description=self.style_patterns["short_sentences"]["description"],
                    suggestion=self.style_patterns["short_sentences"]["suggestion"],
                    start_pos=text.find(sentence),
                    end_pos=text.find(sentence) + len(sentence),
                    original_text=sentence,
                    confidence=0.6
                )
                issues.append(issue)
        
        # فحص التكرار
        repetition_issues = self._check_repetition(text)
        issues.extend(repetition_issues)
        
        # فحص المبني للمجهول
        passive_issues = self._check_passive_voice(text)
        issues.extend(passive_issues)
        
        return issues
    
    def _split_sentences(self, text: str) -> List[str]:
        """تقسيم النص إلى جمل"""
        # تقسيم بسيط بناءً على علامات الترقيم
        sentences = re.split(r'[.!?؟]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _check_repetition(self, text: str) -> List[ReviewIssue]:
        """فحص التكرار"""
        issues = []
        words = text.split()
        word_positions = {}
        
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\u0600-\u06FF]', '', word).lower()
            if len(clean_word) > 3:  # تجاهل الكلمات القصيرة
                if clean_word in word_positions:
                    # إذا تكررت الكلمة في نطاق قريب
                    if i - word_positions[clean_word][-1] < 10:
                        issue = ReviewIssue(
                            id=f"repetition_{i}",
                            type=IssueType.STYLE,
                            severity=IssueSeverity.WARNING,
                            title="تكرار كلمة",
                            description=f"تكرار الكلمة '{clean_word}'",
                            suggestion="استخدم مرادفاً لتجنب التكرار",
                            start_pos=text.find(word),
                            end_pos=text.find(word) + len(word),
                            original_text=word,
                            confidence=0.7
                        )
                        issues.append(issue)
                    word_positions[clean_word].append(i)
                else:
                    word_positions[clean_word] = [i]
        
        return issues
    
    def _check_passive_voice(self, text: str) -> List[ReviewIssue]:
        """فحص المبني للمجهول"""
        issues = []
        pattern = self.style_patterns["passive_voice"]["pattern"]
        matches = list(re.finditer(pattern, text))
        
        for match in matches:
            issue = ReviewIssue(
                id=f"passive_{len(issues)}",
                type=IssueType.STYLE,
                severity=IssueSeverity.INFO,
                title="استخدام المبني للمجهول",
                description=self.style_patterns["passive_voice"]["description"],
                suggestion=self.style_patterns["passive_voice"]["suggestion"],
                start_pos=match.start(),
                end_pos=match.end(),
                original_text=match.group(),
                confidence=0.6
            )
            issues.append(issue)
        
        return issues

class NarrativeAnalyzer:
    """محلل السرد والحبكة"""
    
    def __init__(self):
        self.narrative_patterns = self._load_narrative_patterns()
        self.pov_indicators = self._load_pov_indicators()
    
    def _load_narrative_patterns(self) -> Dict[str, Any]:
        """تحميل أنماط السرد"""
        return {
            "dialogue_tags": {
                "pattern": r"(قال|قالت|همس|صرخ|أجاب|رد)(\s+[\u0600-\u06FF]+)?:",
                "description": "علامات الحوار"
            },
            "time_transitions": {
                "pattern": r"(فجأة|بعد ذلك|في اليوم التالي|منذ|الآن|حينئذ)",
                "description": "انتقالات زمنية"
            },
            "scene_changes": {
                "pattern": r"(في مكان آخر|في نفس الوقت|بينما|من جهة أخرى)",
                "description": "تغييرات المشهد"
            },
            "internal_monologue": {
                "pattern": r"(فكر|تساءل|استغرب|تذكر)\s+(في نفسه|بينه وبين نفسه)",
                "description": "المونولوج الداخلي"
            }
        }
    
    def _load_pov_indicators(self) -> Dict[str, List[str]]:
        """تحميل مؤشرات وجهة النظر"""
        return {
            "first_person": ["أنا", "لي", "بي", "مني", "إلي"],
            "second_person": ["أنت", "لك", "بك", "منك", "إليك"],
            "third_person": ["هو", "هي", "له", "لها", "بهم", "منهم"]
        }
    
    def analyze_narrative_structure(self, text: str) -> Dict[str, Any]:
        """تحليل هيكل السرد"""
        analysis = {
            "pov_analysis": self._analyze_point_of_view(text),
            "dialogue_analysis": self._analyze_dialogue(text),
            "pacing_analysis": self._analyze_pacing(text),
            "scene_structure": self._analyze_scene_structure(text),
            "character_presence": self._analyze_character_presence(text)
        }
        
        return analysis
    
    def _analyze_point_of_view(self, text: str) -> Dict[str, Any]:
        """تحليل وجهة النظر"""
        pov_counts = {
            "first_person": 0,
            "second_person": 0,
            "third_person": 0
        }
        
        for pov_type, indicators in self.pov_indicators.items():
            for indicator in indicators:
                pov_counts[pov_type] += len(re.findall(r'\b' + indicator + r'\b', text))
        
        total_pov = sum(pov_counts.values())
        if total_pov > 0:
            pov_percentages = {k: (v / total_pov) * 100 for k, v in pov_counts.items()}
            dominant_pov = max(pov_percentages, key=pov_percentages.get)
        else:
            pov_percentages = {k: 0 for k in pov_counts.keys()}
            dominant_pov = "غير محدد"
        
        return {
            "dominant_pov": dominant_pov,
            "percentages": pov_percentages,
            "consistency": max(pov_percentages.values()) > 70,
            "raw_counts": pov_counts
        }
    
    def _analyze_dialogue(self, text: str) -> Dict[str, Any]:
        """تحليل الحوار"""
        dialogue_pattern = self.narrative_patterns["dialogue_tags"]["pattern"]
        dialogue_matches = list(re.finditer(dialogue_pattern, text))
        
        total_words = len(text.split())
        dialogue_words = 0
        
        # تقدير كلمات الحوار (تحليل مبسط)
        for match in dialogue_matches:
            # البحث عن النص بعد علامة الحوار حتى نقطة النهاية
            start_pos = match.end()
            dialogue_end = text.find('.', start_pos)
            if dialogue_end == -1:
                dialogue_end = text.find('!', start_pos)
            if dialogue_end == -1:
                dialogue_end = text.find('؟', start_pos)
            
            if dialogue_end > start_pos:
                dialogue_text = text[start_pos:dialogue_end]
                dialogue_words += len(dialogue_text.split())
        
        dialogue_ratio = (dialogue_words / total_words) * 100 if total_words > 0 else 0
        
        return {
            "dialogue_count": len(dialogue_matches),
            "dialogue_ratio": dialogue_ratio,
            "dialogue_density": "عالية" if dialogue_ratio > 40 else "متوسطة" if dialogue_ratio > 20 else "منخفضة"
        }
    
    def _analyze_pacing(self, text: str) -> Dict[str, Any]:
        """تحليل إيقاع السرد"""
        sentences = self._split_sentences(text)
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        
        avg_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # تحليل التنوع في طول الجمل
        short_sentences = sum(1 for length in sentence_lengths if length < 8)
        medium_sentences = sum(1 for length in sentence_lengths if 8 <= length <= 15)
        long_sentences = sum(1 for length in sentence_lengths if length > 15)
        
        total_sentences = len(sentence_lengths)
        
        pacing_analysis = {
            "avg_sentence_length": avg_length,
            "sentence_distribution": {
                "short": (short_sentences / total_sentences) * 100 if total_sentences > 0 else 0,
                "medium": (medium_sentences / total_sentences) * 100 if total_sentences > 0 else 0,
                "long": (long_sentences / total_sentences) * 100 if total_sentences > 0 else 0
            },
            "pacing_assessment": self._assess_pacing(avg_length, sentence_lengths)
        }
        
        return pacing_analysis
    
    def _assess_pacing(self, avg_length: float, lengths: List[int]) -> str:
        """تقييم إيقاع السرد"""
        if avg_length < 8:
            return "سريع - جمل قصيرة تخلق إيقاعاً سريعاً"
        elif avg_length > 15:
            return "بطيء - جمل طويلة تخلق إيقاعاً متأمل"
        else:
            # فحص التنوع
            if len(set(lengths)) / len(lengths) > 0.6:
                return "متوازن - تنوع جيد في طول الجمل"
            else:
                return "رتيب - قلة تنوع في طول الجمل"
    
    def _analyze_scene_structure(self, text: str) -> Dict[str, Any]:
        """تحليل هيكل المشاهد"""
        scene_pattern = self.narrative_patterns["scene_changes"]["pattern"]
        time_pattern = self.narrative_patterns["time_transitions"]["pattern"]
        
        scene_changes = list(re.finditer(scene_pattern, text))
        time_transitions = list(re.finditer(time_pattern, text))
        
        return {
            "scene_changes": len(scene_changes),
            "time_transitions": len(time_transitions),
            "structural_markers": len(scene_changes) + len(time_transitions),
            "scene_length_avg": len(text.split()) / (len(scene_changes) + 1) if scene_changes else len(text.split())
        }
    
    def _analyze_character_presence(self, text: str) -> Dict[str, Any]:
        """تحليل حضور الشخصيات"""
        # أسماء شائعة للشخصيات
        character_patterns = [
            r'\b(محمد|أحمد|فاطمة|عائشة|خالد|سارة|مريم|يوسف|علي|حسن|ليلى|زينب)\b',
            r'\b(الطبيب|المعلم|الكاتب|الشاعر|الأب|الأم|الابن|البنت)\b',
            r'\b(صديق|جار|زميل|معلم|طالب)\b'
        ]
        
        character_mentions = {}
        
        for pattern in character_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                character_mentions[match] = character_mentions.get(match, 0) + 1
        
        return {
            "characters_found": len(character_mentions),
            "character_mentions": character_mentions,
            "main_characters": [char for char, count in character_mentions.items() if count >= 3]
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """تقسيم النص إلى جمل"""
        sentences = re.split(r'[.!?؟]', text)
        return [s.strip() for s in sentences if s.strip()]

class PlotTimelineAnalyzer:
    """محلل الخط الزمني للحبكة"""
    
    def __init__(self):
        self.time_indicators = self._load_time_indicators()
        self.event_patterns = self._load_event_patterns()
    
    def _load_time_indicators(self) -> Dict[str, str]:
        """تحميل مؤشرات الزمن"""
        return {
            "past": r"(كان|كانت|حدث|وقع|تم|انتهى|مات|ولد)",
            "present": r"(يكون|تكون|يحدث|يقع|يتم|ينتهي|يموت|يولد)",
            "future": r"(سيكون|ستكون|سيحدث|سيقع|سيتم|سينتهي|سيموت|سيولد)",
            "sequence": r"(أولاً|ثانياً|ثالثاً|أخيراً|بعد ذلك|قبل ذلك|في البداية|في النهاية)",
            "duration": r"(ساعة|يوم|أسبوع|شهر|سنة|لحظة|دقيقة|عام|فترة|مدة)"
        }
    
    def _load_event_patterns(self) -> Dict[str, str]:
        """تحميل أنماط الأحداث"""
        return {
            "action": r"(ذهب|جاء|دخل|خرج|أخذ|أعطى|فعل|عمل|ركض|قفز)",
            "dialogue": r"(قال|قالت|تحدث|تكلم|أجاب|رد|همس|صرخ)",
            "thought": r"(فكر|تذكر|تساءل|استغرب|تأمل|اعتقد)",
            "emotion": r"(فرح|حزن|غضب|خاف|تعجب|أحب|كره|قلق)",
            "conflict": r"(صراع|قتال|خلاف|نزاع|مشكلة|أزمة|تحدي)"
        }
    
    def analyze_timeline(self, text: str) -> Dict[str, Any]:
        """تحليل الخط الزمني"""
        events = self._extract_events(text)
        timeline = self._build_timeline(events)
        gaps = self._find_timeline_gaps(timeline)
        conflicts = self._find_temporal_conflicts(timeline)
        
        return {
            "events": events,
            "timeline": timeline,
            "gaps": gaps,
            "conflicts": conflicts,
            "timeline_coherence": len(conflicts) == 0
        }
    
    def _extract_events(self, text: str) -> List[PlotEvent]:
        """استخراج الأحداث من النص"""
        events = []
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            event_type = self._classify_event_type(sentence)
            if event_type:
                time_info = self._extract_time_info(sentence)
                characters = self._extract_characters_from_sentence(sentence)
                
                event = PlotEvent(
                    id=f"event_{i}",
                    title=sentence[:50] + "..." if len(sentence) > 50 else sentence,
                    description=sentence,
                    timestamp=time_info.get("timestamp", f"seq_{i}"),
                    duration=time_info.get("duration"),
                    location=self._extract_location(sentence),
                    characters=characters,
                    importance=self._assess_importance(sentence),
                    event_type=event_type,
                    dependencies=[]
                )
                events.append(event)
        
        return events
    
    def _classify_event_type(self, sentence: str) -> Optional[str]:
        """تصنيف نوع الحدث"""
        for event_type, pattern in self.event_patterns.items():
            if re.search(pattern, sentence):
                return event_type
        return None
    
    def _extract_time_info(self, sentence: str) -> Dict[str, str]:
        """استخراج المعلومات الزمنية"""
        time_info = {}
        
        # البحث عن مؤشرات الزمن
        for time_type, pattern in self.time_indicators.items():
            matches = re.findall(pattern, sentence)
            if matches:
                time_info["type"] = time_type
                time_info["indicators"] = matches
                
                # محاولة استخراج timestamp مبسط
                if time_type in ["past", "present", "future"]:
                    time_info["timestamp"] = time_type
        
        return time_info
    
    def _extract_characters_from_sentence(self, sentence: str) -> List[str]:
        """استخراج الشخصيات من الجملة"""
        character_patterns = [
            r'\b(محمد|أحمد|فاطمة|عائشة|خالد|سارة|مريم|يوسف|علي|حسن|ليلى|زينب)\b',
            r'\b(الرجل|المرأة|الطفل|الشاب|الفتاة|الرجل العجوز|المرأة العجوز)\b'
        ]
        
        characters = []
        for pattern in character_patterns:
            matches = re.findall(pattern, sentence)
            characters.extend(matches)
        
        return list(set(characters))
    
    def _extract_location(self, sentence: str) -> str:
        """استخراج الموقع"""
        location_patterns = [
            r'\b(في|بـ|إلى|من)\s+([\u0600-\u06FF\s]+?)\s+(?=[\u0600-\u06FF]+)',
            r'\b(البيت|المنزل|المكتب|المدرسة|الجامعة|المستشفى|السوق|الشارع)\b'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, sentence)
            if matches:
                return matches[0] if isinstance(matches[0], str) else matches[0][-1]
        
        return "غير محدد"
    
    def _assess_importance(self, sentence: str) -> int:
        """تقييم أهمية الحدث (1-10)"""
        importance_indicators = {
            r'(مات|قتل|ولد|تزوج|طلق)': 9,  # أحداث حياتية مهمة
            r'(قرر|اختار|غير|بدل)': 7,     # قرارات مهمة
            r'(وصل|غادر|دخل|خرج)': 5,      # حركة وانتقال
            r'(قال|تحدث|أجاب)': 3,        # حوار عادي
            r'(فكر|تذكر|تأمل)': 4          # تأملات داخلية
        }
        
        for pattern, score in importance_indicators.items():
            if re.search(pattern, sentence):
                return score
        
        return 2  # أهمية افتراضية منخفضة
    
    def _build_timeline(self, events: List[PlotEvent]) -> Dict[str, Any]:
        """بناء الخط الزمني"""
        # تجميع الأحداث حسب الوقت
        timeline_groups = {}
        
        for event in events:
            timestamp = event.timestamp
            if timestamp not in timeline_groups:
                timeline_groups[timestamp] = []
            timeline_groups[timestamp].append(event)
        
        # ترتيب الأحداث
        sorted_timestamps = sorted(timeline_groups.keys())
        
        return {
            "groups": timeline_groups,
            "chronological_order": sorted_timestamps,
            "total_events": len(events)
        }
    
    def _find_timeline_gaps(self, timeline: Dict[str, Any]) -> List[Dict[str, str]]:
        """العثور على فجوات في الخط الزمني"""
        gaps = []
        timestamps = timeline["chronological_order"]
        
        for i in range(len(timestamps) - 1):
            current = timestamps[i]
            next_timestamp = timestamps[i + 1]
            
            # فحص مبسط للفجوات
            if current.startswith("seq_") and next_timestamp.startswith("seq_"):
                current_seq = int(current.split("_")[1])
                next_seq = int(next_timestamp.split("_")[1])
                
                if next_seq - current_seq > 1:
                    gaps.append({
                        "type": "sequence_gap",
                        "description": f"فجوة محتملة بين الحدث {current_seq} والحدث {next_seq}",
                        "suggestion": "قد تحتاج لربط الأحداث بشكل أوضح"
                    })
        
        return gaps
    
    def _find_temporal_conflicts(self, timeline: Dict[str, Any]) -> List[Dict[str, str]]:
        """العثور على تضارب زمني"""
        conflicts = []
        
        # فحص بسيط للتضارب
        groups = timeline["groups"]
        for timestamp, events in groups.items():
            if len(events) > 3:  # عدد كبير من الأحداث في نفس الوقت
                conflicts.append({
                    "type": "overcrowded_timestamp",
                    "description": f"عدد كبير من الأحداث ({len(events)}) في {timestamp}",
                    "suggestion": "فكر في توزيع الأحداث زمنياً"
                })
        
        return conflicts
    
    def _split_sentences(self, text: str) -> List[str]:
        """تقسيم النص إلى جمل"""
        sentences = re.split(r'[.!?؟]', text)
        return [s.strip() for s in sentences if s.strip()]

class AdvancedReviewEngine:
    """محرك المراجعة المتقدم"""
    
    def __init__(self):
        self.grammar_checker = ArabicGrammarChecker()
        self.style_analyzer = StyleAnalyzer()
        self.narrative_analyzer = NarrativeAnalyzer()
        self.plot_analyzer = PlotTimelineAnalyzer()
    
    def comprehensive_review(self, text: str, review_level: ReviewLevel = ReviewLevel.ADVANCED) -> Dict[str, Any]:
        """مراجعة شاملة للنص"""
        review_start_time = datetime.now()
        
        # فحوصات أساسية
        grammar_issues = self.grammar_checker.check_grammar(text)
        morphology_issues = self.grammar_checker.check_morphology(text)
        style_issues = self.style_analyzer.analyze_style(text)
        
        # تحليلات متقدمة
        narrative_analysis = self.narrative_analyzer.analyze_narrative_structure(text)
        plot_analysis = self.plot_analyzer.analyze_timeline(text)
        
        # إحصائيات عامة
        text_stats = self._calculate_text_statistics(text)
        
        # تقييم الجودة الإجمالية
        quality_score = self._calculate_quality_score(
            grammar_issues, style_issues, narrative_analysis, plot_analysis, text_stats
        )
        
        review_end_time = datetime.now()
        review_duration = (review_end_time - review_start_time).total_seconds()
        
        return {
            "review_metadata": {
                "review_level": review_level.value,
                "review_time": review_end_time.isoformat(),
                "duration_seconds": review_duration,
                "text_length": len(text),
                "word_count": len(text.split())
            },
            "grammar_issues": [issue.__dict__ for issue in grammar_issues],
            "morphology_issues": [issue.__dict__ for issue in morphology_issues],
            "style_issues": [issue.__dict__ for issue in style_issues],
            "narrative_analysis": narrative_analysis,
            "plot_analysis": plot_analysis,
            "text_statistics": text_stats,
            "quality_assessment": quality_score,
            "recommendations": self._generate_recommendations(
                grammar_issues, style_issues, narrative_analysis, plot_analysis
            )
        }
    
    def _calculate_text_statistics(self, text: str) -> Dict[str, Any]:
        """حساب إحصائيات النص"""
        words = text.split()
        sentences = re.split(r'[.!?؟]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        unique_words = set(word.lower() for word in words if len(word) > 2)
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "avg_sentences_per_paragraph": len(sentences) / len(paragraphs) if paragraphs else 0,
            "vocabulary_diversity": len(unique_words) / len(words) if words else 0,
            "readability_metrics": {
                "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
                "complex_words": sum(1 for word in words if len(word) > 7),
                "simple_words": sum(1 for word in words if len(word) <= 4)
            }
        }
    
    def _calculate_quality_score(self, grammar_issues: List[ReviewIssue], 
                                style_issues: List[ReviewIssue],
                                narrative_analysis: Dict[str, Any],
                                plot_analysis: Dict[str, Any],
                                text_stats: Dict[str, Any]) -> Dict[str, Any]:
        """حساب نقاط الجودة الإجمالية"""
        
        # نقاط القواعد (40 نقطة)
        grammar_score = max(0, 40 - len(grammar_issues) * 5)
        
        # نقاط الأسلوب (30 نقطة)
        style_score = max(0, 30 - len(style_issues) * 3)
        
        # نقاط السرد (20 نقطة)
        narrative_score = 20
        if not narrative_analysis["pov_analysis"]["consistency"]:
            narrative_score -= 5
        if narrative_analysis["dialogue_analysis"]["dialogue_ratio"] < 10:
            narrative_score -= 3
        
        # نقاط الحبكة (10 نقاط)
        plot_score = 10
        if not plot_analysis["timeline_coherence"]:
            plot_score -= 5
        if len(plot_analysis["gaps"]) > 2:
            plot_score -= 3
        
        total_score = grammar_score + style_score + narrative_score + plot_score
        
        # تحديد التصنيف
        if total_score >= 90:
            grade = "ممتاز"
        elif total_score >= 80:
            grade = "جيد جداً"
        elif total_score >= 70:
            grade = "جيد"
        elif total_score >= 60:
            grade = "مقبول"
        else:
            grade = "يحتاج تحسين"
        
        return {
            "total_score": total_score,
            "max_score": 100,
            "percentage": total_score,
            "grade": grade,
            "breakdown": {
                "grammar": grammar_score,
                "style": style_score,
                "narrative": narrative_score,
                "plot": plot_score
            }
        }
    
    def _generate_recommendations(self, grammar_issues: List[ReviewIssue],
                                 style_issues: List[ReviewIssue],
                                 narrative_analysis: Dict[str, Any],
                                 plot_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """توليد توصيات التحسين"""
        recommendations = []
        
        # توصيات القواعد
        if len(grammar_issues) > 5:
            recommendations.append({
                "category": "القواعد",
                "priority": "عالية",
                "suggestion": "راجع القواعد النحوية والصرفية، يوجد عدد كبير من الأخطاء",
                "action": "استخدم مدقق نحوي أو استشر مختص في اللغة العربية"
            })
        
        # توصيات الأسلوب
        if len(style_issues) > 3:
            recommendations.append({
                "category": "الأسلوب",
                "priority": "متوسطة",
                "suggestion": "حسن الأسلوب عبر تنويع طول الجمل وتجنب التكرار",
                "action": "اقرأ نصوص كتاب مشهورين وحلل أساليبهم"
            })
        
        # توصيات السرد
        if not narrative_analysis["pov_analysis"]["consistency"]:
            recommendations.append({
                "category": "السرد",
                "priority": "عالية",
                "suggestion": "حافظ على ثبات وجهة النظر في السرد",
                "action": "راجع النص واختر وجهة نظر واحدة والتزم بها"
            })
        
        # توصيات الحبكة
        if len(plot_analysis["gaps"]) > 0:
            recommendations.append({
                "category": "الحبكة",
                "priority": "متوسطة",
                "suggestion": "اربط الأحداث بشكل أوضح لتجنب الفجوات الزمنية",
                "action": "أضف انتقالات زمنية ومكانية واضحة"
            })
        
        return recommendations
