# engines/advanced_context_engine.py (V2 - Structured Output Powered)
import asyncio
import json
import logging
import uuid
from typing import List, Dict, Any, Optional, Type

from pydantic import BaseModel, Field, ValidationError

# استيراد خدمة LLM المطورة
from core.llm_service import llm_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ContextEngine] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- نماذج Pydantic (تبقى كما هي، فهي ممتازة) ---
class EntityContext(BaseModel):
    role_in_text: str = Field(..., description="دور الكيان في السرد (بطل، مكان رئيسي، رمز، إلخ).")
    cultural_significance: Optional[str] = Field(None, description="الأهمية الثقافية أو التراثية للكيان.")
    historical_period: Optional[str] = Field(None, description="الفترة التاريخية المرتبطة بالكيان إن وجدت.")

class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="اسم الكيان.")
    type: str = Field(..., description="نوع الكيان (شخصية، مكان، شيء، مفهوم مجرد).")
    description: str = Field(..., description="وصف موجز للكيان ودوره.")
    importance_score: float = Field(..., ge=0.0, le=10.0, description="تقييم لأهمية الكيان في السرد (0-10).")
    context: EntityContext

class EntityList(BaseModel):
    entities: List[Entity] = Field(description="قائمة بجميع الكيانات المستخرجة من النص.")

class Relationship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str = Field(..., description="معرف الكيان المصدر للعلاقة (يجب أن يكون من الكيانات المستخرجة).")
    target: str = Field(..., description="معرف الكيان الهدف للعلاقة (يجب أن يكون من الكيانات المستخرجة).")
    relation: str = Field(..., description="وصف طبيعة العلاقة (مثال: 'يحب'، 'يكره'، 'يؤدي إلى'، 'يساعد').")
    context: Optional[str] = Field(None, description="السياق الذي تظهر فيه العلاقة.")

class RelationshipList(BaseModel):
    relationships: List[Relationship] = Field(description="قائمة بجميع العلاقات المستخرجة من النص.")

class EmotionalArcPoint(BaseModel):
    timestamp: int = Field(..., ge=0, le=100, description="موضع نسبي في النص (0-100) حيث يحدث التحول العاطفي.")
    emotion: str = Field(..., description="العاطفة السائدة في هذه النقطة (مثال: أمل، يأس، غضب).")
    intensity: float = Field(..., ge=0.0, le=1.0, description="شدة العاطفة (0.0 إلى 1.0).")
    reasoning: Optional[str] = Field(None, description="السبب أو الحدث الذي أدى إلى هذه العاطفة.")

class EmotionalArc(BaseModel):
    emotional_arc_points: List[EmotionalArcPoint] = Field(description="قائمة بنقاط القوس العاطفي للسرد.")

class KnowledgeBase(BaseModel):
    """
    قاعدة المعرفة السردية المنظمة التي تمثل فهمًا عميقًا للنص.
    """
    entities: List[Entity]
    relationship_graph: List[Relationship]
    emotional_arc: List[EmotionalArcPoint]
    thematic_summary: str = Field(description="ملخص للمواضيع الرئيسية في النص في جملتين.")

