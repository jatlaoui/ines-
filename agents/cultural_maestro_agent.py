# agents/cultural_maestro_agent.py (V2 - The Cultural Diplomat)
import logging
import random
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("CulturalMaestroAgent")

class CulturalMaestroAgent(BaseAgent):
    """
    وكيل الخبير الثقافي المتكيف (V2).
    يضمن الأصالة الثقافية ويوظف التراث بطريقة معاصرة ومبدعة،
    مع القدرة على التكيف الآلي مع سياقات ثقافية متعددة (تونسي، سعودي، مصري، إلخ).
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "cultural_maestro_agent",
            name="الخبير الثقافي المتكيف",
            description="يُثري النصوص بلمسات ثقافية أصيلة بناءً على سياق محدد (تونسي، سعودي، مصري، إلخ)."
        )
        # [جديد] تحميل مكتبة ثقافية شاملة بدلاً من مكتبة واحدة
        self.cultural_knowledge_base = self._load_cultural_libraries()
        logger.info("✅ CulturalMaestroAgent V2 (Cultural Diplomat) Initialized with Multi-Cultural Knowledge Base.")

    def _load_cultural_libraries(self) -> Dict[str, Dict[str, List[str]]]:
        """
        [جديد] تحميل مكتبات ثقافية متعددة. في نظام حقيقي، ستكون هذه في قاعدة بيانات
        أو ملفات تكوين منفصلة لسهولة إدارتها وتوسيعها.
        """
        return {
            "tunisian": {
                "proverbs": ["اللي يده في الماء موش كي اللي يده في النار.", "اخدم يا صغري على كبري.", "ما يعرف قيمة الحاجة كان فاقدها."],
                "sensory_details": ["رائحة الياسمين في الليل", "صوت فناجين القهوة على صينية نحاسية", "ضجيج أسواق المدينة العتيقة"],
                "social_customs": ["الخطبة قبل الزواج", "احترام الكبير في المجلس", "عادات القهوة التركي"],
                "historical_figures": ["حنبعل", "ابن خلدون", "الحبيب بورقيبة", "الكاهنة ديهيا"]
            },
            "saudi": {
                "proverbs": ["ما كل أبيض شحم ولا كل أسود فحم.", "مد رجولك على قد لحافك.", "اللي ما يعرف الصقر يشويه."],
                "sensory_details": ["رائحة الهيل في القهوة العربية", "صوت حبات المسبحة في يد رجل كبير", "هدوء الصحراء عند الفجر"],
                "social_customs": ["تقديم القهوة للضيف باليد اليمنى", "عزائم العشاء الكبيرة (الولائم)", "لبس الشماغ والبشت في المناسبات الرسمية"],
                "historical_figures": ["الملك عبدالعزيز آل سعود", "عنترة بن شداد", "الزير سالم"]
            },
            "egyptian": {
                "proverbs": ["ادي العيش لخبازه ولو ياكل نصه.", "ابن الوز عوام.", "القرد في عين أمه غزال."],
                "sensory_details": ["صوت أبواق السيارات في القاهرة", "رائحة الفول المدمس من عربة في الشارع صباحًا", "ضجيج وتفاعل الناس على كوبري قصر النيل"],
                "social_customs": ["التجمعات على المقاهي الشعبية ولعب الطاولة", "الفصال عند الشراء", "روح الدعابة والنكتة في الحوار اليومي"],
                "historical_figures": ["صلاح الدين الأيوبي", "نجيب محفوظ", "أم كلثوم", "أحمد زويل"]
            }
        }

    async def enrich_text_dynamically(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [مُحدَّث] الوظيفة الرئيسية: تأخذ نصًا خامًا وتثريه بلمسات ثقافية بناءً على سياق محدد.
        'context' يجب أن يحتوي على:
        - 'text_content': النص للمراجعة.
        - 'cultural_context_id': معرف السياق الثقافي (e.g., "tunisian", "saudi", "egyptian").
        """
        text_content = context.get("text_content")
        cultural_id = context.get("cultural_context_id", "tunisian").lower()

        if not text_content:
            return {"status": "error", "message": "Text content is required for enrichment."}
        
        # [جديد] اختيار المكتبة الثقافية المناسبة أو العودة إلى الافتراضي
        cultural_library = self.cultural_knowledge_base.get(cultural_id)
        if not cultural_library:
            logger.warning(f"Cultural context '{cultural_id}' not found. Using 'tunisian' as default.")
            cultural_library = self.cultural_knowledge_base.get("tunisian")
            
        logger.info(f"Enriching text with DYNAMIC cultural context: '{cultural_id}'...")
        
        # [جديد] بناء prompt يأخذ المكتبة الثقافية المحددة كمرجع
        prompt = self._build_dynamic_enrichment_prompt(text_content, cultural_id, cultural_library)
        
        response = await llm_service.generate_json_response(prompt, temperature=0.6)
        
        if "error" in response:
            logger.error(f"LLM call failed for cultural enrichment. Details: {response.get('details')}")
            return {"status": "error", "message": "LLM call failed"}

        return {
            "status": "success",
            "content": response,
            "summary": f"Text enriched successfully with '{cultural_id}' context."
        }

    def _build_dynamic_enrichment_prompt(self, text: str, culture_id: str, library: Dict) -> str:
        """
        [مُحدَّث] يبني prompt ديناميكيًا، ويزود الـ LLM بأمثلة حقيقية من الثقافة المستهدفة.
        """
        # اختيار عينات عشوائية وحية من المكتبة لتوجيه الـ LLM
        proverbs_sample = random.sample(library["proverbs"], min(len(library["proverbs"]), 2))
        sensory_sample = random.sample(library["sensory_details"], min(len(library["sensory_details"]), 2))
        customs_sample = random.sample(library["social_customs"], min(len(library["social_customs"]), 2))
        
        culture_name_map = {"tunisian": "التونسية", "saudi": "السعودية", "egyptian": "المصرية"}
        culture_name = culture_name_map.get(culture_id, culture_id.title())

        return f"""
مهمتك: أنت كاتب ومحرر أدبي، متخصص وخبير في **الثقافة {culture_name}** وتفاصيلها الدقيقة.
مهمتك هي مراجعة النص التالي وإثرائه بلمسات ثقافية أصيلة لجعله ينبض بالحياة ويعكس روح المكان.

**السياق الثقافي المطلوب:** {culture_name}

**مراجع ثقافية للإلهام (من صميم ثقافة {culture_name}):**
- **أمثال شعبية:** "{'"، "'.join(proverbs_sample)}"
- **تفاصيل حسية:** "{'"، "'.join(sensory_sample)}"
- **عادات اجتماعية:** "{'"، "'.join(customs_sample)}"

**النص الأصلي للمراجعة والإثراء:**
---
{text}
---

**التحسينات المطلوبة:**
1.  **اللهجة والحوار:** عدّل الحوار ليبدو طبيعيًا وأصيلاً ضمن اللهجة المطلوبة.
2.  **دمج الأمثال:** إذا كان السياق يسمح، ادمج بذكاء مثلًا شعبيًا أو تعبيرًا تراثيًا لتعميق المعنى.
3.  **الوصف الحسي:** أضف تفاصيل حسية (روائح، أصوات، مشاهد) فريدة من نوعها وتعكس البيئة المحددة.
4.  **السلوك الاجتماعي:** تأكد من أن سلوك الشخصيات يتوافق مع الأعراف الاجتماعية للسياق المحدد.

أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يتبع الرد المخطط التالي تمامًا:
{{
  "enriched_text": "string // النص الكامل بعد إثرائه باللمسات الثقافية الـ{culture_name}.",
  "added_elements": [
    {{
      "type": "string // نوع العنصر المضاف (مثال: 'تعديل لهجة'، 'مثل شعبي'، 'وصف حسي').",
      "content": "string // العنصر أو الجملة التي تمت إضافتها أو تعديلها.",
      "justification": "string // لماذا تم اختيار هذا العنصر وما القيمة التي يضيفها للنص."
    }}
  ]
}}
"""
        
    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """معالج المهام المحدث."""
        return await self.enrich_text_dynamically(context)

# إنشاء مثيل وحيد
cultural_maestro_agent = CulturalMaestroAgent()
