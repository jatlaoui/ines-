# agents/chapter_composer_agent.py (النسخة المفعّلة)

import logging
import json
from typing import Dict, Any, Optional, List

# --- الاستيرادات المحدثة ---
from .base_agent import BaseAgent
from core.llm_service import llm_service             # <-- الخدمة الحقيقية
from engines.sensory_engine import sensory_engine      # <-- محرك الذاكرة الحسية
# استيراد نماذج البيانات من مكانها الصحيح
try:
    # محاولة الاستيراد من المسار المتوقع في الهيكل الكامل
    from data_models.story_elements import ChapterOutline
except ImportError:
    # استيراد بديل للاختبار المستقل
    from agents.blueprint_architect_agent import ChapterOutline

logger = logging.getLogger(__name__)

class ChapterComposerAgent(BaseAgent):
    """
    وكيل متخصص في كتابة فصول الروايات بناءً على مخططات مفصلة،
    معززة بالذاكرة التجريبية الحسية وباستخدام خدمة LLM حقيقية.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "chapter_composer_agent",
            name="مؤلف الفصول الماهر",
            description="يكتب فصولاً روائية عميقة باستخدام خطط مفصلة وذاكرة حسية."
        )
        # لم نعد بحاجة إلى llm_service في التهيئة
        self.style_profile = {
            "sensory_detail": True,
            "symbolism": True,
            "internal_monologue": True,
        }
        logger.info("ChapterComposerAgent initialized and connected to the live LLM service.")

    async def write_chapter(self, context: Dict[str, Any], feedback: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تكتب فصلًا كاملاً.
        'context' يجب أن يحتوي على كائن 'chapter_outline'.
        """
        chapter_outline = context.get("chapter_outline")
        if not isinstance(chapter_outline, ChapterOutline):
            raise TypeError("A 'ChapterOutline' object is required in the context.")
            
        logger.info(f"Composing chapter: '{chapter_outline.title}'...")

        # --- الخطوة 1: بناء Prompt ذكي ومفصل ومعزز ---
        prompt = self._build_chapter_prompt(chapter_outline, feedback)
        
        # --- الخطوة 2: استدعاء LLM الحقيقي لتوليد محتوى الفصل ---
        response_data = await llm_service.generate_json_response(prompt, temperature=0.7)
        
        # --- الخطوة 3: تحليل وتنظيم المخرجات ---
        if "error" in response_data:
            logger.error(f"LLM call failed for chapter composition. Details: {response_data.get('details')}")
            return {"status": "error", "message": "Failed to get chapter content from LLM.", "raw": response_data}

        # الرد من llm_service هو بالفعل JSON، لذا لا داعي لـ json.loads
        # نتوقع أن يكون الرد مطابقًا للمخطط الذي طلبناه في الـ prompt
        chapter_content = response_data

        try:
            # دمج معلومات المخطط مع النتيجة
            chapter_content['title'] = chapter_outline.title
            chapter_content['chapter_number'] = int(re.search(r'\d+', chapter_outline.title).group())
            
            logger.info(f"Successfully composed and parsed chapter '{chapter_outline.title}'.")
            # تغليف النتيجة لتتوافق مع RefinementService
            return {"status": "success", "content": chapter_content} 
        except (KeyError, TypeError, AttributeError) as e:
            logger.error(f"Error processing chapter data: {e}. Received data: {chapter_content}")
            return {"status": "error", "message": "LLM response structure is invalid.", "raw": chapter_content}

    def _build_chapter_prompt(self, outline: ChapterOutline, feedback: Optional[List[str]] = None) -> str:
        """
        يبني Prompt مفصلاً، معززًا بالتمثيلات الحسية وملاحظات الناقد.
        محسن لـ Gemini API.
        """
        key_events_str = "\n- ".join(outline.key_events)
        character_arcs_str = "\n- ".join([f"{name}: {arc}" for name, arc in outline.character_arcs.items()])

        feedback_section = ""
        if feedback:
            feedback_str = "\n- ".join(feedback)
            feedback_section = f"""
**ملاحظات من المراجعة السابقة (يجب تطبيقها بدقة):**
- {feedback_str}
"""
        # استخدام محرك الذاكرة الحسية
        emotional_focus = outline.emotional_focus
        sensory_data = sensory_engine.get_sensory_representation(emotional_focus)
        
        sensory_instructions = ""
        if sensory_data:
            senses_str = "\n- ".join(sensory_data.get("senses", []))
            behaviors_str = "\n- ".join(sensory_data.get("behaviors", []))
            metaphors_str = "\n- ".join(sensory_data.get("metaphors", []))
            
            sensory_instructions = f"""
**إرشادات حسية (Show, Don't Tell):** للتعبير عن شعور '{emotional_focus}'، لا تقل "شعر بـ{emotional_focus}" مباشرة، بل أظهره من خلال:
*   **الوصف الحسي (استلهم من هذه الصور):**
    - {senses_str}
*   **السلوكيات (اجعل الشخصية تتصرف هكذا):**
    - {behaviors_str}
*   **الاستعارات (استخدم تشبيهات قوية كهذه):**
    - {metaphors_str}
"""
        # --- بناء الـ Prompt النهائي ---
        return f"""
مهمتك: أنت روائي عربي محترف وخبير في أسلوب الكتابة الأدبي العميق والمؤثر. اكتب الفصل التالي من الرواية بدقة وإبداع، بناءً على المواصفات التالية.
يجب أن يكون ردك **حصريًا** بتنسيق JSON صالح، بدون أي نص تمهيدي أو ملاحظات إضافية.

**مواصفات الفصل المطلوب:**
- **عنوان الفصل:** {outline.title}
- **ملخص الفصل:** {outline.summary}
- **التركيز العاطفي الأساسي:** {outline.emotional_focus}
- **الأحداث الرئيسية التي يجب أن تقع:**
  - {key_events_str}
- **تطور الشخصيات في هذا الفصل:**
  - {character_arcs_str}
{feedback_section}
{sensory_instructions}

**تعليمات الكتابة النهائية:**
1.  ابدأ الفصل بمشهد قوي وجذاب يغمر القارئ في الأجواء الحسية.
2.  تأكد من تغطية جميع الأحداث الرئيسية وتطورات الشخصيات المذكورة.
3.  أظهر مشاعر الشخصيات من خلال أفعالها وحواراتها الداخلية، وليس فقط من خلال السرد المباشر.
4.  انهِ الفصل بطريقة مشوقة تثير فضول القارئ للفصل التالي.
5.  اكتب بأسلوب أدبي غني ومؤثر.

**مخطط JSON المطلوب (Schema):**
{{
  "chapter_content": "string // المحتوى الكامل للفصل كنص واحد متدفق.",
  "word_count": "integer // العدد الفعلي للكلمات في المحتوى.",
  "quality_score": "float // تقييمك الذاتي لجودة الفصل الذي كتبته (من 0.0 إلى 10.0).",
  "notes": "string // ملاحظة قصيرة حول كيفية تطبيق الإرشادات الحسية أو أي تحد واجهته."
}}
"""

