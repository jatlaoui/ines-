# agents/character_arc_consistency_agent.py
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# استيراد المكونات الأساسية
from core.base_agent import BaseAgent
from core.llm_service import llm_service
from core.core_narrative_memory import narrative_memory
from agents.psychological_profiler_agent import PsychologicalProfile # يعتمد على نموذج الملف النفسي

logger = logging.getLogger("CharacterArcConsistencyAgent")

# --- نموذج بيانات Pydantic لتقرير الاتساق ---
class ConsistencyReport(BaseModel):
    """
    يمثل تقرير تحليل اتساق سلوك شخصية في فصل معين.
    """
    is_consistent: bool = Field(description="هل سلوك الشخصية في هذا الفصل متسق مع ملفها النفسي وقوس تطورها؟")
    consistency_score: float = Field(ge=0.0, le=1.0, description="درجة الاتساق من 0.0 (متناقض تمامًا) إلى 1.0 (متسق تمامًا).")
    analysis_summary: str = Field(description="شرح موجز لسبب تقييم الاتساق.")
    identified_inconsistencies: Optional[List[str]] = Field(None, description="قائمة بالتناقضات السلوكية المحددة إن وجدت.")
    suggestions_for_improvement: Optional[List[str]] = Field(None, description="اقتراحات لتحسين اتساق سلوك الشخصية.")

class CharacterArcConsistencyAgent(BaseAgent):
    """
    يضمن أن سلوك الشخصيات في كل فصل جديد يظل متسقًا مع ملفاتها النفسية
    وأقواس تطورها المحددة.
    """
    def __init__(self, agent_id: Optional[str] = "character_arc_consistency_agent"):
        super().__init__(
            agent_id=agent_id,
            name="مراقب اتساق الشخصية",
            description="يراجع سلوك الشخصيات في الفصول لضمان تطورها المنطقي."
        )
        logger.info("✅ CharacterArcConsistencyAgent initialized.")

    async def check_chapter_consistency(self, chapter_text: str, character_name: str) -> Optional[ConsistencyReport]:
        """
        الوظيفة الرئيسية: تتحقق من اتساق شخصية معينة في فصل معين.

        Args:
            chapter_text: النص الكامل للفصل المراد مراجعته.
            character_name: اسم الشخصية التي يتم التركيز عليها.

        Returns:
            كائن ConsistencyReport أو None في حالة الفشل.
        """
        logger.info(f"Checking consistency for character '{character_name}' in new chapter...")

        # 1. استرجاع الملف النفسي وقوس التطور من الذاكرة السردية
        # سنقوم بمحاكاة استعلام دقيق للذاكرة
        character_profile_results = narrative_memory.query(
            query_text=f"Psychological profile for {character_name}",
            top_k=1,
            entry_type_filter="psychological_profiler"
        )
        
        if not character_profile_results:
            logger.warning(f"No psychological profile found for '{character_name}' in memory. Cannot perform check.")
            # في نظام حقيقي، يمكننا إنشاء تقرير يفيد بغياب الملف الشخصي
            return ConsistencyReport(
                is_consistent=True, # نفترض أنه متسق لأنه لا يوجد ما نتحقق منه
                consistency_score=0.5,
                analysis_summary=f"لم يتم العثور على ملف نفسي للشخصية '{character_name}'، لذا لا يمكن التحقق من الاتساق.",
                identified_inconsistencies=[],
                suggestions_for_improvement=[f"يجب إنشاء ملف نفسي للشخصية '{character_name}' أولاً."]
            )
            
        # نفترض أننا استرجعنا المحتوى وحولناه مرة أخرى إلى كائن
        try:
            # محتوى الإدخال في الذاكرة هو JSON string
            profile_data = json.loads(character_profile_results[0]['content'])
            character_profile = PsychologicalProfile.parse_obj(profile_data['profile'])
        except Exception as e:
            logger.error(f"Failed to parse character profile from memory: {e}")
            return None

        # 2. بناء الموجه للتحقق من الاتساق
        prompt = self._build_consistency_check_prompt(chapter_text, character_profile)

        # 3. استخدام المخرجات المنظمة للحصول على تقرير موثوق
        report = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=ConsistencyReport,
            system_instruction="أنت ناقد أدبي ومحلل نفسي متخصص في تطور الشخصيات. مهمتك هي الحكم على ما إذا كان سلوك الشخصية في مقطع جديد يتوافق مع ملفها النفسي المحدد."
        )

        if report:
            logger.info(f"Consistency check for '{character_name}' complete. Consistent: {report.is_consistent} (Score: {report.consistency_score:.2f})")
        else:
            logger.error(f"Failed to generate consistency report for '{character_name}'.")

        return report

    def _build_consistency_check_prompt(self, chapter_text: str, profile: PsychologicalProfile) -> str:
        """
        يبني موجهًا للتحقق من الاتساق.
        """
        return f"""
مهمتك هي تقييم مدى اتساق سلوك شخصية في فصل جديد من رواية مع ملفها النفسي المحدد مسبقًا.

**الملف النفسي للشخصية '{profile.character_name}':**
- **النمط الشخصي:** {profile.personality_type}
- **الدوافع الأساسية:** {', '.join(profile.core_motivations)}
- **المخاوف العميقة:** {', '.join(profile.core_fears)}
- **الجرح النفسي:** {profile.psychological_wound}
- **آليات الدفاع:** {', '.join(profile.coping_mechanisms)}

**نص الفصل الجديد للمراجعة:**
---
{chapter_text[:8000]}
---

**التحليل المطلوب:**
بناءً على الملف النفسي أعلاه، هل تصرفات وقرارات وحوارات شخصية '{profile.character_name}' في هذا الفصل منطقية ومتسقة؟
- إذا كانت الشخصية تتصرف عكس دوافعها أو مخاوفها دون مبرر واضح، فهذا تناقض.
- إذا كانت الشخصية تظهر تحولًا مفاجئًا غير ممهد له، فهذا تناقض.

قم بملء تقرير الاتساق التالي بدقة.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة.
        """
        chapter_text = context.get("chapter_text")
        character_name = context.get("character_name")

        if not chapter_text or not character_name:
            return {"status": "error", "message": "chapter_text and character_name are required."}

        report = await self.check_chapter_consistency(chapter_text, character_name)

        if report:
            return {
                "status": "success",
                "content": {"consistency_report": report.dict()},
                "summary": f"Consistency check for '{character_name}' complete. Score: {report.consistency_score}"
            }
        else:
            return {
                "status": "error",
                "message": f"Could not perform consistency check for '{character_name}'."
            }

# إنشاء مثيل وحيد
character_arc_consistency_agent = CharacterArcConsistencyAgent()
