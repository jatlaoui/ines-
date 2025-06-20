# agents/chapter_composer_agent.py
"""
ChapterComposerAgent (مؤلف الفصول) - الإصدار المحسن
الغرض: تحويل ChapterOutline إلى نثر أدبي غني ومؤثر، معزز بالذاكرة التجريبية الحسية.
"""
import logging
import json
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from engines.sensory_engine import sensory_engine # <-- الإضافة الجديدة: استيراد محرك التمثيلات الحسية
# نفترض أن هذا الملف موجود في المسار الصحيح
from agents.blueprint_architect_agent import ChapterOutline 

logger = logging.getLogger("ChapterComposerAgent")

# --- محاكاة خدمة LLM (للتوضيح فقط) ---
class MockLLMChapterService:
    async def write_chapter(self, prompt: str) -> str:
        # طباعة الـ prompt لنرى كيف تم بناؤه
        print("--- LLM Prompt (ChapterComposer - Enhanced) ---")
        print(prompt)
        print("---------------------------------------------")
        
        # محاكاة لاستجابة تحتوي على فصل مكتوب
        mock_chapter = {
            "content": {
                "chapter_content": "تحت سماء القاهرة الرمادية، وقف علي يراقب المارة. لم يكن يشعر ببرودة الهواء بقدر ما كان يشعر ببرودة روحه الفارغة. رائحة الشواء المنبعثة من مطعم قريب لم تعد تثير شهيته، بل ذكرته فقط بموائد الطعام الدافئة التي تركها خلفه. أمسك بالرسالة القديمة في جيبه، ملمسها الخشن كان بمثابة مرساة تربطه بعالم يكاد ينساه. كانت غربته صحراء لا تنتهي، وكانت هذه الرسالة بئر الماء الوحيد في أفقه.",
                "word_count": 85,
                "quality_score": 9.2,
                "notes": "تم استخدام إرشادات 'الغربة' الحسية بنجاح."
            }
        }
        return json.dumps(mock_chapter, ensure_ascii=False)

