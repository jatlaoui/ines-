# agents/cultural_maestro_agent.py (النسخة المفعّلة)

import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("CulturalMaestroAgent")

class CulturalMaestroAgent(BaseAgent):
    """
    وكيل متخصص في إثراء النصوص بالعمق الثقافي والتراثي الأصيل.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "cultural_maestro_agent",
            name="الخبير الثقافي",
            description="يضمن الأصالة الثقافية ويوظف التراث بطريقة معاصرة ومبدعة."
        )
        logger.info("CulturalMaestroAgent initialized.")

    async def enrich_text(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ نصًا خامًا ويثريه بلمسات ثقافية.
        'context' يجب أن يحتوي على 'text_content' و 'cultural_context' (مثل: 'تونس الخمسينيات').
        """
        text_content = context.get("text_content")
        cultural_context = context.get("cultural_context")
        
        if not text_content or not cultural_context:
            raise ValueError("النص والسياق الثقافي مطلوبان لعملية الإثراء.")
            
        logger.info(f"Enriching text with cultural context: {cultural_context}...")
        
        prompt = self._build_enrichment_prompt(text_content, cultural_context)
        response = await llm_service.generate_json_response(prompt, temperature=0.5)
        
        if "error" in response:
            logger.error(f"LLM call failed for cultural enrichment. Details: {response.get('details')}")
            return {"status": "error", "message": "LLM call failed"}

        return {"status": "success", "enriched_text": response.get("enriched_text"), "details": response}

    def _build_enrichment_prompt(self, text: str, culture: str) -> str:
        return f"""
مهمتك: أنت خبير في التراث والثقافة، ومحرر أدبي. قم بمراجعة النص التالي وإثرائه بلمسات ثقافية أصيلة تتناسب مع السياق المحدد.
**السياق الثقافي:** {culture}
**النص للمراجعة والإثراء:**
---
{text}
---

**التحسينات المطلوبة:**
1.  أضف تفاصيل حسية (روائح، أصوات، مشاهد) تعكس الفترة والمكان.
2.  ادمج أمثالاً شعبية أو تعابير تراثية مناسبة في الحوار أو السرد.
3.  تأكد من أن سلوك الشخصيات يتوافق مع الأعراف الاجتماعية لتلك الفترة.

أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يتبع الرد المخطط التالي تمامًا:
{{
  "enriched_text": "string // النص الكامل بعد إثرائه باللمسات الثقافية.",
  "added_elements": [
    {{
      "type": "string // نوع العنصر المضاف (مثال: 'مثل شعبي'، 'وصف حسي').",
      "content": "string // العنصر الذي تمت إضافته.",
      "justification": "string // لماذا تم اختيار هذا العنصر."
    }}
  ]
}}
"""