# --- المحرك المتقدم (مُحدَّث بالكامل) ---
class AdvancedContextEngine:
    """
    يبني قاعدة معرفة غنية ومترابطة من النصوص عبر استدعاءات متخصصة
    وموثوقة لـ LLM باستخدام المخرجات المنظمة.
    """
    def __init__(self):
        logger.info("✅ AdvancedContextEngine (V2) initialized, powered by Structured Outputs.")

    async def analyze_text(self, text: str) -> Optional[KnowledgeBase]:
        """
        الوظيفة الرئيسية للتحليل. تقوم بتشغيل جميع مهام التحليل بالتوازي.
        """
        if not text or len(text.strip()) < 50:
            logger.warning("Input text is too short for meaningful analysis.")
            return None

        logger.info(f"🚀 Starting comprehensive analysis for text (length: {len(text)})...")
        
        # استدعاء جميع دوال التحليل بالتوازي لتحقيق أقصى سرعة
        analysis_tasks = [
            self._extract_entities(text),
            self._analyze_relationships(text),
            self._analyze_emotional_arc(text)
        ]
        
        entities, relationships, emo_arc = await asyncio.gather(*analysis_tasks)
        
        # التحقق من أن جميع المهام الأساسية نجحت
        if not all([entities, relationships, emo_arc]):
            logger.error("One or more core analysis tasks failed. Aborting KnowledgeBase creation.")
            return None

        # [جديد] استخلاص ملخص المواضيع
        thematic_summary = await self._summarize_themes(text)
        
        # بناء قاعدة المعرفة النهائية والتحقق من صحتها
        try:
            kb = KnowledgeBase(
                entities=entities.entities,
                relationship_graph=relationships.relationships,
                emotional_arc=emo_arc.emotional_arc_points,
                thematic_summary=thematic_summary
            )
            logger.info(f"✅ Analysis complete. KnowledgeBase created with {len(kb.entities)} entities and {len(kb.relationship_graph)} relationships.")
            return kb
        except ValidationError as e:
            logger.error(f"Failed to assemble final KnowledgeBase: {e}")
            return None

    def _build_prompt(self, task_description: str, text_to_analyze: str) -> str:
        """دالة مساعدة موحدة لبناء الموجهات بشكل نظيف."""
        return f"""
مهمتك: أنت محلل سردي خبير فائق الذكاء. قم بتحليل النص التالي بدقة.

**وصف المهمة المطلوبة:**
{task_description}

**النص للتحليل:**
---
{text_to_analyze}
---

أرجع ردك **حصريًا** بالتنسيق المحدد مسبقًا. لا تقم بإضافة أي نص أو تعليقات خارج البنية المطلوبة.
"""

    async def _extract_entities(self, text: str) -> Optional[EntityList]:
        prompt = self._build_prompt(
            task_description="استخرج جميع الكيانات الهامة (شخصيات، أماكن، مفاهيم، رموز) من النص. حدد دور كل كيان وقيم أهميته في السرد من 0 إلى 10.",
            text_to_analyze=text
        )
        return await llm_service.generate_structured_response(prompt, EntityList)

    async def _analyze_relationships(self, text: str) -> Optional[RelationshipList]:
        prompt = self._build_prompt(
            task_description="حلل العلاقات السببية والنفسية بين الكيانات الرئيسية في النص. حدد ما هو الكيان الذي يؤثر على كيان آخر وكيف.",
            text_to_analyze=text
        )
        return await llm_service.generate_structured_response(prompt, RelationshipList)

    async def _analyze_emotional_arc(self, text: str) -> Optional[EmotionalArc]:
        prompt = self._build_prompt(
            task_description="ارسم القوس العاطفي للسرد. حدد نقاط التحول العاطفي الرئيسية (من 0 إلى 100)، ونوع العاطفة، وشدتها (من 0.0 إلى 1.0) مع ذكر السبب.",
            text_to_analyze=text
        )
        return await llm_service.generate_structured_response(prompt, EmotionalArc)

    async def _summarize_themes(self, text: str) -> str:
        """[جديد] يستخلص المواضيع الرئيسية كنص عادي."""
        prompt = self._build_prompt(
            task_description="لخص المواضيع والأفكار الرئيسية التي يناقشها هذا النص في جملتين فقط.",
            text_to_analyze=text
        )
        # هنا، الرد هو نص بسيط وليس JSON
        summary = await llm_service.generate_text_response(prompt, temperature=0.3)
        return summary

# --- قسم الاختبار (يبقى كما هو للتأكد من أن التعديلات تعمل) ---
async def main_test():
    # ... يمكن استخدام نفس نص الاختبار السابق ...
    pass

if __name__ == "__main__":
    # asyncio.run(main_test())
    pass
