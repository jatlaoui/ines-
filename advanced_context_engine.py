# advanced_context_engine.py
"""
محرك التحليل المعماري المتقدم (Advanced Context Engine)
الغرض: بناء "قاعدة معرفة" مترابطة للنصوص، مع تحليل الكيانات، العلاقات، السياقات، والقوس العاطفي.
"""
import asyncio
import json
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# --- نماذج Pydantic ---
class EntityContext(BaseModel):
    role_in_text: str = Field(..., description="دور الكيان في السرد (مثال: البطل، الحدث المحرك)")
    cultural_significance: Optional[str] = Field(None, description="الأهمية الثقافية أو الرمزية")
    historical_period: Optional[str] = Field(None, description="الفترة الزمنية المرتبطة بالكيان")

class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="معرف فريد للكيان")
    name: str = Field(..., description="اسم الكيان")
    type: str = Field(..., description="نوع الكيان: 'character','event','location','concept','object'")
    description: str = Field(..., description="وصف موجز للكيان (جملة واحدة)")
    importance_score: float = Field(..., ge=0.0, le=10.0, description="درجة أهمية من 0.0 إلى 10.0")
    context: EntityContext = Field(..., description="السياق التفصيلي للكيان")

class EntityList(BaseModel):
    entities: List[Entity]

class Relationship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="معرف فريد للعلاقة")
    source: str = Field(..., description="اسم الكيان المصدر")
    target: str = Field(..., description="اسم الكيان الهدف")
    relation: str = Field(..., description="وصف العلاقة (مثال: 'يؤدي إلى', 'يسبب')")
    context: Optional[str] = Field(None, description="الجملة التي تصف العلاقة في النص")

class RelationshipList(BaseModel):
    relationships: List[Relationship]

class EmotionalArcPoint(BaseModel):
    timestamp: int = Field(..., description="موضع تقريبي في النص (0-100)")
    emotion: str = Field(..., description="العاطفة السائدة في هذه النقطة")
    intensity: float = Field(..., ge=0.0, le=10.0, description="شدة العاطفة (0-10)")
    reasoning: Optional[str] = Field(None, description="شرح موجز للحدث أو الفكرة التي أثارت هذه العاطفة")

class EmotionalArc(BaseModel):
    emotional_arc_points: List[EmotionalArcPoint]

class KnowledgeBase(BaseModel):
    entities: List[Entity]
    relationship_graph: List[Relationship]
    emotional_arc: List[EmotionalArcPoint]
    historical_context: Dict[str, Any]

# --- خدمات LLM ومحاكاة الاستدعاء ---
class GeminiService:
    async def generate_content(self, prompt: str) -> str:
        print(f"--- LLM Prompt ---\n{prompt[:600]}...\n------------------")
        if 'analyze_events_with_causality' in prompt:
            mock = {
                "relationships": [
                    {"source": "الرسالة القديمة", "target": "علي", "relation": "يُحفِّز على البحث", "context": "الرسالة القديمة كانت مفتاحًا لماضيه المجهول."},
                    {"source": "علي", "target": "سوق المدينة العتيق", "relation": "يذهب إلى", "context": "كان علي يبحث... فالسوق العتيق الذي يحتضن سره."},
                    {"source": "البحث عن الكنز", "target": "المخاطر", "relation": "يؤدي إلى", "context": "كان يعلم أن رحلته محفوفة بالمخاطر."}
                ]
            }
        elif 'analyze_emotional_arc' in prompt:
            mock = {
                "emotional_arc_points": [
                    {"timestamp": 10, "emotion": "أمل حذر", "intensity": 6.0, "reasoning": "العثور على الرسالة يمثل بداية أمل."},
                    {"timestamp": 30, "emotion": "قلق وتوتر", "intensity": 7.5, "reasoning": "إدراك المخاطر في السوق العتيق."},
                    {"timestamp": 60, "emotion": "حيرة وشك", "intensity": 7.0, "reasoning": "مواجهة أول عقبة."},
                    {"timestamp": 90, "emotion": "إصرار وتصميم", "intensity": 8.5, "reasoning": "اتخاذ قرار بالمضي قدمًا رغم الصعوبات."}
                ]
            }
        else:
            mock = {"entities": []}
        return json.dumps(mock, ensure_ascii=False)