class ChapterComposerAgent(BaseAgent):
    """
    وكيل متخصص في كتابة فصول الروايات بناءً على مخططات مفصلة،
    معززة بالذاكرة التجريبية الحسية.
    """
    def __init__(self, agent_id: Optional[str] = None, llm_service=None):
        super().__init__(
            agent_id=agent_id,
            name="مؤلف الفصول الماهر",
            description="يكتب فصولاً روائية عميقة باستخدام خطط مفصلة وذاكرة حسية."
        )
        self.llm = llm_service or MockLLMChapterService()
        self.style_profile = { # يمكن تخصيص هذا لاحقًا
            "sensory_detail": True,
            "symbolism": True,
            "internal_monologue": True,
        }

    async def write_chapter(self, context: Dict[str, Any], feedback: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تكتب فصلًا كاملاً.
        'context' يجب أن يحتوي على كائن 'chapter_outline'.
        """
        chapter_outline = context.get("chapter_outline")
        if not isinstance(chapter_outline, ChapterOutline):
            raise TypeError("A 'ChapterOutline' object is required in the context.")
            
        logger.info(f"Composing chapter: '{chapter_outline.title}'")

        # --- الخطوة 1: بناء Prompt ذكي ومفصل ومعزز ---
        prompt = self._build_chapter_prompt(chapter_outline, feedback)
        
        # --- الخطوة 2: استدعاء LLM لتوليد محتوى الفصل ---
        response_json = await self.llm.write_chapter(prompt)
        
        try:
            # --- الخطوة 3: تحليل وتنظيم المخرجات ---
            result = json.loads(response_json)
            # دمج معلومات المخطط مع النتيجة
            final_result = result.get("content", {})
            final_result['title'] = chapter_outline.title
            final_result['chapter_number'] = int(chapter_outline.title.split()[1].replace(':', ''))
            return {"content": final_result} # تغليف النتيجة لتتوافق مع RefinementService
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing chapter generation response: {e}")
            return {"error": "Failed to parse LLM response for the chapter.", "raw": response_json}

    def _build_chapter_prompt(self, outline: ChapterOutline, feedback: Optional[List[str]] = None) -> str:
        """
        يبني Prompt مفصلاً، معززًا بالتمثيلات الحسية وملاحظات الناقد.
        """
        # تحويل القوائم والقواميس إلى نصوص واضحة
        key_events_str = "\n- ".join(outline.key_events)
        character_arcs_str = "\n- ".join([f"{name}: {arc}" for name, arc in outline.character_arcs.items()])

        # --- الإضافة 1: دمج ملاحظات الناقد (Feedback) ---
        feedback_section = ""
        if feedback:
            feedback_str = "\n- ".join(feedback)
            feedback_section = f"""
            **ملاحظات من المراجعة السابقة (يجب تطبيقها بدقة):**
            - {feedback_str}

            يرجى إعادة كتابة الفصل مع معالجة هذه الملاحظات.
            """

        # --- الإضافة 2: إثراء الـ Prompt بالذاكرة التجريبية ---
        emotional_focus = outline.emotional_focus
        sensory_data = sensory_engine.get_sensory_representation(emotional_focus)
        
        sensory_instructions = ""
        if sensory_data:
            senses_str = "\n- ".join(sensory_data.get("senses", []))
            behaviors_str = "\n- ".join(sensory_data.get("behaviors", []))
            metaphors_str = "\n- ".join(sensory_data.get("metaphors", []))
            
            sensory_instructions = f"""
            **إرشادات حسية وسلوكية (من الذاكرة التجريبية):**
            للتعبير عن شعور '{emotional_focus}'، لا تقل "شعر بـ{emotional_focus}" مباشرة، بل أظهر ذلك من خلال:

            *   **الوصف الحسي (استلهم من هذه الصور، لا تنسخها حرفيًا):**
                - {senses_str}

            *   **السلوكيات (اجعل الشخصية تقوم بهذه الأفعال لتعكس مشاعرها):**
                - {behaviors_str}
            
            *   **الاستعارات (استخدم تشبيهات قوية مثل هذه):**
                - {metaphors_str}
            """

        # --- بناء الـ Prompt النهائي ---
        full_prompt = f"""
        مهمتك: أنت روائي عربي محترف وخبير في أسلوب الجطلاوي. اكتب الفصل التالي من الرواية بدقة وإبداع، بناءً على المواصفات التالية.

        **عنوان الفصل:** {outline.title}

        **ملخص الفصل:**
        {outline.summary}

        **التركيز العاطفي:**
        {outline.emotional_focus}

        **الأحداث الرئيسية التي يجب أن تحدث في هذا الفصل:**
        - {key_events_str}

        **تطور الشخصيات في هذا الفصل:**
        - {character_arcs_str}

        {feedback_section}

        {sensory_instructions}

        **تعليمات الكتابة النهائية:**
        1.  ابدأ الفصل بمشهد قوي وجذاب يغمر القارئ في الأجواء الحسية.
        2.  تأكد من تغطية جميع الأحداث الرئيسية المذكورة في المخطط.
        3.  أظهر تطور الشخصيات ومشاعرها من خلال أفعالها وحواراتها الداخلية، وليس فقط من خلال السرد المباشر.
        4.  التزم بالمسار العاطفي المحدد للفصل بدقة.
        5.  اكتب بأسلوب أدبي غني ومؤثر، مستلهمًا من الإرشادات الحسية والسلوكية.
        6.  انهِ الفصل بطريقة تثير فضول القارئ للفصل التالي.

        أرجع الإجابة **حصريًا** بتنسيق JSON. يجب أن يحتوي الكائن على مفتاح واحد هو "content"، وقيمته كائن يتبع الهيكل التالي:
        - "chapter_content": (string) المحتوى الكامل للفصل كنص واحد.
        - "word_count": (integer) العدد الفعلي للكلمات في المحتوى.
        - "quality_score": (float) تقييمك لجودة الفصل الذي كتبته (من 0.0 إلى 10.0).
        - "notes": (string) ملاحظة قصيرة حول كيفية تطبيق الإرشادات الحسية.
        """
        return full_prompt.strip()

# --- مثال اختبار ---
async def main_test():
    from agents.blueprint_architect_agent import ChapterOutline # للتوافق

    # 1. محاكاة مخطط فصل تم إنتاجه بواسطة BlueprintArchitectAgent
    sample_chapter_outline = ChapterOutline(
        title="الفصل 1: الرسالة الغامضة",
        summary="يجد البطل 'علي' رسالة قديمة من جده في القاهرة، مما يطلق شرارة الأحداث التي تدفعه للبحث عن ماضيه.",
        emotional_focus="الغربة", # <-- نستخدم مفهوماً موجوداً في الذاكرة الحسية
        key_events=["علي يجد الرسالة", "علي يقرر فك شفرة الرسالة"],
        character_arcs={"علي": "ينتقل من حالة الركود والضياع إلى امتلاك هدف جديد ومحفوف بالمخاطر."}
    )
    
    # 2. إنشاء وكيل مؤلف الفصول
    composer_agent = ChapterComposerAgent()
    
    # 3. كتابة الفصل
    print("--- بدء كتابة الفصل 1 مع تعزيز حسي ---")
    generated_chapter_data = await composer_agent.write_chapter(context={"chapter_outline": sample_chapter_outline})
    
    # 4. عرض النتائج
    print("\n--- ✅ الفصل تم إنتاجه بنجاح ---")
    print(json.dumps(generated_chapter_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    from agents.base_agent import BaseAgent # للتوافق
    asyncio.run(main_test())