# --- قسم الاختبار المحدّث ---
async def main_test():
    import os
    import re
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود. يرجى إضافته في ملف .env")
        return

    # 1. محاكاة مخطط فصل
    sample_chapter_outline = ChapterOutline(
        title="الفصل 1: الرسالة الغامضة",
        summary="يجد البطل 'علي' رسالة قديمة من جده في القاهرة، مما يطلق شرارة الأحداث التي تدفعه للبحث عن ماضيه.",
        emotional_focus="الغربة", 
        key_events=["علي يجد الرسالة في صندوق خشبي قديم.", "علي يقرر فك شفرة الرسالة مهما كلف الأمر."],
        character_arcs={"علي": "ينتقل من حالة الركود والضياع إلى امتلاك هدف جديد ومحفوف بالمخاطر."}
    )
    
    composer_agent = ChapterComposerAgent()
    
    print(f"--- 🧪 بدء اختبار كتابة الفصل '{sample_chapter_outline.title}' مع اتصال LLM حقيقي... ---")
    
    result = await composer_agent.write_chapter(context={"chapter_outline": sample_chapter_outline})
    
    if result.get("status") == "success":
        print("\n--- ✅ الفصل تم إنتاجه بنجاح ---")
        final_content = result.get("content", {})
        print(json.dumps(final_content, indent=2, ensure_ascii=False))
        # print("\n--- محتوى الفصل ---")
        # print(final_content.get("chapter_content"))
    else:
        print("\n--- ❌ فشل إنتاج الفصل ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main_test())
