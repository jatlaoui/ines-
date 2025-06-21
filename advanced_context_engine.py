# engines/advanced_context_engine.py (النسخة المفعّلة)

import asyncio
import json
import logging
import uuid
from typing import List, Dict, Any, Optional, Type

from pydantic import BaseModel, Field, ValidationError

# --- استيراد الخدمة الحقيقية ---
from core.llm_service import llm_service

# --- إعدادات التسجيل ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ContextEngine] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- نماذج Pydantic (تبقى كما هي) ---
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
    entities: List[Entity]

class Relationship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str = Field(..., description="اسم الكيان المصدر للعلاقة.")
    target: str = Field(..., description="اسم الكيان الهدف للعلاقة.")
    relation: str = Field(..., description="وصف طبيعة العلاقة (مثال: 'يحب'، 'يكره'، 'يؤدي إلى'، 'يساعد').")
    context: Optional[str] = Field(None, description="السياق الذي تظهر فيه العلاقة.")

class RelationshipList(BaseModel):
    relationships: List[Relationship]

class EmotionalArcPoint(BaseModel):
    timestamp: int = Field(..., description="موضع نسبي في النص (0-100) حيث يحدث التحول العاطفي.")
    emotion: str = Field(..., description="العاطفة السائدة في هذه النقطة (مثال: أمل، يأس، غضب).")
    intensity: float = Field(..., ge=0.0, le=1.0, description="شدة العاطفة (0.0 إلى 1.0).")
    reasoning: Optional[str] = Field(None, description="السبب أو الحدث الذي أدى إلى هذه العاطفة.")

class EmotionalArc(BaseModel):
    emotional_arc_points: List[EmotionalArcPoint]

class KnowledgeBase(BaseModel):
    entities: List[Entity]
    relationship_graph: List[Relationship]
    emotional_arc: List[EmotionalArcPoint]
    historical_context: Dict[str, Any]

