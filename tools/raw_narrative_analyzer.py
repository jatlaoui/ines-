"""
وكيل محلل السرد الخام (Raw Narrative Analyzer)
يقوم بتحليل الترانسكريبت واستخلاص العناصر السردية الأساسية
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from .base_agent import BaseAgent

@dataclass
class Character:
    """بنية بيانات الشخصية"""
    name: str
    role: str
    traits: List[str]
    emotional_arc: List[str]
    relationships: Dict[str, str]
    first_appearance: int
    significance_score: float

@dataclass
class PlotPoint:
    """نقطة حبكة في السرد"""
    timestamp: int
    event_type: str
    description: str
    emotional_intensity: float
    characters_involved: List[str]
    themes: List[str]

@dataclass
class NarrativeLayer:
    """طبقة سردية في النص"""
    layer_type: str  # main_plot, subplot, flashback, dialogue
    content: str
    time_range: Tuple[int, int]
    emotional_tone: str
    complexity_level: int

class RawNarrativeAnalyzer(BaseAgent):
    """وكيل محلل السرد الخام المتطور"""
    
    def __init__(self):
        super().__init__("محلل السرد الخام", "تحليل الترانسكريبت واستخلاص العناصر السردية")
        self.emotional_markers = {
            "فرح": ["فرح", "سعادة", "ابتسم", "ضحك", "مرح"],
            "حزن": ["حزن", "بكى", "دموع", "أسى", "كآبة"],
            "غضب": ["غضب", "انفعل", "صرخ", "ثار", "احتد"],
            "خوف": ["خوف", "رعب", "قلق", "توتر", "هلع"],
            "حب": ["حب", "عشق", "إعجاب", "افتتان", "هيام"],
            "كره": ["كره", "بغض", "نفور", "اشمئزاز", "احتقار"]
        }
        
        self.narrative_indicators = {
            "حوار": ["قال", "أجاب", "سأل", "صرح", "همس"],
            "وصف": ["كان", "وصف", "بدا", "ظهر", "لوحظ"],
            "حدث": ["حدث", "وقع", "جرى", "طرأ", "استجد"],
            "انتقال": ["ثم", "بعدها", "لاحقاً", "في النهاية", "أخيراً"]
        }

    async def analyze_raw_transcript(self, transcript: str, metadata: Dict = None) -> Dict[str, Any]:
        """تحليل شامل للترانسكريبت"""
        
        analysis_result = {
            "characters": await self._extract_characters(transcript),
            "plot_structure": await self._analyze_plot_structure(transcript),
            "narrative_layers": await self._identify_narrative_layers(transcript),
            "emotional_arc": await self._map_emotional_journey(transcript),
            "temporal_structure": await self._analyze_temporal_structure(transcript),
            "thematic_analysis": await self._extract_themes(transcript),
            "dialogue_analysis": await self._analyze_dialogue_patterns(transcript),
            "narrative_voice": await self._identify_narrative_voice(transcript),
            "cultural_context": await self._extract_cultural_elements(transcript),
            "conflict_analysis": await self._identify_conflicts(transcript)
        }
        
        return analysis_result

    async def _extract_characters(self, transcript: str) -> List[Character]:
        """استخلاص الشخصيات من النص"""
        characters = []
        
        # البحث عن أسماء الأشخاص
        name_patterns = [
            r'\b[أ-ي][أ-ي]{2,}\b',  # أسماء عربية
            r'\b[A-Z][a-z]{2,}\b'     # أسماء أجنبية
        ]
        
        potential_names = []
        for pattern in name_patterns:
            matches = re.findall(pattern, transcript)
            potential_names.extend(matches)
        
        # تحليل كل اسم محتمل
        for name in set(potential_names):
            if await self._is_character_name(name, transcript):
                character = await self._analyze_character(name, transcript)
                characters.append(character)
        
        return characters

    async def _is_character_name(self, name: str, transcript: str) -> bool:
        """تحديد ما إذا كان النص اسم شخصية"""
        # البحث عن مؤشرات أن هذا اسم شخصية
        character_indicators = [
            f"{name} قال",
            f"{name} فعل",
            f"تحدث {name}",
            f"ذهب {name}",
            f"جاء {name}"
        ]
        
        count = 0
        for indicator in character_indicators:
            count += transcript.count(indicator)
        
        return count >= 2  # إذا ظهر مرتين على الأقل مع مؤشرات الشخصية

    async def _analyze_character(self, name: str, transcript: str) -> Character:
        """تحليل شخصية محددة"""
        # البحث عن النص المتعلق بهذه الشخصية
        character_context = await self._extract_character_context(name, transcript)
        
        # تحليل السمات
        traits = await self._extract_character_traits(character_context)
        
        # تحليل الدور
        role = await self._determine_character_role(name, transcript)
        
        # تحليل القوس العاطفي
        emotional_arc = await self._trace_emotional_arc(name, transcript)
        
        # تحليل العلاقات
        relationships = await self._analyze_relationships(name, transcript)
        
        # العثور على أول ظهور
        first_appearance = transcript.find(name)
        
        # حساب درجة الأهمية
        significance_score = await self._calculate_significance(name, transcript)
        
        return Character(
            name=name,
            role=role,
            traits=traits,
            emotional_arc=emotional_arc,
            relationships=relationships,
            first_appearance=first_appearance,
            significance_score=significance_score
        )

    async def _extract_character_context(self, name: str, transcript: str) -> str:
        """استخلاص السياق المتعلق بشخصية معينة"""
        sentences = transcript.split('.')
        character_sentences = []
        
        for sentence in sentences:
            if name in sentence:
                character_sentences.append(sentence.strip())
        
        return '. '.join(character_sentences)

    async def _extract_character_traits(self, context: str) -> List[str]:
        """استخلاص سمات الشخصية"""
        trait_keywords = {
            "شجاع": ["شجاع", "بطل", "مقدام", "جريء"],
            "ذكي": ["ذكي", "فطن", "حكيم", "عاقل"],
            "طيب": ["طيب", "كريم", "نبيل", "خيّر"],
            "شرير": ["شرير", "خبيث", "ماكر", "سيئ"],
            "جميل": ["جميل", "حسن", "وسيم", "فاتن"],
            "قوي": ["قوي", "جبار", "عملاق", "قدير"]
        }
        
        traits = []
        for trait, keywords in trait_keywords.items():
            for keyword in keywords:
                if keyword in context:
                    traits.append(trait)
                    break
        
        return traits

    async def _determine_character_role(self, name: str, transcript: str) -> str:
        """تحديد دور الشخصية في السرد"""
        appearance_count = transcript.count(name)
        
        if appearance_count > 10:
            return "بطل"
        elif appearance_count > 5:
            return "شخصية ثانوية مهمة"
        elif appearance_count > 2:
            return "شخصية مساعدة"
        else:
            return "شخصية عابرة"

    async def _trace_emotional_arc(self, name: str, transcript: str) -> List[str]:
        """تتبع القوس العاطفي للشخصية"""
        emotional_arc = []
        character_mentions = []
        
        # العثور على جميع المواضع التي تذكر فيها الشخصية
        sentences = transcript.split('.')
        for i, sentence in enumerate(sentences):
            if name in sentence:
                character_mentions.append((i, sentence))
        
        # تحليل الحالة العاطفية في كل موضع
        for position, sentence in character_mentions:
            emotion = await self._detect_emotion_in_sentence(sentence)
            if emotion:
                emotional_arc.append(f"الموضع {position}: {emotion}")
        
        return emotional_arc

    async def _detect_emotion_in_sentence(self, sentence: str) -> Optional[str]:
        """كشف العاطفة في جملة"""
        for emotion, markers in self.emotional_markers.items():
            for marker in markers:
                if marker in sentence:
                    return emotion
        return None

    async def _analyze_relationships(self, name: str, transcript: str) -> Dict[str, str]:
        """تحليل علاقات الشخصية مع الآخرين"""
        relationships = {}
        
        # البحث عن العلاقات المذكورة صراحة
        relationship_patterns = [
            (r'(.+) زوج (.+)', 'زوج'),
            (r'(.+) أخ (.+)', 'أخ'),
            (r'(.+) أخت (.+)', 'أخت'),
            (r'(.+) صديق (.+)', 'صديق'),
            (r'(.+) عدو (.+)', 'عدو'),
            (r'(.+) والد (.+)', 'والد'),
            (r'(.+) ابن (.+)', 'ابن')
        ]
        
        for pattern, relation_type in relationship_patterns:
            matches = re.findall(pattern, transcript)
            for match in matches:
                if name in match:
                    other_person = match[0] if match[1] == name else match[1]
                    relationships[other_person.strip()] = relation_type
        
        return relationships

    async def _calculate_significance(self, name: str, transcript: str) -> float:
        """حساب درجة أهمية الشخصية"""
        factors = {
            'frequency': transcript.count(name) / len(transcript.split()) * 1000,
            'first_appearance': (1.0 - transcript.find(name) / len(transcript)) * 0.3,
            'dialogue_presence': transcript.count(f'{name} قال') * 0.1,
            'action_involvement': transcript.count(f'{name} فعل') * 0.1
        }
        
        return sum(factors.values())

    async def _analyze_plot_structure(self, transcript: str) -> Dict[str, Any]:
        """تحليل بنية الحبكة"""
        plot_points = await self._identify_plot_points(transcript)
        
        structure = {
            "exposition": await self._find_exposition(transcript),
            "rising_action": await self._find_rising_action(plot_points),
            "climax": await self._find_climax(plot_points),
            "falling_action": await self._find_falling_action(plot_points),
            "resolution": await self._find_resolution(transcript),
            "plot_points": plot_points,
            "pacing_analysis": await self._analyze_pacing(plot_points)
        }
        
        return structure

    async def _identify_plot_points(self, transcript: str) -> List[PlotPoint]:
        """تحديد نقاط الحبكة"""
        plot_points = []
        sentences = transcript.split('.')
        
        for i, sentence in enumerate(sentences):
            if await self._is_significant_event(sentence):
                plot_point = PlotPoint(
                    timestamp=i,
                    event_type=await self._classify_event_type(sentence),
                    description=sentence.strip(),
                    emotional_intensity=await self._measure_emotional_intensity(sentence),
                    characters_involved=await self._identify_involved_characters(sentence),
                    themes=await self._extract_themes_from_sentence(sentence)
                )
                plot_points.append(plot_point)
        
        return plot_points

    async def _is_significant_event(self, sentence: str) -> bool:
        """تحديد ما إذا كانت الجملة تحتوي على حدث مهم"""
        event_indicators = [
            "حدث", "وقع", "فجأة", "بشكل مفاجئ", "لأول مرة",
            "أخيراً", "في النهاية", "قرر", "اكتشف", "علم"
        ]
        
        return any(indicator in sentence for indicator in event_indicators)

    async def _classify_event_type(self, sentence: str) -> str:
        """تصنيف نوع الحدث"""
        event_types = {
            "صراع": ["قاتل", "حارب", "نازع", "صارع"],
            "اكتشاف": ["اكتشف", "علم", "وجد", "كشف"],
            "قرار": ["قرر", "اختار", "حسم", "عزم"],
            "لقاء": ["التقى", "واجه", "قابل", "لاقى"],
            "فراق": ["ترك", "رحل", "فارق", "انفصل"],
            "تحول": ["تغير", "تحول", "أصبح", "صار"]
        }
        
        for event_type, keywords in event_types.items():
            if any(keyword in sentence for keyword in keywords):
                return event_type
        
        return "حدث عام"

    async def _measure_emotional_intensity(self, sentence: str) -> float:
        """قياس الكثافة العاطفية للجملة"""
        intensity_markers = {
            "عالية": ["بشدة", "بقوة", "جداً", "للغاية", "كثيراً"],
            "متوسطة": ["نوعاً ما", "إلى حد ما", "قليلاً"],
            "منخفضة": ["بهدوء", "برفق", "بلطف"]
        }
        
        high_count = sum(1 for marker in intensity_markers["عالية"] if marker in sentence)
        medium_count = sum(1 for marker in intensity_markers["متوسطة"] if marker in sentence)
        low_count = sum(1 for marker in intensity_markers["منخفضة"] if marker in sentence)
        
        return (high_count * 0.9 + medium_count * 0.5 + low_count * 0.2) / max(1, high_count + medium_count + low_count)

    async def _identify_involved_characters(self, sentence: str) -> List[str]:
        """تحديد الشخصيات المشاركة في الحدث"""
        # هذا مبسط - في التطبيق الحقيقي سنستخدم قائمة الشخصيات المستخلصة
        potential_names = re.findall(r'\b[أ-ي][أ-ي]{2,}\b', sentence)
        return list(set(potential_names))

    async def _extract_themes_from_sentence(self, sentence: str) -> List[str]:
        """استخلاص المواضيع من الجملة"""
        theme_keywords = {
            "الحب": ["حب", "عشق", "غرام", "هيام"],
            "الصداقة": ["صداقة", "صديق", "رفيق", "زميل"],
            "العدالة": ["عدالة", "حق", "إنصاف", "قضاء"],
            "التضحية": ["ضحى", "تضحية", "فداء", "بذل"],
            "الخيانة": ["خيانة", "غدر", "خذلان", "نكث"],
            "الشجاعة": ["شجاعة", "جرأة", "بطولة", "إقدام"]
        }
        
        themes = []
        for theme, keywords in theme_keywords.items():
            if any(keyword in sentence for keyword in keywords):
                themes.append(theme)
        
        return themes

    async def _find_exposition(self, transcript: str) -> str:
        """العثور على المقدمة"""
        first_quarter = transcript[:len(transcript)//4]
        return first_quarter

    async def _find_rising_action(self, plot_points: List[PlotPoint]) -> List[PlotPoint]:
        """العثور على الحدث الصاعد"""
        total_points = len(plot_points)
        rising_start = total_points // 4
        rising_end = 3 * total_points // 4
        return plot_points[rising_start:rising_end]

    async def _find_climax(self, plot_points: List[PlotPoint]) -> Optional[PlotPoint]:
        """العثور على الذروة"""
        if not plot_points:
            return None
        
        # الذروة هي النقطة ذات أعلى كثافة عاطفية
        return max(plot_points, key=lambda p: p.emotional_intensity)

    async def _find_falling_action(self, plot_points: List[PlotPoint]) -> List[PlotPoint]:
        """العثور على الحدث الهابط"""
        total_points = len(plot_points)
        falling_start = 3 * total_points // 4
        return plot_points[falling_start:]

    async def _find_resolution(self, transcript: str) -> str:
        """العثور على الخاتمة"""
        last_quarter = transcript[3*len(transcript)//4:]
        return last_quarter

    async def _analyze_pacing(self, plot_points: List[PlotPoint]) -> Dict[str, Any]:
        """تحليل وتيرة السرد"""
        if not plot_points:
            return {"pacing": "غير محدد", "tension_curve": []}
        
        # حساب المسافات بين نقاط الحبكة
        distances = []
        for i in range(1, len(plot_points)):
            distance = plot_points[i].timestamp - plot_points[i-1].timestamp
            distances.append(distance)
        
        avg_distance = sum(distances) / len(distances) if distances else 0
        
        # تحليل منحنى التوتر
        tension_curve = [p.emotional_intensity for p in plot_points]
        
        pacing_type = "سريع" if avg_distance < 10 else "متوسط" if avg_distance < 30 else "بطيء"
        
        return {
            "pacing": pacing_type,
            "average_distance": avg_distance,
            "tension_curve": tension_curve,
            "plot_density": len(plot_points) / 100  # نقاط لكل 100 جملة
        }

    async def _identify_narrative_layers(self, transcript: str) -> List[NarrativeLayer]:
        """تحديد الطبقات السردية"""
        layers = []
        
        # تحليل الحوار
        dialogue_sections = await self._extract_dialogue_sections(transcript)
        for section in dialogue_sections:
            layer = NarrativeLayer(
                layer_type="dialogue",
                content=section["content"],
                time_range=section["range"],
                emotional_tone=await self._analyze_emotional_tone(section["content"]),
                complexity_level=await self._assess_complexity(section["content"])
            )
            layers.append(layer)
        
        # تحليل الوصف
        description_sections = await self._extract_description_sections(transcript)
        for section in description_sections:
            layer = NarrativeLayer(
                layer_type="description",
                content=section["content"],
                time_range=section["range"],
                emotional_tone=await self._analyze_emotional_tone(section["content"]),
                complexity_level=await self._assess_complexity(section["content"])
            )
            layers.append(layer)
        
        return layers

    async def _extract_dialogue_sections(self, transcript: str) -> List[Dict]:
        """استخلاص أقسام الحوار"""
        dialogue_sections = []
        sentences = transcript.split('.')
        
        current_section = None
        for i, sentence in enumerate(sentences):
            if any(indicator in sentence for indicator in self.narrative_indicators["حوار"]):
                if current_section is None:
                    current_section = {
                        "content": sentence,
                        "start": i,
                        "range": (i, i)
                    }
                else:
                    current_section["content"] += ". " + sentence
                    current_section["range"] = (current_section["start"], i)
            else:
                if current_section is not None:
                    dialogue_sections.append(current_section)
                    current_section = None
        
        return dialogue_sections

    async def _extract_description_sections(self, transcript: str) -> List[Dict]:
        """استخلاص أقسام الوصف"""
        description_sections = []
        sentences = transcript.split('.')
        
        current_section = None
        for i, sentence in enumerate(sentences):
            if any(indicator in sentence for indicator in self.narrative_indicators["وصف"]):
                if current_section is None:
                    current_section = {
                        "content": sentence,
                        "start": i,
                        "range": (i, i)
                    }
                else:
                    current_section["content"] += ". " + sentence
                    current_section["range"] = (current_section["start"], i)
            else:
                if current_section is not None:
                    description_sections.append(current_section)
                    current_section = None
        
        return description_sections

    async def _analyze_emotional_tone(self, content: str) -> str:
        """تحليل النبرة العاطفية"""
        emotion_scores = {}
        for emotion, markers in self.emotional_markers.items():
            score = sum(1 for marker in markers if marker in content)
            emotion_scores[emotion] = score
        
        if not any(emotion_scores.values()):
            return "محايد"
        
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        return dominant_emotion

    async def _assess_complexity(self, content: str) -> int:
        """تقييم مستوى التعقيد"""
        factors = {
            'sentence_length': len(content.split()) / 20,  # طول الجملة
            'vocabulary_complexity': len(set(content.split())) / len(content.split()),  # تنوع المفردات
            'punctuation_density': content.count(',') + content.count(';') / len(content.split())  # كثافة علامات الترقيم
        }
        
        complexity_score = sum(factors.values()) / len(factors)
        
        if complexity_score > 0.7:
            return 3  # عالي
        elif complexity_score > 0.4:
            return 2  # متوسط
        else:
            return 1  # منخفض

    async def _map_emotional_journey(self, transcript: str) -> Dict[str, Any]:
        """رسم الرحلة العاطفية"""
        sentences = transcript.split('.')
        emotional_timeline = []
        
        for i, sentence in enumerate(sentences):
            emotion = await self._detect_emotion_in_sentence(sentence)
            intensity = await self._measure_emotional_intensity(sentence)
            
            if emotion:
                emotional_timeline.append({
                    "position": i,
                    "emotion": emotion,
                    "intensity": intensity,
                    "context": sentence.strip()
                })
        
        # تحليل الأنماط العاطفية
        emotion_patterns = await self._analyze_emotion_patterns(emotional_timeline)
        
        return {
            "timeline": emotional_timeline,
            "patterns": emotion_patterns,
            "dominant_emotions": await self._find_dominant_emotions(emotional_timeline),
            "emotional_shifts": await self._identify_emotional_shifts(emotional_timeline)
        }

    async def _analyze_emotion_patterns(self, timeline: List[Dict]) -> Dict[str, Any]:
        """تحليل أنماط العواطف"""
        if not timeline:
            return {}
        
        emotions = [entry["emotion"] for entry in timeline]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # تحليل التسلسل
        sequences = []
        for i in range(len(emotions) - 1):
            sequence = f"{emotions[i]} -> {emotions[i+1]}"
            sequences.append(sequence)
        
        sequence_counts = {}
        for seq in sequences:
            sequence_counts[seq] = sequence_counts.get(seq, 0) + 1
        
        return {
            "emotion_distribution": emotion_counts,
            "common_sequences": sequence_counts,
            "emotional_volatility": await self._calculate_emotional_volatility(timeline)
        }

    async def _calculate_emotional_volatility(self, timeline: List[Dict]) -> float:
        """حساب التقلب العاطفي"""
        if len(timeline) < 2:
            return 0.0
        
        intensity_changes = []
        for i in range(1, len(timeline)):
            change = abs(timeline[i]["intensity"] - timeline[i-1]["intensity"])
            intensity_changes.append(change)
        
        return sum(intensity_changes) / len(intensity_changes)

    async def _find_dominant_emotions(self, timeline: List[Dict]) -> List[str]:
        """العثور على العواطف المهيمنة"""
        emotion_counts = {}
        for entry in timeline:
            emotion = entry["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        sorted_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)
        return [emotion for emotion, count in sorted_emotions[:3]]  # أفضل 3 عواطف

    async def _identify_emotional_shifts(self, timeline: List[Dict]) -> List[Dict]:
        """تحديد التحولات العاطفية"""
        shifts = []
        
        for i in range(1, len(timeline)):
            current_emotion = timeline[i]["emotion"]
            previous_emotion = timeline[i-1]["emotion"]
            
            if current_emotion != previous_emotion:
                shift = {
                    "position": timeline[i]["position"],
                    "from": previous_emotion,
                    "to": current_emotion,
                    "intensity_change": timeline[i]["intensity"] - timeline[i-1]["intensity"],
                    "context": timeline[i]["context"]
                }
                shifts.append(shift)
        
        return shifts

    async def _analyze_temporal_structure(self, transcript: str) -> Dict[str, Any]:
        """تحليل البنية الزمنية"""
        time_markers = await self._identify_time_markers(transcript)
        chronology = await self._establish_chronology(time_markers)
        
        return {
            "time_markers": time_markers,
            "chronological_order": chronology,
            "narrative_time": await self._analyze_narrative_time(transcript),
            "temporal_techniques": await self._identify_temporal_techniques(transcript)
        }

    async def _identify_time_markers(self, transcript: str) -> List[Dict]:
        """تحديد المؤشرات الزمنية"""
        time_patterns = {
            "ماضي": [r"في الماضي", r"قديماً", r"منذ سنوات", r"كان يا ما كان"],
            "حاضر": [r"الآن", r"حالياً", r"في هذه اللحظة", r"اليوم"],
            "مستقبل": [r"غداً", r"في المستقبل", r"قريباً", r"سوف"],
            "تسلسلي": [r"ثم", r"بعد ذلك", r"لاحقاً", r"في النهاية"]
        }
        
        markers = []
        sentences = transcript.split('.')
        
        for i, sentence in enumerate(sentences):
            for time_type, patterns in time_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, sentence):
                        markers.append({
                            "position": i,
                            "type": time_type,
                            "marker": pattern,
                            "context": sentence.strip()
                        })
        
        return markers

    async def _establish_chronology(self, time_markers: List[Dict]) -> List[str]:
        """إنشاء التسلسل الزمني"""
        chronology = []
        
        # ترتيب المؤشرات حسب الموضع
        sorted_markers = sorted(time_markers, key=lambda x: x["position"])
        
        for marker in sorted_markers:
            chronology.append(f"الموضع {marker['position']}: {marker['type']} - {marker['context'][:50]}...")
        
        return chronology

    async def _analyze_narrative_time(self, transcript: str) -> Dict[str, Any]:
        """تحليل الزمن السردي"""
        total_length = len(transcript.split('.'))
        
        # تقدير مدة الأحداث المروية
        estimated_story_duration = await self._estimate_story_duration(transcript)
        
        # تحليل الإيقاع السردي
        narrative_pace = await self._analyze_narrative_pace(transcript)
        
        return {
            "narrative_length": total_length,
            "estimated_duration": estimated_story_duration,
            "narrative_pace": narrative_pace,
            "time_compression": await self._detect_time_compression(transcript)
        }

    async def _estimate_story_duration(self, transcript: str) -> str:
        """تقدير مدة القصة"""
        duration_clues = {
            "دقائق": [r"دقيقة", r"دقائق", r"لحظة"],
            "ساعات": [r"ساعة", r"ساعات", r"صباح", r"مساء"],
            "أيام": [r"يوم", r"أيام", r"أمس", r"غداً"],
            "أسابيع": [r"أسبوع", r"أسابيع"],
            "شهور": [r"شهر", r"شهور"],
            "سنوات": [r"سنة", r"سنوات", r"عام", r"أعوام"]
        }
        
        max_duration = "دقائق"
        for duration, patterns in duration_clues.items():
            for pattern in patterns:
                if re.search(pattern, transcript):
                    max_duration = duration
        
        return max_duration

    async def _analyze_narrative_pace(self, transcript: str) -> str:
        """تحليل إيقاع السرد"""
        pace_indicators = {
            "سريع": [r"فجأة", r"بسرعة", r"على الفور", r"مباشرة"],
            "بطيء": [r"ببطء", r"تدريجياً", r"بهدوء", r"بتأني"],
            "متوسط": [r"بعد قليل", r"تدريجياً", r"بعد فترة"]
        }
        
        pace_scores = {}
        for pace, indicators in pace_indicators.items():
            score = sum(1 for indicator in indicators if re.search(indicator, transcript))
            pace_scores[pace] = score
        
        if not any(pace_scores.values()):
            return "متوسط"
        
        return max(pace_scores, key=pace_scores.get)

    async def _detect_time_compression(self, transcript: str) -> List[str]:
        """كشف ضغط الزمن في السرد"""
        compression_techniques = []
        
        compression_patterns = {
            "تلخيص": [r"خلاصة القول", r"باختصار", r"في النهاية"],
            "تسريع": [r"مرت السنوات", r"بعد فترة طويلة", r"بمرور الوقت"],
            "قفز زمني": [r"بعدها بسنوات", r"في اليوم التالي", r"بعد أشهر"]
        }
        
        for technique, patterns in compression_patterns.items():
            for pattern in patterns:
                if re.search(pattern, transcript):
                    compression_techniques.append(technique)
                    break
        
        return compression_techniques

    async def _extract_themes(self, transcript: str) -> Dict[str, Any]:
        """استخلاص المواضيع الرئيسية"""
        universal_themes = {
            "الحب والعلاقات": ["حب", "زواج", "صداقة", "عائلة", "علاقة"],
            "الصراع والتحدي": ["صراع", "معركة", "تحدي", "عقبة", "مشكلة"],
            "النمو والتطور": ["تعلم", "تطور", "نضج", "تغيير", "نمو"],
            "الهوية والانتماء": ["هوية", "انتماء", "جذور", "أصل", "شخصية"],
            "العدالة والأخلاق": ["عدالة", "حق", "أخلاق", "قيم", "مبادئ"],
            "الموت والحياة": ["موت", "حياة", "وجود", "مصير", "نهاية"]
        }
        
        theme_analysis = {}
        for theme, keywords in universal_themes.items():
            score = sum(1 for keyword in keywords if keyword in transcript)
            if score > 0:
                theme_analysis[theme] = {
                    "score": score,
                    "examples": await self._find_theme_examples(theme, keywords, transcript)
                }
        
        return {
            "identified_themes": theme_analysis,
            "dominant_theme": max(theme_analysis.keys(), key=lambda k: theme_analysis[k]["score"]) if theme_analysis else "غير محدد",
            "theme_development": await self._analyze_theme_development(theme_analysis, transcript)
        }

    async def _find_theme_examples(self, theme: str, keywords: List[str], transcript: str) -> List[str]:
        """العثور على أمثلة للموضوع"""
        examples = []
        sentences = transcript.split('.')
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                examples.append(sentence.strip())
                if len(examples) >= 3:  # حد أقصى 3 أمثلة
                    break
        
        return examples

    async def _analyze_theme_development(self, themes: Dict, transcript: str) -> Dict[str, Any]:
        """تحليل تطور المواضيع"""
        if not themes:
            return {}
        
        sentences = transcript.split('.')
        theme_timeline = {}
        
        for theme in themes.keys():
            theme_timeline[theme] = []
            
        for i, sentence in enumerate(sentences):
            for theme, data in themes.items():
                # تحقق من وجود كلمات مفتاحية للموضوع
                theme_keywords = {
                    "الحب والعلاقات": ["حب", "زواج", "صداقة", "عائلة"],
                    "الصراع والتحدي": ["صراع", "معركة", "تحدي", "عقبة"],
                    # يمكن إضافة المزيد
                }
                
                if theme in theme_keywords:
                    if any(keyword in sentence for keyword in theme_keywords[theme]):
                        theme_timeline[theme].append(i)
        
        development_patterns = {}
        for theme, positions in theme_timeline.items():
            if len(positions) > 1:
                development_patterns[theme] = {
                    "frequency": len(positions),
                    "distribution": "متساوي" if self._is_evenly_distributed(positions, len(sentences)) else "متجمع",
                    "progression": "متصاعد" if positions[-1] > positions[0] else "متنازل"
                }
        
        return development_patterns

    def _is_evenly_distributed(self, positions: List[int], total_length: int) -> bool:
        """تحقق من التوزيع المتساوي"""
        if len(positions) < 2:
            return False
        
        expected_distance = total_length / len(positions)
        actual_distances = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        avg_distance = sum(actual_distances) / len(actual_distances)
        
        return abs(avg_distance - expected_distance) < expected_distance * 0.3

    async def _analyze_dialogue_patterns(self, transcript: str) -> Dict[str, Any]:
        """تحليل أنماط الحوار"""
        dialogue_analysis = {
            "dialogue_ratio": await self._calculate_dialogue_ratio(transcript),
            "speech_patterns": await self._analyze_speech_patterns(transcript),
            "conversation_structure": await self._analyze_conversation_structure(transcript),
            "character_voices": await self._analyze_character_voices(transcript)
        }
        
        return dialogue_analysis

    async def _calculate_dialogue_ratio(self, transcript: str) -> float:
        """حساب نسبة الحوار في النص"""
        sentences = transcript.split('.')
        dialogue_sentences = 0
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in self.narrative_indicators["حوار"]):
                dialogue_sentences += 1
        
        return dialogue_sentences / len(sentences) if sentences else 0

    async def _analyze_speech_patterns(self, transcript: str) -> Dict[str, Any]:
        """تحليل أنماط الكلام"""
        speech_verbs = ["قال", "أجاب", "سأل", "صرخ", "همس", "تمتم"]
        verb_usage = {}
        
        for verb in speech_verbs:
            count = transcript.count(verb)
            if count > 0:
                verb_usage[verb] = count
        
        return {
            "speech_verb_usage": verb_usage,
            "most_common_speech_verb": max(verb_usage, key=verb_usage.get) if verb_usage else "غير محدد",
            "dialogue_variety": len(verb_usage)
        }

    async def _analyze_conversation_structure(self, transcript: str) -> Dict[str, Any]:
        """تحليل بنية المحادثات"""
        # البحث عن بداية ونهاية المحادثات
        conversations = []
        sentences = transcript.split('.')
        
        current_conversation = None
        for i, sentence in enumerate(sentences):
            if any(indicator in sentence for indicator in self.narrative_indicators["حوار"]):
                if current_conversation is None:
                    current_conversation = {"start": i, "length": 1}
                else:
                    current_conversation["length"] += 1
            else:
                if current_conversation is not None:
                    conversations.append(current_conversation)
                    current_conversation = None
        
        if conversations:
            avg_length = sum(conv["length"] for conv in conversations) / len(conversations)
            return {
                "conversation_count": len(conversations),
                "average_length": avg_length,
                "longest_conversation": max(conversations, key=lambda x: x["length"])["length"],
                "conversation_density": len(conversations) / len(sentences)
            }
        
        return {"conversation_count": 0}

    async def _analyze_character_voices(self, transcript: str) -> Dict[str, Any]:
        """تحليل أصوات الشخصيات"""
        # تحليل مبسط - في التطبيق الحقيقي سنربط مع تحليل الشخصيات
        voice_characteristics = {
            "formal": ["سيدي", "حضرتك", "تفضل", "من فضلك"],
            "informal": ["يا أخي", "شوف", "اسمع", "والله"],
            "emotional": ["للأسف", "بصراحة", "والله", "يا رب"],
            "authoritative": ["يجب", "لازم", "ضروري", "احذر"]
        }
        
        voice_analysis = {}
        for voice_type, indicators in voice_characteristics.items():
            count = sum(1 for indicator in indicators if indicator in transcript)
            if count > 0:
                voice_analysis[voice_type] = count
        
        return voice_analysis

    async def _identify_narrative_voice(self, transcript: str) -> Dict[str, Any]:
        """تحديد صوت السارد"""
        voice_indicators = {
            "first_person": ["أنا", "نحن", "لي", "لنا"],
            "third_person": ["هو", "هي", "هم", "هن"],
            "omniscient": ["كان يفكر", "شعر بـ", "لم يعرف أحد"],
            "limited": ["بدا", "ظهر", "كما لو"]
        }
        
        voice_scores = {}
        for voice_type, indicators in voice_indicators.items():
            score = sum(1 for indicator in indicators if indicator in transcript)
            voice_scores[voice_type] = score
        
        dominant_voice = max(voice_scores, key=voice_scores.get) if any(voice_scores.values()) else "غير محدد"
        
        return {
            "narrative_perspective": dominant_voice,
            "voice_consistency": await self._check_voice_consistency(transcript),
            "narrator_reliability": await self._assess_narrator_reliability(transcript)
        }

    async def _check_voice_consistency(self, transcript: str) -> str:
        """فحص اتساق صوت السارد"""
        # تحليل مبسط للاتساق
        first_half = transcript[:len(transcript)//2]
        second_half = transcript[len(transcript)//2:]
        
        first_voice = await self._identify_narrative_voice(first_half)
        second_voice = await self._identify_narrative_voice(second_half)
        
        if first_voice["narrative_perspective"] == second_voice["narrative_perspective"]:
            return "متسق"
        else:
            return "متغير"

    async def _assess_narrator_reliability(self, transcript: str) -> str:
        """تقييم موثوقية السارد"""
        reliability_indicators = {
            "reliable": ["في الواقع", "بالفعل", "حقيقة", "فعلاً"],
            "unreliable": ["ربما", "قد يكون", "لست متأكد", "أعتقد"]
        }
        
        reliable_count = sum(1 for indicator in reliability_indicators["reliable"] if indicator in transcript)
        unreliable_count = sum(1 for indicator in reliability_indicators["unreliable"] if indicator in transcript)
        
        if reliable_count > unreliable_count:
            return "موثوق"
        elif unreliable_count > reliable_count:
            return "غير موثوق"
        else:
            return "متوسط الموثوقية"

    async def _extract_cultural_elements(self, transcript: str) -> Dict[str, Any]:
        """استخلاص العناصر الثقافية"""
        cultural_categories = {
            "دينية": ["الله", "صلاة", "مسجد", "قرآن", "حج", "رمضان"],
            "تقليدية": ["عادات", "تقاليد", "تراث", "أجداد", "قبيلة"],
            "اجتماعية": ["عائلة", "زواج", "أطفال", "مجتمع", "جيران"],
            "جغرافية": ["صحراء", "جبال", "بحر", "مدينة", "قرية"],
            "تاريخية": ["ماضي", "تاريخ", "أسلاف", "حضارة", "عصر"]
        }
        
        cultural_analysis = {}
        for category, keywords in cultural_categories.items():
            count = sum(1 for keyword in keywords if keyword in transcript)
            if count > 0:
                cultural_analysis[category] = {
                    "frequency": count,
                    "examples": [keyword for keyword in keywords if keyword in transcript]
                }
        
        return {
            "cultural_elements": cultural_analysis,
            "cultural_density": sum(data["frequency"] for data in cultural_analysis.values()),
            "dominant_cultural_aspect": max(cultural_analysis.keys(), key=lambda k: cultural_analysis[k]["frequency"]) if cultural_analysis else "غير محدد"
        }

    async def _identify_conflicts(self, transcript: str) -> Dict[str, Any]:
        """تحديد أنواع الصراعات"""
        conflict_types = {
            "internal": ["صراع داخلي", "تردد", "حيرة", "قلق", "شك"],
            "interpersonal": ["خلاف", "نزاع", "شجار", "صراع مع"],
            "societal": ["ظلم اجتماعي", "تمييز", "فقر", "فساد"],
            "nature": ["عاصفة", "زلزال", "فيضان", "جفاف", "برد"],
            "supernatural": ["قدر", "مصير", "غيب", "خارق", "سحر"]
        }
        
        identified_conflicts = {}
        for conflict_type, indicators in conflict_types.items():
            count = sum(1 for indicator in indicators if indicator in transcript)
            if count > 0:
                identified_conflicts[conflict_type] = {
                    "intensity": count,
                    "examples": await self._find_conflict_examples(indicators, transcript)
                }
        
        return {
            "conflict_types": identified_conflicts,
            "primary_conflict": max(identified_conflicts.keys(), key=lambda k: identified_conflicts[k]["intensity"]) if identified_conflicts else "غير محدد",
            "conflict_complexity": len(identified_conflicts)
        }

    async def _find_conflict_examples(self, indicators: List[str], transcript: str) -> List[str]:
        """العثور على أمثلة للصراعات"""
        examples = []
        sentences = transcript.split('.')
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in indicators):
                examples.append(sentence.strip())
                if len(examples) >= 2:  # حد أقصى مثالين
                    break
        
        return examples

    async def generate_analysis_report(self, analysis_result: Dict[str, Any]) -> str:
        """إنشاء تقرير شامل للتحليل"""
        report_sections = []
        
        # قسم الشخصيات
        if analysis_result.get("characters"):
            characters_section = "## تحليل الشخصيات\n\n"
            for character in analysis_result["characters"]:
                characters_section += f"### {character.name}\n"
                characters_section += f"- الدور: {character.role}\n"
                characters_section += f"- السمات: {', '.join(character.traits)}\n"
                characters_section += f"- درجة الأهمية: {character.significance_score:.2f}\n\n"
            report_sections.append(characters_section)
        
        # قسم البنية السردية
        if analysis_result.get("plot_structure"):
            plot_section = "## البنية السردية\n\n"
            plot_structure = analysis_result["plot_structure"]
            plot_section += f"- عدد نقاط الحبكة: {len(plot_structure.get('plot_points', []))}\n"
            plot_section += f"- إيقاع السرد: {plot_structure.get('pacing_analysis', {}).get('pacing', 'غير محدد')}\n\n"
            report_sections.append(plot_section)
        
        # قسم التحليل العاطفي
        if analysis_result.get("emotional_arc"):
            emotional_section = "## التحليل العاطفي\n\n"
            emotional_arc = analysis_result["emotional_arc"]
            dominant_emotions = emotional_arc.get("dominant_emotions", [])
            if dominant_emotions:
                emotional_section += f"- العواطف المهيمنة: {', '.join(dominant_emotions[:3])}\n"
            emotional_section += f"- التقلب العاطفي: {emotional_arc.get('patterns', {}).get('emotional_volatility', 0):.2f}\n\n"
            report_sections.append(emotional_section)
        
        # قسم المواضيع
        if analysis_result.get("thematic_analysis"):
            themes_section = "## التحليل الموضوعي\n\n"
            thematic_analysis = analysis_result["thematic_analysis"]
            dominant_theme = thematic_analysis.get("dominant_theme", "غير محدد")
            themes_section += f"- الموضوع المهيمن: {dominant_theme}\n"
            identified_themes = thematic_analysis.get("identified_themes", {})
            if identified_themes:
                themes_section += "- المواضيع المحددة:\n"
                for theme, data in identified_themes.items():
                    themes_section += f"  - {theme}: {data['score']} مرة\n"
            themes_section += "\n"
            report_sections.append(themes_section)
        
        # دمج جميع الأقسام
        final_report = "# تقرير تحليل السرد الخام\n\n"
        final_report += "\n".join(report_sections)
        
        return final_report
