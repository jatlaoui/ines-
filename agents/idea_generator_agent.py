# agents/idea_generator_agent.py
"""
IdeaGeneratorAgent (مولد الأفكار)
وكيل متخصص في توليد وتطوير أفكار إبداعية للقصص والروايات.
"""
import logging
import json
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent

logger = logging.getLogger("IdeaGeneratorAgent")

# --- محاكاة خدمة LLM (للتوضيح فقط) ---
class MockLLMIdeaService:
    async def generate_idea(self, prompt: str) -> str:
        mock_idea = {
            "content": {
                "premise": "عالم آثار يكتشف مخطوطة قديمة تكشف عن تاريخ مزيف للبشرية، ويصبح مطاردًا من قبل منظمة سرية تسعى لإخفاء الحقيقة.",
                "genre": "إثارة ومغامرات تاريخية",
                "theme": "صراع بين الحقيقة والسلطة",
                "setting": "مزيج بين القاهرة الحديثة ومواقع أثرية في مصر."
            }
        }
        return json.dumps(mock_idea, ensure_ascii=False)

class IdeaGeneratorAgent(BaseAgent):
    """
    وكيل متخصص في توليد الأفكار الإبداعية وتطويرها.
    """
    def __init__(self, agent_id: Optional[str] = None, llm_service=None):
        super().__init__(
            agent_id=agent_id,
            name="مولد الأفكار الإبداعي",
            description="متخصص في توليد وتطوير أفكار مبتكرة للقصص والروايات."
        )
        self.llm = llm_service or MockLLMIdeaService()

    async def generate_idea(self, context: Dict[str, Any], feedback: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يولد فكرة قصة بناءً على سياق وملاحظات.
        """
        logger.info(f"Generating new idea with context: {context.get('genre_hint', 'N/A')}")
        prompt = self._build_idea_prompt(context, feedback)
        response_json = await self.llm.generate_idea(prompt)
        
        try:
            return json.loads(response_json)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing idea generation response: {e}")
            return {"error": "Parsing error in idea generation"}

    def _build_idea_prompt(self, context: Dict[str, Any], feedback: Optional[List[str]] = None) -> str:
        """
        يبني Prompt لتوجيه الـ LLM لتوليد فكرة قصة.
        """
        genre_hint = context.get('genre_hint', 'أي نوع إبداعي')
        theme_hint = context.get('theme_hint', 'أي موضوع عميق')

        feedback_section = ""
        if feedback:
            feedback_str = "\n- ".join(feedback)
            feedback_section = f"""
            **ملاحظات من المراجعة السابقة (يجب تحسينها):**
            - {feedback_str}
            """

        prompt = f"""
        مهمتك: أنت كاتب محترف ومفكر إبداعي. قم بتوليد فكرة قصة جديدة ومبتكرة.

        **التوجيهات:**
        - **النوع الأدبي المطلوب:** {genre_hint}
        - **الموضوع المقترح:** {theme_hint}
        - **الهدف:** فكرة تكون أصلية، جذابة، وقابلة للتطوير إلى عمل كامل.

        {feedback_section}

        أرجع الإجابة **حصريًا** بتنسيق JSON يحتوي على مفتاح واحد هو "content"، وقيمته كائن يتبع الهيكل التالي:
        - "premise": (string) الفكرة الأساسية للقصة في جملة واحدة.
        - "genre": (string) النوع الأدبي المقترح.
        - "theme": (string) الموضوع أو الرسالة الأساسية.
        - "setting": (string) وصف موجز لعالم القصة.
        """
        return prompt
