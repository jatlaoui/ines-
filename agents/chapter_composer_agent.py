# agents/chapter_composer_agent.py (V2 - Context-Aware & Refinable)
import logging
from typing import Dict, Any, Optional, List

# استيراد المكونات الأساسية والنماذج
from core.base_agent import BaseAgent
from core.llm_service import llm_service
from agents.blueprint_architect_agent import ChapterOutline # يعتمد على نموذج المخطط

logger = logging.getLogger("ChapterComposerAgent")

class ChapterComposerAgent(BaseAgent):
    """
    وكيل متخصص في كتابة فصول روائية طويلة ومفصلة.
    V2: أصبح الآن واعيًا بالسياق (يأخذ مخططًا) وقابلاً للتحسين (يأخذ ملاحظات).
    """
    def __init__(self, agent_id: Optional[str] = "chapter_composer"):
        super().__init__(
            agent_id=agent_id,
            name="مؤلف الفصول",
            description="يكتب فصولاً روائية غنية بالتفاصيل بناءً على مخططات وملاحظات محددة."
        )
        logger.info("✅ ChapterComposerAgent (V2) initialized.")

    async def write_chapter(
        self, 
        chapter_outline: ChapterOutline, 
        previous_chapter_summary: Optional[str] = None,
        feedback: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        الوظيفة الرئيسية: تكتب مسودة فصل كاملة.

        Args:
            chapter_outline: مخطط الفصل المطلوب كتابته.
            previous_chapter_summary: ملخص للفصل السابق لتوفير السياق.
            feedback: (اختياري) قائمة بملاحظات من الناقد لتحسين الكتابة.

        Returns:
            نص الفصل المكتوب أو None في حالة الفشل.
        """
        logger.info(f"Writing chapter titled: '{chapter_outline.title}'...")
        if feedback:
            logger.info(f"Applying feedback from previous critique: {feedback}")

        prompt = self._build_writing_prompt(chapter_outline, previous_chapter_summary, feedback)
        
        # هنا نستخدم دالة توليد النص العادي لأن المخرج هو نص إبداعي طويل
        chapter_content = await llm_service.generate_text_response(
            prompt=prompt,
            system_instruction="أنت روائي مبدع ومتمكن. مهمتك هي تحويل المخطط إلى سرد حي ومؤثر. استخدم لغة غنية ووصفًا حسيًا عميقًا.",
            temperature=0.7 # درجة حرارة أعلى قليلاً للإبداع
        )

        if "Error:" in chapter_content:
            logger.error(f"Failed to generate content for chapter: {chapter_outline.title}")
            return None
            
        return chapter_content

    def _build_writing_prompt(
        self, 
        outline: ChapterOutline, 
        prev_summary: Optional[str], 
        feedback: Optional[List[str]]
    ) -> str:
        """
        يبني موجهًا فعالاً ومفصلاً لكتابة الفصل.
        """
        prompt = f"""
مهمتك هي كتابة فصل كامل ومفصل من رواية. اتبع المخطط والإرشادات التالية بدقة.

**عنوان الفصل:** {outline.title}

**ملخص أحداث هذا الفصل (المخطط):**
{outline.summary}

**الأحداث الرئيسية التي يجب أن تقع:**
- {"\n- ".join(outline.key_events)}

**تطور الشخصيات في هذا الفصل:**
"""
        for char, arc in outline.character_arcs.items():
            prompt += f"- **{char}:** {arc}\n"

        if prev_summary:
            prompt += f"""
**سياق من الفصل السابق:**
{prev_summary}
"""
        if feedback:
            prompt += f"""
**ملاحظات نقدية (يجب معالجتها في هذه المسودة):**
- {"\n- ".join(feedback)}
"""
        
        prompt += """
**إرشادات الكتابة:**
- تعمق في السرد، لا تلخص.
- استخدم الوصف الحسي (أصوات، روائح، مشاهد) لغمر القارئ في العالم.
- أظهر مشاعر الشخصيات من خلال أفعالها وحواراتها، لا تخبرها مباشرة.
- يجب أن يكون الفصل طويلاً ومفصلاً.

**الفصل الكامل:**
"""
        return prompt

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة لمعالجة مهام كتابة الفصل.
        """
        try:
            # استخدام Pydantic لتحويل القاموس إلى كائن منظم
            chapter_outline = ChapterOutline.parse_obj(context.get("chapter_outline"))
        except Exception as e:
            return {"status": "error", "message": f"Invalid chapter_outline structure: {e}"}

        previous_chapter_summary = context.get("previous_chapter_summary")
        feedback = context.get("feedback")

        chapter_content = await self.write_chapter(chapter_outline, previous_chapter_summary, feedback)

        if chapter_content:
            return {
                "status": "success",
                "content": {"chapter_content": chapter_content},
                "summary": f"Chapter '{chapter_outline.title}' composed successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Could not compose chapter '{chapter_outline.title}'."
            }

# إنشاء مثيل وحيد
chapter_composer_agent = ChapterComposerAgent()
