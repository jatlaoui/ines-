# agents/scenario_builder_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("ScenarioBuilderAgent")

class ScenarioBuilderAgent(BaseAgent):
    """
    وكيل "بنّاء السيناريو".
    يحول موضوعًا مجردًا إلى سيناريو حسي وملموس
    يمكن لوكيل التقمص (مثل PoemComposerAgent) أن "يعيشه".
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "scenario_builder",
            name="بنّاء السيناريو",
            description="يحول المواضيع المجردة إلى سيناريوهات درامية حسية."
        )

    async def build_scenario(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يبني سيناريو دراميًا.
        'context' يجب أن يحتوي على:
        - topic: الموضوع العام (e.g., "الوحدة في العصر الرقمي").
        - artist_profile: الملف الروحي للفنان المستهدف.
        """
        topic = context.get("topic")
        artist_profile = context.get("artist_profile")

        if not topic or not artist_profile:
            return {"status": "error", "message": "Topic and artist profile are required."}

        logger.info(f"Building a sensory scenario for topic: '{topic}' in the style of '{artist_profile.get('artist_name')}'")

        prompt = self._build_scenario_prompt(topic, artist_profile)
        
        # المخرج هو نص وصفي للسيناريو
        scenario_text = await llm_service.generate_text_response(prompt, temperature=0.8)
        
        if "Error:" in scenario_text:
            return {"status": "error", "message": scenario_text}

        return {
            "status": "success",
            "content": {"embodiment_prompt": scenario_text}, # هذا هو المخرج الذي سيستخدمه الوكيل التالي
            "summary": "Sensory scenario for embodiment has been created."
        }

    def _build_scenario_prompt(self, topic: str, profile: Dict) -> str:
        return f"""
مهمتك: أنت كاتب سيناريو ومخرج مبدع. مهمتك هي تحويل موضوع مجرد إلى مشهد حسي وملموس يمكن لممثل (أو لوكيل ذكاء اصطناعي) أن يتقمصه بالكامل.

**الفنان المستهدف:** {profile.get('artist_name', 'فنان غير محدد')}
**ملفه الروحي:** يميل إلى المواضيع الاجتماعية، الواقعية، مع لمسة من الحزن والنقد.
**الموضوع المطلوب تجسيده:** "{topic}"

**التعليمات:**
اكتب فقرة قصيرة (5-7 أسطر) تصف مشهداً درامياً حسياً يجسد هذا الموضوع. يجب أن يكون المشهد مناسبًا لروح الفنان المستهدف.
- **حدد الزمان والمكان.**
- **صف الحالة النفسية للشخصية الرئيسية.**
- **استخدم تفاصيل حسية (أصوات، روائح، مشاهد).**
- **اجعل الموقف ملموسًا ومليئًا بالدراما الكامنة.**
- **اكتب النص كأنه توجيه لممثل، بصيغة "أنت الآن..."**

**مثال:**
لو كان الموضوع "الحنين للوطن"، قد يكون السيناريو: "أنت تجلس في شقة صغيرة في مدينة باريسية باردة. تنظر من النافذة إلى المطر. رائحة القهوة التي تعدها لا تشبه رائحة قهوة والدتك. تسمع أصواتًا غريبة في الشارع. تشعر بغربة عميقة ووخزة من الحنين. ماذا يدور في رأسك الآن؟"

**السيناريو الحسي للموضوع "{topic}":**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.build_scenario(context)

# إنشاء مثيل وحيد
scenario_builder_agent = ScenarioBuilderAgent()
