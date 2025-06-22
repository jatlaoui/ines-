# agents/psychological_profiler_agent.py (V2 - Methodical Profiler)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("PsychologicalProfilerAgent")

class PsychologicalProfilerAgent(BaseAgent):
    """
    وكيل التحليل النفسي المنهجي (V2).
    يستخدم أطر عمل نفسية محددة (مثل السمات الخمس الكبرى) لبناء
    ملفات شخصية عميقة ومتماسكة بناءً على أدلة نصية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "psychological_profiler",
            name="المحلل النفسي المنهجي",
            description="يبني ملفات نفسية عميقة للشخصيات باستخدام نظريات علم النفس."
        )
        logger.info("✅ Methodical Psychological Profiler Agent (V2) Initialized.")

    async def create_profile(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: إنشاء ملف نفسي كامل للشخصية باستخدام إطار عمل محدد.
        'context' يجب أن يحتوي على:
        - character_name: اسم الشخصية.
        - character_context: نص يصف أفعال وحوارات وسلوك الشخصية.
        - framework: (اختياري) إطار العمل النفسي المطلوب، الافتراضي هو "BigFive".
        """
        character_name = context.get("character_name")
        character_context = context.get("character_context")
        framework = context.get("framework", "BigFive") # يمكن إضافة أطر أخرى مستقبلاً

        if not character_name or not character_context:
            return {"status": "error", "message": "Character name and context are required."}
            
        logger.info(f"Creating '{framework}' psychological profile for character: {character_name}...")
        
        prompt = self._build_big_five_prompt(character_name, character_context)
        response = await llm_service.generate_json_response(prompt, temperature=0.3) # حرارة منخفضة للدقة
        
        if "error" in response:
            return {"status": "error", "message": "LLM call failed for psychological profile.", "details": response}

        # إضافة استنتاجات إضافية بناءً على التحليل
        response["derived_insights"] = self._derive_insights(response)

        return {
            "status": "success",
            "content": {"psychological_profile": response},
            "summary": f"Psychological profile created for {character_name}."
        }

    def _build_big_five_prompt(self, name: str, context_text: str) -> str:
        return f"""
مهمتك: أنت خبير في علم النفس، متخصص في نموذج "السمات الخمس الكبرى" (Big Five Traits). مهمتك هي تحليل شخصية '{name}' بدقة وموضوعية بناءً على النص التالي الذي يصف أفعالها وحواراتها.

**النص للتحليل:**
---
{context_text}
---

**التعليمات:**
1.  قم بتقييم شخصية '{name}' على المقاييس الخمسة التالية. لكل سمة، أعطِ تقييمًا (مرتفع، متوسط، منخفض) وقدم **دليلاً نصيًا واحدًا على الأقل** من سلوك الشخصية يدعم تقييمك.
    *   **الانفتاح على التجربة (Openness):** (فضولي ومبدع مقابل حذر ومتسق)
    *   **الضمير الحي (Conscientiousness):** (منظم وفعال مقابل سهل ومهمِل)
    *   **الانبساط (Extraversion):** (اجتماعي ونشيط مقابل منعزل ومتحفظ)
    *   **القبول (Agreeableness):** (ودود ومتعاطف مقابل ناقد ومتحدي)
    *   **العصابية (Neuroticism):** (حساس وعصبي مقابل آمن وواثق)
2.  بناءً على هذا التحليل، استنتج ما يلي:
    *   **الدافع الأساسي (Core Motivation):** ما هو الشيء الوحيد الذي يحرك هذه الشخصية أكثر من أي شيء آخر؟
    *   **الجرح النفسي المحتمل (Potential Wound):** ما هو الحدث أو الشعور من الماضي الذي قد يكون شكل شخصيتها الحالية؟

أرجع ردك **حصريًا** بتنسيق JSON صالح يتبع الهيكل التالي تمامًا:
{{
  "character_name": "{name}",
  "big_five_analysis": {{
    "openness": {{"score": "string (منخفض/متوسط/مرتفع)", "evidence": "string // الدليل من النص"}},
    "conscientiousness": {{"score": "string (منخفض/متوسط/مرتفع)", "evidence": "string // الدليل من النص"}},
    "extraversion": {{"score": "string (منخفض/متوسط/مرتفع)", "evidence": "string // الدليل من النص"}},
    "agreeableness": {{"score": "string (منخفض/متوسط/مرتفع)", "evidence": "string // الدليل من النص"}},
    "neuroticism": {{"score": "string (منخفض/متوسط/مرتفع)", "evidence": "string // الدليل من النص"}}
  }},
  "core_motivation": "string // الدافع الأساسي المستنتج",
  "potential_wound": "string // الجرح النفسي المستنتج"
}}
"""
        
    def _derive_insights(self, profile_data: Dict) -> Dict:
        """يستنتج رؤى إضافية من ملف الشخصية."""
        insights = {}
        analysis = profile_data.get("big_five_analysis", {})
        
        if analysis.get("neuroticism", {}).get("score") == "مرتفع":
            insights["coping_mechanism"] = "من المحتمل أن يلجأ إلى آليات دفاع مثل القلق أو الانسحاب عند مواجهة الضغط."
        
        if analysis.get("agreeableness", {}).get("score") == "منخفض" and analysis.get("conscientiousness", {}).get("score") == "مرتفع":
             insights["conflict_style"] = "يميل إلى الدخول في صراعات مباشرة ومنظمة لتحقيق أهدافه بدلاً من تجنبها."
        
        return insights

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.create_profile(context)

# إنشاء مثيل وحيد
psychological_profiler_agent = PsychologicalProfilerAgent()
