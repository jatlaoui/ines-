# agents/narrative_constructor_agent.py (النسخة المحدثة والشاملة)

import logging
from typing import Dict, Any, Optional, List

# --- الاستيرادات الأساسية ---
from .base_agent import BaseAgent

# --- استيراد المحركات والأدوات المتخصصة التي سيتعامل معها المايسترو ---
from engines.creative_layer_engine import CreativeLayerEngine
from engines.advanced_context_engine import AdvancedContextEngine # لتحليل الشخصيات
from tools.tunisian_dialogue_gallery import dialogue_engine # المحرك الجديد والمحسن

logger = logging.getLogger("NarrativeConstructorAgent")

class NarrativeConstructorAgent(BaseAgent):
    """
    وكيل بناء المشاهد السردية (المايسترو).
    ينسق بين المحركات المختلفة (الحسية، السياقية، اللهجة) لبناء مشاهد مسرحية
    أو روائية كاملة، غنية بالتفاصيل، وذات حوار أصيل.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "narrative_constructor_agent",
            name="مايسترو المشهد السردي",
            description="ينسق بين المحركات المتخصصة لبناء مشاهد كاملة وذات عمق."
        )
        # تهيئة المحركات التي سيستخدمها
        self.creative_engine = CreativeLayerEngine()
        self.context_engine = AdvancedContextEngine()
        self.dialogue_engine = dialogue_engine # استخدام المثيل الوحيد
        logger.info("NarrativeConstructorAgent initialized with its specialized engines.")

    async def construct_play_scene(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يبني مشهدًا مسرحيًا كاملاً بناءً على مخطط تفصيلي.
        'context' يجب أن يحتوي على 'scene_outline'.
        """
        scene_outline = context.get("scene_outline")
        if not scene_outline:
            logger.error("Scene outline is missing from the context.")
            return {"status": "error", "message": "مخطط المشهد مطلوب لبناء المشهد."}
            
        logger.info(f"Constructing play scene: '{scene_outline.get('title', 'Untitled Scene')}'")

        try:
            # --- الخطوة 1: فهم الشخصيات بعمق ---
            # تحليل أنماط الشخصيات للحصول على دوافعها وقيمها
            character_profiles = {}
            for interaction in scene_outline.get("interactions", []):
                char_name = interaction["character_name"]
                char_archetype_id = interaction["character_archetype"]
                # يمكنك هنا إضافة وصف أكثر للشخصية إذا كان متوفرًا
                profile = await self.context_engine.analyze_tunisian_character(f"شخصية من نمط {char_archetype_id}")
                character_profiles[char_name] = profile

            # --- الخطوة 2: بناء عالم المشهد الحسي ---
            location_type = scene_outline.get("location", "generic")
            sensory_details = await self.creative_engine.generate_tunisian_sensory_details(location_type)

            # --- الخطوة 3: توليد الحوارات الأصيلة ---
            dialect_id = scene_outline.get("dialect", "tunisois") # الافتراضي هو اللهجة العاصمية
            dialogues = []
            for interaction in scene_outline.get("interactions", []):
                dialogue_line = self.dialogue_engine.generate_dialogue(
                    character_archetype=interaction["character_archetype"],
                    topic=interaction["topic"],
                    mood=interaction["mood"],
                    dialect_id=dialect_id  # تمرير اللهجة المحددة
                )
                dialogues.append({
                    "character": interaction["character_name"], 
                    "line": dialogue_line,
                    "mood": interaction["mood"] # حفظ المزاج لإضافته في التوجيهات
                })

            # --- الخطوة 4: تجميع المشهد بشكل فني ---
            scene_script = self._assemble_scene(sensory_details, dialogues, scene_outline)

            # النتيجة النهائية التي تتوافق مع RefinementService
            return {
                "status": "success",
                "content": {"scene_script": scene_script, "character_profiles": character_profiles},
                "summary": f"تم بناء مشهد مسرحي متكامل بعنوان '{scene_outline.get('title')}'."
            }
        
        except Exception as e:
            logger.error(f"Failed to construct scene: {e}", exc_info=True)
            return {"status": "error", "message": f"فشل بناء المشهد: {e}"}

    def _assemble_scene(self, sensory: Dict, dialogues: List[Dict], outline: Dict) -> str:
        """
        يقوم بتجميع المشهد في صيغة مسرحية قياسية، مع دمج التوجيهات الإخراجية.
        """
        
        # --- بداية المشهد ---
        script = f"### {outline.get('title', 'مشهد جديد')} ###\n\n"
        
        # --- الوصف الافتتاحي (التوجيهات الإخراجية) ---
        opening_desc = f"[المكان: {outline.get('location_name', 'مكان غير محدد')}. "
        
        # دمج التفاصيل الحسية
        if sights := sensory.get("sights"):
            opening_desc += f"{sights[0]}. "
        if sounds := sensory.get("sounds"):
            opening_desc += f"{sounds[0]}. "
        if smells := sensory.get("smells"):
            opening_desc += f"{smells[0]}. "
            
        script += opening_desc.strip() + "]\n\n"

        # --- الحوار والتوجيهات الداخلية ---
        for dialogue_entry in dialogues:
            character_name = dialogue_entry['character'].upper()
            line = dialogue_entry['line']
            mood = dialogue_entry['mood']
            
            # إضافة اسم الشخصية
            script += f"{character_name}\n"
            
            # إضافة توجيه أدائي بسيط بناءً على المزاج
            script += f"({mood})\n"
            
            # إضافة سطر الحوار
            script += f"{line}\n\n"
            
        return script.strip()

# --- قسم الاختبار ---
async def main_test():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود.")
        return

    # إنشاء وكيل المايسترو
    maestro_agent = NarrativeConstructorAgent()

    # تعريف مخطط مشهد صفاقسي
    sfaxian_scene_outline = {
        "title": "في سوق الحوت",
        "dialect": "sfaxien",
        "location": "souk", # يتوافق مع مفتاح في creative_layer_engine
        "location_name": "سوق السمك في صفاقس، رائحة البحر تملأ المكان.",
        "interactions": [
            {
                "character_name": "المعلم الشاذلي", 
                "character_archetype": "tajer_sfaxi",
                "topic": "business", 
                "mood": "يتفاوض بحذر"
            },
            {
                "character_name": "الحريفة",
                "character_archetype": "al_hajja", # يمكن استخدام نفس النمط مع لهجة مختلفة
                "topic": "price", 
                "mood": "تشكو من الغلاء"
            }
        ]
    }
    
    print("\n--- 🧪 Testing Scene Construction (Sfaxian Dialect) ---")
    result = await maestro_agent.construct_play_scene(context={"scene_outline": sfaxian_scene_outline})

    if result.get("status") == "success":
        print("✅ Scene constructed successfully!")
        print("-" * 50)
        print(result.get("content", {}).get("scene_script", "No script generated."))
        print("-" * 50)
        # print("Character Profiles Analyzed:")
        # print(json.dumps(result.get("content", {}).get("character_profiles", {}), indent=2, ensure_ascii=False))
    else:
        print(f"❌ Scene construction failed: {result.get('message')}")
        
if __name__ == "__main__":
    # تأكد من أن مسار الاستيراد صحيح
    # يجب تشغيل هذا الملف من جذر المشروع
    # python -m agents.narrative_constructor_agent
    asyncio.run(main_test())
