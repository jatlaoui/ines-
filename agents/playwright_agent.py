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
