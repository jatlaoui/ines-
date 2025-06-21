# agents/soul_profiler_agent.py (ملف جديد)

import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("SoulProfilerAgent")

class SoulProfilerAgent(BaseAgent):
    """
    وكيل متخصص في تحليل النصوص لبناء "الملف الروحي" للشاعر،
    مع التركيز على عالمه الداخلي ومصادر إلهامه.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "soul_profiler_agent",
            name="محلل الروح الشعرية",
            description="يحلل النصوص بعمق لاستخلاص البصمة الوجدانية والجمالية للشاعر."
        )

    async def create_soul_profile(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        يأخذ نصًا ويستخلص منه الملف الروحي للشاعر.
        """
        text_content = context.get("text_content")
        artist_name = context.get("artist_name", "الشاعر")

        if not text_content:
            return {"status": "error", "message": "No text content provided for soul profiling."}

        logger.info(f"Creating soul profile for {artist_name}...")
        
        prompt = self._build_soul_profile_prompt(text_content, artist_name)
        response = await llm_service.generate_json_response(prompt, temperature=0.4)

        if "error" in response:
            return {"status": "error", "message": "LLM call failed for soul profile."}

        return {"status": "success", "profile": response}

    def _build_soul_profile_prompt(self, text: str, artist: str) -> str:
        return f"""
مهمتك: أنت ناقد أدبي وخبير في التحليل النفسي-الفني. قم بتحليل مجموعة النصوص التالية التي تنتمي إلى '{artist}' واستخلص "ملفه الروحي".
**النصوص للتحليل:**
---
{text[:4000]}
---

أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يتبع الرد المخطط التالي:
{{
  "artist_name": "{artist}",
  "core_themes": [
    "string // الموضوع الرئيسي الأول (مثال: الحنين للوطن المفقود).",
    "string // الموضوع الرئيسي الثاني (مثال: الشكوى من الزمن)."
  ],
  "dominant_emotions": [
    "string // العاطفة السائدة الأولى (مثال: الشجن الهادئ).",
    "string // العاطفة السائدة الثانية (مثال: لوعة الفراق)."
  ],
  "symbolic_lexicon": {{
    "key_symbols": ["string"], "description": "الرموز الأساسية التي يستخدمها الشاعر (مثال: الليل، القمر، الصحراء)."
  }},
  "stylistic_fingerprint": {{
    "vocabulary": "string // طبيعة المفردات (بسيطة، شعبية، تراثية).",
    "rhythm": "string // الإيقاع العام للشعر (بطيء وحزين، سريع وحماسي)."
  }}
}}
"""
