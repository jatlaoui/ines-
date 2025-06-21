# agents/rhythm_flow_analyzer_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..tools.performance_tonality_analyzer import PerformanceTonalityAnalyzer

logger = logging.getLogger("RhythmFlowAnalyzerAgent")

class RhythmFlowAnalyzerAgent(BaseAgent):
    """
    وكيل متخصص في تحليل البصمة الإيقاعية والأدائية لفنان.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "rhythm_flow_analyzer",
            name="محلل الإيقاع والتدفق",
            description="يستخلص البصمة الإيقاعية والأدائية من ملفات صوتية."
        )
        self.tonality_analyzer = PerformanceTonalityAnalyzer()

    async def create_rhythmic_fingerprint(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يحلل ملفًا صوتيًا وينتج بصمة إيقاعية.
        """
        audio_source = context.get("audio_source")
        if not audio_source:
            return {"status": "error", "message": "Audio source path is required."}

        logger.info(f"Creating rhythmic fingerprint for '{audio_source}'...")
        
        # استدعاء الأداة المتخصصة
        performance_data = self.tonality_analyzer.analyze_audio_file(audio_source)
        
        # ترجمة البيانات التقنية إلى توجيهات إبداعية
        rhythmic_fingerprint = {
            "overall_bpm": performance_data["tempo_bpm"],
            "flow_style": performance_data["dominant_performance_style"],
            "vocal_tone": "Mid-to-low pitch with significant emotional variation.",
            "pacing_directives": [
                "Start with a slow, narrative flow.",
                "Gradually accelerate the pace towards the middle of the verse.",
                "Use sharp, short pauses for emphasis before key lines.",
                "The chorus should be more melodic and slower than the verses."
            ],
            "raw_data": performance_data
        }
        
        return {
            "status": "success",
            "content": {"rhythmic_fingerprint": rhythmic_fingerprint},
            "summary": f"Rhythmic fingerprint created with a BPM of {performance_data['tempo_bpm']}."
        }

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.create_rhythmic_fingerprint(context)

# إنشاء مثيل وحيد
rhythm_flow_analyzer_agent = RhythmFlowAnalyzerAgent()
