# agents/dialogue_subtext_agent.py
"""
DialogueSubtextAgent (وكيل الحوار واللغة الخفية)
متخصص في كتابة حوارات مسرحية طبيعية، ذات إيقاع، وتحمل معاني خفية.
"""
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent

logger = logging.getLogger("DialogueSubtextAgent")

class DialogueSubtextAgent(BaseAgent):
    """
    وكيل متخصص في صياغة الحوار المسرحي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="صانع الحوار",
            description="يكتب حوارات طبيعية وذات معنى خفي (Subtext)."
        )

    async def generate_play_chapter(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يكتب مشهدًا كاملاً (حوار + وصف) بناءً على المخطط وقوس الشخصية.
        """
        chapter_outline = context.get("chapter_outline")
        character_arcs = context.get("character_arcs")
        
        if not chapter_outline or not character_arcs:
            raise ValueError("مخطط الفصل وأقواس الشخصيات مطلوبة لكتابة المشهد.")
            
        logger.info(f"Writing dialogue for: '{chapter_outline.get('title')}'")

        # محاكاة لكتابة المشهد
        # الـ Prompt سيطلب من النموذج كتابة حوار يعكس الحالة النفسية للشخصيات
        # في تلك المرحلة من قوس تطورها.
        
        chapter_content = f"""
        ### {chapter_outline.get('title')} ###

        [مساء. المقهى شبه فارغ. مبروك يجلس وحيدًا ينظر إلى الكرسي الفارغ. يدخل الهادي.]

        الهادي: (بنبرة تحمل ثقة زائدة)
        مازلت قاعد هنا يا عمي مبروك؟ الدنيا تجري والوقت ما يستناش.
        
        مبروك: (دون أن يلتفت إليه، بهدوء)
        الوقت يجري... أما فمة حاجات ما تجريش معاه.

        الهادي: (يضحك بسخرية خفيفة)
        زي الكراسي الفاضية مثلاً؟ يا عمي، المستقبل ما يبناش بالذكريات. المستقبل يبنى بالفلوس... وبالعلاقات الصح.

        مبروك: (يلتفت إليه لأول مرة، ونظرته تحمل عتابًا)
        والكرسي هذا يا ولدي... موش بالفلوس يتعمر.
        """
        
        return {
            "content": {"chapter_content": chapter_content},
            "summary": "تمت كتابة مشهد حواري يعكس الصراع بين الشخصيات."
        }
