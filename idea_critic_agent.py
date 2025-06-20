# idea_critic_agent.py
from typing import Dict, Any, List
import logging

logger = logging.getLogger("IdeaCriticAgent")

class IdeaCriticAgent:
    def review_idea(self, idea_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        يراجع فكرة قصة ويعطي تقييمًا وملاحظات.
        """
        logger.info(f"[IdeaCritic] Reviewing idea: '{idea_content.get('premise', 'N/A')}'")

        issues: List[str] = []
        score = 10.0

        # تقييم الأصالة (هل الفكرة مبتكرة أم مكررة؟)
        if "تاريخ مزيف" in idea_content.get("premise", ""):
            score -= 1.5
            issues.append("فكرة 'التاريخ المزيف' شائعة. حاول إيجاد زاوية جديدة وفريدة.")
        
        # تقييم القابلية للتطوير (هل يمكن بناء رواية كاملة عليها؟)
        if len(idea_content.get("premise", "").split()) < 10:
            score -= 1.0
            issues.append("الفكرة الأساسية موجزة جدًا. تحتاج إلى تفاصيل أكثر لتحديد إمكانية تطويرها.")
            
        # تقييم الجاذبية (هل الفكرة مثيرة للاهتمام؟)
        if "منظمة سرية" in idea_content.get("premise", ""):
            score += 0.5 # عنصر تشويق جيد
        else:
            score -= 1.0
            issues.append("الفكرة تفتقر إلى عنصر تشويق أو صراع واضح لجذب القارئ.")

        return {
            "overall_score": max(min(score, 10.0), 0.0),
            "issues": issues, # سيتم استخدامها كـ feedback
        }