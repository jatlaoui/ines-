"""
مفسر الأحلام والرموز
Dream & Symbol Interpreter - Professional tool for symbolic depth and meaning

أداة متخصصة لإضافة عمق رمزي ونفسي للنصوص:
- توليد أحلام رمزية مرتبطة بحالة الشخصية
- تحليل الرموز والدلالات النفسية والثقافية
- ربط الأحلام بتطور الأحداث
- تفسير الرموز وفق التراث العربي والإسلامي
"""

import asyncio
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SymbolCategory(Enum):
    """فئات الرموز"""
    NATURE = "nature"  # الطبيعة
    ANIMALS = "animals"  # الحيوانات
    COLORS = "colors"  # الألوان
    NUMBERS = "numbers"  # الأرقام
    RELIGIOUS = "religious"  # ديني
    MYTHOLOGICAL = "mythological"  # أسطوري
    PERSONAL = "personal"  # شخصي
    CULTURAL = "cultural"  # ثقافي

class DreamType(Enum):
    """أنواع الأحلام"""
    PROPHETIC = "prophetic"  # نبوئية
    PSYCHOLOGICAL = "psychological"  # نفسية
    SYMBOLIC = "symbolic"  # رمزية
    NIGHTMARE = "nightmare"  # كابوس
    LUCID = "lucid"  # واعية
    RECURRING = "recurring"  # متكررة

class SymbolInterpretation(Enum):
    """تفسيرات الرموز"""
    POSITIVE = "positive"  # إيجابي
    NEGATIVE = "negative"  # سلبي
    NEUTRAL = "neutral"  # محايد
    WARNING = "warning"  # تحذيري
    GUIDANCE = "guidance"  # إرشادي

@dataclass
class Symbol:
    """رمز وتفسيره"""
    name: str
    category: SymbolCategory
    arabic_meaning: str
    islamic_interpretation: str
    psychological_meaning: str
    cultural_context: str
    emotional_association: str
    interpretation_type: SymbolInterpretation

@dataclass
class Dream:
    """حلم وتفاصيله"""
    dreamer: str
    dream_content: str
    symbols_present: List[str]
    dream_type: DreamType
    emotional_tone: str
    main_themes: List[str]
    interpretation: str
    psychological_significance: str
    narrative_function: str

@dataclass
class SymbolicPattern:
    """نمط رمزي"""
    pattern_name: str
    symbols_involved: List[str]
    meaning: str
    cultural_significance: str
    usage_context: str
    effectiveness_score: float

