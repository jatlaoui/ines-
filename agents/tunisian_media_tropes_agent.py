# agents/tunisian_media_tropes_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("TunisianMediaTropesAgent")

class TunisianMediaTropesAgent(BaseAgent):
    """
    وكيل متخصص في تحليل الكليشيهات (Tropes) في الدراما والسينما التونسية.
    يمكنه المساعدة في محاكاة أو كسر هذه الأنماط.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "tunisian_media_tropes_analyzer",
            name="محلل الكليشيهات الإعلامية التونسية",
            description="يحلل ويحدد الأنماط السردية الشائعة في الإعلام التونسي."
        )

    async def analyze_or_suggest(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: إما يحلل نصًا للكشف عن الكليشيهات، أو يقترح كليشيهات لدمجها/كسرها.
        'context' يجب أن يحتوي على:
        - mode: 'analyze' or 'suggest'.
        - text_content: (في وضع التحليل) النص المراد تحليله.
        - story_idea: (في وضع الاقتراح) فكرة القصة.
        """
        mode = context.get("mode", "analyze")
        
        prompt = self._build_prompt(context)
        response = await llm_service.generate_json_response(prompt, temperature=0.7)

        return {"status": "success", "content": {"tropes_report": response}}

    def _build_prompt(self, context: Dict) -> str:
        if context.get("mode") == "suggest":
            idea = context.get("story_idea", "")
            return f"""
مهمتك: أنت ناقد وسيناريست تونسي خبير، على دراية تامة بالمسلسلات والأفلام التونسية.
لدينا فكرة قصة جديدة: "{idea}"
**المطلوب:** اقترح 3 كليشيهات (Tropes) درامية تونسية شائعة يمكن دمجها في هذه القصة لجعلها أكثر قربًا من الجمهور التونسي. ثم، اقترح "كسرًا" مبتكرًا لأحد هذه الكليشيهات لجعل القصة غير متوقعة. أرجع ردك بصيغة JSON.
"""
        else: # analyze mode
            text = context.get("text_content", "")
            return f"""
مهمتك: أنت ناقد وسيناريست تونسي خبير. حلل النص التالي وحدد أي كليشيهات (Tropes) درامية تونسية شائعة مستخدمة فيه.
النص: "{text[:4000]}"
أرجع ردك بصيغة JSON، مع تحديد الكليشيه ونقده.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.analyze_or_suggest(context)

# إنشاء مثيل وحيد
tunisian_media_tropes_agent = TunisianMediaTropesAgent()
