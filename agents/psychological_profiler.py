# agents/psychological_profiler_agent.py (V2 - Structured & Functional)
import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# استيراد المكونات الأساسية
from core.base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("PsychologicalProfilerAgent")

# --- [جديد] تعريف نموذج Pydantic للملف النفسي ---
# هذا يضمن أن المخرجات ستكون دائمًا منظمة وموثوقة.
class PsychologicalProfile(BaseModel):
    """
    يمثل الملف النفسي العميق للشخصية، مع تبرير لكل استنتاج.
    """
    character_name: str = Field(description="اسم الشخصية التي يتم تحليلها.")
    personality_type: str = Field(description="النمط الشخصي العام (مثال: 'INFJ - المستشار' أو وصف مثل 'قيادي براغماتي لكنه مندفع').")
    core_motivations: List[str] = Field(description="قائمة بالدوافع الأساسية التي تحرك الشخصية.")
    core_fears: List[str] = Field(description="قائمة بالمخاوف العميقة التي تؤثر على قرارات الشخصية.")
    psychological_wound: str = Field(description="الجرح النفسي أو الصدمة من الماضي التي لا تزال تشكل سلوك الشخصية اليوم.")
    coping_mechanisms: List[str] = Field(description="قائمة بآليات الدفاع أو طرق التعامل التي تلجأ إليها الشخصية عند مواجهة الضغط.")
    analysis_justification: str = Field(description="فقرة موجزة تبرر الاستنتاجات المذكورة أعلاه بناءً على الأدلة النصية.")


class PsychologicalProfilerAgent(BaseAgent):
    """
    وكيل متخصص في التحليل النفسي العميق للشخصيات لبناء دوافع وسلوكيات واقعية.
    V2: يستخدم المخرجات المنظمة لضمان الدقة والاتساق.
    """
    def __init__(self, agent_id: Optional[str] = "psychological_profiler"):
        super().__init__(
            agent_id=agent_id,
            name="المحلل النفسي للشخصيات",
            description="يبني ملفات نفسية عميقة للشخصيات ويحلل دوافعها وصدماتها وسلوكها."
        )
        logger.info("✅ PsychologicalProfilerAgent (V2) initialized.")

    async def create_profile(self, character_name: str, character_context: str) -> Optional[PsychologicalProfile]:
        """
        الوظيفة الرئيسية: إنشاء ملف نفسي كامل للشخصية باستخدام المخرجات المنظمة.
        
        Args:
            character_name: اسم الشخصية.
            character_context: نص يصف الشخصية وأفعالها وحواراتها.

        Returns:
            كائن PsychologicalProfile صالح أو None في حالة الفشل.
        """
        if not character_name or not character_context:
            logger.error("Character name and context are required to create a profile.")
            return None
            
        logger.info(f"Creating psychological profile for character: {character_name}...")
        
        prompt = self._build_profile_prompt(character_name, character_context)
        
        # استخدام دالة المخرجات المنظمة الجديدة من llm_service
        profile = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=PsychologicalProfile,
            system_instruction="أنت محلل نفسي وخبير في علم نفس الشخصية. مهمتك هي تحليل الشخصيات الأدبية بعمق وموضوعية."
        )
        
        if not profile:
            logger.error(f"Failed to generate a valid psychological profile for {character_name}.")
            return None

        logger.info(f"Successfully created psychological profile for {character_name}.")
        return profile
        
    def _build_profile_prompt(self, name: str, context_text: str) -> str:
        """
        يبني موجهًا فعالاً لتحليل الشخصية.
        """
        return f"""
قم بتحليل شخصية '{name}' بدقة بناءً على النص التالي الذي يصفها ويصف أفعالها وحواراتها.
استنتج ملفها النفسي مع تقديم تبرير واضح لتحليلك.

**النص للتحليل:**
---
{context_text}
---

قم بملء جميع حقول الملف النفسي بناءً على تحليلك.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة لمعالجة المهام.
        """
        character_name = context.get("character_name")
        character_context = context.get("character_context")
        
        profile = await self.create_profile(character_name, character_context)

        if profile:
            return {
                "status": "success",
                "content": {"profile": profile.dict()},
                "summary": f"Psychological profile created for {profile.character_name}."
            }
        else:
            return {
                "status": "error",
                "message": f"Could not generate psychological profile for {character_name}."
            }

# إنشاء مثيل وحيد
psychological_profiler_agent = PsychologicalProfilerAgent()
