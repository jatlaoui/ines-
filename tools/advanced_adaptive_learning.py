"""
نظام التعلم التكيفي المتقدم - المرحلة الثانية
يحلل أنماط المستخدم ويتعلم من تفاعلاته لتقديم تجربة مخصصة ومحسنة باستمرار

الميزات الجديدة:
- التعلم من التعديلات اليدوية
- التعلم من تفضيلات الحبكة والشخصيات
- تحليل الأسلوب الشخصي للمستخدم
- تخصيص دقيق لأسلوب الجطلاوي
"""

import json
import re
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import numpy as np
try:
    from unified_database import UnifiedDatabase
except ImportError:
    from .unified_database import UnifiedDatabase

try:
    from adaptive_learning_service import AdaptiveLearningService
except ImportError:
    # استيراد بديل إذا لم يكن موجود
    class AdaptiveLearningService:
        def __init__(self):
            pass
        def initialize_user_profile(self, user_id):
            return {}
        def log_interaction(self, *args, **kwargs):
            pass

@dataclass
class UserEdit:
    """تمثيل تعديل المستخدم"""
    edit_id: str
    original_text: str
    edited_text: str
    edit_type: str  # 'style', 'structure', 'content', 'grammar'
    timestamp: datetime
    context: Dict[str, Any]

@dataclass
class PlotPreference:
    """تفضيلات الحبكة"""
    plot_type: str
    complexity_level: float
    pacing_preference: str  # 'slow', 'medium', 'fast'
    conflict_types: List[str]
    resolution_style: str
    frequency: int

@dataclass
class CharacterPreference:
    """تفضيلات الشخصيات"""
    character_archetype: str
    development_style: str  # 'gradual', 'dramatic', 'static'
    dialogue_style: str
    relationship_complexity: float
    frequency: int

@dataclass
class StylePattern:
    """نمط أسلوبي للمستخدم"""
    pattern_id: str
    description: str
    linguistic_features: Dict[str, float]
    usage_frequency: int
    contexts: List[str]

