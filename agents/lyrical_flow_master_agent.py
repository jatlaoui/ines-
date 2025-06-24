# agents/lyrical_flow_master_agent.py (V2 - Sectionally Aware)
import logging
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("LyricalFlowMasterAgent")

class LyricalFlowMasterAgent(BaseAgent):
    """
    [مُحسّن] وكيل متخصص في هندسة التدفق الموسيقي والقافية بناءً على بصمة مقطعية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "lyrical_flow_master",
            name="مهندس التدفق الغنائي المقطعي",
            description="يعيد هيكلة النصوص الخام إلى أغنية ذات بنية (مقاطع ولازمة)."
        )

    async def engineer_flow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [مُحسّن] يأخذ نصًا خامًا ويحوله إلى كلمات راب متقنة ذات بنية.
        """
        raw_lyrics = context.get("raw_lyrics")
        sectional_fingerprints = context.get("sectional_fingerprints") # [جديد]
        
        if not raw_lyrics or not sectional_fingerprints:
            return {"status": "error", "message": "Raw lyrics and sectional fingerprints are required."}
            
        logger.info("Engineering lyrical flow with sectional awareness...")
        
        prompt = self._build_flow_engineering_prompt(raw_lyrics, sectional_fingerprints)
        engineered_lyrics = await llm_service.generate_text_response(prompt, temperature=0.7)
        
        return {
            "status": "success",
            "content": {"engineered_lyrics": engineered_lyrics},
            "summary": "The raw text has been engineered into a structured song."
        }

    def _build_flow_engineering_prompt(self, raw_text: str, fingerprints: Dict) -> str:
        # [مُحسّن] الـ Prompt الآن يوجه الـ LLM لبناء الأغنية مقطعًا بمقطع
        return f"""
مهمتك: أنت مهندس كلمات (Lyric Engineer) محترف. مهمتك هي تحويل "تيار الوعي" الخام التالي إلى أغنية متكاملة ذات بنية واضحة (مقطع 1، لازمة، مقطع 2).

**النص الخام للمراجعة والهندسة:**
---
{raw_text}
---

**التعليمات الهيكلية والأدائية (مهم جدًا):**
1.  **بنية الأغنية:** يجب أن تتبع الهيكل التالي: [المقطع الأول] -> [اللازمة] -> [المقطع الثاني].
2.  **المقطع الأول (Verse 1):**
    - **المحتوى:** استخدم الأفكار الأولية من النص الخام التي تصف المشكلة أو الحكاية.
    - **الأسلوب:** يجب أن يكون التدفق {fingerprints['verse_fingerprint']['flow']}.
3.  **اللازمة (Chorus):**
    - **المحتوى:** استخلص الفكرة الرئيسية أو الشعور الأعمق من النص الخام واجعله اللازمة. يجب أن تكون اللازمة قوية وموجزة.
    - **الأسلوب:** يجب أن يكون التدفق {fingerprints['chorus_fingerprint']['flow']}.
4.  **المقطع الثاني (Verse 2):**
    - **المحتوى:** استخدم الأفكار المتبقية التي تطور القصة أو تتعمق في الصراع.
    - **الأسلوب:** يجب أن يكون التدفق {fingerprints['verse_fingerprint']['flow']}.
5.  **القافية والإيقاع:** حافظ على القافية والوزن مع الحفاظ على صدق المعنى. استخدم قوافي داخلية ومتعددة المقاطع.

**الناتج النهائي يجب أن يكون الكلمات المهندسة فقط، مقسمة بوضوح.**

[المقطع الأول]
(اكتب هنا)

[اللازمة]
(اكتب هنا)

[المقطع الثاني]
(اكتب هنا)
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.engineer_flow(context)

# إنشاء مثيل وحيد
lyrical_flow_master_agent = LyricalFlowMasterAgent()
