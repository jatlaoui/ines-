# agents/playwright_agent.py (V3 - The Drama & Dialect Expert)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
# استيراد محرك اللهجات ومحرك الطبقة الإبداعية
from ..engines.tunisian_dialogue_gallery import dialogue_engine
from ..engines.creative_layer_engine import CreativeLayerEngine

logger = logging.getLogger("PlaywrightAgent")

class PlaywrightAgent(BaseAgent):
    """
    وكيل "الكاتب المسرحي" (V3).
    يكتب مشاهد مسرحية كاملة وغنية، بناءً على مخطط درامي مفصل (Dramatic Beats)،
    وملفات نفسية للشخصيات، وتفاصيل حسية للمكان، مع حقن أمثلة حية من اللهجة المطلوبة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "playwright_agent",
            name="الكاتب المسرحي الخبير",
            description="يكتب مشاهد مسرحية احترافية ذات هيكل درامي وتفاصيل حسية وحوارات أصيلة."
        )
        self.dialogue_gallery = dialogue_engine
        self.creative_engine = CreativeLayerEngine() # لإضافة التفاصيل الحسية

    async def write_full_scene(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يكتب مشهداً مسرحياً كاملاً ومعززاً.
        'context' يجب أن يحتوي على:
        - scene_blueprint: مخطط المشهد المفصل (مع dramatic_beats).
        - characters_psych_profiles: الملفات النفسية للشخصيات.
        """
        scene_blueprint = context.get("scene_blueprint")
        psych_profiles = context.get("characters_psych_profiles")

        if not scene_blueprint or not psych_profiles:
            return {"status": "error", "message": "A detailed scene blueprint and psychological profiles are required."}

        logger.info(f"Expert Playwright: Writing full, enhanced scene for '{scene_blueprint.get('title')}'...")
        
        # [جديد] جلب التفاصيل الحسية للمكان من المحرك الإبداعي
        location_type = scene_blueprint.get("location_type", "generic") # e.g., "cafe", "souk"
        sensory_details = await self.creative_engine.generate_tunisian_sensory_details(location_type)
        
        # دمج التفاصيل الحسية في المخطط لتمريرها للـ prompt
        scene_blueprint["sensory_details"] = sensory_details
        
        prompt = self._build_playwriting_prompt(scene_blueprint, psych_profiles)
        
        scene_script = await llm_service.generate_text_response(prompt, temperature=0.7)
        
        if "Error:" in scene_script:
            return {"status": "error", "message": scene_script}

        return {
            "status": "success",
            "content": {"scene_script": scene_script},
            "summary": f"Full, enhanced scene script for '{scene_blueprint.get('title')}' has been generated."
        }

    def _build_playwriting_prompt(self, blueprint: Dict, profiles: Dict) -> str:
        
        # --- [محسّن] بناء وصف الشخصيات النفسي ---
        character_descriptions = "\n".join(
            f"- **{name}:** الدافع الأساسي: '{profile.get('core_motivation')}'. آلية الدفاع عند الضغط: '{profile.get('coping_mechanism', 'غير محددة')}'."
            for name, profile in profiles.items()
        )

        # --- [جديد] بناء قسم النبضات الدرامية ---
        dramatic_beats_text = "لا توجد نبضات محددة."
        if "dramatic_beats" in blueprint and blueprint["dramatic_beats"]:
            dramatic_beats_text = "\n".join(
                f"  {i+1}. {beat}" for i, beat in enumerate(blueprint["dramatic_beats"])
            )

        # --- [جديد] بناء قسم اللهجات الحية ---
        dialect_id = blueprint.get("dialect", "tunisois")
        # استخراج archetypes من الملفات النفسية الممررة
        archetypes_in_scene = [p.get("archetype_id") for p in profiles.values() if p.get("archetype_id")]
        
        dialect_examples = []
        if archetypes_in_scene:
            for archetype_id in set(archetypes_in_scene): # استخدام set لتجنب التكرار
                example = self.dialogue_gallery.generate_dialogue(
                    character_archetype=archetype_id, topic="general",
                    mood="neutral", dialect_id=dialect_id
                )
                if example and "..." not in example:
                    dialect_examples.append(example)

        examples_block = "لا توجد أمثلة محددة، اعتمد على فهمك العام للهجة."
        if dialect_examples:
            examples_text = "\n".join(f'  - "{ex}"' for ex in set(dialect_examples))
            examples_block = f"""**أمثلة حية من اللهجة المطلوبة ({dialect_id}) لتستلهم منها:**
{examples_text}
"""
        
        # --- [جديد] بناء قسم التفاصيل الحسية ---
        sensory_block = "لا توجد تفاصيل حسية محددة."
        if "sensory_details" in blueprint and blueprint["sensory_details"]:
            sounds = ", ".join(blueprint['sensory_details'].get('sounds', []))
            smells = ", ".join(blueprint['sensory_details'].get('smells', []))
            sights = ", ".join(blueprint['sensory_details'].get('sights', []))
            sensory_block = f"""
- **الأصوات:** {sounds or "صمت"}
- **الروائح:** {smells or "لا شيء مميز"}
- **المشاهد:** {sights or "مكان عادي"}
"""

        # --- [تجميع الـ Prompt النهائي والمحسّن] ---
        return f"""
مهمتك: أنت كاتب مسرحي تونسي محترف وخبير في الدراما النفسية واللهجات المحلية. مهمتك هي كتابة مشهد مسرحي كامل، حي، وعميق.

### مخطط المشهد ###
- **العنوان:** {blueprint.get('title', 'مشهد بدون عنوان')}
- **الهدف الدرامي:** {blueprint.get('objective', 'تطور الشخصيات')}

### تحليل الشخصيات ###
{character_descriptions}

### النبضات الدرامية للمشهد (يجب أن يتبع الحوار هذا التصاعد المنطقي):
{dramatic_beats_text}

### التفاصيل الحسية للمكان (استخدمها في الوصف والتوجيهات المسرحية):
{sensory_block}

### أمثلة اللهجة (لضمان الأصالة):
{examples_block}

### التعليمات النهائية ###
1.  **ابدأ بوصف حسي للمكان:** استخدم التفاصيل الحسية المتاحة لغمر الجمهور في أجواء المشهد.
2.  **اكتب حوارًا كاملاً:** يجب أن يتبع الحوار النبضات الدرامية المحددة.
3.  **أظهر، لا تخبر:** دع الحوار والأفعال تعكس دوافع الشخصيات وصراعاتها النفسية.
4.  **أضف توجيهات مسرحية دقيقة:** بين قوسين `()`، صف لغة الجسد، نبرة الصوت، والوقفات الدرامية.
5.  **التزم بالأصالة:** يجب أن يكون الحوار باللهجة المطلوبة، مستلهماً من الأمثلة المقدمة.

**نص المشهد المسرحي الكامل:**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.write_full_scene(context)

# إنشاء مثيل وحيد
playwright_agent = PlaywrightAgent()
