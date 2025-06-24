# agents/blueprint_architect_agent.py (V2 - Merged & Structured)
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# استيراد المكونات الأساسية والنماذج
from core.base_agent import BaseAgent
from core.llm_service import llm_service
from engines.advanced_context_engine import KnowledgeBase # يعتمد على مخرجات محرك السياق

logger = logging.getLogger("BlueprintArchitectAgent")

# --- [جديد] تعريف نماذج Pydantic للمخطط السردي ---
class ChapterOutline(BaseModel):
    title: str = Field(description="عنوان جذاب وموجز للفصل.")
    summary: str = Field(description="ملخص لجوهر الأحداث الرئيسية في هذا الفصل.")
    emotional_focus: str = Field(description="العاطفة أو الحالة المزاجية السائدة التي يجب أن يشعر بها القارئ في هذا الفصل (مثال: توتر، أمل، حيرة).")
    key_events: List[str] = Field(description="قائمة بالأحداث الرئيسية التي تدفع الحبكة إلى الأمام في هذا الفصل.")
    character_arcs: Dict[str, str] = Field(description="قاموس يصف تطور كل شخصية رئيسية خلال هذا الفصل.")

class StoryBlueprint(BaseModel):
    """
    المخطط السردي المتكامل للقصة، مصمم ليكون خارطة طريق للكتابة.
    """
    logline: str = Field(description="القصة في جملة واحدة جذابة.")
    main_conflict: str = Field(description="الصراع المركزي الذي يحرك القصة بأكملها.")
    themes: List[str] = Field(description="قائمة بالمواضيع أو الأفكار الرئيسية التي تستكشفها القصة.")
    chapters: List[ChapterOutline] = Field(description="قائمة مفصلة بالفصول التي تشكل هيكل القصة.")
    conclusion_summary: str = Field(description="ملخص لكيفية حل الصراع الرئيسي وما هو مصير الشخصيات.")


class BlueprintArchitectAgent(BaseAgent):
    """
    [مُرقَّى] وكيل متخصص في تحويل قاعدة المعرفة (KnowledgeBase) إلى مخطط سردي (Blueprint) ذكي ومتكامل.
    يدمج الآن مسؤوليات الكاتب الدرامي (Dramaturg).
    """
    def __init__(self, agent_id: Optional[str] = "blueprint_architect"):
        super().__init__(
            agent_id=agent_id,
            name="مهندس المخططات السردية",
            description="يصمم الهيكل السردي للقصص بناءً على تحليل عميق للمحتوى."
        )
        logger.info("✅ BlueprintArchitectAgent (V2) initialized.")

    async def create_blueprint_from_kb(self, kb: KnowledgeBase) -> Optional[StoryBlueprint]:
        """
        الوظيفة الرئيسية: تأخذ KnowledgeBase وتنتج StoryBlueprint.
        """
        logger.info(f"Creating blueprint from KnowledgeBase with {len(kb.entities)} entities...")
        
        prompt = self._build_blueprint_prompt(kb)
        
        # استخدام المخرجات المنظمة لضمان الحصول على مخطط صالح
        blueprint = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=StoryBlueprint,
            system_instruction="أنت كاتب درامي (Dramaturg) وخبير في بناء القصص. مهمتك هي تحويل تحليل نصي إلى مخطط روائي متكامل ومتماسك."
        )

        if not blueprint:
            logger.error("Failed to generate a valid StoryBlueprint from the KnowledgeBase.")
            return None
        
        logger.info(f"Successfully created a blueprint with {len(blueprint.chapters)} chapters.")
        return blueprint

    def _build_blueprint_prompt(self, kb: KnowledgeBase) -> str:
        """
        يبني موجهًا فعالاً لتحويل قاعدة المعرفة إلى مخطط سردي.
        """
        # تحويل قاعدة المعرفة إلى نص موجز يمكن للـ LLM فهمه
        kb_summary = f"""
- **ملخص المواضيع:** {kb.thematic_summary}
- **الشخصيات الرئيسية:** {', '.join([e.name for e in kb.entities if e.type == 'شخصية' and e.importance_score > 7])}
- **العلاقات الأساسية:** {', '.join([f"{r.source} {r.relation} {r.target}" for r in kb.relationship_graph[:5]])}
- **الرحلة العاطفية:** تبدأ بـ '{kb.emotional_arc[0].emotion if kb.emotional_arc else 'N/A'}' وتنتهي بـ '{kb.emotional_arc[-1].emotion if kb.emotional_arc else 'N/A'}'.
"""
        return f"""
بناءً على ملخص التحليل التالي، قم ببناء مخطط قصة (Story Blueprint) كامل ومتكامل من 3 إلى 5 فصول.
يجب أن يكون المخطط بمثابة خارطة طريق واضحة لكتابة الرواية.

**ملخص التحليل (من قاعدة المعرفة):**
---
{kb_summary}
---

قم بتصميم المخطط السردي الكامل، مع التأكد من ملء جميع الحقول المطلوبة بدقة وتفصيل.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة لمعالجة المهام.
        """
        kb_data = context.get("knowledge_base")
        if not kb_data:
            return {"status": "error", "message": "KnowledgeBase is required to create a blueprint."}
        
        try:
            # التحقق من صحة بنية KnowledgeBase المدخلة
            kb = KnowledgeBase.parse_obj(kb_data)
        except ValidationError as e:
            return {"status": "error", "message": f"Invalid KnowledgeBase structure provided: {e}"}

        blueprint = await self.create_blueprint_from_kb(kb)
        
        if blueprint:
            return {
                "status": "success",
                "content": {"blueprint": blueprint.dict()},
                "summary": f"Blueprint created successfully with logline: '{blueprint.logline}'"
            }
        else:
            return {
                "status": "error",
                "message": "Could not generate a story blueprint."
            }

# إنشاء مثيل وحيد
blueprint_architect_agent = BlueprintArchitectAgent()
