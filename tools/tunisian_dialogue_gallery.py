# tools/tunisian_dialogue_gallery.py (النسخة المحسنة)

import logging
import random
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger("TunisianDialogueEngine")

class TunisianDialogueEngine:
    """
    محرك متقدم لتوليد الحوارات باللهجات التونسية المختلفة.
    """
    def __init__(self, data_file_path: str = "data/tunisian_dialects.json"):
        self.dialects_data = self._load_dialects_data(data_file_path)
        if not self.dialects_data:
            logger.error("Failed to load dialect data. The engine will not function correctly.")
        else:
            logger.info(f"✅ Tunisian Dialogue Engine initialized with {len(self.dialects_data.get('dialects', []))} dialects.")

    def _load_dialects_data(self, file_path: str) -> Dict[str, Any]:
        """
        تحميل بيانات اللهجات من ملف JSON.
        """
        try:
            p = Path(file_path)
            if not p.exists():
                logger.warning(f"Dialect data file not found at: {file_path}. Creating a default one.")
                self._create_default_data_file(p)
            
            with p.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading or parsing dialect data file: {e}")
            return {}

    def _create_default_data_file(self, p: Path):
        """
        إنشاء ملف بيانات افتراضي إذا لم يكن موجودًا.
        """
        p.parent.mkdir(parents=True, exist_ok=True)
        default_data = { "dialects": [] } # ابدأ فارغًا للسماح للمستخدم بإضافات
        with p.open('w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)

    def generate_dialogue(
        self,
        character_archetype: str,
        topic: str,
        mood: str,
        dialect_id: str = "tunisois" # إضافة معرف اللهجة
    ) -> str:
        """
        يولد جملة حوارية مناسبة للشخصية، الموقف، واللهجة الجهوية.
        """
        logger.info(f"Generating dialogue for: [Dialect: {dialect_id}, Archetype: {character_archetype}, Topic: {topic}, Mood: {mood}]")
        
        # 1. البحث عن اللهجة المطلوبة
        dialect_data = next((d for d in self.dialects_data.get('dialects', []) if d['id'] == dialect_id), None)
        if not dialect_data:
            logger.warning(f"Dialect '{dialect_id}' not found. Falling back to default.")
            return "..."

        # 2. البحث عن نمط الشخصية داخل اللهجة
        archetype_data = dialect_data.get('archetypes', {}).get(character_archetype)
        if not archetype_data:
            logger.warning(f"Archetype '{character_archetype}' not found for dialect '{dialect_id}'.")
            return "آش نقول...؟" # رد افتراضي يعكس الحيرة

        # 3. اختيار الحوار بناءً على المزاج والموضوع (أكثر ذكاءً)
        dialogue_options = []
        if mood in archetype_data.get('moods', {}):
            dialogue_options.extend(archetype_data['moods'][mood])
            
        if topic in archetype_data.get('topics', {}):
            dialogue_options.extend(archetype_data['topics'][topic])

        if not dialogue_options:
            # إذا لم نجد شيئًا محددًا، نستخدم الأمثال العامة لهذه اللهجة
            dialogue_options.extend(dialect_data.get("proverbs", ["..."]))

        return random.choice(dialogue_options)

    def get_available_dialects(self) -> List[Dict[str, str]]:
        """
        إرجاع قائمة باللهجات المتاحة.
        """
        return [
            {"id": d.get("id"), "name": d.get("name")} 
            for d in self.dialects_data.get('dialects', [])
        ]

# إنشاء مثيل وحيد من المحرك
dialogue_engine = TunisianDialogueEngine()
