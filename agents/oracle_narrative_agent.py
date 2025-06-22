# agents/oracle_narrative_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..core.core_narrative_memory import narrative_memory # للوصول إلى الذاكرة

logger = logging.getLogger("OracleNarrativeAgent")

class OracleNarrativeAgent(BaseAgent):
    """
    وكيل "المنبئ السردي".
    يحلل الوضع الحالي للقصة ويتنبأ بالمسارات السردية المستقبلية المحتملة،
    مما يساعد الكاتب على اتخاذ قرارات واعية وتجنب الكليشيهات.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "narrative_oracle",
            name="المنبئ السردي",
            description="يتنبأ بالمسارات السردية المحتملة (المتوقع، المفاجئ، الكارثي)."
        )

    async def forecast_narrative_paths(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ حالة القصة الحالية ويولد تقريرًا بالمسارات المستقبلية.
        'context' يجب أن يحتوي على:
        - story_summary: ملخص للقصة حتى الآن.
        - key_conflicts: قائمة بالصراعات الرئيسية التي لم تُحل بعد.
        - main_characters_profiles: ملفات الشخصيات الرئيسية.
        """
        story_summary = context.get("story_summary")
        key_conflicts = context.get("key_conflicts")
        character_profiles = context.get("main_characters_profiles")

        if not story_summary or not key_conflicts or not character_profiles:
            return {"status": "error", "message": "Story summary, key conflicts, and character profiles are required."}

        logger.info("Oracle: Forecasting potential narrative paths...")
        
        prompt = self._build_forecasting_prompt(story_summary, key_conflicts, character_profiles)
        
        forecast_report = await llm_service.generate_json_response(prompt, temperature=0.8)

        if "error" in forecast_report:
            return {"status": "error", "message": "LLM call failed for narrative forecasting.", "details": forecast_report}
            
        return {
            "status": "success",
            "content": {"narrative_forecast": forecast_report},
            "summary": "Narrative forecast generated successfully."
        }

    def _build_forecasting_prompt(self, summary: str, conflicts: List[str], profiles: List[Dict]) -> str:
        
        profiles_text = "\n".join(
            f"- **{prof['name']}:** الدافع الرئيسي: '{prof.get('psych_profile', {}).get('core_motivation')}', "
            f"الخوف الأكبر: '{prof.get('psych_profile', {}).get('potential_wound')}'."
            for prof in profiles
        )

        return f"""
مهمتك: أنت "المنبئ السردي"، محلل درامي وخبير في نظرية القصص. لديك القدرة على رؤية كل المسارات المستقبلية المحتملة لقصة ما. مهمتك ليست كتابة القصة، بل تقديم تقرير استراتيجي للكاتب لمساعدته على اتخاذ قراراته.

**ملخص القصة حتى الآن:**
---
{summary}
---

**الصراعات الرئيسية المفتوحة:**
- {', '.join(conflicts)}

**ملفات الشخصيات الرئيسية النفسية:**
{profiles_text}

**المطلوب:**
بناءً على المعطيات أعلاه، قم بتوليد تقرير يتنبأ بثلاثة مسارات مستقبلية رئيسية ومختلفة تمامًا للقصة. لكل مسار، قدم:
- **title:** عنوان جذاب للمسار (مثال: "مسار الانتقام المحتوم").
- **description:** وصف موجز لكيفية تطور الأحداث في هذا المسار، وما هي النتيجة النهائية المحتملة.
- **justification:** تبرير درامي يشرح لماذا هذا المسار منطقي بناءً على دوافع الشخصيات والصراعات الحالية.

**المسارات الثلاثة المطلوبة هي:**

1.  **المسار الأكثر احتمالاً (The Probable Path):**
    *   هذا هو المسار الذي تمليه الكليشيهات وقواعد النوع الأدبي. ماذا سيتوقع الجمهور أن يحدث؟ ماذا سيحدث لو اتبعت القصة المسار الأكثر تقليدية؟

2.  **المسار المفاجئ (The Twist Path):**
    *   هذا هو المسار الذي يقلب التوقعات رأسًا على عقب. اقترح تحولاً دراميًا (Plot Twist) يغير فهمنا للقصة أو الشخصيات. يجب أن يكون مفاجئًا، ولكنه منطقي عند إعادة النظر في الأحداث السابقة.

3.  **المسار الكارثي (The Catastrophic Path):**
    *   هذا هو مسار "ماذا لو ساء كل شيء؟". ماذا لو فشل البطل تمامًا؟ ماذا لو انتصر الشر؟ ماذا لو كانت التضحيات بلا معنى؟ صف العواقب المأساوية لهذا المسار.

أرجع ردك **حصريًا** بتنسيق JSON صالح يحتوي على مفتاح رئيسي واحد هو "forecast"، وقيمته كائن يحتوي على المفاتيح الثلاثة: `probable_path`, `twist_path`, `catastrophic_path`.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        # استخلاص السياق اللازم من الذاكرة
        summary = "\n".join([mem.content for mem in narrative_memory.get_full_chronology()])
        # يمكن إضافة منطق أكثر تعقيدًا لاستخلاص الصراعات والشخصيات
        
        enriched_context = {
            "story_summary": summary,
            "key_conflicts": context.get("key_conflicts", ["البحث عن العدالة"]),
            "main_characters_profiles": context.get("main_characters_profiles", [])
        }
        
        return await self.forecast_narrative_paths(enriched_context)

# إنشاء مثيل وحيد
oracle_narrative_agent = OracleNarrativeAgent()
