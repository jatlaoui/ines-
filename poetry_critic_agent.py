# poetry_critic_agent.py
"""
PoetryCriticAgent (ناقد القصائد)
يقوم بتقييم القصائد من حيث الجمالية والعاطفة واللغة.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger("PoetryCriticAgent")

class PoetryCriticAgent:
    def review_poem(self, poem: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Reviewing poem titled: {poem.get('title', 'N/A')}")
        issues: List[str] = []
        score = 10.0

        lines = poem.get("lines", [])
        if len(lines) < 3:
            score -= 2.0
            issues.append("القصيدة قصيرة جدًا. حاول التوسيع في الصور والمعاني.")
        
        if not any("ضوء" in line or "صوت" in line for line in lines):
            score -= 1.0
            issues.append("تفتقر القصيدة إلى عناصر حسية قوية.")
        
        if poem.get("style") != "شعر حر":
            score -= 0.5
            issues.append("الأسلوب غير متناسق مع التوجيه (كان متوقعًا شعر حر).")

        return {
            "overall_score": max(min(score, 10.0), 0.0),
            "issues": issues
        }
