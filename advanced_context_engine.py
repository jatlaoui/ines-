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

# --- نماذج Pydantic (محسنة) ---
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
    source: str  # ID of the source entity
    target: str  # ID of the target entity
    relation: str

class EmotionalArcPoint(BaseModel):
    timestamp: int
    emotion: str
    intensity: float

class KnowledgeBase(BaseModel):
    entities: List[Entity]
    relationship_graph: List[Relationship]
    emotional_arc: List[EmotionalArcPoint]
    historical_context: Dict[str, Any]

# --- خدمات الـ LLM ومحاكاة الاستدعاء ---
class GeminiService:
    async def generate_content(self, prompt: str) -> str:
        # محاكاة استجابة من LLM بتنسيق JSON
        # ستُستبدل هذه الوظيفة باستدعاء API حقيقي لـ LLM
        print(f"--- LLM Prompt (extract_entities) ---\n{prompt[:600]}...\n---------------------------------")
        mock_response = {"entities": []}
        return json.dumps(mock_response, ensure_ascii=False)

class WebSearchService:
    async def search(self, query: str) -> Any:
        return {}

# --- المحرك المتقدم ---
class AdvancedContextEngine:
    """بناء قاعدة معرفة غنية من النص المدخل"""
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
        """استدعاء LLM وتنظيف والتحقق من الصحة."""
        response = await self.gemini_service.generate_content(prompt)
        try:
            json_str = self._clean_llm_output(response)
            return model.parse_raw(json_str)
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error parsing LLM response: {e}\nRaw: {response[:500]}")
            raise

    async def _extract_advanced_entities(self, text: str) -> List[Entity]:
        """
        استخراج متقدم للكيانات مع تحليل عميق باستخدام Prompt مصمم بعناية.
        """
        prompt = f"""
        مهمتك: تحليل النص التالي واستخراج الكيانات الأكثر أهمية.
        لكل كيان، حدد: name, type (character/event/location/concept/object), description (جملة واحدة), importance_score (0.0-10.0), context.
        أرجع JSON جذري بمفتاح واحد 'entities' وهو قائمة الكيانات.
        مثال:
        {{
          "entities": [
            {{ "name":"علي","type":"character","description":"شاب طموح.","importance_score":8.5,
              "context":{{"role_in_text":"البطل","cultural_significance":"رمز للشباب.","historical_period":"معاصر"}}
            }}
          ]
        }}
        النص:
        ---
        {text[:10000]}
        ---
        """
        result = await self._process_llm_json_response(prompt, EntityList)
        return result.entities

    async def _analyze_events_with_causality(self, text: str, entities: List[Entity]) -> List[Relationship]:
        print("Warning: events analysis not implemented.")
        return []

    async def _analyze_characters_psychological(self, text: str, entities: List[Entity]) -> List[Relationship]:
        print("Warning: characters analysis not implemented.")
        return []

    async def _analyze_emotional_arc(self, text: str) -> List[EmotionalArcPoint]:
        print("Warning: emotional arc analysis not implemented.")
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
