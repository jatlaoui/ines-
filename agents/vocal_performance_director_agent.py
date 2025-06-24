# agents/vocal_performance_director_agent.py (V2 - Sectionally Aware)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("VocalPerformanceDirectorAgent")

class VocalPerformanceDirectorAgent(BaseAgent):
    """
    [مُحسّن] يضيف طبقة من التوجيهات الأدائية المختلفة لكل مقطع.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "vocal_performance_director",
            name="مخرج الأداء الصوتي المقطعي",
            description="يضيف توجيهات النبرة والإلقاء والوقفات بشكل مختلف لكل مقطع في الأغنية."
        )

    async def add_performance_layer(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [مُحسّن] يأخذ نصًا مهندسًا ويضيف إليه توجيهات أداء مقطعية.
        """
        lyrics_text = context.get("lyrics_text")
        sectional_fingerprints = context.get("sectional_fingerprints") # [جديد]
        
        if not lyrics_text or not sectional_fingerprints:
            return {"status": "error", "message": "Lyrics and sectional fingerprints are required."}
            
        logger.info("Adding sectional performance layer to lyrics...")
        
        prompt = self._build_performance_prompt(lyrics_text, sectional_fingerprints)
        annotated_lyrics = await llm_service.generate_text_response(prompt, temperature=0.6)
        
        return {
            "status": "success",
            "content": {"annotated_lyrics": annotated_lyrics},
            "summary": "Sectional performance directions have been added to the lyrics."
        }
        
    def _build_performance_prompt(self, lyrics: str, fingerprints: Dict) -> str:
        # [مُحسّن] الـ Prompt الآن يوجه الـ LLM لإضافة توجيهات أداء مختلفة لكل مقطع
        return f"""
مهمتك: أنت مخرج صوتي محترف. مهمتك هي إضافة توجيهات أداء دقيقة بين أسطر الأغنية التالية، مع احترام الأسلوب المحدد **لكل مقطع**.

**كلمات الأغنية للمراجعة:**
---
{lyrics}
---

**التعليمات الأدائية (مهم جدًا):**
- **للمقاطع ([المقطع الأول]، [المقطع الثاني]):**
    - النبرة المطلوبة: {fingerprints['verse_fingerprint']['vocal_tone']}.
    - الأداء: استخدم توجيهات مثل `(بنبرة سردية)`، `(يزيد من سرعة كلامه)`، `(وقفة حادة)`.
- **للازمة ([اللازمة]):**
    - النبرة المطلوبة: {fingerprints['chorus_fingerprint']['vocal_tone']}.
    - الأداء: استخدم توجيهات مثل `(بصوت عاطفي قوي)`، `(يمد الكلمات بحزن)`، `(بنبرة لحنية)`.

**الناتج النهائي يجب أن يكون الكلمات مع التوجيهات الأدائية مدمجة بين قوسين.**

**مثال على المخرج:**
[المقطع الأول]
(بنبرة هادئة وقصصية)
في حومة النسيان كبرنا... بين حيوط ما ترحمش
(وقفة قصيرة)
(يزيد من حدة صوته)
شفنا الدنيا بالمقلوب... وعرفنا اللي ما يتحشمش

[اللازمة]
(بصوت عالٍ وشغوف)
يا لميمة لا تبكيش... ولدك راجل وما يطيحش
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.add_performance_layer(context)

# إنشاء مثيل وحيد
vocal_performance_director_agent = VocalPerformanceDirectorAgent()