class DreamSymbolInterpreter:
    """مفسر الأحلام والرموز المتقدم"""
    
    def __init__(self):
        self.symbol_database = self._load_symbol_database()
        self.dream_patterns = self._load_dream_patterns()
        self.islamic_interpretations = self._load_islamic_interpretations()
        self.psychological_meanings = self._load_psychological_meanings()
        self.cultural_symbols = self._load_cultural_symbols()
        self.narrative_functions = self._load_narrative_functions()
    
    def get_name(self) -> str:
        return "مفسر الأحلام والرموز"
    
    def get_description(self) -> str:
        return "أداة متخصصة لتفسير الرموز والأحلام وإضافة العمق الرمزي للنصوص الأدبية"
    
    def get_features(self) -> List[str]:
        return [
            "تفسير الرموز والإشارات",
            "تحليل الأحلام الأدبية",
            "ربط الرموز بالسياق النفسي",
            "التفسير الثقافي والديني",
            "إنتاج محتوى رمزي جديد"
        ]
    
    def get_supported_formats(self) -> List[str]:
        return ["text", "dream_sequence", "symbolic_analysis"]
    
    def get_output_types(self) -> List[str]:
        return ["analysis", "interpretations", "dream_content", "recommendations"]
    
    async def analyze(self, content: str, context: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """التحليل الشامل للأحلام والرموز"""
        try:
            # تحليل الرموز الموجودة
            symbols_found = await self._extract_symbols(content)
            
            # تفسير الرموز المكتشفة
            symbol_interpretations = await self._interpret_symbols(symbols_found, content)
            
            # تحليل الأحلام الموجودة
            dreams_found = await self._extract_dreams(content)
            
            # تفسير الأحلام
            dream_interpretations = await self._interpret_dreams(dreams_found, content)
            
            # تحليل الأنماط الرمزية
            symbolic_patterns = await self._analyze_symbolic_patterns(symbols_found, content)
            
            # ربط الرموز بالسياق النفسي
            psychological_connections = await self._connect_psychology_symbols(content, symbols_found)
            
            # تحليل الوظيفة السردية للرموز
            narrative_functions = await self._analyze_narrative_functions(symbols_found, dreams_found, content)
            
            # إنتاج محتوى رمزي جديد
            suggested_symbols = await self._suggest_new_symbols(content, context)
            
            # إنتاج أحلام مقترحة
            suggested_dreams = await self._generate_dream_sequences(content, context)
            
            # إنتاج التوصيات
            recommendations = await self._generate_symbolic_recommendations(
                symbols_found, dreams_found, symbolic_patterns, psychological_connections
            )
            
            # حساب درجة الثقة
            confidence_score = self._calculate_confidence_score(
                symbols_found, dreams_found, symbolic_patterns
            )
            
            # إنشاء البيانات المرئية
            visual_data = await self._generate_visual_data(
                symbols_found, dreams_found, symbolic_patterns, symbol_interpretations
            )
            
            return {
                "analysis": {
                    "symbols_detected": len(symbols_found),
                    "dreams_found": len(dreams_found),
                    "symbolic_patterns": len(symbolic_patterns),
                    "psychological_connections": len(psychological_connections),
                    "symbolic_density": self._calculate_symbolic_density(symbols_found, content),
                    "cultural_authenticity": self._assess_cultural_authenticity(symbols_found)
                },
                "symbols_found": [self._symbol_to_dict(symbol) for symbol in symbols_found],
                "symbol_interpretations": symbol_interpretations,
                "dreams_found": [self._dream_to_dict(dream) for dream in dreams_found],
                "dream_interpretations": dream_interpretations,
                "symbolic_patterns": [self._pattern_to_dict(pattern) for pattern in symbolic_patterns],
                "psychological_connections": psychological_connections,
                "narrative_functions": narrative_functions,
                "suggested_symbols": suggested_symbols,
                "suggested_dreams": suggested_dreams,
                "recommendations": recommendations,
                "confidence_score": confidence_score,
                "visual_data": visual_data,
                "metadata": {
                    "analysis_type": "dream_symbol_interpretation",
                    "processing_time": datetime.now().isoformat(),
                    "cultural_framework": "arabic_islamic"
                }
            }
            
        except Exception as e:
            raise Exception(f"خطأ في تفسير الأحلام والرموز: {str(e)}")
    
    async def _extract_symbols(self, content: str) -> List[Symbol]:
        """استخراج الرموز من النص"""
        symbols = []
        
        # رموز الطبيعة
        nature_symbols = {
            "الشمس": ("النور والحياة", "الهداية الإلهية", "الوعي والوضوح", "رمز القوة والسلطان"),
            "القمر": ("الجمال والأنوثة", "التقلب والتغيير", "اللاوعي والغموض", "رمز الليل والسكون"),
            "النجوم": ("الأمل والطموح", "الهداية في الظلام", "الأحلام والرغبات", "رمز المصير"),
            "البحر": ("العمق واللامحدود", "المجهول والغموض", "العواطف الجارفة", "رمز الحياة"),
            "الجبل": ("الثبات والقوة", "التحدي والصعوبة", "الرسوخ والاستقرار", "رمز العظمة"),
            "الريح": ("التغيير والحركة", "الرسالة الإلهية", "الحرية والانطلاق", "رمز القدر"),
            "المطر": ("الرحمة والبركة", "التطهير والنماء", "الحياة الجديدة", "رمز الخير"),
            "النار": ("الطاقة والحيوية", "التطهير والابتلاء", "الشغف والرغبة", "رمز القوة")
        }
        
        for symbol_name, meanings in nature_symbols.items():
            if symbol_name in content:
                symbol = Symbol(
                    name=symbol_name,
                    category=SymbolCategory.NATURE,
                    arabic_meaning=meanings[0],
                    islamic_interpretation=meanings[1],
                    psychological_meaning=meanings[2],
                    cultural_context=meanings[3],
                    emotional_association=self._determine_emotional_association(symbol_name),
                    interpretation_type=self._determine_interpretation_type(symbol_name)
                )
                symbols.append(symbol)
        
        # رموز الحيوانات
        animal_symbols = {
            "الأسد": ("الشجاعة والقوة", "الملك والسلطان", "الثقة بالنفس", "رمز القيادة"),
            "النسر": ("العلو والسمو", "الرؤية الثاقبة", "الحرية والاستقلال", "رمز الفخر"),
            "الحمامة": ("السلام والطهارة", "الروح القدس", "الحب والوفاء", "رمز الأمل"),
            "الذئب": ("الخطر والمكر", "الوحشية والعدوان", "الخوف والقلق", "رمز التهديد"),
            "الغزال": ("الجمال والرقة", "السرعة والرشاقة", "النعومة والرقة", "رمز الأنوثة"),
            "الثعبان": ("الحكمة والخداع", "التجديد والتحول", "الخوف والخطر", "رمز المكر"),
            "الصقر": ("الحدة والدقة", "الصيد والقنص", "الحرية والنبل", "رمز الفروسية"),
            "الحصان": ("النبل والكرامة", "الجهاد والحرب", "القوة والسرعة", "رمز الفخر")
        }
        
        for symbol_name, meanings in animal_symbols.items():
            if symbol_name in content:
                symbol = Symbol(
                    name=symbol_name,
                    category=SymbolCategory.ANIMALS,
                    arabic_meaning=meanings[0],
                    islamic_interpretation=meanings[1],
                    psychological_meaning=meanings[2],
                    cultural_context=meanings[3],
                    emotional_association=self._determine_emotional_association(symbol_name),
                    interpretation_type=self._determine_interpretation_type(symbol_name)
                )
                symbols.append(symbol)
        
        # رموز الألوان
        color_symbols = {
            "الأبيض": ("الطهارة والنقاء", "الإيمان والتقوى", "البراءة والصفاء", "رمز الخير"),
            "الأسود": ("القوة والجلال", "الليل والغموض", "الحزن والموت", "رمز الهيبة"),
            "الأحمر": ("الحب والشغف", "الدم والحياة", "الغضب والثورة", "رمز القوة"),
            "الأخضر": ("الطبيعة والنمو", "الجنة والخلود", "الأمل والتجديد", "رمز البركة"),
            "الأزرق": ("السماء والعلو", "السكينة والهدوء", "الحكمة والعمق", "رمز الصفاء"),
            "الذهبي": ("الثراء والنبل", "النور الإلهي", "القيمة والأهمية", "رمز المجد"),
            "الفضي": ("النقاء والوضوح", "القمر والليل", "الرقة والجمال", "رمز الطهارة")
        }
        
        for symbol_name, meanings in color_symbols.items():
            if symbol_name in content:
                symbol = Symbol(
                    name=symbol_name,
                    category=SymbolCategory.COLORS,
                    arabic_meaning=meanings[0],
                    islamic_interpretation=meanings[1],
                    psychological_meaning=meanings[2],
                    cultural_context=meanings[3],
                    emotional_association=self._determine_emotional_association(symbol_name),
                    interpretation_type=self._determine_interpretation_type(symbol_name)
                )
                symbols.append(symbol)
        
        # رموز دينية
        religious_symbols = {
            "المسجد": ("بيت الله", "مكان العبادة", "السكينة والطمأنينة", "رمز الإيمان"),
            "الكعبة": ("قبلة المسلمين", "وحدة الأمة", "المركز الروحي", "رمز التوحيد"),
            "المصحف": ("كلام الله", "الهداية والنور", "العلم والحكمة", "رمز الإسلام"),
            "السجدة": ("الخضوع لله", "التواضع والانكسار", "السكينة الروحية", "رمز العبودية"),
            "الدعاء": ("التوسل لله", "الرجاء والأمل", "التواصل الروحي", "رمز الإيمان"),
            "الصلاة": ("الصلة بالله", "النظام والانضباط", "السكينة النفسية", "رمز الدين")
        }
        
        for symbol_name, meanings in religious_symbols.items():
            if symbol_name in content:
                symbol = Symbol(
                    name=symbol_name,
                    category=SymbolCategory.RELIGIOUS,
                    arabic_meaning=meanings[0],
                    islamic_interpretation=meanings[1],
                    psychological_meaning=meanings[2],
                    cultural_context=meanings[3],
                    emotional_association=self._determine_emotional_association(symbol_name),
                    interpretation_type=self._determine_interpretation_type(symbol_name)
                )
                symbols.append(symbol)
        
        return symbols
    
    async def _interpret_symbols(self, symbols: List[Symbol], content: str) -> List[Dict[str, Any]]:
        """تفسير الرموز المكتشفة"""
        interpretations = []
        
        for symbol in symbols:
            interpretation = {
                "symbol_name": symbol.name,
                "category": symbol.category.value,
                "interpretations": {
                    "arabic_traditional": symbol.arabic_meaning,
                    "islamic_perspective": symbol.islamic_interpretation,
                    "psychological_meaning": symbol.psychological_meaning,
                    "cultural_context": symbol.cultural_context
                },
                "emotional_impact": symbol.emotional_association,
                "narrative_significance": self._assess_narrative_significance(symbol, content),
                "usage_frequency": content.count(symbol.name),
                "contextual_meaning": self._determine_contextual_meaning(symbol, content)
            }
            interpretations.append(interpretation)
        
        return interpretations
    
    async def _extract_dreams(self, content: str) -> List[Dream]:
        """استخراج الأحلام من النص"""
        dreams = []
        
        # البحث عن مؤشرات الأحلام
        dream_indicators = [
            r"حلم[تاه]?\s+(.*?)(?:استيقظ|صحا|انتهى الحلم)",
            r"رأى في المنام\s+(.*?)(?:فاستيقظ|ثم صحا)",
            r"في الحلم\s+(.*?)(?:انتهى|توقف)",
            r"كابوس\s+(.*?)(?:استيقظ|صحا)"
        ]
        
        dream_id = 1
        for pattern in dream_indicators:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                dream_content = match.group(1).strip()
                
                # تحديد الحالم
                dreamer = self._identify_dreamer(match.start(), content)
                
                # تحليل الرموز في الحلم
                dream_symbols = [symbol.name for symbol in await self._extract_symbols(dream_content)]
                
                # تحديد نوع الحلم
                dream_type = self._classify_dream_type(dream_content)
                
                # تحليل النبرة العاطفية
                emotional_tone = self._analyze_emotional_tone(dream_content)
                
                # تحديد المواضيع الرئيسية
                main_themes = self._identify_dream_themes(dream_content)
                
                # تفسير الحلم
                interpretation = await self._interpret_dream_content(dream_content, dream_symbols)
                
                # الأهمية النفسية
                psychological_significance = self._assess_psychological_significance(dream_content, dreamer)
                
                # الوظيفة السردية
                narrative_function = self._determine_dream_narrative_function(dream_content, content)
                
                dream = Dream(
                    dreamer=dreamer,
                    dream_content=dream_content,
                    symbols_present=dream_symbols,
                    dream_type=dream_type,
                    emotional_tone=emotional_tone,
                    main_themes=main_themes,
                    interpretation=interpretation,
                    psychological_significance=psychological_significance,
                    narrative_function=narrative_function
                )
                dreams.append(dream)
                dream_id += 1
        
        return dreams
    
    def _identify_dreamer(self, position: int, content: str) -> str:
        """تحديد هوية الحالم"""
        # البحث في النص قبل موضع الحلم
        before_dream = content[:position]
        
        # البحث عن أسماء في الجملة السابقة
        sentences = before_dream.split('.')
        if sentences:
            last_sentence = sentences[-1]
            
            # البحث عن أنماط الأسماء
            name_patterns = [
                r'([أ-ي]{3,})\s+حلم',
                r'رأى\s+([أ-ي]{3,})',
                r'([أ-ي]{3,})\s+في المنام'
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, last_sentence)
                if match:
                    return match.group(1)
        
        return "شخصية غير محددة"
    
    def _classify_dream_type(self, dream_content: str) -> DreamType:
        """تصنيف نوع الحلم"""
        # كابوس
        nightmare_indicators = ["خوف", "فزع", "مطاردة", "سقوط", "موت", "ظلام"]
        if any(indicator in dream_content for indicator in nightmare_indicators):
            return DreamType.NIGHTMARE
        
        # نبوئي
        prophetic_indicators = ["رؤيا", "بشارة", "إنذار", "مستقبل", "غيب"]
        if any(indicator in dream_content for indicator in prophetic_indicators):
            return DreamType.PROPHETIC
        
        # رمزي
        symbolic_indicators = ["رمز", "إشارة", "دلالة", "معنى خفي"]
        if any(indicator in dream_content for indicator in symbolic_indicators):
            return DreamType.SYMBOLIC
        
        return DreamType.PSYCHOLOGICAL
    
    def _analyze_emotional_tone(self, dream_content: str) -> str:
        """تحليل النبرة العاطفية للحلم"""
        positive_emotions = ["فرح", "سعادة", "راحة", "أمان", "حب", "جمال"]
        negative_emotions = ["خوف", "حزن", "قلق", "غضب", "ألم", "يأس"]
        
        positive_count = sum(1 for emotion in positive_emotions if emotion in dream_content)
        negative_count = sum(1 for emotion in negative_emotions if emotion in dream_content)
        
        if positive_count > negative_count:
            return "إيجابية"
        elif negative_count > positive_count:
            return "سلبية"
        else:
            return "محايدة"
    
    def _identify_dream_themes(self, dream_content: str) -> List[str]:
        """تحديد مواضيع الحلم"""
        themes = []
        
        theme_patterns = {
            "الموت والحياة": ["موت", "حياة", "قبر", "بعث"],
            "الحب والعلاقات": ["حب", "زواج", "حبيب", "أسرة"],
            "القوة والسلطة": ["ملك", "سلطان", "قوة", "حكم"],
            "الخوف والقلق": ["خوف", "قلق", "فزع", "رعب"],
            "النجاح والفشل": ["نجح", "فشل", "فوز", "خسارة"],
            "الماضي والذكريات": ["ذكرى", "ماضي", "طفولة", "أيام"],
            "المستقبل والأمل": ["مستقبل", "أمل", "حلم", "طموح"]
        }
        
        for theme, keywords in theme_patterns.items():
            if any(keyword in dream_content for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    async def _interpret_dream_content(self, dream_content: str, symbols: List[str]) -> str:
        """تفسير محتوى الحلم"""
        interpretations = []
        
        # تفسير الرموز الموجودة
        for symbol in symbols:
            if symbol in self.symbol_database:
                symbol_meaning = self.symbol_database[symbol]["islamic_interpretation"]
                interpretations.append(f"{symbol}: {symbol_meaning}")
        
        # تفسير عام للحلم
        if "نور" in dream_content or "ضوء" in dream_content:
            interpretations.append("النور في الحلم يدل على الهداية والخير")
        
        if "ماء" in dream_content:
            interpretations.append("الماء في الحلم يدل على الحياة والطهارة")
        
        if "طيران" in dream_content:
            interpretations.append("الطيران يدل على علو الهمة والطموح")
        
        return "; ".join(interpretations) if interpretations else "حلم يحتاج لتفسير أعمق"
    
    def _assess_psychological_significance(self, dream_content: str, dreamer: str) -> str:
        """تقييم الأهمية النفسية للحلم"""
        significance_factors = []
        
        if "خوف" in dream_content:
            significance_factors.append("يعكس القلق الداخلي للشخصية")
        
        if "طموح" in dream_content or "نجاح" in dream_content:
            significance_factors.append("يظهر رغبات الشخصية ودوافعها")
        
        if "ماضي" in dream_content or "ذكرى" in dream_content:
            significance_factors.append("يشير لمشاعر غير محلولة من الماضي")
        
        return "; ".join(significance_factors) if significance_factors else "أهمية نفسية محدودة"
    
    def _determine_dream_narrative_function(self, dream_content: str, full_content: str) -> str:
        """تحديد الوظيفة السردية للحلم"""
        # البحث عن الحلم في السياق
        dream_position = full_content.find(dream_content)
        
        if dream_position < len(full_content) * 0.3:
            return "تمهيد للأحداث وبناء التوقعات"
        elif dream_position > len(full_content) * 0.7:
            return "تلخيص للتجربة وإضافة عمق نهائي"
        else:
            return "نقطة تحول أو كشف مهم في الحبكة"
    
    async def _analyze_symbolic_patterns(self, symbols: List[Symbol], content: str) -> List[SymbolicPattern]:
        """تحليل الأنماط الرمزية"""
        patterns = []
        
        # نمط الطبيعة والروحانية
        nature_symbols = [s for s in symbols if s.category == SymbolCategory.NATURE]
        religious_symbols = [s for s in symbols if s.category == SymbolCategory.RELIGIOUS]
        
        if len(nature_symbols) >= 2 and len(religious_symbols) >= 1:
            pattern = SymbolicPattern(
                pattern_name="الطبيعة والروحانية",
                symbols_involved=[s.name for s in nature_symbols + religious_symbols],
                meaning="ربط بين الخلق والخالق، تأمل في عظمة الله",
                cultural_significance="نمط عربي إسلامي أصيل",
                usage_context="التعبير عن التدين والتأمل",
                effectiveness_score=0.8
            )
            patterns.append(pattern)
        
        # نمط الألوان العاطفية
        color_symbols = [s for s in symbols if s.category == SymbolCategory.COLORS]
        if len(color_symbols) >= 3:
            pattern = SymbolicPattern(
                pattern_name="الألوان العاطفية",
                symbols_involved=[s.name for s in color_symbols],
                meaning="التعبير عن الحالات النفسية والعاطفية",
                cultural_significance="استخدام الألوان في التعبير العربي",
                usage_context="وصف المشاعر والأحوال",
                effectiveness_score=0.7
            )
            patterns.append(pattern)
        
        # نمط الحيوانات الرمزية
        animal_symbols = [s for s in symbols if s.category == SymbolCategory.ANIMALS]
        if len(animal_symbols) >= 2:
            pattern = SymbolicPattern(
                pattern_name="الحيوانات الرمزية",
                symbols_involved=[s.name for s in animal_symbols],
                meaning="استخدام الحيوانات للتعبير عن الصفات البشرية",
                cultural_significance="تقليد عربي في الأمثال والحكايات",
                usage_context="وصف الشخصيات والصفات",
                effectiveness_score=0.75
            )
            patterns.append(pattern)
        
        return patterns
    
    async def _connect_psychology_symbols(self, content: str, symbols: List[Symbol]) -> List[Dict[str, Any]]:
        """ربط الرموز بالسياق النفسي"""
        connections = []
        
        for symbol in symbols:
            psychological_states = self._identify_psychological_states(content, symbol.name)
            
            if psychological_states:
                connection = {
                    "symbol": symbol.name,
                    "psychological_states": psychological_states,
                    "symbolic_function": self._determine_symbolic_function(symbol, psychological_states),
                    "emotional_resonance": self._assess_emotional_resonance(symbol, content),
                    "therapeutic_potential": self._assess_therapeutic_potential(symbol, psychological_states)
                }
                connections.append(connection)
        
        return connections
    
    def _identify_psychological_states(self, content: str, symbol_name: str) -> List[str]:
        """تحديد الحالات النفسية المرتبطة بالرمز"""
        states = []
        
        # البحث في النص حول الرمز
        symbol_contexts = re.finditer(rf'.{{0,50}}{symbol_name}.{{0,50}}', content)
        
        for context in symbol_contexts:
            context_text = context.group()
            
            # تحديد الحالات النفسية
            if any(word in context_text for word in ["قلق", "خوف", "توتر"]):
                states.append("القلق والخوف")
            
            if any(word in context_text for word in ["حزن", "اكتئاب", "يأس"]):
                states.append("الحزن والاكتئاب")
            
            if any(word in context_text for word in ["فرح", "سعادة", "بهجة"]):
                states.append("الفرح والسعادة")
            
            if any(word in context_text for word in ["غضب", "ثورة", "انفعال"]):
                states.append("الغضب والانفعال")
        
        return list(set(states))  # إزالة التكرار
    
    def _determine_symbolic_function(self, symbol: Symbol, psychological_states: List[str]) -> str:
        """تحديد الوظيفة الرمزية"""
        if "القلق والخوف" in psychological_states:
            return "رمز تعبيري عن المخاوف الداخلية"
        elif "الحزن والاكتئاب" in psychological_states:
            return "رمز للمعاناة النفسية والألم"
        elif "الفرح والسعادة" in psychological_states:
            return "رمز للسعادة والإيجابية"
        else:
            return "رمز متعدد الدلالات حسب السياق"
    
    def _assess_emotional_resonance(self, symbol: Symbol, content: str) -> float:
        """تقييم الصدى العاطفي للرمز"""
        # حساب تكرار الرمز
        frequency = content.count(symbol.name)
        
        # حساب السياق العاطفي
        emotional_contexts = 0
        emotion_words = ["حب", "خوف", "فرح", "حزن", "غضب", "أمل"]
        
        for emotion in emotion_words:
            if emotion in content and symbol.name in content:
                emotional_contexts += 1
        
        # حساب الصدى
        resonance = min(1.0, (frequency * 0.1) + (emotional_contexts * 0.2))
        return round(resonance, 2)
    
    def _assess_therapeutic_potential(self, symbol: Symbol, psychological_states: List[str]) -> str:
        """تقييم الإمكانية العلاجية للرمز"""
        if symbol.interpretation_type == SymbolInterpretation.POSITIVE:
            return "إمكانية عالية للاستخدام في العلاج الرمزي"
        elif symbol.interpretation_type == SymbolInterpretation.GUIDANCE:
            return "مناسب للإرشاد والتوجيه النفسي"
        elif symbol.interpretation_type == SymbolInterpretation.WARNING:
            return "يحتاج حذر في الاستخدام العلاجي"
        else:
            return "إمكانية محدودة للاستخدام العلاجي"
    
    async def _analyze_narrative_functions(self, symbols: List[Symbol], dreams: List[Dream], content: str) -> Dict[str, Any]:
        """تحليل الوظائف السردية للرموز والأحلام"""
        functions = {
            "symbols": {},
            "dreams": {},
            "overall_impact": ""
        }
        
        # وظائف الرموز
        for symbol in symbols:
            functions["symbols"][symbol.name] = {
                "function": self._determine_symbol_narrative_function(symbol, content),
                "frequency": content.count(symbol.name),
                "placement": self._analyze_symbol_placement(symbol.name, content)
            }
        
        # وظائف الأحلام
        for dream in dreams:
            functions["dreams"][f"dream_{dream.dreamer}"] = {
                "function": dream.narrative_function,
                "psychological_role": dream.psychological_significance,
                "symbolic_weight": len(dream.symbols_present)
            }
        
        # التأثير العام
        functions["overall_impact"] = self._assess_overall_symbolic_impact(symbols, dreams, content)
        
        return functions
    
    def _determine_symbol_narrative_function(self, symbol: Symbol, content: str) -> str:
        """تحديد الوظيفة السردية للرمز"""
        symbol_position = content.find(symbol.name)
        content_length = len(content)
        
        if symbol_position < content_length * 0.25:
            return "تأسيس المزاج والجو العام"
        elif symbol_position > content_length * 0.75:
            return "تعزيز الخاتمة وترك انطباع نهائي"
        else:
            return "دعم الأحداث وتعميق المعنى"
    
    def _analyze_symbol_placement(self, symbol_name: str, content: str) -> Dict[str, Any]:
        """تحليل مواضع الرمز في النص"""
        positions = []
        start = 0
        
        while True:
            pos = content.find(symbol_name, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        return {
            "total_occurrences": len(positions),
            "first_occurrence": positions[0] / len(content) if positions else 0,
            "last_occurrence": positions[-1] / len(content) if positions else 0,
            "distribution": "متنوع" if len(positions) > 2 else "محدود"
        }
    
    def _assess_overall_symbolic_impact(self, symbols: List[Symbol], dreams: List[Dream], content: str) -> str:
        """تقييم التأثير الرمزي العام"""
        symbol_count = len(symbols)
        dream_count = len(dreams)
        
        if symbol_count >= 5 and dream_count >= 1:
            return "تأثير رمزي قوي وعمق نفسي ملحوظ"
        elif symbol_count >= 3:
            return "تأثير رمزي متوسط مع بعض العمق"
        elif symbol_count >= 1:
            return "تأثير رمزي محدود"
        else:
            return "افتقار للعمق الرمزي"
    
    async def _suggest_new_symbols(self, content: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """اقتراح رموز جديدة"""
        suggestions = []
        
        # تحليل النقص في الرموز
        existing_categories = set()
        if "symbols_found" in context:
            existing_categories = {s.get("category") for s in context["symbols_found"]}
        
        # اقتراح رموز مفقودة
        if SymbolCategory.NATURE.value not in existing_categories:
            suggestions.append({
                "symbol": "النجوم",
                "category": "nature",
                "reason": "لإضافة عمق رمزي للأمل والطموح",
                "usage_example": "نظر إلى النجوم وتذكر أحلامه القديمة"
            })
        
        if SymbolCategory.RELIGIOUS.value not in existing_categories:
            suggestions.append({
                "symbol": "المسجد",
                "category": "religious",
                "reason": "لتعزيز البعد الروحي والثقافي",
                "usage_example": "وجد في صوت الأذان سكينة لروحه المضطربة"
            })
        
        # اقتراح بناءً على المحتوى
        if "حزن" in content or "ألم" in content:
            suggestions.append({
                "symbol": "المطر",
                "category": "nature",
                "reason": "المطر يرمز للتطهير والتجديد بعد الألم",
                "usage_example": "بدأ المطر ينزل كأنه يغسل أحزان قلبه"
            })
        
        return suggestions[:3]  # أفضل 3 اقتراحات
    
    async def _generate_dream_sequences(self, content: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """إنتاج تسلسلات أحلام مقترحة"""
        dream_sequences = []
        
        # حلم بناءً على الحالة النفسية
        if "قلق" in content or "خوف" in content:
            dream_sequences.append({
                "dreamer": "الشخصية الرئيسية",
                "dream_content": "رأى نفسه يجري في ظلام دامس، والنجوم تضيء له الطريق تدريجياً",
                "interpretation": "رمز للخروج من القلق نحو الأمل",
                "narrative_function": "توقع التطور الإيجابي للشخصية",
                "symbols": ["الظلام", "النجوم", "الجري"]
            })
        
        # حلم روحي
        if "دين" in content or "إيمان" in content:
            dream_sequences.append({
                "dreamer": "الشخصية المؤمنة",
                "dream_content": "وجد نفسه في مسجد عظيم، نوره يملأ المكان، وصوت جميل يتلو القرآن",
                "interpretation": "رمز للهداية والطمأنينة الروحية",
                "narrative_function": "تعزيز البعد الديني للشخصية",
                "symbols": ["المسجد", "النور", "القرآن"]
            })
        
        # حلم رمزي للمستقبل
        dream_sequences.append({
            "dreamer": "شخصية ثانوية",
            "dream_content": "رأى حديقة واسعة مليئة بالورود البيضاء، وفي وسطها نافورة ماء صافي",
            "interpretation": "رمز للنقاء والتجديد والأمل في المستقبل",
            "narrative_function": "التنبؤ بنهاية إيجابية",
            "symbols": ["الحديقة", "الورود البيضاء", "النافورة"]
        })
        
        return dream_sequences
    
    async def _generate_symbolic_recommendations(self, symbols: List[Symbol], dreams: List[Dream],
                                               patterns: List[SymbolicPattern], 
                                               psychological_connections: List[Dict[str, Any]]) -> List[str]:
        """إنتاج توصيات رمزية"""
        recommendations = []
        
        # توصيات للرموز
        if len(symbols) < 3:
            recommendations.append("زيادة الكثافة الرمزية لإثراء النص")
        
        # توصيات للأحلام
        if not dreams:
            recommendations.append("إضافة أحلام رمزية لتعميق البعد النفسي")
        
        # توصيات للأنماط
        if not patterns:
            recommendations.append("تطوير أنماط رمزية متماسكة عبر النص")
        
        # توصيات للربط النفسي
        if not psychological_connections:
            recommendations.append("ربط الرموز بالحالات النفسية للشخصيات")
        
        # توصيات ثقافية
        religious_symbols = [s for s in symbols if s.category == SymbolCategory.RELIGIOUS]
        if not religious_symbols:
            recommendations.append("إدراج رموز دينية لتعزيز الأصالة الثقافية")
        
        # توصيات فنية
        recommendations.extend([
            "استخدام الرموز للتنبؤ بالأحداث",
            "ربط الرموز بتطور الشخصيات",
            "تكرار الرموز المهمة في مواضع استراتيجية"
        ])
        
        return recommendations[:5]
    
    def _calculate_symbolic_density(self, symbols: List[Symbol], content: str) -> float:
        """حساب الكثافة الرمزية"""
        if not content:
            return 0.0
        
        word_count = len(content.split())
        symbol_count = len(symbols)
        
        density = symbol_count / max(word_count, 1) * 100
        return round(min(density, 10.0), 2)  # حد أقصى 10%
    
    def _assess_cultural_authenticity(self, symbols: List[Symbol]) -> float:
        """تقييم الأصالة الثقافية للرموز"""
        if not symbols:
            return 0.0
        
        cultural_symbols = sum(1 for s in symbols if s.category in [
            SymbolCategory.RELIGIOUS, SymbolCategory.CULTURAL
        ])
        
        authenticity = cultural_symbols / len(symbols)
        return round(authenticity, 2)
    
    def _calculate_confidence_score(self, symbols: List[Symbol], dreams: List[Dream], 
                                   patterns: List[SymbolicPattern]) -> float:
        """حساب درجة الثقة في التحليل"""
        base_score = 0.7
        
        # زيادة الثقة بناءً على عدد الرموز
        symbols_bonus = min(0.2, len(symbols) * 0.03)
        
        # زيادة الثقة بناءً على وجود أحلام
        dreams_bonus = min(0.1, len(dreams) * 0.05)
        
        # زيادة الثقة بناءً على الأنماط
        patterns_bonus = min(0.1, len(patterns) * 0.03)
        
        final_score = base_score + symbols_bonus + dreams_bonus + patterns_bonus
        return round(max(0.0, min(1.0, final_score)), 2)
    
    async def _generate_visual_data(self, symbols: List[Symbol], dreams: List[Dream],
                                   patterns: List[SymbolicPattern], 
                                   interpretations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """إنتاج البيانات المرئية للتحليل"""
        return {
            "symbol_categories": {
                "type": "pie",
                "data": self._get_symbol_category_distribution(symbols)
            },
            "interpretation_types": {
                "type": "bar",
                "data": self._get_interpretation_type_distribution(symbols)
            },
            "dream_themes": {
                "type": "radar",
                "data": self._get_dream_themes_distribution(dreams)
            },
            "symbolic_patterns": {
                "type": "network",
                "data": self._get_pattern_network_data(patterns)
            },
            "cultural_authenticity": {
                "type": "gauge",
                "value": self._assess_cultural_authenticity(symbols) * 100,
                "max": 100
            }
        }
    
    def _get_symbol_category_distribution(self, symbols: List[Symbol]) -> List[Dict[str, Any]]:
        """توزيع فئات الرموز"""
        from collections import Counter
        
        categories = Counter(symbol.category.value for symbol in symbols)
        
        return [
            {"category": category, "count": count}
            for category, count in categories.items()
        ]
    
    def _get_interpretation_type_distribution(self, symbols: List[Symbol]) -> List[Dict[str, Any]]:
        """توزيع أنواع التفسيرات"""
        from collections import Counter
        
        interpretations = Counter(symbol.interpretation_type.value for symbol in symbols)
        
        return [
            {"type": interpretation_type, "count": count}
            for interpretation_type, count in interpretations.items()
        ]
    
    def _get_dream_themes_distribution(self, dreams: List[Dream]) -> List[Dict[str, Any]]:
        """توزيع مواضيع الأحلام"""
        all_themes = []
        for dream in dreams:
            all_themes.extend(dream.main_themes)
        
        from collections import Counter
        themes = Counter(all_themes)
        
        return [
            {"theme": theme, "frequency": count}
            for theme, count in themes.items()
        ]
    
    def _get_pattern_network_data(self, patterns: List[SymbolicPattern]) -> Dict[str, List[Dict[str, Any]]]:
        """بيانات شبكة الأنماط الرمزية"""
        nodes = []
        edges = []
        
        for i, pattern in enumerate(patterns):
            # إضافة عقدة للنمط
            nodes.append({
                "id": f"pattern_{i}",
                "label": pattern.pattern_name,
                "type": "pattern",
                "score": pattern.effectiveness_score
            })
            
            # إضافة عقد للرموز
            for symbol in pattern.symbols_involved:
                symbol_id = f"symbol_{symbol}"
                if not any(node["id"] == symbol_id for node in nodes):
                    nodes.append({
                        "id": symbol_id,
                        "label": symbol,
                        "type": "symbol"
                    })
                
                # إضافة حافة بين النمط والرمز
                edges.append({
                    "source": f"pattern_{i}",
                    "target": symbol_id,
                    "weight": pattern.effectiveness_score
                })
        
        return {"nodes": nodes, "edges": edges}
    
    def _determine_emotional_association(self, symbol_name: str) -> str:
        """تحديد الارتباط العاطفي للرمز"""
        positive_symbols = ["الشمس", "النجوم", "المطر", "الأبيض", "الأخضر", "الحمامة", "الذهبي"]
        negative_symbols = ["الأسود", "الذئب", "الثعبان", "العاصفة", "الظلام"]
        
        if symbol_name in positive_symbols:
            return "إيجابي"
        elif symbol_name in negative_symbols:
            return "سلبي"
        else:
            return "محايد"
    
    def _determine_interpretation_type(self, symbol_name: str) -> SymbolInterpretation:
        """تحديد نوع التفسير للرمز"""
        positive_symbols = ["الشمس", "النجوم", "المطر", "الأبيض", "الحمامة"]
        warning_symbols = ["الذئب", "الثعبان", "العاصفة", "الأسود"]
        guidance_symbols = ["المسجد", "المصحف", "الصلاة", "الدعاء"]
        
        if symbol_name in positive_symbols:
            return SymbolInterpretation.POSITIVE
        elif symbol_name in warning_symbols:
            return SymbolInterpretation.WARNING
        elif symbol_name in guidance_symbols:
            return SymbolInterpretation.GUIDANCE
        else:
            return SymbolInterpretation.NEUTRAL
    
    def _assess_narrative_significance(self, symbol: Symbol, content: str) -> str:
        """تقييم الأهمية السردية للرمز"""
        frequency = content.count(symbol.name)
        
        if frequency >= 3:
            return "أهمية عالية - رمز محوري"
        elif frequency == 2:
            return "أهمية متوسطة - رمز داعم"
        else:
            return "أهمية محدودة - رمز عابر"
    
    def _determine_contextual_meaning(self, symbol: Symbol, content: str) -> str:
        """تحديد المعنى السياقي للرمز"""
        # البحث عن السياق المحيط بالرمز
        contexts = re.finditer(rf'.{{0,30}}{symbol.name}.{{0,30}}', content)
        
        contextual_meanings = []
        for context in contexts:
            context_text = context.group()
            
            if "حزن" in context_text or "ألم" in context_text:
                contextual_meanings.append("رمز للمعاناة")
            elif "فرح" in context_text or "سعادة" in context_text:
                contextual_meanings.append("رمز للبهجة")
            elif "أمل" in context_text or "تفاؤل" in context_text:
                contextual_meanings.append("رمز للأمل")
            else:
                contextual_meanings.append("رمز عام")
        
        return "; ".join(set(contextual_meanings)) if contextual_meanings else symbol.arabic_meaning
    
    def _symbol_to_dict(self, symbol: Symbol) -> Dict[str, Any]:
        """تحويل الرمز إلى قاموس"""
        return {
            "name": symbol.name,
            "category": symbol.category.value,
            "arabic_meaning": symbol.arabic_meaning,
            "islamic_interpretation": symbol.islamic_interpretation,
            "psychological_meaning": symbol.psychological_meaning,
            "cultural_context": symbol.cultural_context,
            "emotional_association": symbol.emotional_association,
            "interpretation_type": symbol.interpretation_type.value
        }
    
    def _dream_to_dict(self, dream: Dream) -> Dict[str, Any]:
        """تحويل الحلم إلى قاموس"""
        return {
            "dreamer": dream.dreamer,
            "dream_content": dream.dream_content,
            "symbols_present": dream.symbols_present,
            "dream_type": dream.dream_type.value,
            "emotional_tone": dream.emotional_tone,
            "main_themes": dream.main_themes,
            "interpretation": dream.interpretation,
            "psychological_significance": dream.psychological_significance,
            "narrative_function": dream.narrative_function
        }
    
    def _pattern_to_dict(self, pattern: SymbolicPattern) -> Dict[str, Any]:
        """تحويل النمط الرمزي إلى قاموس"""
        return {
            "pattern_name": pattern.pattern_name,
            "symbols_involved": pattern.symbols_involved,
            "meaning": pattern.meaning,
            "cultural_significance": pattern.cultural_significance,
            "usage_context": pattern.usage_context,
            "effectiveness_score": pattern.effectiveness_score
        }
    
    def _load_symbol_database(self) -> Dict[str, Dict[str, str]]:
        """تحميل قاعدة بيانات الرموز"""
        return {
            "الشمس": {
                "arabic_meaning": "النور والحياة",
                "islamic_interpretation": "الهداية الإلهية",
                "psychological_meaning": "الوعي والوضوح",
                "cultural_context": "رمز القوة والسلطان"
            },
            "القمر": {
                "arabic_meaning": "الجمال والأنوثة",
                "islamic_interpretation": "التقلب والتغيير",
                "psychological_meaning": "اللاوعي والغموض",
                "cultural_context": "رمز الليل والسكون"
            }
            # يمكن إضافة المزيد من الرموز هنا
        }
    
    def _load_dream_patterns(self) -> Dict[str, List[str]]:
        """تحميل أنماط الأحلام"""
        return {
            "prophetic_dreams": ["رؤيا", "بشارة", "إنذار", "غيب"],
            "anxiety_dreams": ["مطاردة", "سقوط", "فقدان", "ضياع"],
            "healing_dreams": ["نور", "ماء", "شفاء", "سكينة"],
            "symbolic_dreams": ["رموز", "إشارات", "معاني خفية"]
        }
    
    def _load_islamic_interpretations(self) -> Dict[str, str]:
        """تحميل التفسيرات الإسلامية للرموز"""
        return {
            "الماء": "الحياة والطهارة والرحمة",
            "النور": "الهداية والإيمان والعلم",
            "الطائر": "الروح والحرية والرسالة",
            "الشجرة": "الإيمان الراسخ والنمو الروحي"
        }
    
    def _load_psychological_meanings(self) -> Dict[str, str]:
        """تحميل المعاني النفسية للرموز"""
        return {
            "الماء": "العواطف واللاوعي والتطهير النفسي",
            "النار": "الشغف والغضب والتحول",
            "الطيران": "الحرية والهروب من القيود",
            "السقوط": "فقدان السيطرة والخوف من الفشل"
        }
    
    def _load_cultural_symbols(self) -> Dict[str, str]:
        """تحميل الرموز الثقافية العربية"""
        return {
            "النخلة": "الصمود والكرم والخير",
            "الصحراء": "التحدي والصبر والتأمل",
            "الخيمة": "الضيافة والأصالة والبداوة",
            "السيف": "الشجاعة والكرامة والحق"
        }
    
    def _load_narrative_functions(self) -> Dict[str, str]:
        """تحميل الوظائف السردية للرموز"""
        return {
            "foreshadowing": "التنبؤ بالأحداث القادمة",
            "mood_setting": "إنشاء الجو العام للنص",
            "character_development": "تطوير الشخصيات وعمقها",
            "theme_reinforcement": "تعزيز الموضوع الرئيسي",
            "emotional_resonance": "خلق صدى عاطفي مع القارئ"
        }
