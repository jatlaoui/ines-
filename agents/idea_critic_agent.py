# agents/idea_critic_agent.py
"""
IdeaCriticAgent (ناقد الأفكار)
يقوم بتقييم الأفكار الإبداعية من حيث الأصالة والجاذبية وقابلية التطوير.
"""
import logging
from typing import Dict, Any, List

from .base_agent import BaseAgent

logger = logging.getLogger("IdeaCriticAgent")

class IdeaCriticAgent(BaseAgent):
    """
    وكيل متخصص في نقد وتقييم الأفكار الإبداعية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="ناقد الأفكار",
            description="يقوم بتقييم مدى جاذبية الأفكار وأصالتها وإمكانية تطويرها."
        )
        
    def review_idea(self, idea_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يراجع فكرة قصة ويعطي تقييمًا وملاحظات.
        """
        logger.info(f"Reviewing idea: '{idea_content.get('premise', 'N/A')}'")

        issues: List[str] = []
        score = 10.0

        premise = idea_content.get("premise", "")
        
        # تقييم الأصالة (هل الفكرة مبتكرة أم مكررة؟)
        if "تاريخ مزيف" in premise or "اكتشاف سر" in premise:
            score -= 1.5
            issues.append("الفكرة تحتوي على عناصر شائعة. حاول إيجاد زاوية جديدة وفريدة.")
        
        # تقييم القابلية للتطوير (هل يمكن بناء رواية كاملة عليها؟)
        if len(premise.split()) < 10:
            score -= 1.0
            issues.append("الفكرة الأساسية موجزة جدًا. تحتاج إلى تفاصيل أكثر لتحديد إمكانية تطويرها.")
            
        # تقييم الجاذبية (هل الفكرة مثيرة للاهتمام؟)
        if "منظمة سرية" not in premise and "مطارد" not in premise:
            score -= 1.0
            issues.append("الفكرة تفتقر إلى عنصر تشويق أو صراع واضح لجذب القارئ.")

        return {
            "overall_score": max(min(score, 10.0), 0.0),
            "issues": issues, # سيتم استخدامها كـ feedback
            "summary": f"التقييم: {max(min(score, 10.0), 0.0):.1f}/10. {'فكرة واعدة.' if not issues else 'تحتاج الفكرة إلى تطوير.'}"
        }
