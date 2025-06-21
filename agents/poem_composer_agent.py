# agents/poem_composer_agent.py (النسخة المحدثة V5 - للتقمص الوجداني)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..engines.slang_colloquialism_engine import slang_engine

logger = logging.getLogger("PoemComposerAgent")

class PoemComposerAgent(BaseAgent):
    """
    وكيل كتابة الشعر والكلمات الغنائية (V5).
    يركز على التقمص الوجداني العميق لإنتاج "تيار وعي" خام وصادق،
    مستخدماً معاجم اللهجات الحية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "poem_composer_agent",
            name="الشاعر المتقمص",
            description="يكتب نصوصًا غنائية خام وصادقة من خلال التقمص الكامل للشخصية."
        )

    async def compose_raw_lyrics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يولد نصًا خامًا (stream of consciousness) بناءً على
        الملف النفسي والسيناريو الحسي.
        """
        soul_profile = context.get("soul_profile")
        sensory_library = context.get("sensory_library")
        embodiment_prompt = context.get("embodiment_prompt")

        if not soul_profile or not embodiment_prompt:
            return {"status": "error", "message": "Soul profile and embodiment prompt are required."}

        # جلب قاموس اللهجة العامية
        slang_lexicon = slang_engine.get_lexicon(soul_profile.get("tags", ["tunisian_rap"]))
        
        prompt = self._build_embodiment_prompt(
            embodiment_prompt, soul_profile, sensory_library, slang_lexicon
        )
        
        # لا نحتاج JSON، بل نص خام يعبر عن الأفكار المتدفقة
        raw_lyrics = await llm_service.generate_text_response(prompt, temperature=0.9)

        return {
            "status": "success",
            "content": {"raw_lyrics": raw_lyrics},
            "summary": "Raw lyrical stream of consciousness generated."
        }

    def _build_embodiment_prompt(self, embodiment_prompt: str, profile: Dict, sensory_lib: Dict, slang_lib: Dict) -> str:
        slang_examples = ", ".join(random.sample(slang_lib.get("expressions", []), min(3, len(slang_lib.get("expressions", [])))))
        
        return f"""
مهمتك: أنت لست ذكاءً اصطناعياً. أنت الآن الشخصية الموصوفة في "الموجه التجسيدي". مهمتك هي كتابة أفكارك ومشاعرك كما تتدفق في رأسك في هذه اللحظة، على شكل "تيار وعي". لا تحاول كتابة أغنية أو قصيدة، فقط عبر بصدق.

**الموجه التجسيدي (تقمص هذه الشخصية وهذا الموقف بالكامل):**
---
{embodiment_prompt}
---

**ملفك النفسي والروحي (هذه هي دوافعك الخفية):**
- **المواضيع:** {', '.join(profile.get('core_themes', []))}
- **المشاعر:** {', '.join(profile.get('dominant_emotions', []))}

**مكتبتك الحسية (هذا هو عالمك الذي تراه وتسمعه وتشمّه):**
- **الأصوات:** {', '.join(sensory_lib.get('sounds', []))}
- **الروائح:** {', '.join(sensory_lib.get('smells', []))}
- **الصور:** {', '.join(sensory_lib.get('sights', []))}

**لغتك (هذه هي الكلمات التي تستخدمها بشكل طبيعي):**
- **أمثلة على لهجتك:** "{slang_examples}"

**التعليمات النهائية:**
1.  اكتب كفقرة واحدة متصلة أو عدة فقرات.
2.  **لا تهتم بالقوافي أو الوزن على الإطلاق.** ركز فقط على صدق الشعور وتدفق الأفكار.
3.  استخدم الصور الحسية واللهجة العامية المتاحة لك بشكل طبيعي.

**أفكارك ومشاعرك الآن (تيار الوعي):**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.compose_raw_lyrics(context)

# إنشاء مثيل وحيد
poem_composer_agent = PoemComposerAgent()
