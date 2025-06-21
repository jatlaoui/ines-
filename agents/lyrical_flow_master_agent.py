# agents/lyrical_flow_master_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("LyricalFlowMasterAgent")

class LyricalFlowMasterAgent(BaseAgent):
    """
    وكيل متخصص في هندسة التدفق الموسيقي (Flow) والقافية للنصوص الغنائية.
    يعمل كـ "منتج موسيقي" للنص.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "lyrical_flow_master",
            name="مهندس التدفق الغنائي",
            description="يراجع النصوص الغنائية الخام ويحسن إيقاعها وقوافيها وتدفقها."
        )

    async def engineer_flow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ نصًا خامًا (تيار وعي) ويحوله إلى كلمات راب متقنة.
        """
        raw_lyrics = context.get("raw_lyrics")
        rhythmic_fingerprint = context.get("rhythmic_fingerprint") # من محلل الإيقاع
        
        if not raw_lyrics or not rhythmic_fingerprint:
            return {"status": "error", "message": "Raw lyrics and rhythmic fingerprint are required."}
            
        logger.info("Engineering lyrical flow...")
        
        prompt = self._build_flow_engineering_prompt(raw_lyrics, rhythmic_fingerprint)
        
        engineered_lyrics = await llm_service.generate_text_response(prompt, temperature=0.7)
        
        return {
            "status": "success",
            "content": {"engineered_lyrics": engineered_lyrics},
            "summary": "The raw text has been engineered into structured rap lyrics."
        }

    def _build_flow_engineering_prompt(self, raw_text: str, fingerprint: Dict) -> str:
        return f"""
مهمتك: أنت منتج موسيقي وخبير في كتابة أغاني الراب. لديك "نص خام" (Stream of Consciousness) من فنان، ومهمتك هي إعادة هيكلته وهندسته ليصبح أغنية راب ذات تدفق (Flow) قوي وإيقاع جذاب، مع الالتزام بالبصمة الإيقاعية للفنان.

**البصمة الإيقاعية للفنان:**
- **السرعة العامة:** {fingerprint.get('overall_bpm')} BPM
- **أسلوب التدفق (Flow):** {fingerprint.get('flow_style')}
- **توجيهات الإيقاع:** {', '.join(fingerprint.get('pacing_directives', []))}

**النص الخام للمراجعة والهندسة:**
---
{raw_text}
---

**التعليمات:**
1.  **الحفاظ على الروح:** حافظ على جوهر ومعنى وأفكار النص الخام. لا تضف أفكارًا جديدة.
2.  **هندسة القافية:** أعد ترتيب الكلمات والجمل لإنشاء قوافي قوية. استخدم قوافي داخلية (internal rhymes) وقوافي متعددة المقاطع (multi-syllable rhymes). لا تتردد في كسر القافية إذا كان ذلك يخدم الإيقاع.
3.  **ضبط التدفق:** قم بتقسيم النص إلى "بارات" (سطور) قصيرة وطويلة لتعكس التنوع في التدفق المطلوب. أضف وقفات أو كرر كلمات لخلق إيقاع مميز.
4.  **اللغة:** حافظ على نفس مستوى اللغة واللهجة العامية الموجودة في النص الأصلي.

**الناتج النهائي يجب أن يكون الكلمات المهندسة فقط، جاهزة للغناء.**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.engineer_flow(context)

# إنشاء مثيل وحيد
lyrical_flow_master_agent = LyricalFlowMasterAgent()
