# agents/educational_content_critic.py
import logging
from typing import Dict, Any

from .base_agent import BaseAgent

logger = logging.getLogger("EducationalContentCritic")

class EducationalContentCritic(BaseAgent):
    """
    وكيل متخصص في نقد المحتوى التعليمي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="ناقد المحتوى التعليمي",
            description="يقيم المحتوى التعليمي بناءً على معايير تربوية مثل الوضوح والتسلسل والفعالية."
        )
        
    def review_curriculum_map(self, curriculum_map: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يراجع خريطة المنهج.
        """
        logger.info(f"Reviewing curriculum map: '{curriculum_map.get('title')}'")
        
        issues = []
        score = 10.0

        # تقييم وضوح الأهداف
        if not curriculum_map.get("learning_objectives"):
            score -= 2.0
            issues.append("الأهداف التعليمية غير واضحة أو مفقودة.")
            
        # تقييم تسلسل الوحدات
        if len(curriculum_map.get("units", [])) < 2:
            score -= 1.5
            issues.append("الهيكل يفتقر إلى وحدات كافية لتغطية الموضوع بعمق.")
        
        # تقييم تنوع الأنشطة
        all_activities = [activity for unit in curriculum_map.get("units", []) for activity in unit.get("activities", [])]
        if len(set(all_activities)) < 2:
            score -= 1.0
            issues.append("الأنشطة المقترحة غير متنوعة، مما قد يسبب الملل.")
            
        return {
            "overall_score": max(min(score, 10.0), 0.0),
            "issues": issues,
            "summary": f"التقييم التربوي: {max(min(score, 10.0), 0.0):.1f}/10."
        }
