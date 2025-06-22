# agents/chapter_composer_agent.py (النسخة المطورة V2 - متعددة الأوضاع)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("ChapterComposerAgent")

class ChapterComposerAgent(BaseAgent):
    """
    وكيل متخصص في كتابة المحتوى الطويل.
    يعمل في وضعين: "narrative" لكتابة فصول الروايات، و "academic" لكتابة ملخصات الدروس.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "chapter_composer",
            name="مؤلف المحتوى",
            description="يكتب محتوى مفصلاً، سواء كان فصلاً روائياً أو ملخص درس."
        )

    async def compose_content(self, context: Dict[str, Any]) -> Dict[str, Any]:
        mode = context.get("mode", "narrative")
        logger.info(f"Content Composer operating in '{mode}' mode.")

        if mode == "academic":
            prompt = self._build_academic_summary_prompt(context)
            key = "lesson_summary"
        else: # narrative
            # يجب أن يحتوي السياق على chapter_outline
            prompt = self._build_chapter_prompt(context.get("chapter_outline"), context.get("feedback"))
            key = "chapter_content"
        
        response_data = await llm_service.generate_text_response(prompt, temperature=0.7)
        if "Error:" in response_data:
             return {"status": "error", "message": response_data}

        return {"status": "success", "content": {key: response_data}}


    def _build_academic_summary_prompt(self, context: Dict) -> str:
        """يبني prompt لكتابة ملخص درس واضح ومنظم."""
        return f"""
مهمتك: أنت أستاذ وخبير في تبسيط المواد المعقدة. بناءً على المعلومات التالية، اكتب ملخصًا واضحًا ومنظمًا للدرس.

**عنوان الدرس:** {context.get('lesson_title')}
**المفاهيم الأساسية:** {', '.join(context.get('key_concepts', []))}
**الهدف التعليمي:** {context.get('learning_objective')}

**التعليمات:**
1. ابدأ بتعريف بسيط للمفهوم الرئيسي.
2. اشرح الأبعاد المختلفة للدرس نقطة بنقطة.
3. قدم مثالاً عملياً أو تاريخياً لتوضيح الفكرة.
4. استخدم لغة واضحة ومباشرة ومناسبة لطلاب البكالوريا.
5. يجب أن يكون الملخص شاملاً ويغطي كل الجوانب المطلوبة.

**ملخص الدرس:**
"""

    def _build_chapter_prompt(self, outline, feedback) -> str:
        """يبني prompt لكتابة فصل روائي (المنطق الأصلي)."""
        # ... (نفس دالة بناء prompt الفصول الروائية من الملف الأصلي)
        if not outline: return "Error: Chapter outline is missing for narrative mode."
        return f"مهمتك: اكتب فصلاً روائياً بناءً على: {outline.summary}"

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.compose_content(context)

# إنشاء مثيل وحيد
chapter_composer_agent = ChapterComposerAgent()
