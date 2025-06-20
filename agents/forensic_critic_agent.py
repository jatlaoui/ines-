# agents/forensic_critic_agent.py
# (الكود كما هو في ردنا السابق)
import logging
from typing import Dict, Any, List

from .base_agent import BaseAgent

logger = logging.getLogger("ForensicCriticAgent")

class ForensicCriticAgent(BaseAgent):
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id=agent_id, name="خبير النقد الجنائي", description="مراجعة التحليلات الجنائية لضمان دقتها.")
        logger.info("ForensicCriticAgent initialized.")
        
    def review_forensic_analysis(self, analysis_content: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Reviewing forensic analysis report...")
        issues = []
        score = 10.0
        analysis = analysis_content.get("analysis", {})
        if analysis.get("inconsistencies_count", 0) > 0:
            score -= 2.0
            issues.append("يوجد تناقضات منطقية.")
        if analysis.get("procedural_errors_count", 0) > 0:
            score -= 1.5
            issues.append("تم اكتشاف أخطاء إجرائية.")

        return {"overall_score": max(min(score, 10.0), 0.0), "issues": issues}
