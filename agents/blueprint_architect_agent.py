# agents/blueprint_architect_agent.py (النسخة المفعّلة)

import logging
import json
import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from .base_agent import BaseAgent
from core.llm_service import llm_service
# استيراد نماذج البيانات التي يعتمد عليها
from engines.advanced_context_engine import KnowledgeBase

# تعريف نماذج البيانات محليًا لتسهيل الاستخدام
class ChapterOutline(BaseModel):
    title: str
    summary: str
    emotional_focus: str
    key_events: List[str]
    character_arcs: Dict[str, str]

class StoryBlueprint(BaseModel):
    introduction: str
    chapters: List[ChapterOutline]
    conclusion: str
    main_conflict: str
    themes: List[str]

logger = logging.getLogger("BlueprintArchitectAgent")

class BlueprintArchitectAgent(BaseAgent):
    """
    وكيل متخصص في تحويل قاعدة المعرفة (KnowledgeBase) إلى مخطط سردي (Blueprint) ذكي ومتكامل.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "blueprint_architect_agent",
            name="مهندس المخططات",
            description="يصمم الهيكل السردي للقصص بناءً على تحليل عميق للمحتوى."
        )
        logger.info("BlueprintArchitectAgent initialized.")

    async def create_blueprint(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تأخذ KnowledgeBase وتنتج StoryBlueprint.
        'context' يجب أن يحتوي على 'knowledge_base'.
        """
        kb_data = context.get("knowledge_base")
        if not kb_data:
            raise ValueError("KnowledgeBase is required to create a blueprint.")
        
        # تحويل القاموس مرة أخرى إلى كائن Pydantic للتحقق من صحته
        try:
            kb = KnowledgeBase.parse_obj(kb_data)
        except Exception as e:
            raise ValueError(f"Invalid KnowledgeBase structure provided: {e}")

        logger.info(f"Creating blueprint from KnowledgeBase with {len(kb.entities)} entities...")
        
        prompt = self._build_blueprint_prompt(kb)
        response = await llm_service.generate_json_response(prompt, temperature=0.5)

        if "error" in response:
            logger.error(f"LLM call failed for blueprint creation. Details: {response.get('details')}")
            return {"status": "error", "message": "LLM call failed"}

        try:
            # التحقق من صحة المخطط الناتج باستخدام Pydantic
            blueprint = StoryBlueprint.parse_obj(response)
            return {"status": "success", "blueprint": blueprint.dict()}
        except ValidationError as e:
            logger.error(f"LLM returned an invalid blueprint structure: {e}")
            return {"status": "error", "message": "Invalid blueprint structure from LLM", "raw": response}

    def _build_blueprint_prompt(self, kb: KnowledgeBase) -> str:
        # تحويل قاعدة المعرفة إلى نص يمكن للـ LLM فهمه
        kb_summary = f"""
- **الشخصيات الرئيسية:** {', '.join([e.name for e in kb.entities if e.type == 'character' and e.importance_score > 7])}
- **العلاقات الأساسية:** {', '.join([f"{r.source} {r.relation} {r.target}" for r in kb.relationship_graph[:5]])}
- **الرحلة العاطفية:** تبدأ بـ {kb.emotional_arc[0].emotion if kb.emotional_arc else 'N/A'} وتنتهي بـ {kb.emotional_arc[-1].emotion if kb.emotional_arc else 'N/A'}.
- **عدد الأحداث الهامة:** {len(kb.relationship_graph)}
"""
        return f"""
مهمتك: أنت مهندس معماري للسرد (Narrative Architect). مهمتك هي تحويل التحليل التالي إلى مخطط رواية (Story Blueprint) من 3 إلى 5 فصول.
**ملخص التحليل (قاعدة المعرفة):**
{kb_summary}

**التعليمات:**
1.  اكتب مقدمة (introduction) تعرف بالشخصيات والصراع الرئيسي.
2.  صمم من 3 إلى 5 فصول (chapters). لكل فصل، حدد عنوانًا، ملخصًا للأحداث، تركيزًا عاطفيًا، وتطورًا للشخصيات.
3.  اكتب خاتمة (conclusion) تقدم حلاً مرضيًا للصراع.
4.  لخص الصراع الرئيسي (main_conflict) في جملة واحدة.
5.  استخلص أهم 3 مواضيع (themes) من التحليل.

أرجع ردك **حصريًا** بتنسيق JSON صالح يتبع المخطط التالي تمامًا:
{{
  "introduction": "string",
  "chapters": [
    {{
      "title": "string",
      "summary": "string",
      "emotional_focus": "string",
      "key_events": ["string"],
      "character_arcs": {{
        "اسم الشخصية": "string // وصف تطور الشخصية في هذا الفصل"
      }}
    }}
  ],
  "conclusion": "string",
  "main_conflict": "string",
  "themes": ["string"]
}}
"""