# --- المحرك المتقدم (مُحدَّث) ---
class AdvancedContextEngine:
    """
    يبني قاعدة معرفة غنية ومترابطة من النصوص عبر استدعاءات متخصصة لـ LLM.
    """
    def __init__(self):
        # لم نعد بحاجة لخدمات وهمية هنا
        logger.info("✅ AdvancedContextEngine initialized and connected to the live LLM service.")

    async def analyze_text(self, text: str) -> KnowledgeBase:
        """
        الوظيفة الرئيسية للتحليل. تقوم بتشغيل جميع مهام التحليل بالتوازي.
        """
        logger.info(f"🚀 Starting comprehensive analysis for text (length: {len(text)})...")
        
        # استدعاء جميع دوال التحليل بالتوازي لتحقيق أقصى سرعة
        analysis_tasks = [
            self._extract_advanced_entities(text),
            self._analyze_events_with_causality(text),
            self._analyze_characters_psychological(text),
            self._analyze_emotional_arc(text)
        ]
        
        entities_list, event_rels, char_rels, emo_arc = await asyncio.gather(*analysis_tasks)
        
        # تجميع النتائج
        all_rels = (event_rels.relationships if event_rels else []) + (char_rels.relationships if char_rels else [])
        
        # محاكاة لإثراء السياق التاريخي (يمكن تفعيله لاحقًا)
        hist_ctx = {}

        kb = KnowledgeBase(
            entities=entities_list.entities if entities_list else [],
            relationship_graph=all_rels,
            emotional_arc=emo_arc.emotional_arc_points if emo_arc else [],
            historical_context=hist_ctx
        )
        logger.info(f"✅ Analysis complete. KnowledgeBase created with {len(kb.entities)} entities and {len(kb.relationship_graph)} relationships.")
        return kb

    async def _process_llm_json_response(self, prompt: str, pydantic_model: Type[BaseModel]) -> Optional[BaseModel]:
        """
        دالة مساعدة موحدة لاستدعاء الـ LLM، تحليل الـ JSON، والتحقق من صحته باستخدام Pydantic.
        """
        response_json = await llm_service.generate_json_response(prompt)

        if "error" in response_json:
            logger.error(f"LLM call failed: {response_json.get('details')}")
            return None # إرجاع None في حالة فشل استدعاء الـ LLM
        
        try:
            # استخدام Pydantic لتحليل وتحقق من صحة بنية الـ JSON
            validated_data = pydantic_model.parse_obj(response_json)
            logger.info(f"Successfully parsed and validated response for {pydantic_model.__name__}.")
            return validated_data
        except ValidationError as e:
            logger.error(f"Pydantic validation failed for {pydantic_model.__name__}: {e}")
            logger.error(f"Invalid JSON received: {response_json}")
            return None # إرجاع None في حالة فشل التحقق

    def _build_prompt_for_model(self, task_description: str, json_schema: Dict, text: str) -> str:
        """دالة مساعدة لبناء الـ Prompts بشكل موحد."""
        return f"""
مهمتك: أنت محلل سردي خبير. قم بتحليل النص التالي بدقة.
**وصف المهمة:** {task_description}

**النص للتحليل:**
---
{text}
---

أرجع ردك **حصريًا** بتنسيق JSON صالح يتبع المخطط التالي تمامًا. لا تقم بإضافة أي نص أو تعليقات خارج كائن الـ JSON.
**مخطط JSON المطلوب (Schema):**
{json.dumps(json_schema, indent=2, ensure_ascii=False)}
"""

    async def _extract_advanced_entities(self, text: str) -> Optional[EntityList]:
        prompt = self._build_prompt_for_model(
            task_description="استخرج جميع الكيانات (شخصيات، أماكن، مفاهيم، أشياء) من النص. حدد دور كل كيان وقيم أهميته في السرد.",
            json_schema=EntityList.schema(),
            text=text
        )
        return await self._process_llm_json_response(prompt, EntityList)

    async def _analyze_events_with_causality(self, text: str) -> Optional[RelationshipList]:
        prompt = self._build_prompt_for_model(
            task_description="حلل العلاقات السببية بين الأحداث الرئيسية في النص. حدد ما هو الحدث الذي يؤدي إلى حدث آخر.",
            json_schema=RelationshipList.schema(),
            text=text
        )
        return await self._process_llm_json_response(prompt, RelationshipList)

    async def _analyze_characters_psychological(self, text: str) -> Optional[RelationshipList]:
        prompt = self._build_prompt_for_model(
            task_description="حلل العلاقات النفسية والدوافع الداخلية للشخصيات. صف علاقات الحب، الكراهية، الصداقة، والطموح.",
            json_schema=RelationshipList.schema(),
            text=text
        )
        return await self._process_llm_json_response(prompt, RelationshipList)

    async def _analyze_emotional_arc(self, text: str) -> Optional[EmotionalArc]:
        prompt = self._build_prompt_for_model(
            task_description="ارسم القوس العاطفي للسرد. حدد نقاط التحول العاطفي الرئيسية (0-100)، ونوع العاطفة، وشدتها (0.0-1.0).",
            json_schema=EmotionalArc.schema(),
            text=text
        )
        return await self._process_llm_json_response(prompt, EmotionalArc)

# --- قسم الاختبار المحدّث ---
async def main_test():
    # تأكد من أن متغير البيئة GEMINI_API_KEY معين
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود. يرجى إضافته في ملف .env")
        return

    engine = AdvancedContextEngine()
    sample_text = """
    في زقاق ضيق من أزقة القاهرة القديمة، وجد علي، الشاب الحالم الذي فقد شغفه، رسالة غامضة في صندوق جده الخشبي.
    الرسالة، التي كتبتها جدته الراحلة، تحدثت عن كنز ليس من ذهب، بل كنز من الحكمة مدفون تحت شجرة عتيقة في سيناء.
    شعر علي بمزيج من الحنين والفضول، وشعلة أمل خافتة بدأت تضيء ظلمة روحه. 
    كان هذا الاكتشاف هو ما يحتاجه تمامًا. قرار البحث عن هذا الكنز لم يكن سهلاً، فقد كان يعني ترك حياته الرتيبة ومواجهة المجهول.
    لكن دافعه لتحقيق ذاته كان أقوى من خوفه.
    """
    
    print(f"--- 🧪 بدء اختبار محرك السياق المتقدم مع نص حقيقي... ---")
    try:
        knowledge_base = await engine.analyze_text(sample_text)
        
        print("\n--- ✅ التحليل اكتمل بنجاح! ---")
        print("--- قاعدة المعرفة (KnowledgeBase) الناتجة: ---")
        # طباعة النتيجة بتنسيق JSON جميل
        print(knowledge_base.json(indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"--- ❌ فشل الاختبار ---")
        logger.error(f"An error occurred during the test: {e}", exc_info=True)

if __name__ == "__main__":
    # تشغيل الاختبار
    asyncio.run(main_test())
