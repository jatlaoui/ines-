# agents/poem_composer_agent.py (V6 - Metaphor-Aware)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
# ... (بقية الاستيرادات)

logger = logging.getLogger("PoemComposerAgent")

class PoemComposerAgent(BaseAgent):
    """
    [مُحسّن] وكيل كتابة الشعر (V6).
    يتقمص صورة شعرية مركزية لإنتاج "تيار وعي" عميق وغير مباشر.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "poem_composer_agent",
            name="الشاعر المتقمص للرموز",
            description="يكتب نصوصًا خامًا وصادقة من خلال التقمص الكامل لرمز شعري."
        )

    async def compose_raw_lyrics_from_metaphor(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [مُحسّن] يولد نصًا خامًا بناءً على استعارة مركزية.
        """
        soul_profile = context.get("soul_profile")
        central_metaphor = context.get("central_metaphor")

        if not soul_profile or not central_metaphor:
            return {"status": "error", "message": "Soul profile and central metaphor are required."}

        prompt = self._build_embodiment_prompt(central_metaphor, soul_profile)
        raw_lyrics = await llm_service.generate_text_response(prompt, temperature=0.9)

        return {
            "status": "success",
            "content": {"raw_lyrics": raw_lyrics},
            "summary": "Raw lyrical stream of consciousness generated from a central metaphor."
        }

    def _build_embodiment_prompt(self, metaphor: Dict, profile: Dict) -> str:
        # [مُحسّن] الـ Prompt الآن يركز على الرمز وليس الشعور المباشر
        return f"""
مهمتك: أنت لست ذكاءً اصطناعياً. أنت الآن الشخصية الموصوفة في "الملف الروحي". أنت تعيش الموقف التالي:
**كل ما تملكه وتفكر فيه الآن هو '{metaphor.get('metaphor_object')}' الذي يعني لك '{metaphor.get('metaphor_meaning')}'**.

**ملفك الروحي (هذه هي دوافعك الخفية):**
- **المواضيع:** {', '.join(profile.get('core_themes', []))}
- **المشاعر:** {', '.join(profile.get('dominant_emotions', []))}

**تفاصيل حسية مرتبطة برمزك:**
{', '.join(metaphor.get('sensory_details', []))}

**التعليمات النهائية:**
- اكتب "تيار وعي" (Stream of Consciousness).
- **لا تشرح الرمز أو تتحدث عنه مباشرة.** فقط عبر عن الأفكار والمشاعر التي يثيرها فيك.
- لا تهتم بالقافية أو الوزن. ركز على الصدق وتدفق الأفكار.

**أفكارك ومشاعرك الآن:**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.compose_raw_lyrics_from_metaphor(context)

# إنشاء مثيل وحيد
poem_composer_agent = PoemComposerAgent()
