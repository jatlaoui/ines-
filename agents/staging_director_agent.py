# agents/staging_director_agent.py
"""
StagingDirectorAgent (وكيل الإخراج المسرحي)
يضيف التوجيهات الإخراجية (حركة، إضاءة، صوت) إلى النص المسرحي.
"""
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent

logger = logging.getLogger("StagingDirectorAgent")

class StagingDirectorAgent(BaseAgent):
    """
    وكيل متخصص في إضافة التوجيهات الإخراجية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="المخرج المسرحي",
            description="يحول النص إلى رؤية مسرحية من خلال توجيهات الحركة والإضاءة والصوت."
        )
        
    async def add_staging_directions(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ نصًا مسرحيًا خامًا ويضيف إليه التوجيهات الإخراجية.
        """
        script = context.get("script")
        if not script:
            raise ValueError("النص المسرحي مطلوب لإضافة التوجيهات.")
            
        logger.info("Adding staging directions to the script...")
        
        # محاكاة لعملية الإخراج
        # الـ Prompt سيطلب من النموذج أن يتخيل المشهد ويضيف توجيهات تخدم المعنى.
        
        # مثال على إضافة توجيهات لمقتطف من النص السابق
        staged_script = script.replace(
            "[مساء. المقهى شبه فارغ. مبروك يجلس وحيدًا ينظر إلى الكرسي الفارغ. يدخل الهادي.]",
            "[إضاءة خافتة تركز على مبروك الجالس في زاوية المقهى. يجلس مطأطئ الرأس. بقية المقهى في شبه ظلام. صوت رياح خفيفة يُسمع من الخارج. يدخل الهادي، خطواته واثقة ومسموعة، يكسر الصمت.]"
        ).replace(
            "والكرسي هذا يا ولدي... موش بالفلوس يتعمر.",
            "والكرسي هذا يا ولدي... (يشير إلى قلبه) يتعمر من هنا... موش بالفلوس."
        )
        
        return {
            "content": {"final_script": staged_script},
            "summary": "تم إثراء النص بتوجيهات إخراجية لتعميق المعنى."
        }
