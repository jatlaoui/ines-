# agents/aesthetic_critic_agent.py
import logging
from typing import Dict, Any
from .base_agent import BaseAgent

logger = logging.getLogger("AestheticCriticAgent")

class AestheticCriticAgent(BaseAgent):
    """
    وكيل متخصص في تقييم "الصدق الفني" و "الأثر الجمالي" للنصوص.
    """
    def __init__(self, agent_id: str = "aesthetic_critic_agent"):
        super().__init__(
            agent_id=agent_id,
            name="الناقد الجمالي",
            description="يقيم مدى إيلام الصورة، وصدق الانكسار، وقوة الأثر العاطفي."
        )

    def review_aesthetic_impact(self, text_content: str) -> Dict[str, Any]:
        """
        يراجع الأثر الجمالي للنص.
        """
        logger.info(f"Reviewing aesthetic impact of text (length: {len(text_content)})...")

        # هنا يكمن السحر: الـ Prompt سيتم تصميمه ليطلب من LLM تقييم مفاهيم مجردة
        # سنحاكي النتيجة الآن
        score = 8.5 # درجة عالية لأننا سنفترض أن النص جيد
        issues = []
        
        # محاكاة لنقد جمالي
        if "صرخة صامتة" not in text_content: # مثال بسيط
            score -= 2.0
            issues.append("النص جيد، لكنه يفتقر إلى 'صدمة التشبيه' أو الصورة المتناقضة التي تترك أثراً.")
            
        if "انكسار" not in text_content:
            score -= 1.0
            issues.append("الشعور بالحزن موجود، لكن 'صدق الانكسار' ليس واضحًا بما فيه الكفاية.")

        return {
            "overall_score": score, # هذا التقييم الآن له معنى أعمق
            "issues": issues
        }
