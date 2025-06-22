# engines/slang_colloquialism_engine.py (V3 - Live & Targeted)
import logging
from typing import Dict, List, Optional
import asyncio

from ..services.web_search_service import web_search_service
from ..core.llm_service import llm_service

logger = logging.getLogger("SlangEngine")

class SlangAndColloquialismEngine:
    """
    محرك اللهجات العامية الحي (V3).
    يستخدم الكشط الآلي المستهدف لجمع وتحليل المصطلحات الحية.
    """
    def __init__(self):
        self.web_service = web_search_service
        self.cache: Dict[str, Dict] = {} # كاش لتسريع الطلبات المتكررة
        logger.info("✅ Live & Targeted Slang Engine (V3) Initialized.")

    async def get_live_lexicon(self, context_tags: List[str], target_urls: List[str] = None) -> Dict[str, List[str]]:
        """
        الوظيفة الرئيسية: يبحث في مصادر محددة ويستخلص معجماً حياً.
        """
        if not context_tags and not target_urls:
            return {}
        
        cache_key = "_".join(sorted(context_tags))
        if cache_key in self.cache:
            logger.info(f"Returning cached lexicon for: {cache_key}")
            return self.cache[cache_key]
        
        logger.info(f"Performing live scraping for slang related to: {context_tags}")

        # 1. تحديد المصادر
        # في نظام حقيقي، ستكون هناك قاعدة بيانات للمصادر الموثوقة لكل لهجة
        if not target_urls:
            target_urls = [
                "https://www.tunisia-sat.com/forums/threads/4181983/", # مثال لمنتدى تونسي
                # يمكن إضافة روابط لصفحات فيسبوك أو تعليقات يوتيوب هنا
            ]

        # 2. تنفيذ الكشط والتنظيف بشكل متوازٍ
        scraping_tasks = [self.web_service.scrape_and_clean_url(url) for url in target_urls]
        scraped_results = await asyncio.gather(*scraping_tasks)

        # 3. تجميع النصوص النظيفة
        combined_text = ""
        for result in scraped_results:
            if result.get("status") == "success":
                combined_text += result["data"]["cleaned_text"] + "\n\n"

        if not combined_text.strip():
            logger.warning("No text could be scraped from the target URLs.")
            return {}

        # 4. استخلاص المصطلحات باستخدام LLM
        prompt = self._build_extraction_prompt(combined_text, context_tags)
        
        response = await llm_service.generate_json_response(prompt, temperature=0.2)
        if "error" in response:
            logger.error("Failed to extract slang from scraped results.")
            return {}
            
        self.cache[cache_key] = response
        logger.info(f"Successfully generated and cached new lexicon for: {cache_key}")
        return response

    def _build_extraction_prompt(self, text: str, tags: List[str]) -> str:
        return f"""
مهمتك: أنت عالم لغويات اجتماعية وخبير في اللهجة التونسية العامية. لقد تم تزويدك بنص تم تجميعه من منتديات وصفحات تونسية على الإنترنت.

**النص المجمع للتحليل (قد يحتوي على ضوضاء):**
---
{text[:8000]}
---

**المطلوب:**
بناءً على هذا النص، استخلص قائمة من الكلمات والعبارات العامية الأصيلة التي تتناسب مع سياق: '{', '.join(tags)}'.
1.  ركز على الكلمات والعبارات التي تبدو حقيقية، شائعة، وتعبر عن روح الشارع.
2.  صنف المخرجات إلى "أفعال"، "أسماء"، و"تعبيرات شائعة".
3.  أرجع ردك **حصريًا** بتنسيق JSON.

**القاموس العامي المستخلص:**
"""

# إنشاء مثيل وحيد
slang_engine = SlangAndColloquialismEngine()
```**شرح الترقية النهائية:**
-   **الاعتماد على الكشط الآلي:** الدالة الرئيسية `get_live_lexicon` لم تعد تعتمد على قاموس داخلي. الآن، وظيفتها هي استدعاء `web_search_service` لجلب المحتوى **الحقيقي** من روابط محددة.
-   **التخصص:** يمكن الآن توجيه المحرك لكشط مواقع معينة (منتديات، مدونات) للحصول على لهجة دقيقة جدًا.
-   **سير العمل المتكامل:** العملية أصبحت: **تحديد المصادر -> كشط وتنظيف -> تجميع -> استخلاص بالـ LLM**. هذا يحاكي تمامًا عمل الباحث البشري.

---
### **كيف سيغير هذا النتيجة؟**

عندما نطلب من النظام الآن كتابة أغنية راب بأسلوب بلطي، سيقوم `SlangAndColloquialismEngine` بالخطوات التالية قبل أن يكتب `PoemComposerAgent` أي كلمة:
1.  يذهب إلى منتديات مثل `tunisia-sat.com` أو تعليقات على فيديو لبلطي.
2.  يقوم بكشط مئات التعليقات والحوارات الحقيقية.
3.  ينظفها من الضوضاء ("رد مع اقتباس"، إلخ).
4.  يسلم هذا النص النظيف إلى نموذج لغوي مع طلب: "استخلص لي أكثر 20 تعبيرًا عاميًا وحيًا من هذا النص".
5.  القاموس الناتج (الذي قد يحتوي على كلمات مثل "يا غالي"، "يعطيك الصحة"، "صاحبي الباهي"، أو حتى أخطاء إملائية شائعة تستخدم عمدًا) هو ما سيتم استخدامه في كتابة الأغنية.

**النتيجة ستكون نصًا لا "يشبه" اللهجة التونسية فحسب، بل "يتنفسها"**، لأنه مبني على اللغة كما يستخدمها الناس فعليًا في نفس اللحظة.
