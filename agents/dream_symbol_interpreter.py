# agents/dream_symbol_interpreter_agent.py (V2 - Functional)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("DreamSymbolInterpreterAgent")

class DreamSymbolInterpreterAgent(BaseAgent):
    """
    وكيل مفسر الأحلام والرموز (V2).
    يستخدم LLM لتحليل المشاهد الحلمية وتقديم تفسيرات رمزية وسردية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "dream_symbol_interpreter",
            name="مفسر الأحلام والرموز",
            description="يضيف عمقًا رمزيًا وفلسفيًا للنص من خلال توليد وتفسير الأحلام."
        )
        logger.info("✅ Functional Dream & Symbol Interpreter Agent (V2) Initialized.")

    async def generate_symbolic_dream_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يحلل مشهد حلم ويقدم تفسيراً.
        'context' يجب أن يحتوي على:
        - dream_content: النص الذي يصف الحلم.
        - character_profile: الملف النفسي للشخصية الحالمة.
        """
        dream_content = context.get("dream_content")
        character_profile = context.get("character_profile")
        
        if not dream_content or not character_profile:
            return {"status": "error", "message": "Dream content and character profile are required."}
            
        logger.info(f"Analyzing symbolic dream for '{character_profile.get('name')}'...")
        
        prompt = self._build_analysis_prompt(dream_content, character_profile)
        
        analysis = await llm_service.generate_json_response(prompt, temperature=0.6)

        if "error" in analysis:
            return {"status": "error", "message": "LLM call for dream analysis failed.", "details": analysis}

        return {
            "status": "success",
            "content": {"dream_analysis": analysis},
            "summary": "Symbolic dream analysis complete."
        }
        
    def _build_analysis_prompt(self, dream: str, profile: Dict) -> str:
        return f"""
مهمتك: أنت محلل نفسي خبير في تفسير الأحلام والرموز، متخصص في مدرسة "كارل يونغ" للنماذج الأصلية (Archetypes) واللاوعي الجمعي.

**الشخصية الحالمة:**
- **الاسم:** {profile.get('name')}
- **ملفها النفسي:** الدافع الأساسي هو '{profile.get('core_motivation')}', والجرح النفسي هو '{profile.get('psychological_wound')}'.

**نص الحلم للتحليل:**
---
{dream}
---

**المطلوب:**
بناءً على الحلم وملف الشخصية، قدم تحليلاً نفسياً ورمزياً عميقاً. أرجع ردك **حصريًا** بتنسيق JSON.
1.  **symbols_interpretation:** حدد أهم 3 رموز في الحلم وفسر معناها في سياق حالة الشخصية النفسية.
2.  **narrative_function:** اشرح الوظيفة الدرامية لهذا الحلم في القصة. ماذا يكشف؟ ماذا ينذر؟
3.  **jungian_archetype:** حدد النموذج الأصلي (حسب يونغ) الذي يظهر في هذا الحلم (مثال: الظل 'The Shadow'، الحكيم 'The Wise Old Man'، القناع 'The Persona').

**التحليل (JSON):**
{{
  "symbols_interpretation": [
    {{"symbol": "string", "meaning": "string"}},
    {{"symbol": "string", "meaning": "string"}},
    {{"symbol": "string", "meaning": "string"}}
  ],
  "narrative_function": "string",
  "jungian_archetype": "string"
}}
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.generate_symbolic_dream_analysis(context)

# إنشاء مثيل وحيد
dream_symbol_interpreter_agent = DreamSymbolInterpreterAgent()
