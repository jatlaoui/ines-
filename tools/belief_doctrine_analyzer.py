# tools/belief_doctrine_analyzer.py
"""
Belief & Doctrine Analyzer
أداة متخصصة لبناء عمق روحي وعقائدي أصيل للشخصيات.
"""
import logging
import re
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger("BeliefDoctrineAnalyzer")

class BeliefSystem(Enum):
    ISLAMIC = "إسلامي"
    CHRISTIAN = "مسيحي"
    SECULAR = "علماني"
    MIXED = "مختلط"
    UNKNOWN = "غير محدد"

class DevotionLevel(Enum):
    DEVOUT = "متدين بشدة"
    MODERATE = "معتدل التدين"
    NOMINAL = "اسمي/بالوراثة"
    CONFLICTED = "في صراع"

class BeliefDoctrineAnalyzer:
    """
    أداة لتحليل المعتقدات والمذاهب في النصوص السردية.
    """
    def __init__(self):
        # قاعدة معرفة بالأنظمة العقائدية (يمكن توسيعها بشكل كبير)
        self.belief_knowledge_base = {
            BeliefSystem.ISLAMIC: {
                "keywords": ["الله", "محمد", "قرآن", "سنة", "صلاة", "زكاة", "حج", "إيمان", "مسجد"],
                "core_values": ["التوحيد", "العدل", "الرحمة", "الصبر", "الأمانة"],
                "prohibitions": ["الربا", "الزنا", "الكذب", "الظلم", "شرب الخمر"],
                "rituals": ["الصلوات الخمس", "صوم رمضان", "قراءة القرآن"]
            },
            BeliefSystem.CHRISTIAN: {
                "keywords": ["يسوع", "المسيح", "إنجيل", "كنيسة", "صليب", "قداس", "ثالوث"],
                "core_values": ["المحبة", "الغفران", "التضحية", "الإيمان", "الرجاء"],
                "prohibitions": ["الخطايا السبع المميتة", "عبادة الأوثان"],
                "rituals": ["العماد", "التناول", "الصلاة الربانية"]
            },
            BeliefSystem.SECULAR: {
                "keywords": ["العقل", "المنطق", "العلم", "الإنسانية", "الدولة المدنية"],
                "core_values": ["الحرية", "المساواة", "حقوق الإنسان", "الكرامة"],
                "prohibitions": ["الدوغمائية", "الخرافة", "انتهاك حقوق الآخرين"],
                "rituals": ["الانتخابات", "الاحتفالات الوطنية"]
            }
        }
        logger.info("BeliefDoctrineAnalyzer initialized.")

    async def analyze(self, content: str, context: Dict, options: Dict) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تقوم بتحليل شامل للمعتقدات في النص.
        """
        logger.info("Performing belief and doctrine analysis...")
        
        dominant_belief_system = self._identify_dominant_belief_system(content)
        values_analysis = self._analyze_values(content, dominant_belief_system)
        character_profiles = self._analyze_character_beliefs(content, dominant_belief_system)
        conflicts = self._identify_belief_conflicts(character_profiles)
        authenticity_score = self._assess_cultural_authenticity(content, dominant_belief_system)

        analysis_summary = {
            "dominant_belief_system": dominant_belief_system.value,
            "values_identified": len(values_analysis["values"]),
            "characters_analyzed": len(character_profiles),
            "conflicts_detected": len(conflicts),
            "authenticity_score": round(authenticity_score, 2)
        }
        
        return {
            "analysis": analysis_summary,
            "details": {
                "character_profiles": character_profiles,
                "values_analysis": values_analysis,
                "belief_conflicts": conflicts
            },
            "confidence_score": self._calculate_confidence(analysis_summary),
            "recommendations": self._generate_recommendations(analysis_summary, character_profiles),
            "visual_data": {}
        }

    def _identify_dominant_belief_system(self, text: str) -> BeliefSystem:
        """تحديد النظام العقائدي السائد."""
        scores = {system: 0 for system in self.belief_knowledge_base}
        
        text_lower = text.lower()
        for system, data in self.belief_knowledge_base.items():
            for keyword in data["keywords"]:
                scores[system] += text_lower.count(keyword.lower())
                
        # تحديد الأنظمة التي لها حضور
        present_systems = [system for system, score in scores.items() if score > 1]
        
        if len(present_systems) > 1:
            return BeliefSystem.MIXED
        elif len(present_systems) == 1:
            return present_systems[0]
        else:
            return BeliefSystem.UNKNOWN

    def _analyze_values(self, text: str, belief_system: BeliefSystem) -> Dict[str, List[str]]:
        """تحليل القيم والمحرمات والطقوس."""
        if belief_system not in self.belief_knowledge_base:
            return {"values": [], "prohibitions": [], "rituals": []}
            
        system_data = self.belief_knowledge_base[belief_system]
        
        found_values = [v for v in system_data["core_values"] if v in text]
        found_prohibitions = [p for p in system_data["prohibitions"] if p in text]
        found_rituals = [r for r in system_data["rituals"] if r in text]
        
        return {
            "values": found_values,
            "prohibitions": found_prohibitions,
            "rituals": found_rituals
        }
        
    def _analyze_character_beliefs(self, text: str, belief_system: BeliefSystem) -> List[Dict[str, Any]]:
        """بناء ملفات تعريف عقائدية للشخصيات."""
        profiles = []
        # استخلاص أسماء الشخصيات (منطق مبسط)
        character_names = set(re.findall(r"\b(علي|فاطمة|محمد|أحمد|خالد|زينب)\b", text))
        
        for name in character_names:
            profile = {
                "name": name,
                "belief_system": belief_system.value,
                "devotion_level": self._assess_devotion_level(name, text).value,
                "core_belief": f"أهم قيمة للشخصية '{name}' هي '{random.choice(self.belief_knowledge_base[belief_system]['core_values'])}'"
            }
            profiles.append(profile)
        return profiles

    def _assess_devotion_level(self, character_name: str, text: str) -> DevotionLevel:
        """تقييم مستوى التدين للشخصية."""
        devout_indicators = ["يصلي بخشوع", "دائم الذكر", "يقرأ القرآن"]
        conflicted_indicators = ["يشك في إيمانه", "يعاني من صراع ديني", "يتساءل عن القدر"]
        
        # البحث عن الجمل التي تذكر الشخصية
        char_sentences = [s for s in text.split('.') if character_name in s]
        char_text = ". ".join(char_sentences)
        
        if any(kw in char_text for kw in conflicted_indicators):
            return DevotionLevel.CONFLICTED
        if any(kw in char_text for kw in devout_indicators):
            return DevotionLevel.DEVOUT
        if "يؤمن بـ" in char_text:
            return DevotionLevel.MODERATE
        return DevotionLevel.NOMINAL

    def _identify_belief_conflicts(self, profiles: List[Dict]) -> List[str]:
        """كشف الصراعات الناتجة عن المعتقدات."""
        conflicts = []
        if len(profiles) < 2:
            return []

        # صراع بين شخصيتين
        p1, p2 = profiles[0], profiles[1]
        if p1["devotion_level"] != p2["devotion_level"]:
            conflicts.append(f"صراع محتمل بين تدين '{p1['name']}' المعتدل وتدين '{p2['name']}' المختلف.")
        
        # صراع داخلي
        for p in profiles:
            if p["devotion_level"] == DevotionLevel.CONFLICTED.value:
                conflicts.append(f"صراع داخلي لدى شخصية '{p['name']}' حول معتقداتها.")
                
        return conflicts

    def _assess_cultural_authenticity(self, text: str, belief_system: BeliefSystem) -> float:
        """تقييم الأصالة الثقافية والدينية للنص."""
        if belief_system not in self.belief_knowledge_base:
            return 0.5
            
        system_data = self.belief_knowledge_base[belief_system]
        keywords_found = sum(1 for kw in system_data["keywords"] if kw in text)
        
        # الأصالة تعتمد على مدى استخدام المفردات الصحيحة
        score = min(1.0, keywords_found / 5.0) * 10
        return round(score, 2)

    def _calculate_confidence(self, analysis_summary: Dict) -> float:
        """حساب درجة الثقة في التحليل."""
        score = 0.5 # أساس
        if analysis_summary["dominant_belief_system"] != BeliefSystem.UNKNOWN.value:
            score += 0.2
        if analysis_summary["characters_analyzed"] > 0:
            score += 0.1
        if analysis_summary["values_identified"] > 0:
            score += 0.1
        return min(1.0, score)

    def _generate_recommendations(self, summary: Dict, profiles: List) -> List[str]:
        """توليد توصيات لتحسين العمق العقائدي."""
        recs = []
        if summary["conflicts_detected"] == 0:
            recs.append("إضافة صراع عقائدي (داخلي أو خارجي) لزيادة عمق الحبكة.")
        if summary["characters_analyzed"] < 2:
            recs.append("تطوير شخصية أخرى بمعتقدات مختلفة أو متعارضة لخلق توتر درامي.")
        if summary["authenticity_score"] < 7.0:
            recs.append("استخدام مصطلحات وطقوس أكثر تحديدًا للنظام العقائدي لزيادة الأصالة.")
        return recs
