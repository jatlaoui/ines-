# agents/ali_douagi_dialogue_agent.py
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("AliDouagiDialogueAgent")

class AliDouagiDialogueAgent(BaseAgent):
    """
    وكيل متخصص في محاكاة الحوار الساخر والذكي على طريقة الكاتب التونسي علي الدوعاجي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "ali_douagi_dialogue_agent",
            name="وكيل علي الدوعاجي للحوار الساخر",
            description="يضيف لمسة من السخرية الذكية، التورية، والعبارات ذات المعنى المزدوج."
        )

    async def refine_dialogue(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ حوارًا خامًا ويعيد صياغته بأسلوب "الدوعاجي".
        'context' يجب أن يحتوي على:
        - dialogue_text: نص الحوار الأصلي.
        - scene_objective: الهدف من المشهد لضمان بقاء المعنى.
        """
        dialogue_text = context.get("dialogue_text")
        objective = context.get("scene_objective")
        if not dialogue_text or not objective:
            return {"status": "error", "message": "Dialogue text and scene objective are required."}

        logger.info("Refining dialogue with the satirical style of Ali Douagi...")

        prompt = self._build_refinement_prompt(dialogue_text, objective)
        rewritten_dialogue = await llm_service.generate_text_response(prompt, temperature=0.8)

        return {"status": "success", "content": {"rewritten_dialogue": rewritten_dialogue}}

    def _build_refinement_prompt(self, dialogue: str, objective: str) -> str:
        return f"""
مهمتك: أنت الأديب التونسي الساخر علي الدوعاجي. لقد طُلب منك مراجعة مسودة حوار وتحويلها إلى قطعة فنية تحمل بصمتك الخاصة.

**الهدف الدرامي للمشهد:**
"{objective}"

**مسودة الحوار للمراجعة:**
---
{dialogue}
---

**التعليمات (أسلوبك الخاص):**
1.  **تجنب المباشرة:** استبدل الاتهامات الصريحة بالتلميحات الذكية والساخرة (التكتيكات).
2.  **استخدم التورية:** اجعل الكلمات تحمل أكثر من معنى، مما يضيف طبقة من العمق والكوميديا السوداء.
3.  **اجعل الحوار لاذعًا وموجزًا:** قل الكثير بالقليل.
4.  **حافظ على الهدف الدرامي:** يجب أن يظل هدف المشهد الأصلي واضحًا، لكن طريقة الوصول إليه يجب أن تكون بأسلوبك الخاص.

**الحوار النهائي بعد لمستك الفنية:**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.refine_dialogue(context)

# إنشاء مثيل وحيد
ali_douagi_dialogue_agent = AliDouagiDialogueAgent()
