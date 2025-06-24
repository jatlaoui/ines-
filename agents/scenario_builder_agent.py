# agents/scenario_builder_agent.py (V2 - Visually & Musically Aware)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("ScenarioBuilderAgent")

class ScenarioBuilderAgent(BaseAgent):
    """
    [مُرقَّى] بنّاء السيناريو (V2).
    يحول موضوعًا مجردًا إلى سيناريو حسي وملموس، معتمدًا على التحليل البصري والموسيقي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "scenario_builder",
            name="بنّاء السيناريو الواعي فنيًا",
            description="يحول المواضيع المجردة إلى سيناريوهات درامية حسية بناءً على بصمة فنية كاملة."
        )

    async def build_scenario(self, context: Dict[str, Any]) -> Dict[str, Any]:
        topic = context.get("topic")
        artist_profile = context.get("artist_profile")
        visual_fingerprint = context.get("visual_fingerprint") # [جديد]
        artistic_fingerprint = context.get("artistic_fingerprint") # [جديد]

        if not all([topic, artist_profile, visual_fingerprint, artistic_fingerprint]):
            return {"status": "error", "message": "Topic, profiles, and fingerprints are required."}

        logger.info(f"Building a multi-sensory scenario for topic: '{topic}'")

        prompt = self._build_scenario_prompt(topic, artist_profile, visual_fingerprint, artistic_fingerprint)
        scenario_text = await llm_service.generate_text_response(prompt, temperature=0.8)
        
        return {
            "status": "success",
            "content": {"embodiment_prompt": scenario_text},
            "summary": "Multi-sensory scenario for embodiment has been created."
        }

    def _build_scenario_prompt(self, topic: str, profile: Dict, visual: Dict, artistic: Dict) -> str:
        # [مُحسّن] الـ Prompt الآن غني جدًا بالمعلومات الفنية
        return f"""
مهمتك: أنت مخرج سينمائي وكاتب سيناريو. مهمتك هي تحويل موضوع مجرد إلى مشهد حسي وملموس يمكن لممثل أن يتقمصه بالكامل، مع احترام البصمة الفنية الكاملة للفنان.

**الموضوع المطلوب تجسيده:** "{topic}"

**البصمة الفنية للفنان:**
- **الملف الروحي:** يميل إلى المواضيع {profile.get('core_themes', [])}.
- **الجو البصري:** يفضل الألوان ({visual['color_palette']['mood']}) والرموز مثل ({', '.join(visual['visual_motifs'][:3])}).
- **الجو الموسيقي للمقاطع:** الآلات الرئيسية هي {artistic['verse_fingerprint']['instrumentation']} والجو العام {artistic['verse_fingerprint']['vocal_style']}.

**التعليمات:**
اكتب فقرة قصيرة (5-7 أسطر) تصف مشهداً درامياً حسياً يجسد هذا الموضوع. يجب أن يكون المشهد متوافقًا مع البصمة الفنية الكاملة.
- **حدد زمانًا ومكانًا يعكسان الجو البصري.**
- **صف الحالة النفسية للشخصية لتتناسب مع الجو الموسيقي.**
- **استخدم تفاصيل حسية ومرئية من تحليل الفيديو.**
- **اكتب النص كأنه توجيه لممثل، بصيغة "أنت الآن..."**

**السيناريو الحسي للموضوع "{topic}":**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.build_scenario(context)

# إنشاء مثيل وحيد
scenario_builder_agent = ScenarioBuilderAgent()
