# agents/style_mimic_agent.py (ترجمة وتكييف لـ mimic-author-style.ts)

import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from core.llm_service import llm_service
# سنحتاج إلى أداة لقراءة الملفات، يمكن إضافتها لاحقًا
# from tools.file_reader_tool import read_file_content

logger = logging.getLogger("StyleMimicAgent")

class StyleMimicAgent(BaseAgent):
    """
    وكيل متخصص في محاكاة أساليب الكتاب.
    يأخذ نصًا وأسلوبًا هدفًا، ويعيد كتابة النص ليطابق الأسلوب.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "style_mimic_agent",
            name="محاكي الأسلوب",
            description="يحول النصوص لتحاكي أسلوب كاتب معين."
        )

    async def mimic_style(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تقوم بتحويل أسلوب النص.
        'context' يجب أن يحتوي على:
        - inputText: النص المراد تحويله.
        - targetAuthorStyle: وصف أو عينة من الأسلوب الهدف.
        - intensity: درجة كثافة المحاكاة (0.0 - 1.0).
        """
        input_text = context.get("inputText")
        target_style = context.get("targetAuthorStyle")
        intensity = context.get("intensity", 0.7) # افتراضي 0.7 لتأثير واضح

        if not input_text or not target_style:
            return {"status": "error", "message": "النص الأصلي والأسلوب الهدف مطلوبان."}

        logger.info(f"Mimicking author style with intensity {intensity}...")

        prompt = self._build_mimic_prompt(input_text, target_style, intensity)
        
        # استخدام دالة توليد النص العادي لأن المخرج هو نص وليس JSON
        response_text = await llm_service.generate_text_response(prompt, temperature=0.6)

        if response_text.startswith("Error:"):
            return {"status": "error", "message": response_text}

        return {
            "status": "success",
            "content": {
                "original_text": input_text,
                "transformed_text": response_text
            }
        }

    def _build_mimic_prompt(self, input_text: str, target_style_content: str, intensity: float) -> str:
        
        intensity_desc = "بشكل طفيف جدًا"
        if intensity > 0.8:
            intensity_desc = "بشكل كبير وعميق"
        elif intensity > 0.5:
            intensity_desc = "بشكل واضح"
        elif intensity > 0.2:
            intensity_desc = "بشكل معتدل"

        return f"""
مهمتك: أنت محرر أدبي فائق الذكاء وخبير في تحليل ومحاكاة الأساليب الأدبية العربية.
مهمتك هي إعادة كتابة "النص الأصلي" ليصبح مطابقًا لـ "أسلوب الكاتب الهدف".

**أسلوب الكاتب الهدف (وصف أو عينة من كتاباته):**
---
{target_style_content}
---

**النص الأصلي المراد تحويله:**
---
{input_text}
---

**التعليمات:**
1.  ادرس "أسلوب الكاتب الهدف" بعناية: لاحظ مفرداته، طول جمله، إيقاعه، استعاراته، ونبرته العامة.
2.  أعد كتابة "النص الأصلي" بالكامل، مع الحفاظ على معناه الأساسي ولكن غير أسلوبه ليطابق "أسلوب الكاتب الهدف".
3.  قم بتطبيق التحويل **{intensity_desc}** بناءً على درجة الكثافة المطلوبة.
4.  يجب أن يكون الناتج النهائي باللغة العربية الفصحى، سلساً، ومقنعاً.

**النص المحوّل:**
"""

# لا تنسى تحديث ApolloOrchestrator و WorkflowManager لإضافة هذا الوكيل ومهمته الجديدة
