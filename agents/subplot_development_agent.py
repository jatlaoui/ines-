# agents/subplot_development_agent.py
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# استيراد المكونات الأساسية
from core.base_agent import BaseAgent
from core.llm_service import llm_service
from agents.blueprint_architect_agent import StoryBlueprint # يعتمد على نموذج المخطط الكامل

logger = logging.getLogger("SubplotDevelopmentAgent")

# --- نماذج Pydantic للحبكات الفرعية ---
class Subplot(BaseModel):
    """
    يمثل حبكة فرعية متكاملة مع أهدافها وشخصياتها.
    """
    title: str = Field(description="عنوان موجز للحبكة الفرعية (مثال: 'قصة حب أحمد وعزيزة').")
    type: str = Field(description="نوع الحبكة الفرعية (مثال: 'رومانسية'، 'لغز'، 'صراع ثانوي').")
    involved_characters: List[str] = Field(description="قائمة بأسماء الشخصيات الرئيسية في هذه الحبكة الفرعية.")
    summary: str = Field(description="ملخص لكيفية بدء وتطور وانتهاء هذه الحبكة الفرعية عبر الرواية.")
    connection_to_main_plot: str = Field(description="شرح كيف تتقاطع هذه الحبكة الفرعية مع الحبكة الرئيسية وتؤثر عليها.")

class SubplotSuggestions(BaseModel):
    """
    قائمة بالاقتراحات للحبكات الفرعية.
    """
    subplots: List[Subplot] = Field(description="قائمة من 2-3 اقتراحات للحبكات الفرعية التي يمكن إضافتها للرواية.")

class SubplotDevelopmentAgent(BaseAgent):
    """
    يقترح ويدير الحبكات الفرعية لإثراء السرد في الروايات الطويلة.
    """
    def __init__(self, agent_id: Optional[str] = "subplot_development_agent"):
        super().__init__(
            agent_id=agent_id,
            name="مهندس الحبكات الفرعية",
            description="يصمم ويقترح حبكات فرعية لإضافة عمق وتعقيد للقصة الرئيسية."
        )
        logger.info("✅ SubplotDevelopmentAgent initialized.")

    async def suggest_subplots(self, story_blueprint: StoryBlueprint) -> Optional[SubplotSuggestions]:
        """
        الوظيفة الرئيسية: يقترح حبكات فرعية بناءً على المخطط السردي الحالي.

        Args:
            story_blueprint: المخطط السردي الكامل للرواية.

        Returns:
            كائن SubplotSuggestions يحتوي على قائمة من الحبكات المقترحة.
        """
        logger.info(f"Generating subplot suggestions for story: '{story_blueprint.logline}'")
        
        prompt = self._build_suggestion_prompt(story_blueprint)

        suggestions = await llm_service.generate_structured_response(
            prompt=prompt,
            response_model=SubplotSuggestions,
            system_instruction="أنت روائي ومحرر خبير في بناء القصص المعقدة. مهمتك هي تحليل مخطط قصة واقتراح حبكات فرعية مثيرة للاهتمام."
        )

        if suggestions:
            logger.info(f"Generated {len(suggestions.subplots)} subplot suggestions.")
        else:
            logger.error("Failed to generate subplot suggestions.")
            
        return suggestions

    def _build_suggestion_prompt(self, blueprint: StoryBlueprint) -> str:
        """
        يبني موجهًا لاقتراح حبكات فرعية.
        """
        # تلخيص المخطط الحالي لتوفير السياق
        blueprint_summary = f"""
- **الفكرة الرئيسية:** {blueprint.logline}
- **الصراع الرئيسي:** {blueprint.main_conflict}
- **الشخصيات الرئيسية:** {', '.join([ch.character_arcs.keys() for ch in blueprint.chapters if ch.character_arcs])}
- **المواضيع:** {', '.join(blueprint.themes)}
"""
        return f"""
بناءً على مخطط الرواية التالي، اقترح 2-3 حبكات فرعية (subplots) يمكن أن تثري القصة.

**ملخص مخطط الرواية الحالي:**
---
{blueprint_summary}
---

**إرشادات لاقتراح الحبكات الفرعية:**
- يجب أن تتشابك الحبكة الفرعية مع الحبكة الرئيسية وتؤثر فيها.
- يجب أن تساعد في تطوير شخصية واحدة على الأقل من الشخصيات الرئيسية.
- يجب أن تضيف طبقة جديدة من التوتر أو العمق العاطفي للرواية.
- اقترح أنواعًا متنوعة (قصة حب، لغز، صراع على السلطة، إلخ).

قم بملء قائمة اقتراحات الحبكات الفرعية التالية.
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        نقطة الدخول الموحدة.
        """
        try:
            blueprint = StoryBlueprint.parse_obj(context.get("story_blueprint"))
        except Exception as e:
            return {"status": "error", "message": f"Invalid story_blueprint structure: {e}"}

        suggestions = await self.suggest_subplots(blueprint)

        if suggestions:
            return {
                "status": "success",
                "content": {"subplot_suggestions": suggestions.dict()},
                "summary": f"Generated {len(suggestions.subplots)} subplot suggestions."
            }
        else:
            return {
                "status": "error",
                "message": "Could not generate subplot suggestions."
            }

# إنشاء مثيل وحيد
subplot_development_agent = SubplotDevelopmentAgent()
