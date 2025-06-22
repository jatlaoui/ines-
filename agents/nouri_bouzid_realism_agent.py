# agents/nouri_bouzid_realism_agent.py
import logging
from typing import Dict, Any

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("NouriBouzidAgent")

class NouriBouzidRealismAgent(BaseAgent):
    """
    وكيل متخصص في محاكاة الأسلوب السينمائي الواقعي والجريء للمخرج نوري بوزيد.
    """
    def __init__(self, agent_id: str = "nouri_bouzid_agent"):
        super().__init__(agent_id=agent_id, name="وكيل نوري بوزيد للواقعية", description="يضيف لمسة من الواقعية الجريئة والنقد الاجتماعي للنصوص.")

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        text_content = context.get("text_content")
        prompt = f"""
مهمتك: أنت المخرج التونسي نوري بوزيد. أعد كتابة هذا المشهد أو عالج هذه الفكرة بأسلوبك الخاص.
- **سلط الضوء على المسكوت عنه.**
- **اجعل الحوار مباشرًا وحادًا، ويعكس القلق الوجودي للشخصيات.**
- **اكسر التابوهات الاجتماعية بلغة فنية لا مبتذلة.**
- **ركز على الصراعات النفسية العميقة.**

النص للمراجعة:
---
{text_content}
---

النص بالأسلوب الواقعي الجريء:
"""
        rewritten_text = await llm_service.generate_text_response(prompt, temperature=0.8)
        return {"status": "success", "content": {"rewritten_text": rewritten_text}}

# إنشاء مثيل وحيد
nouri_bouzid_agent = NouriBouzidRealismAgent()
