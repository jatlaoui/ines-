# agents/sami_fehri_drama_agent.py
import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("SamiFehriAgent")

class SamiFehriDramaAgent(BaseAgent):
    """
    وكيل متخصص في محاكاة أسلوب الدراما التلفزيونية الناجحة تجاريًا.
    """
    def __init__(self, agent_id: str = "sami_fehri_agent"):
        super().__init__(agent_id=agent_id, name="وكيل سامي الفهري للدراما", description="يحول النصوص إلى سيناريوهات ذات إيقاع سريع وجاذبية جماهيرية.")

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        text_content = context.get("text_content")
        prompt = f"""
مهمتك: أنت المخرج والمنتج سامي الفهري. أعد كتابة هذا المشهد ليصبح أكثر تشويقًا ومناسبًا للدراما الرمضانية.
- **أضف نقطة تشويق (cliffhanger) في نهاية المشهد.**
- **صعّد الصراع بين الشخصيات بشكل أسرع.**
- **ركز على الدراما العائلية أو الصراعات المالية.**
- **أبرز الشخصيات النمطية التي يترقبها الجمهور (الطيب، الشرير، الضحية).**

النص للمراجعة:
---
{text_content}
---

المشهد بصيغة دراما تلفزيونية:
"""
        rewritten_text = await llm_service.generate_text_response(prompt, temperature=0.7)
        return {"status": "success", "content": {"rewritten_text": rewritten_text}}

# إنشاء مثيل وحيد
sami_fehri_agent = SamiFehriDramaAgent()
