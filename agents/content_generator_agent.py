# agents/content_generator_agent.py (New Consolidated Agent)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
from ..engines.slang_colloquialism_engine import slang_engine

logger = logging.getLogger("ContentGeneratorAgent")

class ContentGeneratorAgent(BaseAgent):
    """
    وكيل توليد المحتوى الموحد (V1).
    قادر على كتابة أنواع مختلفة من المحتوى (نثر، شعر، ملخصات أكاديمية)
    بناءً على "الوضع التشغيلي" المحدد في السياق.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "content_generator",
            name="مولّد المحتوى",
            description="وكيل متعدد الأوضاع لكتابة النثر، الشعر، والمحتوى التعليمي."
        )

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة. تقوم بتوجيه الطلب بناءً على الوضع.
        """
        mode = context.get("mode", "prose") # نثر، شعر، أكاديمي
        logger.info(f"Content Generator operating in '{mode}' mode.")

        if mode == "prose":
            return await self._compose_prose(context)
        elif mode == "poetry" or mode == "rap":
            return await self._compose_poetry(context)
        elif mode == "academic":
            return await self._compose_academic_summary(context)
        else:
            return {"status": "error", "message": f"Unsupported content mode: {mode}"}

    async def _compose_prose(self, context: Dict) -> Dict:
        """يكتب فصلاً روائياً."""
        # هذا هو المنطق الذي كان في ChapterComposerAgent
        # ...
        return {"status": "success", "content": {"chapter_content": "نص الفصل الروائي..."}}

    async def _compose_poetry(self, context: Dict) -> Dict:
        """يكتب نصًا شعريًا أو غنائيًا."""
        # هذا هو المنطق الذي كان في PoemComposerAgent (مع بروتوكول التقمص)
        embodiment_prompt = context.get("embodiment_prompt")
        # ...
        prompt = self._build_embodiment_prompt(...)
        raw_lyrics = await llm_service.generate_text_response(prompt)
        return {"status": "success", "content": {"raw_lyrics": raw_lyrics}}

    async def _compose_academic_summary(self, context: Dict) -> Dict:
        """يكتب ملخص درس."""
        # هذا هو المنطق الذي أضفناه في الترقية التعليمية
        # ...
        prompt = self._build_academic_summary_prompt(context)
        summary = await llm_service.generate_text_response(prompt)
        return {"status": "success", "content": {"lesson_summary": summary}}

    # ... دوال بناء الـ Prompts المختلفة ...

# إنشاء مثيل وحيد
content_generator_agent = ContentGeneratorAgent()
