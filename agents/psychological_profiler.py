# agents/psychological_profiler_agent.py (النسخة المفعّلة)

import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("PsychologicalProfilerAgent")

class PsychologicalProfilerAgent(BaseAgent):
    """
    وكيل متخصص في التحليل النفسي العميق للشخصيات لبناء دوافع وسلوكيات واقعية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "psychological_profiler_agent",
            name="المحلل النفسي للشخصيات",
            description="يبني ملفات نفسية عميقة للشخصيات ويحلل دوافعها وصدماتها وسلوكها."
        )
        logger.info("PsychologicalProfilerAgent initialized.")

    async def create_profile(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: إنشاء ملف نفسي كامل للشخصية.
        'context' يجب أن يحتوي على 'character_name' و 'character_context'.
        """
        character_name = context.get("character_name")
        character_context = context.get("character_context") # هذا هو النص الذي يصف الشخصية وأفعالها
        
        if not character_name or not character_context:
            raise ValueError("اسم الشخصية وسياقها مطلوبان لإنشاء الملف النفسي.")
            
        logger.info(f"Creating psychological profile for character: {character_name}...")
        
        prompt = self._build_profile_prompt(character_name, character_context)
        response = await llm_service.generate_json_response(prompt, temperature=0.6)
        
        if "error" in response:
            logger.error(f"LLM call failed for psychological profile. Details: {response.get('details')}")
            return {"status": "error", "message": "LLM call failed"}

        return {"status": "success", "profile": response}
        
    def _build_profile_prompt(self, name: str, context_text: str) -> str:
        return f"""
مهمتك: أنت محلل نفسي وخبير في علم نفس الشخصية. قم بتحليل شخصية '{name}' بناءً على النص التالي الذي يصفها ويصف أفعالها.
**النص للتحليل:**
---
{context_text}
---

قم بإنشاء ملف نفسي عميق لهذه الشخصية.
أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يتبع الرد المخطط التالي تمامًا:
{{
  "character_name": "{name}",
  "personality_type": "string // مثال: 'INFJ (المستشار)' أو 'شخصية قيادية براغماتية'.",
  "core_motivations": [
    "string // الدافع الأهم الذي يحرك الشخصية (مثال: البحث عن العدالة).",
    "string // دافع ثانوي (مثال: حماية العائلة)."
  ],
  "core_fears": [
    "string // الخوف الأكبر الذي يشل الشخصية (مثال: الخوف من الفشل).",
    "string // خوف ثانوي (مثال: الخوف من الوحدة)."
  ],
  "psychological_wound": "string // حدث أو صدمة من الماضي لا تزال تؤثر على الشخصية اليوم.",
  "coping_mechanisms": [
    "string // كيف تتعامل الشخصية مع الضغط (مثال: العزلة، العمل المفرط، الإنكار)."
  ]
}}
"""
