# agents/vocal_performance_director_agent.py (وكيل جديد)
import logging
import re
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("VocalPerformanceDirectorAgent")

class VocalPerformanceDirectorAgent(BaseAgent):
    """
    وكيل "مخرج الأداء الصوتي". يضيف طبقة من التوجيهات الأدائية
    على النص لجعله قابلاً للأداء وليس مجرد كلمات.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "vocal_performance_director",
            name="مخرج الأداء الصوتي",
            description="يضيف توجيهات النبرة والإلقاء والوقفات للنصوص الغنائية والشعرية."
        )

    async def add_performance_layer(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ نصًا خامًا ويضيف إليه توجيهات الأداء.
        """
        lyrics_text = context.get("lyrics_text")
        rhythmic_fingerprint = context.get("rhythmic_fingerprint") # من وكيل تحليل الإيقاع
        
        if not lyrics_text or not rhythmic_fingerprint:
            return {"status": "error", "message": "Lyrics and rhythmic fingerprint are required."}
            
        logger.info("Adding performance layer to lyrics...")
        
        prompt = self._build_performance_prompt(lyrics_text, rhythmic_fingerprint)
        
        # لا نحتاج JSON هنا، بل نص غني بالتوجيهات
        annotated_lyrics = await llm_service.generate_text_response(prompt, temperature=0.6)
        
        return {
            "status": "success",
            "content": {"annotated_lyrics": annotated_lyrics},
            "summary": "Performance directions have been added to the lyrics."
        }
        
    def _build_performance_prompt(self, lyrics: str, fingerprint: Dict) -> str:
        return f"""
مهمتك: أنت مخرج صوتي وموسيقي متخصص في الراب. مهمتك هي أخذ كلمات الأغنية التالية وإضافة توجيهات دقيقة للأداء الصوتي بين الأسطر لجعلها تنبض بالحياة، بناءً على "البصمة الإيقاعية" للفنان.

**البصمة الإيقاعية للفنان:**
- **السرعة العامة:** {fingerprint.get('overall_bpm')} BPM
- **أسلوب التدفق (Flow):** {fingerprint.get('flow_style')}
- **توجيهات الإيقاع:** {', '.join(fingerprint.get('pacing_directives', []))}

**كلمات الأغنية للمراجعة:**
---
{lyrics}
---

**التعليمات:**
1.  لا تغير الكلمات الأصلية للأغنية.
2.  بين الأسطر، أضف توجيهات الأداء بين قوسين `()`.
3.  يجب أن تعكس التوجيهات البصمة الإيقاعية. استخدم توجيهات مثل: `(بنبرة ساخرة)`، `(يرفع صوته تدريجياً)`، `(وقفة قصيرة حادة)`، `(بصوت مخنوق)`، `(تهمس الكلمات الأخيرة)`.
4.  يجب أن يكون الناتج النهائي نص الأغنية مع التوجيهات المدمجة.

**مثال على المخرج:**
(بصوت هادئ، شبه مهموس)
يا لميمة... ما تبكيش... ولدك راجل وما يطيحش
(وقفة قصيرة)
في حومة النسيان كبرنا... بين الحيوط اللي ما ترحمش

**النص النهائي مع توجيهات الأداء:**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.add_performance_layer(context)

# إنشاء مثيل وحيد
vocal_performance_director_agent = VocalPerformanceDirectorAgent()
