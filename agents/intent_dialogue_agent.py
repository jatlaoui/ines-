# agents/intent_dialogue_agent.py
import logging
from typing import Dict, Any, List
from .base_agent import BaseAgent

logger = logging.getLogger("IntentDialogueAgent")

class IntentDialogueAgent(BaseAgent):
    """
    وكيل متخصص في الحوار العميق مع المستخدم لفهم "النية الوجدانية"
    وراء طلبه الإبداعي.
    """
    def __init__(self, agent_id: str = "intent_dialogue_agent"):
        super().__init__(
            agent_id=agent_id,
            name="المحاور الوجداني",
            description="يطرح أسئلة استكشافية للوصول إلى جوهر الفكرة الفنية."
        )
        self.question_templates = {
            "grief": [
                "هل هذا الحزن يشبه صمت الصحراء أم عصف العاصفة؟",
                "هل الشخصية تشكو من 'الفقد' نفسه، أم من 'أثر الفقد' على ما تبقى؟"
            ],
            "love": [
                "هل هذا الحب هادئ كضوء القمر، أم مشتعل كالجمر؟",
                "هل هو حب التملك، أم حب التضحية؟"
            ]
        }

    async def deepen_intent(self, initial_request: str) -> Dict[str, Any]:
        """
        يبدأ حوارًا مع المستخدم لاستخلاص النية العميقة.
        """
        logger.info(f"Deepening intent for request: '{initial_request[:50]}...'")
        
        # تحليل أولي لتحديد الموضوع (مثلاً، حزن)
        initial_theme = "grief" # سيتم استخلاصه بـ LLM
        
        # طرح أسئلة استكشافية (في تطبيق حقيقي، ستكون هذه حلقة حوار)
        probing_questions = self.question_templates.get(initial_theme, [])
        
        # محاكاة لإجابات المستخدم
        user_answers = {
            "question_1": "يشبه صمت الصحراء.",
            "question_2": "تشكو من أثر الفقد."
        }
        
        # استنتاج "النية الوجدانية" النهائية
        final_intent = {
            "core_emotion": "grief_of_emptiness", # حزن الفراغ
            "dominant_metaphor": "silent_desert", # استعارة الصحراء الصامتة
            "narrative_focus": "the_aftermath_of_loss" # التركيز على ما بعد الفقد
        }
        
        logger.info(f"Deepened intent captured: {final_intent}")
        return final_content
