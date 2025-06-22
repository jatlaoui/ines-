# agents/audio_musical_producer_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..tools.performance_tonality_analyzer import PerformanceTonalityAnalyzer
from ..agents.lyrical_flow_master_agent import lyrical_flow_master_agent
from ..agents.vocal_performance_director_agent import vocal_performance_director_agent

logger = logging.getLogger("AudioMusicalProducerAgent")

class AudioMusicalProducerAgent(BaseAgent):
    """
    وكيل "المنتج الموسيقي الصوتي".
    يدير سير العمل الكامل لإنتاج نص غنائي، من التحليل الصوتي إلى الهندسة الإيقاعية والأدائية.
    إنه يجمع بين قدرات عدة وكلاء وأدوات متخصصة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "audio_musical_producer",
            name="المنتج الموسيقي الصوتي",
            description="ينسق عملية تحويل الأفكار إلى كلمات غنائية ذات تدفق وأداء متكامل."
        )
        # هذا الوكيل ينسق بين أدوات ووكلاء آخرين
        self.tonality_analyzer = PerformanceTonalityAnalyzer()
        self.flow_engineer = lyrical_flow_master_agent
        self.performance_director = vocal_performance_director_agent

    async def produce_lyrics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: ينتج كلمات أغنية متكاملة مع توجيهات الأداء.
        'context' يجب أن يحتوي على:
        - raw_lyrics: النص الخام من وكيل التقمص.
        - audio_source: مسار الملف الصوتي للفنان لتحليل البصمة الأدائية.
        """
        raw_lyrics = context.get("raw_lyrics")
        audio_source = context.get("audio_source")

        if not raw_lyrics or not audio_source:
            return {"status": "error", "message": "Raw lyrics and audio source are required."}

        logger.info(f"Musical Producer: Starting production for lyrics inspired by '{audio_source}'.")

        # الخطوة 1: تحليل البصمة الأدائية والصوتية
        logger.info("...Analyzing performance and rhythmic fingerprint...")
        performance_data = self.tonality_analyzer.analyze_audio_file(audio_source)
        rhythmic_fingerprint = self._translate_to_creative_directives(performance_data)

        # الخطوة 2: هندسة التدفق والقافية
        logger.info("...Engineering lyrical flow and rhymes...")
        engineering_context = {"raw_lyrics": raw_lyrics, "rhythmic_fingerprint": rhythmic_fingerprint}
        engineered_result = await self.flow_engineer.engineer_flow(engineering_context)
        engineered_lyrics = engineered_result.get("content", {}).get("engineered_lyrics")
        if not engineered_lyrics:
            return {"status": "error", "message": "Flow engineering failed."}

        # الخطوة 3: إضافة توجيهات الأداء الصوتي
        logger.info("...Adding vocal performance directions...")
        performance_context = {"lyrics_text": engineered_lyrics, "rhythmic_fingerprint": rhythmic_fingerprint}
        annotated_result = await self.performance_director.add_performance_layer(performance_context)
        annotated_lyrics = annotated_result.get("content", {}).get("annotated_lyrics")
        if not annotated_lyrics:
            return {"status": "error", "message": "Adding performance directions failed."}
            
        return {
            "status": "success",
            "content": {"final_lyrics": annotated_lyrics, "rhythmic_fingerprint": rhythmic_fingerprint},
            "summary": "Full lyrical production complete with performance annotations."
        }

    def _translate_to_creative_directives(self, performance_data: Dict) -> Dict:
        """يترجم البيانات التقنية إلى توجيهات إبداعية."""
        return {
            "overall_bpm": performance_data["tempo_bpm"],
            "flow_style": performance_data["dominant_performance_style"],
            "vocal_tone": "Mid-to-low pitch with significant emotional variation.",
            "pacing_directives": [
                "Start with a slow, narrative flow.",
                "Gradually accelerate the pace.",
                "Use sharp, short pauses for emphasis.",
                "The chorus should be melodic and slower."
            ]
        }

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.produce_lyrics(context)

# إنشاء مثيل وحيد
audio_musical_producer_agent = AudioMusicalProducerAgent()
