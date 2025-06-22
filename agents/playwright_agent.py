# agents/playwright_agent.py (تطوير لـ DialogueSubtextAgent)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..engines.tunisian_dialogue_gallery import dialogue_engine # أو أي محرك لهجات آخر
from ..engines.advanced_context_engine import AdvancedContextEngine

logger = logging.getLogger("PlaywrightAgent")

class PlaywrightAgent(BaseAgent):
    """
    وكيل "الكاتب المسرحي" (V2).
    متخصص في كتابة مشاهد مسرحية كاملة، بما في ذلك الحوار والتوجيهات الإخراجية،
    بناءً على مخطط درامي وفهم عميق للشخصيات.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "playwright_agent",
            name="الكاتب المسرحي",
            description="يكتب مشاهد مسرحية كاملة بالحوار والتوجيهات."
        )
        self.dialogue_gallery = dialogue_engine
        self.context_engine = AdvancedContextEngine() # لفهم دوافع الشخصيات

    async def write_full_scene(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يكتب مشهداً مسرحياً كاملاً.
        'context' يجب أن يحتوي على:
        - scene_blueprint: مخطط المشهد من DramaturgAgent (الشخصيات، المكان، الهدف).
        - characters_psych_profiles: الملفات النفسية للشخصيات المشاركة.
        """
        scene_blueprint = context.get("scene_blueprint")
        psych_profiles = context.get("characters_psych_profiles")

        if not scene_blueprint or not psych_profiles:
            return {"status": "error", "message": "Scene blueprint and psychological profiles are required."}

        logger.info(f"Playwright: Writing full scene for '{scene_blueprint.get('title')}'...")
        
        prompt = self._build_playwriting_prompt(scene_blueprint, psych_profiles)
        
        # المخرج هنا هو نص المسرحية الكامل
        scene_script = await llm_service.generate_text_response(prompt, temperature=0.75)
        
        return {
            "status": "success",
            "content": {"scene_script": scene_script},
            "summary": f"Full scene script for '{scene_blueprint.get('title')}' has been generated."
        }

    def _build_playwriting_prompt(self, blueprint: Dict, profiles: Dict) -> str:
        
        character_descriptions = "\n".join(
            f"- {name}: {profile.get('core_motivation')}. آلية دفاعه هي {profile.get('coping_mechanism')}."
            for name, profile in profiles.items()
        )

        return f"""
مهمتك: أنت كاتب مسرحي محترف وخبير في كتابة الحوارات الواقعية والعميقة. مهمتك هي كتابة مشهد مسرحي كامل بناءً على المخطط والتحليل النفسي التاليين.

**مخطط المشهد:**
- **العنوان:** {blueprint.get('title')}
- **المكان:** {blueprint.get('setting')}
- **الهدف من المشهد:** {blueprint.get('objective')}

**التحليل النفسي للشخصيات في هذا المشهد:**
{character_descriptions}

**التعليمات:**
1.  اكتب حوارًا كاملاً للمشهد. يجب أن يعكس الحوار الدوافع والصراعات النفسية لكل شخصية.
2.  أضف **توجيهات مسرحية (Stage Directions)** بين قوسين `()` لوصف الأفعال، التعبيرات، ولغة الجسد. مثال: `(ينظر بعيدًا وهو يتنهد)`.
3.  يجب أن يكون الحوار طبيعيًا ويعكس اللهجة المطلوبة (تونسي عامي).
4.  يجب أن يحقق المشهد هدفه الدرامي المحدد في المخطط.

**نص المشهد المسرحي الكامل:**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.write_full_scene(context)

# إنشاء مثيل وحيد
playwright_agent = PlaywrightAgent()
