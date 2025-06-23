# agents/playwright_agent.py (V4 - Engine-Dependent)
# ... (استيرادات كما في النسخة السابقة) ...
from ..engines.advanced_context_engine import advanced_context_engine # [جديد]
from ..engines.tunisian_dialogue_engine import dialogue_engine
from ..engines.creative_layer_engine import creative_engine

class PlaywrightAgent(BaseAgent):
    # ... (التهيئة) ...
    
    async def write_full_scene(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # ...
        # [مُعدل] لم يعد هناك منطق داخلي، فقط استدعاءات للمحركات
        
        # 1. فهم دوافع الشخصيات من محرك السياق
        psych_profiles = {}
        for char_name in scene_blueprint.get("characters", []):
            # يستدعي المحرك لتحليل الشخصية بناءً على وصفها في المخطط
            profile_context = {"character_description": f"تحليل لشخصية {char_name} في هذا المشهد"}
            # نفترض أن advanced_context_engine لديه دالة لهذا الغرض
            psych_profiles[char_name] = await advanced_context_engine.analyze_character_psychology(profile_context)

        # 2. جلب التفاصيل الحسية من المحرك الإبداعي
        sensory_details = await creative_engine.generate_tunisian_sensory_details(...)
        
        # 3. جلب أمثلة اللهجة من محرك اللهجات
        dialect_examples = dialogue_engine.get_examples(...) # مثال

        # 4. بناء الـ Prompt وتمرير كل البيانات التي تم جلبها من المحركات
        prompt = self._build_playwriting_prompt(scene_blueprint, psych_profiles, sensory_details, dialect_examples)
        
        # ... (بقية الدالة)
      
# في ملف agents/playwright_agent.py

# ... (استيرادات)
from ..engines.slang_colloquialism_engine import slang_engine

class PlaywrightAgent(BaseAgent):
    # ...
    async def write_full_scene(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # ...
        # [جديد] استخلاص الكلمات العامية الرئيسية من المخطط
        key_slang_words = context.get("scene_blueprint", {}).get("key_slang_words", [])
        
        slang_definitions = {}
        if key_slang_words:
            logger.info(f"Fetching definitions for key slang words: {key_slang_words}")
            defs = await asyncio.gather(*[slang_engine.get_word_details(word) for word in key_slang_words])
            for d in defs:
                if d["status"] == "success":
                    slang_definitions[d["data"]["word"]] = d["data"]["definitions"][0] # أخذ التعريف الأول

        # تمرير التعاريف إلى الـ prompt
        prompt = self._build_playwriting_prompt(..., slang_definitions=slang_definitions)
        # ...
        
    def _build_playwriting_prompt(self, blueprint: Dict, profiles: Dict, ..., slang_definitions: Dict) -> str:
        # ... (بقية الـ prompt)

        # --- [إضافة جديدة] بناء قسم المصطلحات الخاصة ---
        definitions_block = ""
        if slang_definitions:
            defs_text = "\n".join(
                f"- **{word}:** {definition['meaning']} (مثال: '{definition['example_sentence']}')"
                for word, definition in slang_definitions.items()
            )
            definitions_block = f"""
### معجم المصطلحات الخاصة بالمشهد (من derja.ninja):
{defs_text}
"""
        # ... (تجميع الـ Prompt النهائي مع `definitions_block`)

    
