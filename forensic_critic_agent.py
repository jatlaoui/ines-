# forensic_critic_agent.py
import logging
from typing import Dict, Any

from base_agent import BaseAgent

logger = logging.getLogger("ForensicCriticAgent")

class ForensicCriticAgent(BaseAgent):
    """
    وكيل متخصص في نقد التحليلات الجنائية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="خبير النقد الجنائي",
            description="يقوم بمراجعة التحليلات الجنائية لضمان دقتها ومنطقيتها."
        )
        logger.info("ForensicCriticAgent initialized.")
        
    def review_forensic_analysis(self, analysis_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: مراجعة تقرير التحليل الجنائي.
        """
        logger.info("Reviewing forensic analysis report...")
        
        issues = []
        score = 10.0
        
        analysis = analysis_content.get("analysis", {})
        
        if analysis.get("inconsistencies_count", 0) > 2:
            score -= 2.0
            issues.append("يوجد عدد كبير من التناقضات المنطقية.")
            
        if analysis.get("procedural_errors_count", 0) > 1:
            score -= 1.5
            issues.append("تم اكتشاف أخطاء إجرائية في التحقيق.")
            
        if analysis.get("confidence_score", 1.0) < 0.7:
            score -= 1.0
            issues.append("درجة الثقة في التحليل منخفضة، قد تكون النتائج غير دقيقة.")
            
        return {
            "overall_score": max(min(score, 10.0), 0.0),
            "issues": issues,
            "summary": f"التقييم: {score:.1f}/10. {'التحليل جيد.' if not issues else 'يحتاج التحليل إلى مراجعة.'}"
        }
