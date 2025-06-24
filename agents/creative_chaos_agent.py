# agents/creative_chaos_agent.py (V2 - The Mutation Injector)
import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# استيراد المكونات الأساسية
from core.base_agent import BaseAgent
from core.llm_service import llm_service

logger = logging.getLogger("CreativeChaosAgent")

# --- نموذج Pydantic لاقتراح الطفرة السردية ---
class NarrativeMutation(BaseModel):
    """
    يمثل اقتراحًا لتحول جذري وغير متوقع في القصة.
    """
    mutation_title: str = Field(description="عنوان جذاب للطفرة المقترحة (مثال: 'الخائن غير المتوقع').")
    mutation_idea: str = Field(description="شرح للفكرة الأساسية للطفرة أو الانعطافة في الحبكة.")
    dramatic_justification: str = Field(description="تبرير درامي قصير يشرح لماذا هذا التحول سيجعل القصة أفضل وأكثر عمقًا وتأثيرًا.")
    implementation_point: str = Field(description="اقتراح لأفضل مكان في السرد لإدخال هذه الطفرة (مثال: 'في نهاية الفصل الثاني').")

class MutationSuggestions(BaseModel):
    """
    قائمة باقتراحات الطفرات السردية.
    """
    mutations: List[NarrativeMutation] = Field(description="قائمة من 2-3 اقتراحات لطفرات سردية يمكن أن تغير مسار القصة.")


class CreativeChaosAgent(BaseAgent):
    """
    وكيل الفوضى المبدعة (V2).
    يعمل كـ "مُحقِّن طفرات" يقترح انتهاكات مدروسة لقواعد القصة
    لفتح مسارات سردية جديدة وغير متوقعة.
    """
    def __init__(self, agent_id: Optional[str] = "creative_chaos_agent"):
        super().__init__(
            agent_id=agent_id,
            name="مُحقِّن الفوضى المبدعة",
            description="يكسر الأنماط المتوقعة ويقترح تحولات جذرية في الحبكة."
        )
        logger.info("✅ CreativeChaosAgent (V2) initialized.")

    async def inject_mutation(self, story_context: str) -> Optional[MutationSuggestions]:
        """
        الوظيفة الرئيسية: يقترح "طفرة" سردية مدروسة.

        Args:
            story_context: ملخص للقصة حتى الآن، بما في ذلك الشخصيات والصراعات الرئيسية.

        Returns:
            كائن MutationSuggestions يحتوي على قائمة من التحولات المقترحة.
        """
        logger.info("Injecting creative mutation into the narrative...")
        
        prompt = self._build_mutation_prompt(story_context)
        
        suggestions = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=MutationSuggestions,
            system_instruction="أنت كاتب سيناريو عبقري وخبير في إحداث الصدمات الدرامية (Plot Twists). مهمتك هي قراءة سياق القصة واقتراح تحولات جذرية وغير متوقعة.",
            temperature=0.9 # درجة حرارة عالية لتشجيع الإبداع الجريء
        )

        if suggestions:
            logger.info(f"Generated {len(suggestions.mutations)} narrative mutation suggestions.")
        else:
            logger.error("Failed to generate narrative mutations.")
            
        return suggestions

    def _build_mutation_prompt(self, context: str) -> str:
        return f"""
بناءً على سياق القصة الحالي، اقترح 2-3 "طفرات سردية" (Plot Twists) جريئة وغير متوقعة يمكن أن تقلب القصة رأسًا على عقب بطريقة مثيرة.

**سياق القصة الحالي:**
---
{context[:8000]}
---

**التعليمات:**
- يجب أن تكون الاقتراحات مفاجئة ولكن منطقية عند إعادة النظر في الأحداث السابقة.
- يجب أن يكون لكل طفرة تأثير كبير على الشخصيات الرئيسية والصراع.
- تجنب الكليشيهات المعتادة واقترح أفكارًا أصلية.

قم بملء قائمة اقتراحات الطفرات السردية التالية.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة.
        """
        story_context = context.get("story_context")
        if not story_context:
            return {"status": "error", "message": "story_context is required."}

        suggestions = await self.inject_mutation(story_context)

        if suggestions:
            return {
                "status": "success",
                "content": {"mutation_suggestions": suggestions.dict()},
                "summary": f"Generated {len(suggestions.mutations)} creative mutations."
            }
        else:
            return {
                "status": "error",
                "message": "Could not generate creative mutations."
            }

# إنشاء مثيل وحيد
creative_chaos_agent = CreativeChaosAgent()
