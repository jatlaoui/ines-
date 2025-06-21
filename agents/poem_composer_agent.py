# agents/poem_composer_agent.py (النسخة الإبداعية)

import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("PoemComposerAgent")

class PoemComposerAgent(BaseAgent):
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "poem_composer_agent",
            name="الشاعر الوجداني",
            description="متخصص في كتابة الشعر بتقمص روح الشاعر المستهدف."
        )

    async def compose_poem(self, context: Dict[str, Any], feedback: Optional[List[str]] = None) -> Dict[str, Any]:
        soul_profile = context.get("soul_profile")
        if not soul_profile:
            return {"status": "error", "message": "Soul profile is required for poem composition."}

        prompt = self._build_poem_prompt(soul_profile, context.get("topic"), feedback)
        response = await llm_service.generate_json_response(prompt, temperature=0.95)
        
        if "error" in response:
            return {"status": "error", "message": "LLM call failed for poem composition."}

        return {"status": "success", "content": response}

    def _build_poem_prompt(self, profile: Dict, topic: str, feedback: Optional[List[str]]) -> str:
        feedback_section = f"\n**ملاحظات من المراجعة السابقة (يجب تطبيقها):**\n- {'\n- '.join(feedback)}" if feedback else ""

        return f"""
مهمتك: تقمص شخصية وروح الشاعر '{profile.get('artist_name', 'مجهول')}' واكتب قصيدة جديدة وأصيلة.
**الموضوع المطلوب للقصيدة:** {topic}

**هذا هو الملف الروحي للشاعر الذي يجب أن تتقمصه بالكامل:**
- **مواضيعه الأساسية:** {', '.join(profile.get('core_themes', []))}
- **مشاعره السائدة:** {', '.join(profile.get('dominant_emotions', []))}
- **قاموسه الرمزي:** {profile.get('symbolic_lexicon', {}).get('description')} (استخدم رموز مثل: {', '.join(profile.get('symbolic_lexicon', {}).get('key_symbols', []))})
- **بصمته الأسلوبية:** مفرداته '{profile.get('stylistic_fingerprint', {}).get('vocabulary')}' وإيقاعه '{profile.get('stylistic_fingerprint', {}).get('rhythm')}'.
{feedback_section}

**التعليمات النهائية:**
1. لا تقلد، بل ابدع من داخل هذه الروح.
2. اكتب قصيدة قصيرة (4 إلى 6 أبيات).
3. يجب أن تكون القصيدة مؤثرة وعميقة.

أرجع ردك **حصريًا** بتنسيق JSON صالح.
{{
  "title": "string // عنوان شاعري ومناسب للقصيدة.",
  "poem_text": "string // نص القصيدة الكامل، مع فواصل أسطر باستخدام \\n.",
  "inspiration_notes": "string // ملاحظة قصيرة عن كيف استلهمت القصيدة من الملف الروحي."
}}
"""