class AdvancedAdaptiveLearning(AdaptiveLearningService):
    """نظام التعلم التكيفي المتقدم"""
    
    def __init__(self):
        super().__init__()
        self.db = UnifiedDatabase()
        self.edit_patterns_cache = {}
        self.style_analysis_cache = {}
        self.jattlaoui_customization_cache = {}
        
        # معايير تحليل الأسلوب
        self.style_metrics = {
            'sentence_length': self._analyze_sentence_length,
            'vocabulary_richness': self._analyze_vocabulary_richness,
            'metaphor_usage': self._analyze_metaphor_usage,
            'dialogue_ratio': self._analyze_dialogue_ratio,
            'emotional_tone': self._analyze_emotional_tone,
            'temporal_structure': self._analyze_temporal_structure,
            'character_focus': self._analyze_character_focus,
            'descriptive_density': self._analyze_descriptive_density
        }
        
        # أنماط الجطلاوي القابلة للتخصيص
        self.jattlaoui_elements = {
            'metaphorical_intensity': 0.8,
            'symbolic_references': 0.7,
            'emotional_depth': 0.9,
            'philosophical_undertones': 0.6,
            'cultural_references': 0.8,
            'narrative_complexity': 0.7,
            'sensory_descriptions': 0.8,
            'mystical_elements': 0.5
        }
    
    # === التعلم من التعديلات اليدوية ===
    
    def log_user_edit(
        self, 
        user_id: str, 
        original_text: str, 
        edited_text: str, 
        context: Dict[str, Any] = None
    ) -> str:
        """تسجيل تعديل المستخدم وتحليله"""
        edit_id = hashlib.md5(f"{user_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        # تحليل نوع التعديل
        edit_type = self._classify_edit_type(original_text, edited_text)
        
        edit = UserEdit(
            edit_id=edit_id,
            original_text=original_text,
            edited_text=edited_text,
            edit_type=edit_type,
            timestamp=datetime.now(),
            context=context or {}
        )
        
        # حفظ في قاعدة البيانات
        self._save_user_edit(user_id, edit)
        
        # تحديث أنماط التعلم
        self._update_edit_patterns(user_id, edit)
        
        return edit_id
    
    def _classify_edit_type(self, original: str, edited: str) -> str:
        """تصنيف نوع التعديل"""
        original_words = set(original.split())
        edited_words = set(edited.split())
        
        # تحليل التغييرات
        added_words = edited_words - original_words
        removed_words = original_words - edited_words
        
        # قواعد التصنيف
        if len(added_words) > len(removed_words) * 1.5:
            return 'expansion'
        elif len(removed_words) > len(added_words) * 1.5:
            return 'condensation'
        elif any(word in ['جميل', 'رائع', 'ممتاز', 'بديع'] for word in added_words):
            return 'style_enhancement'
        elif any(word in ['لكن', 'إلا', 'غير'] for word in added_words):
            return 'logical_refinement'
        elif len(edited.split('.')) != len(original.split('.')):
            return 'structure_change'
        else:
            return 'content_refinement'
    
    def _update_edit_patterns(self, user_id: str, edit: UserEdit):
        """تحديث أنماط التعديل للمستخدم"""
        profile = self.initialize_user_profile(user_id)
        
        # تحليل الأنماط
        patterns = profile.get('edit_patterns', {})
        
        # تحديث إحصائيات نوع التعديل
        patterns[edit.edit_type] = patterns.get(edit.edit_type, 0) + 1
        
        # تحليل التفضيلات الأسلوبية
        style_changes = self._analyze_style_changes(edit.original_text, edit.edited_text)
        
        for style_aspect, change_value in style_changes.items():
            if style_aspect not in patterns:
                patterns[style_aspect] = []
            patterns[style_aspect].append(change_value)
            
            # الاحتفاظ بآخر 20 تغيير فقط
            if len(patterns[style_aspect]) > 20:
                patterns[style_aspect] = patterns[style_aspect][-20:]
        
        # حفظ التحديثات
        self._save_edit_patterns(user_id, patterns)
    
    def _analyze_style_changes(self, original: str, edited: str) -> Dict[str, float]:
        """تحليل التغييرات الأسلوبية"""
        changes = {}
        
        # تحليل طول الجمل
        orig_avg_sentence = np.mean([len(s.split()) for s in original.split('.') if s.strip()])
        edit_avg_sentence = np.mean([len(s.split()) for s in edited.split('.') if s.strip()])
        changes['sentence_length_preference'] = edit_avg_sentence - orig_avg_sentence
        
        # تحليل استخدام الصفات
        orig_adjectives = len(re.findall(r'\b\w+ة\b|\b\w+ي\b', original))
        edit_adjectives = len(re.findall(r'\b\w+ة\b|\b\w+ي\b', edited))
        changes['descriptive_preference'] = (edit_adjectives - orig_adjectives) / max(len(original.split()), 1)
        
        # تحليل استخدام الاستعارات
        metaphor_words = ['كأن', 'مثل', 'شبه', 'يشبه', 'كالـ']
        orig_metaphors = sum(original.count(word) for word in metaphor_words)
        edit_metaphors = sum(edited.count(word) for word in metaphor_words)
        changes['metaphor_preference'] = edit_metaphors - orig_metaphors
        
        # تحليل التعقيد
        orig_complexity = len(re.findall(r'[،؛:]', original))
        edit_complexity = len(re.findall(r'[،؛:]', edited))
        changes['complexity_preference'] = edit_complexity - orig_complexity
        
        return changes
    
    # === التعلم من تفضيلات الحبكة والشخصيات ===
    
    def analyze_plot_preferences(self, user_id: str, blueprint_data: Dict[str, Any]) -> PlotPreference:
        """تحليل تفضيلات الحبكة من المخططات"""
        
        # استخراج عناصر الحبكة
        plot_structure = blueprint_data.get('plot_structure', {})
        conflicts = blueprint_data.get('conflicts', [])
        pacing = blueprint_data.get('pacing', 'medium')
        
        # تحليل نوع الحبكة
        plot_type = self._identify_plot_type(plot_structure)
        
        # تحليل مستوى التعقيد
        complexity_level = self._calculate_plot_complexity(plot_structure, conflicts)
        
        # تحليل أنواع الصراع
        conflict_types = [conflict.get('type', 'unknown') for conflict in conflicts]
        
        preference = PlotPreference(
            plot_type=plot_type,
            complexity_level=complexity_level,
            pacing_preference=pacing,
            conflict_types=conflict_types,
            resolution_style=plot_structure.get('resolution_style', 'satisfying'),
            frequency=1
        )
        
        # حفظ التفضيل
        self._save_plot_preference(user_id, preference)
        
        return preference
    
    def analyze_character_preferences(self, user_id: str, characters_data: List[Dict[str, Any]]) -> List[CharacterPreference]:
        """تحليل تفضيلات الشخصيات"""
        preferences = []
        
        for character in characters_data:
            # تحليل نمط الشخصية
            archetype = self._identify_character_archetype(character)
            
            # تحليل أسلوب التطوير
            development_style = character.get('development_style', 'gradual')
            
            # تحليل أسلوب الحوار
            dialogue_style = self._analyze_character_dialogue_style(character)
            
            # تحليل تعقيد العلاقات
            relationship_complexity = self._calculate_relationship_complexity(character)
            
            preference = CharacterPreference(
                character_archetype=archetype,
                development_style=development_style,
                dialogue_style=dialogue_style,
                relationship_complexity=relationship_complexity,
                frequency=1
            )
            
            preferences.append(preference)
        
        # حفظ التفضيلات
        for pref in preferences:
            self._save_character_preference(user_id, pref)
        
        return preferences
    
    def _identify_plot_type(self, plot_structure: Dict[str, Any]) -> str:
        """تحديد نوع الحبكة"""
        structure_elements = plot_structure.get('elements', [])
        
        if 'mystery' in str(structure_elements).lower():
            return 'mystery'
        elif 'romance' in str(structure_elements).lower():
            return 'romance'
        elif 'adventure' in str(structure_elements).lower():
            return 'adventure'
        elif 'drama' in str(structure_elements).lower():
            return 'drama'
        else:
            return 'literary'
    
    def _calculate_plot_complexity(self, plot_structure: Dict[str, Any], conflicts: List[Dict]) -> float:
        """حساب مستوى تعقيد الحبكة"""
        complexity_factors = [
            len(plot_structure.get('subplots', [])) * 0.2,
            len(conflicts) * 0.3,
            len(plot_structure.get('time_shifts', [])) * 0.25,
            len(plot_structure.get('perspective_changes', [])) * 0.25
        ]
        
        return min(sum(complexity_factors), 1.0)
    
    def _identify_character_archetype(self, character: Dict[str, Any]) -> str:
        """تحديد نمط الشخصية"""
        traits = character.get('traits', [])
        role = character.get('role', '').lower()
        
        if 'hero' in role or 'protagonist' in role:
            return 'hero'
        elif 'villain' in role or 'antagonist' in role:
            return 'villain'
        elif 'mentor' in traits or 'wise' in traits:
            return 'mentor'
        elif 'comic' in traits or 'funny' in traits:
            return 'comic_relief'
        else:
            return 'supporting'
    
    # === تحليل الأسلوب الشخصي ===
    
    def analyze_personal_style(self, user_id: str, text_samples: List[str]) -> Dict[str, Any]:
        """تحليل الأسلوب الشخصي للمستخدم من نصوصه"""
        
        if not text_samples:
            return {}
        
        style_profile = {}
        
        for metric_name, analyzer in self.style_metrics.items():
            try:
                values = [analyzer(text) for text in text_samples]
                style_profile[metric_name] = {
                    'average': np.mean(values),
                    'std': np.std(values),
                    'trend': self._calculate_trend(values)
                }
            except Exception as e:
                print(f"Error analyzing {metric_name}: {e}")
                style_profile[metric_name] = {'average': 0, 'std': 0, 'trend': 0}
        
        # استخراج الأنماط المميزة
        distinctive_patterns = self._extract_distinctive_patterns(text_samples)
        style_profile['distinctive_patterns'] = distinctive_patterns
        
        # حفظ الملف الأسلوبي
        self._save_style_profile(user_id, style_profile)
        
        return style_profile
    
    def _analyze_sentence_length(self, text: str) -> float:
        """تحليل متوسط طول الجملة"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if not sentences:
            return 0
        return np.mean([len(sentence.split()) for sentence in sentences])
    
    def _analyze_vocabulary_richness(self, text: str) -> float:
        """تحليل ثراء المفردات"""
        words = text.split()
        if not words:
            return 0
        unique_words = set(words)
        return len(unique_words) / len(words)
    
    def _analyze_metaphor_usage(self, text: str) -> float:
        """تحليل استخدام الاستعارات"""
        metaphor_indicators = ['كأن', 'مثل', 'شبه', 'يشبه', 'كالـ', 'بمثابة']
        total_words = len(text.split())
        if total_words == 0:
            return 0
        metaphor_count = sum(text.count(indicator) for indicator in metaphor_indicators)
        return metaphor_count / total_words
    
    def _analyze_dialogue_ratio(self, text: str) -> float:
        """تحليل نسبة الحوار"""
        dialogue_lines = len(re.findall(r'"[^"]*"', text))
        total_lines = len(text.split('\n'))
        if total_lines == 0:
            return 0
        return dialogue_lines / total_lines
    
    def _analyze_emotional_tone(self, text: str) -> float:
        """تحليل النبرة العاطفية"""
        emotional_words = ['حزن', 'فرح', 'غضب', 'خوف', 'أمل', 'حب', 'كره', 'شوق']
        total_words = len(text.split())
        if total_words == 0:
            return 0
        emotional_count = sum(text.count(word) for word in emotional_words)
        return emotional_count / total_words
    
    def _analyze_temporal_structure(self, text: str) -> float:
        """تحليل البنية الزمنية"""
        time_indicators = ['أمس', 'اليوم', 'غداً', 'قبل', 'بعد', 'عندما', 'حين', 'بينما']
        total_words = len(text.split())
        if total_words == 0:
            return 0
        time_count = sum(text.count(indicator) for indicator in time_indicators)
        return time_count / total_words
    
    def _analyze_character_focus(self, text: str) -> float:
        """تحليل التركيز على الشخصيات"""
        pronouns = ['هو', 'هي', 'هم', 'هن', 'أنت', 'أنتم', 'أنا', 'نحن']
        total_words = len(text.split())
        if total_words == 0:
            return 0
        pronoun_count = sum(text.count(pronoun) for pronoun in pronouns)
        return pronoun_count / total_words
    
    def _analyze_descriptive_density(self, text: str) -> float:
        """تحليل كثافة الوصف"""
        adjectives = re.findall(r'\b\w+ة\b|\b\w+ي\b|\b\w+ية\b', text)
        total_words = len(text.split())
        if total_words == 0:
            return 0
        return len(adjectives) / total_words
    
    def _calculate_trend(self, values: List[float]) -> float:
        """حساب الاتجاه العام للقيم"""
        if len(values) < 2:
            return 0
        
        x = np.arange(len(values))
        z = np.polyfit(x, values, 1)
        return z[0]  # الميل
    
    def _extract_distinctive_patterns(self, texts: List[str]) -> List[StylePattern]:
        """استخراج الأنماط الأسلوبية المميزة"""
        patterns = []
        
        # تحليل العبارات المتكررة
        all_text = ' '.join(texts)
        words = all_text.split()
        
        # البحث عن العبارات ثلاثية الكلمات المتكررة
        trigrams = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
        trigram_counts = Counter(trigrams)
        
        for trigram, count in trigram_counts.most_common(10):
            if count >= 2:  # تكرار مرتين على الأقل
                pattern = StylePattern(
                    pattern_id=hashlib.md5(trigram.encode()).hexdigest()[:8],
                    description=f"العبارة المتكررة: {trigram}",
                    linguistic_features={'frequency': count, 'length': len(trigram.split())},
                    usage_frequency=count,
                    contexts=['general']
                )
                patterns.append(pattern)
        
        return patterns
    
    # === تخصيص أسلوب الجطلاوي ===
    
    def customize_jattlaoui_style(self, user_id: str) -> Dict[str, float]:
        """تخصيص أسلوب الجطلاوي بناءً على تفضيلات المستخدم"""
        
        # جلب بيانات المستخدم
        edit_patterns = self._get_edit_patterns(user_id)
        style_profile = self._get_style_profile(user_id)
        
        # نسخة من العناصر الأساسية للجطلاوي
        customized_elements = self.jattlaoui_elements.copy()
        
        # تخصيص بناءً على أنماط التعديل
        if 'metaphor_preference' in edit_patterns:
            metaphor_changes = edit_patterns['metaphor_preference']
            if len(metaphor_changes) > 0:
                avg_change = np.mean(metaphor_changes)
                customized_elements['metaphorical_intensity'] += avg_change * 0.1
        
        # تخصيص بناءً على الملف الأسلوبي
        if style_profile and 'metaphor_usage' in style_profile:
            user_metaphor_level = style_profile['metaphor_usage']['average']
            if user_metaphor_level > 0.05:  # مستوى عالي من الاستعارات
                customized_elements['metaphorical_intensity'] = min(1.0, 
                    customized_elements['metaphorical_intensity'] + 0.1)
            elif user_metaphor_level < 0.02:  # مستوى منخفض
                customized_elements['metaphorical_intensity'] = max(0.3, 
                    customized_elements['metaphorical_intensity'] - 0.1)
        
        # تخصيص العمق العاطفي
        if style_profile and 'emotional_tone' in style_profile:
            user_emotion_level = style_profile['emotional_tone']['average']
            customized_elements['emotional_depth'] = min(1.0, 
                max(0.3, user_emotion_level * 2))
        
        # تخصيص التعقيد السردي
        if 'complexity_preference' in edit_patterns:
            complexity_changes = edit_patterns['complexity_preference']
            if len(complexity_changes) > 0:
                avg_complexity_change = np.mean(complexity_changes)
                customized_elements['narrative_complexity'] += avg_complexity_change * 0.05
        
        # ضمان القيم ضمن النطاق المقبول
        for key in customized_elements:
            customized_elements[key] = max(0.1, min(1.0, customized_elements[key]))
        
        # حفظ التخصيص
        self._save_jattlaoui_customization(user_id, customized_elements)
        
        return customized_elements
    
    def generate_personalized_prompt(self, user_id: str, task_type: str, context: Dict[str, Any]) -> str:
        """توليد prompt مخصص للمستخدم"""
        
        # جلب التخصيصات
        jattlaoui_customization = self._get_jattlaoui_customization(user_id)
        style_profile = self._get_style_profile(user_id)
        edit_patterns = self._get_edit_patterns(user_id)
        
        # بناء الـ prompt الأساسي
        base_prompt = self._get_base_prompt(task_type)
        
        # إضافة التخصيصات الأسلوبية
        style_instructions = []
        
        if jattlaoui_customization:
            if jattlaoui_customization.get('metaphorical_intensity', 0) > 0.7:
                style_instructions.append("استخدم استعارات غنية ومعبرة")
            
            if jattlaoui_customization.get('emotional_depth', 0) > 0.8:
                style_instructions.append("اجعل النص عميق المشاعر ومؤثراً")
            
            if jattlaoui_customization.get('philosophical_undertones', 0) > 0.6:
                style_instructions.append("أضف تأملات فلسفية مناسبة")
        
        # إضافة تفضيلات من أنماط التعديل
        if edit_patterns:
            if edit_patterns.get('expansion', 0) > edit_patterns.get('condensation', 0):
                style_instructions.append("اجعل النص مفصلاً ومتوسعاً")
            elif edit_patterns.get('condensation', 0) > edit_patterns.get('expansion', 0):
                style_instructions.append("اجعل النص مقتضباً ومركزاً")
        
        # دمج التعليمات
        if style_instructions:
            personalized_prompt = f"{base_prompt}\n\nتعليمات أسلوبية مخصصة:\n" + "\n".join(f"- {instruction}" for instruction in style_instructions)
        else:
            personalized_prompt = base_prompt
        
        return personalized_prompt
    
    # === وظائف مساعدة لقاعدة البيانات ===
    
    def _save_user_edit(self, user_id: str, edit: UserEdit):
        """حفظ تعديل المستخدم في قاعدة البيانات"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_edits 
            (edit_id, user_id, original_text, edited_text, edit_type, timestamp, context)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            edit.edit_id, user_id, edit.original_text, edit.edited_text,
            edit.edit_type, edit.timestamp.isoformat(), json.dumps(edit.context)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_edit_patterns(self, user_id: str, patterns: Dict[str, Any]):
        """حفظ أنماط التعديل"""
        profile = self.initialize_user_profile(user_id)
        profile['edit_patterns'] = patterns
        
        from database import update_writer_profile
        update_writer_profile(user_id, {
            'edit_patterns_json': json.dumps(patterns),
            'last_updated': datetime.now().isoformat()
        })
    
    def _save_style_profile(self, user_id: str, style_profile: Dict[str, Any]):
        """حفظ الملف الأسلوبي"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # التحقق من وجود العمود، وإنشاؤه إذا لم يكن موجوداً
        cursor.execute("PRAGMA table_info(writer_profiles)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'personal_style_json' not in columns:
            cursor.execute('ALTER TABLE writer_profiles ADD COLUMN personal_style_json TEXT DEFAULT "{}"')
            cursor.execute('ALTER TABLE writer_profiles ADD COLUMN style_analysis_date TEXT')
        
        cursor.execute('''
            UPDATE writer_profiles 
            SET personal_style_json = ?, style_analysis_date = ?
            WHERE user_id = ?
        ''', (json.dumps(style_profile), datetime.now().isoformat(), user_id))
        
        if cursor.rowcount == 0:
            # إنشاء سجل جديد إذا لم يكن موجوداً
            cursor.execute('''
                INSERT INTO writer_profiles (user_id, personal_style_json, style_analysis_date)
                VALUES (?, ?, ?)
            ''', (user_id, json.dumps(style_profile), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def _save_jattlaoui_customization(self, user_id: str, customization: Dict[str, float]):
        """حفظ تخصيص الجطلاوي"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # التحقق من وجود العمود، وإنشاؤه إذا لم يكن موجوداً
        cursor.execute("PRAGMA table_info(writer_profiles)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'jattlaoui_customization_json' not in columns:
            cursor.execute('ALTER TABLE writer_profiles ADD COLUMN jattlaoui_customization_json TEXT DEFAULT "{}"')
            cursor.execute('ALTER TABLE writer_profiles ADD COLUMN customization_date TEXT')
        
        cursor.execute('''
            UPDATE writer_profiles 
            SET jattlaoui_customization_json = ?, customization_date = ?
            WHERE user_id = ?
        ''', (json.dumps(customization), datetime.now().isoformat(), user_id))
        
        if cursor.rowcount == 0:
            # إنشاء سجل جديد إذا لم يكن موجوداً
            cursor.execute('''
                INSERT INTO writer_profiles (user_id, jattlaoui_customization_json, customization_date)
                VALUES (?, ?, ?)
            ''', (user_id, json.dumps(customization), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def _get_edit_patterns(self, user_id: str) -> Dict[str, Any]:
        """جلب أنماط التعديل"""
        if user_id in self.edit_patterns_cache:
            return self.edit_patterns_cache[user_id]
        
        profile = self.initialize_user_profile(user_id)
        patterns = profile.get('edit_patterns', {})
        self.edit_patterns_cache[user_id] = patterns
        return patterns
    
    def _get_style_profile(self, user_id: str) -> Dict[str, Any]:
        """جلب الملف الأسلوبي"""
        if user_id in self.style_analysis_cache:
            return self.style_analysis_cache[user_id]
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT personal_style_json FROM writer_profiles WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            style_profile = json.loads(result[0])
            self.style_analysis_cache[user_id] = style_profile
            return style_profile
        
        return {}
    
    def _get_jattlaoui_customization(self, user_id: str) -> Dict[str, float]:
        """جلب تخصيص الجطلاوي"""
        if user_id in self.jattlaoui_customization_cache:
            return self.jattlaoui_customization_cache[user_id]
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT jattlaoui_customization_json FROM writer_profiles WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            customization = json.loads(result[0])
            self.jattlaoui_customization_cache[user_id] = customization
            return customization
        
        return self.jattlaoui_elements.copy()
    
    def _get_base_prompt(self, task_type: str) -> str:
        """الحصول على الـ prompt الأساسي حسب نوع المهمة"""
        base_prompts = {
            'generate_chapter': "اكتب فصلاً من الرواية يتبع أسلوب الجطلاوي في السرد",
            'generate_dialogue': "اكتب حواراً يتسم بعمق الشخصيات وواقعية التفاعل",
            'generate_description': "اكتب وصفاً يجمع بين الدقة والشاعرية",
            'generate_character': "طور شخصية معقدة ومتعددة الأبعاد",
            'refine_text': "حسن النص ليكون أكثر تماسكاً وإثارة للاهتمام"
        }
        
        return base_prompts.get(task_type, "اكتب نصاً إبداعياً عالي الجودة")
    
    # === وظائف إضافية للمساعدة ===
    
    def get_learning_insights(self, user_id: str) -> Dict[str, Any]:
        """الحصول على رؤى التعلم للمستخدم"""
        edit_patterns = self._get_edit_patterns(user_id)
        style_profile = self._get_style_profile(user_id)
        jattlaoui_customization = self._get_jattlaoui_customization(user_id)
        
        insights = {
            'writing_evolution': self._analyze_writing_evolution(user_id),
            'style_consistency': self._calculate_style_consistency(style_profile),
            'improvement_areas': self._identify_improvement_areas(edit_patterns),
            'personalization_level': self._calculate_personalization_level(jattlaoui_customization),
            'learning_progress': self._calculate_learning_progress(user_id)
        }
        
        return insights
    
    def _analyze_writing_evolution(self, user_id: str) -> Dict[str, Any]:
        """تحليل تطور الكتابة عبر الوقت"""
        # هذه وظيفة متقدمة يمكن تطويرها لاحقاً
        return {
            'trend': 'improving',
            'key_changes': ['increased_metaphor_usage', 'better_pacing'],
            'confidence_score': 0.75
        }
    
    def _calculate_style_consistency(self, style_profile: Dict[str, Any]) -> float:
        """حساب ثبات الأسلوب"""
        if not style_profile:
            return 0.0
        
        consistency_scores = []
        for metric, data in style_profile.items():
            if isinstance(data, dict) and 'std' in data:
                # كلما قل الانحراف المعياري، زاد الثبات
                consistency = 1.0 / (1.0 + data['std'])
                consistency_scores.append(consistency)
        
        return np.mean(consistency_scores) if consistency_scores else 0.0
    
    def _identify_improvement_areas(self, edit_patterns: Dict[str, Any]) -> List[str]:
        """تحديد مجالات التحسين"""
        areas = []
        
        if edit_patterns.get('style_enhancement', 0) > 5:
            areas.append('التحسين الأسلوبي')
        
        if edit_patterns.get('structure_change', 0) > 3:
            areas.append('البناء السردي')
        
        if edit_patterns.get('logical_refinement', 0) > 4:
            areas.append('التماسك المنطقي')
        
        return areas
    
    def _calculate_personalization_level(self, customization: Dict[str, float]) -> float:
        """حساب مستوى التخصيص"""
        if not customization:
            return 0.0
        
        # مقارنة مع القيم الافتراضية
        default_values = self.jattlaoui_elements
        differences = []
        
        for key, value in customization.items():
            if key in default_values:
                diff = abs(value - default_values[key])
                differences.append(diff)
        
        return np.mean(differences) if differences else 0.0
    
    def _calculate_learning_progress(self, user_id: str) -> float:
        """حساب تقدم التعلم"""
        # يمكن تطوير هذه الوظيفة بناءً على المقاييس المختلفة
        return 0.68  # قيمة مؤقتة

# إنشاء مثيل النظام المتقدم
advanced_adaptive_learning = AdvancedAdaptiveLearning()

def get_advanced_adaptive_learning() -> AdvancedAdaptiveLearning:
    """الحصول على مثيل النظام المتقدم"""
    return advanced_adaptive_learning
