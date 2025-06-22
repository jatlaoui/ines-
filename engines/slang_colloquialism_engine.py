# engines/slang_colloquialism_engine.py (V2 - Live Search & Extraction)
import logging
from typing import Dict, List, Optional
import asyncio

# سنحتاج إلى خدمة بحث ويب، يمكننا استخدام واحدة موجودة أو تصميمها
from ..services.web_search_service import web_inspiration_service # نفترض وجود خدمة بحث
from ..core.llm_service import llm_service

logger = logging.getLogger("SlangEngine")

class SlangAndColloquialismEngine:
    """
    محرك اللهجات العامية الحي (V2).
    يستخدم البحث في الويب لاستخلاص أحدث المصطلحات والعبارات العامية.
    """
    def __init__(self):
        self.web_search_service = web_inspiration_service
        self.cache: Dict[str, Dict] = {} # كاش بسيط لتجنب البحث المتكرر
        logger.info("✅ Live Slang & Colloquialism Engine (V2) Initialized.")

    async def get_live_lexicon(self, context_tags: List[str]) -> Dict[str, List[str]]:
        """
        الوظيفة الرئيسية: يبحث عن مصطلحات عامية حية بناءً على وسوم السياق.
        """
        if not context_tags:
            return {}
        
        cache_key = "_".join(sorted(context_tags))
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        logger.info(f"Performing live search for slang related to: {context_tags}")
        
        # 1. بناء استعلامات البحث
        search_queries = [f"كلمات أغاني {tag}" for tag in context_tags] + \
                         [f"مصطلحات عامية {tag}" for tag in context_tags]
        
        # 2. تنفيذ البحث (محاكاة لاستدعاءات متوازية)
        search_results = []
        # في نظام حقيقي، سنقوم بالبحث في الويب فعلياً
        # هنا سنحاكي النتائج
        await asyncio.sleep(1) # محاكاة للبحث
        if "راب تونسي" in context_tags:
            search_results.append("النص المستخرج من بحث الويب: الدنيا كاسحة، يعطيه على راسو، طايح أكثر من النايض...")

        if not search_results:
            return {}

        # 3. استخلاص المصطلحات باستخدام LLM
        combined_results = "\n---\n".join(search_results)
        prompt = self._build_extraction_prompt(combined_results, context_tags)
        
        response = await llm_service.generate_json_response(prompt, temperature=0.2)
        if "error" in response:
            logger.error("Failed to extract slang from search results.")
            return {}
            
        self.cache[cache_key] = response
        return response

    def _build_extraction_prompt(self, text: str, tags: List[str]) -> str:
        return f"""
مهمتك: أنت لغوي وخبير في اللهجات العامية. من النص التالي الذي تم تجميعه من الإنترنت، استخلص قائمة من الكلمات والعبارات العامية الأصيلة التي تتناسب مع السياق: '{', '.join(tags)}'.

**النص للتحليل:**
---
{text[:4000]}
---

**التعليمات:**
1.  ركز على الكلمات والعبارات التي تبدو حقيقية ومستخدمة بكثرة.
2.  صنف المخرجات إلى "أفعال"، "أسماء"، و"تعبيرات".
3.  أرجع ردك **حصريًا** بتنسيق JSON.

**مثال على المخرج:**
{{
  "verbs": ["يحرق", "يكلّش"],
  "nouns": ["الحومة", "الباطيندة"],
  "expressions": ["الدنيا كاسحة", "يعطيه على راسو"]
}}

**القاموس المستخلص:**
"""

# إنشاء مثيل وحيد
slang_engine = SlangAndColloquialismEngine()
