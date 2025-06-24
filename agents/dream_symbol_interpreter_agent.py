# agents/dream_symbol_interpreter_agent.py (V2 - Functional)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("DreamSymbolInterpreterAgent")

class DreamSymbolInterpreterAgent(BaseAgent):
    """
    وكيل مفسر الأحلام والرموز (V2).
    يستخدم LLM لتحليل المشاهد الحلمية وتقديم تفسيرات رمزية وسردية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "dream_symbol_interpreter",
            name="مفسر الأحلام والرموز",
            description="يضيف عمقًا رمزيًا وفلسفيًا للنص من خلال توليد وتفسير الأحلام."
        )
        logger.info("✅ Functional Dream & Symbol Interpreter Agent (V2) Initialized.")

    async def generate_central_metaphor(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [مهمة جديدة] يولد صورة شعرية مركزية (استعارة) لموضوع معين.
        'context' يجب أن يحتوي على:
        - topic: الموضوع العام (مثل "الغربة والحنين").
        - soul_profile: الملف الروحي للفنان.
        """
        topic = context.get("topic")
        soul_profile = context.get("soul_profile")
        
        if not topic or not soul_profile:
            return {"status": "error", "message": "Topic and soul profile are required."}
            
        logger.info(f"Generating a central metaphor for topic: '{topic}'...")
        
        prompt = self._build_metaphor_prompt(topic, soul_profile)
        
        metaphor = await llm_service.generate_json_response(prompt, temperature=0.9)

        if "error" in metaphor:
            return {"status": "error", "message": "LLM call for metaphor generation failed.", "details": metaphor}

        return {
            "status": "success",
            "content": {"central_metaphor": metaphor},
            "summary": "Central metaphor generated successfully."
        }
        
    def _build_metaphor_prompt(self, topic: str, profile: Dict) -> str:
        return f"""
مهمتك: أنت شاعر و فيلسوف. مهمتك ليست كتابة أغنية، بل خلق **الصورة الشعرية المركزية (Central Metaphor)** التي ستكون قلب الأغنية.

**الموضوع:** {topic}
**روح الفنان:** يميل إلى مواضيع {profile.get('core_themes', [])}، ويستخدم رموزًا مثل {profile.get('symbolic_lexicon', {}).get('key_symbols', [])}.

**المطلوب:**
ابتكر صورة شعرية واحدة، ملموسة، ومبتكرة لتجسيد هذا الموضوع. يجب أن تكون الصورة قابلة للتطور داخل الأغنية.
أرجع ردك **حصريًا** بتنسيق JSON.
{{
  "metaphor_object": "string // الشيء المادي الذي يمثل الرمز (مثال: 'مفتاح صدئ').",
  "metaphor_meaning": "string // المعنى العميق لهذا الرمز (مثال: 'يمثل الأمل المفقود والذكريات التي لا يمكن الوصول إليها').",
  "sensory_details": ["string"] // قائمة بتفاصيل حسية مرتبطة بالرمز (مثال: 'ملمسه بارد'، 'رائحته كرائحة التراب القديم').
}}
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        # تم تعديل المهمة الافتراضية لتكون توليد الاستعارة
        return await self.generate_central_metaphor(context)

# إنشاء مثيل وحيد
dream_symbol_interpreter_agent = DreamSymbolInterpreterAgent()
