# tools/tunisian_dialogue_gallery.py
import logging
import random
from typing import Dict, Any, List

logger = logging.getLogger("TunisianDialogueGallery")

class TunisianDialogueGallery:
    """
    معرض ومولد للحوارات باللهجة التونسية الدارجة.
    """
    def __init__(self):
        # قاعدة بيانات مبسطة، في نظام حقيقي ستكون ضخمة
        self.proverbs = [
            "امشي بالنية وارقد في الثنية.",
            "اللي يده في الماء موش كي اللي يده في النار.",
            "ما يغرك زين الطفلة حتى تشوف الفعايل.",
            "جاء يكحلها عماها."
        ]
        self.dialogue_patterns = {
            "al_hajja": {
                "greetings": ["السلام عليكم يا بنتي", "أهلا بيك"],
                "complaints": ["ربي يهدي ما خلق", "الدنيا ما عادش فيها أمان"],
                "advice": ["رد بالك على روحك", "اسمع كلامي يهديك"],
                "linking_phrases": self.proverbs
            },
            "al_mothaqafa": {
                "greetings": ["Bonjour", "أهلاً، لاباس؟"],
                "objections": ["C'est pas logique", "هذا موش معقول بالكل"],
                "questions": ["علاش لازم نعمل هكة؟", "شنوة الهدف من هذا؟"],
                "linking_phrases": ["في الأخير", "المهم هو"]
            }
        }
        logger.info("TunisianDialogueGallery initialized.")

    def generate_dialogue(self, character_archetype: str, topic: str, mood: str) -> str:
        """
        يولد جملة حوارية مناسبة للشخصية والموقف.
        """
        logger.info(f"Generating dialogue for archetype '{character_archetype}' on topic '{topic}' with mood '{mood}'")
        
        patterns = self.dialogue_patterns.get(character_archetype)
        if not patterns:
            return "..." # حوار افتراضي

        # اختيار نمط بناءً على المزاج والموضوع
        if mood == "قلق":
            return random.choice(patterns.get("complaints", ["..."]))
        elif mood == "ملل" and "objections" in patterns:
            return random.choice(patterns.get("objections", ["..."]))
        else:
            # دمج جملة مع مثل شعبي
            base_sentence = random.choice(patterns.get("advice", ["..."]))
            proverb = random.choice(patterns.get("linking_phrases", [""]))
            return f"{base_sentence}... {proverb}"