class WebSearchService:
    async def search(self, query: str) -> Any:
        return {}

# --- المحرك المتقدم ---
class AdvancedContextEngine:
    def __init__(self, web_search_service=None):
        self.web_search_service = web_search_service or WebSearchService()
        self.gemini_service = GeminiService()

    async def analyze_text(self, text: str, external_sources: Optional[List[str]] = None) -> KnowledgeBase:
        entities = await self._extract_advanced_entities(text)
        event_rel, char_psy, emo_arc = await asyncio.gather(
            self._analyze_events_with_causality(text, entities),
            self._analyze_characters_psychological(text, entities),
            self._analyze_emotional_arc(text)
        )
        hist_ctx = await self._enrich_with_external_context(entities, external_sources)
        return KnowledgeBase(
            entities=entities,
            relationship_graph=event_rel,
            emotional_arc=emo_arc,
            historical_context=hist_ctx
        )

    async def _process_llm_json_response(self, prompt: str, model: BaseModel) -> Any:
        response = await self.gemini_service.generate_content(prompt)
        try:
            json_str = self._clean_llm_output(response)
            return model.parse_raw(json_str)
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error parsing LLM response: {e}\nRaw: {response[:500]}")
            raise

    async def _extract_advanced_entities(self, text: str) -> List[Entity]:
        prompt = f"""
        مهمتك: تحليل النص التالي واستخراج الكيانات الأكثر أهمية.
        لكل كيان، حدد: name, type (character/event/location/concept/object), description, importance_score (0.0-10.0), context.
        أرجع JSON جذري بمفتاح 'entities'.
        النص:
        ---
        {text[:10000]}
        ---
        """
        result = await self._process_llm_json_response(prompt, EntityList)
        return result.entities

    async def _analyze_events_with_causality(self, text: str, entities: List[Entity]) -> List[Relationship]:
        if not entities:
            return []
        relevant_names = [e.name for e in entities if e.type in ['character','event','object','location']]
        prompt = f"analyze_events_with_causality\nمهمتك: تحديد العلاقات السببية بين الكيانات: {', '.join(relevant_names)}\nالنص:\n---\n{text[:10000]}\n---"
        result = await self._process_llm_json_response(prompt, RelationshipList)
        return result.relationships

    async def _analyze_characters_psychological(self, text: str, entities: List[Entity]) -> List[Relationship]:
        print("Warning: characters analysis not implemented.")
        return []

    async def _analyze_emotional_arc(self, text: str) -> List[EmotionalArcPoint]:
        prompt = f"analyze_emotional_arc\nمهمتك: تعقب القوس العاطفي عبر النص، 4-7 نقاط رئيسية.\nالنص:\n---\n{text[:10000]}\n---"
        result = await self._process_llm_json_response(prompt, EmotionalArc)
        if result and result.emotional_arc_points:
            return sorted(result.emotional_arc_points, key=lambda p: p.timestamp)
        return []

    def _clean_llm_output(self, raw: str) -> str:
        raw_str = raw.strip()
        if raw_str.startswith("```json"):
            return raw_str[7:-3].strip()
        if raw_str.startswith("```"):
            return raw_str[3:-3].strip()
        return raw_str

    async def _enrich_with_external_context(self, entities: List[Entity], external_sources: Optional[List[str]]) -> Dict[str, Any]:
        if not external_sources:
            return {}
        tasks = [self.web_search_service.search(src) for src in external_sources]
        results = await asyncio.gather(*tasks)
        return dict(zip(external_sources, results))

# --- مثال اختبار ---
async def main_test():
    engine = AdvancedContextEngine()
    sample_text = "في زقاق ضيق من أزقة القاهرة القديمة، وجد علي رسالة غامضة..."
    kb = await engine.analyze_text(sample_text)
    print(kb.json(indent=2, ensure_ascii=False))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main_test())
