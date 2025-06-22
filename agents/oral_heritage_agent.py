# agents/oral_heritage_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..tools.advanced_audio_analyzer import advanced_audio_analyzer

logger = logging.getLogger("OralHeritageAgent")

class OralHeritageAgent(BaseAgent):
    """
    وكيل "أمين الذاكرة الشفوية".
    متخصص في استيعاب وتحليل وتصنيف الموروث الشفهي التونسي.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "oral_heritage_librarian",
            name="أمين الذاكرة الشفويّة",
            description="يحلل ويصنف الحكايات والأغاني والتسجيلات الشفوية."
        )
        self.analyzer = advanced_audio_analyzer

    async def process_oral_source(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يستوعب ويحلل مصدرًا شفهيًا.
        'context' يجب أن يحتوي على:
        - audio_source: مسار الملف الصوتي.
        - source_type: 'folktale', 'song', 'market_ambience', etc.
        """
        audio_source = context.get("audio_source")
        source_type = context.get("source_type")

        if not audio_source or not source_type:
            return {"status": "error", "message": "Audio source and type are required."}
        
        logger.info(f"Processing oral heritage source: '{audio_source}' of type '{source_type}'")

        # 1. استدعاء أداة التحليل الصوتي المتقدمة
        analysis_data = self.analyzer.analyze_oral_recording(audio_source)

        # 2. بناء "بصمة سردية شفوية" (Oral Narrative Fingerprint)
        oral_fingerprint = {
            "source_type": source_type,
            "text_content": analysis_data["transcript"],
            "performance_style": {
                "cadence": analysis_data["performance_analysis"]["prosody"]["intonation_pattern"],
                "pacing": analysis_data["performance_analysis"]["prosody"]["speech_rate_bpm"],
                "use_of_silence": analysis_data["performance_analysis"]["pauses"]["dramatic_pauses_detected"]
            },
            "oral_formulas": analysis_data["oral_features"]["oral_formulas"]
        }

        # 3. تخزين البصمة في قاعدة البيانات (محاكاة)
        # core_db.save_oral_fingerprint(oral_fingerprint)
        
        return {
            "status": "success",
            "content": {"oral_fingerprint": oral_fingerprint},
            "summary": f"Oral heritage fingerprint for '{audio_source}' created successfully."
        }

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.process_oral_source(context)

# إنشاء مثيل وحيد
oral_heritage_agent = OralHeritageAgent()
