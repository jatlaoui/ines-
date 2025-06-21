# engines/advanced_context_engine.py (النسخة المحدثة مع التخصيص التونسي)
import logging
from typing import Dict, Any, List, Optional
# ... (بقية الاستيرادات كما هي)

logger = logging.getLogger("AdvancedContextEngine")

class AdvancedContextEngine:
    def __init__(self):
        # ... (بقية التهيئة كما هي) ...
        self._tunisian_archetypes = self._load_tunisian_archetypes()
        logger.info("AdvancedContextEngine initialized with Tunisian Archetypes.")

    def _load_tunisian_archetypes(self) -> Dict[str, Dict[str, Any]]:
        """تحميل قاعدة معرفة بالأنماط الشخصية التونسية."""
        return {
            "al_hajja": {
                "name": "الحاجة (الأم التقليدية)",
                "values": ["السترة", "كلام الناس", "مصلحة الأبناء", "التقاليد"],
                "language": ["أمثال شعبية", "دعاء", "لهجة محافظة"],
                "motivations": ["تزويج بناتها", "الحفاظ على سمعة العائلة"],
                "keywords": ["يا بنتي", "ربي يهدي", "شنوا يقولوا الناس", "العار"]
            },
            "al_mothaqafa": {
                "name": "المثقفة (الشابة العصرية)",
                "values": ["الاستقلالية", "تحقيق الذات", "الحب عن قناعة", "العلم"],
                "language": ["مزيج بين الدارجة والفرنسية", "مصطلحات حديثة", "منطقية"],
                "motivations": ["النجاح المهني", "إثبات النفس", "رفض التقاليد العمياء"],
                "keywords": ["C'est pas logique", "مستقبلي", "قراري", "نحب نفهم"]
            },
            "al_fahlawi": {
                "name": "الفهلوى (الانتهازي)",
                "values": ["المصلحة الشخصية", "المظاهر", "الوصول السريع"],
                "language": ["معسولة", "مليئة بالوعود", "تتملق"],
                "motivations": ["الحصول على المال أو النفوذ", "استغلال الفرص"],
                "keywords": ["مصلحتك معايا", "ثق فيا", "الخدمة ساهلة", "فلوس"]
            },
            "ammi_salah": {
                "name": "عمي صالح (الرجل الحكيم)",
                "values": ["الأصالة", "الحكمة", "الصبر", "الكلمة الطيبة"],
                "language": ["هادئة", "قليلة الكلام", "موزونة"],
                "motivations": ["إصلاح ذات البين", "الحفاظ على الود", "نقل الحكمة"],
                "keywords": ["يا ولدي", "الدنيا دروس", "الصبر مفتاح الفرج", "كل شي بالمكتوب"]
            }
        }

    async def analyze_tunisian_character(self, character_description: str) -> Dict[str, Any]:
        """
        يحلل وصف شخصية ويحدد نمطها التونسي.
        """
        logger.info(f"Analyzing Tunisian character archetype for: '{character_description[:50]}...'")
        scores = {name: 0 for name in self._tunisian_archetypes}

        for name, archetype_data in self._tunisian_archetypes.items():
            for keyword in archetype_data["keywords"]:
                if keyword in character_description:
                    scores[name] += 1
        
        if not any(scores.values()):
            return {"archetype": "غير محدد", "confidence": 0.3}

        best_match = max(scores, key=scores.get)
        confidence = scores[best_match] / len(self._tunisian_archetypes[best_match]["keywords"])
        
        return {
            "archetype_id": best_match,
            "archetype_name": self._tunisian_archetypes[best_match]["name"],
            "confidence": round(min(confidence, 1.0), 2),
            "matched_details": self._tunisian_archetypes[best_match]
        }

    # ... (بقية دوال المحرك كما هي) ...
