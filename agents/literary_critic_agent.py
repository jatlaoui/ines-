# agents/literary_critic_agent.py (النسخة المفعّلة)

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, Tuple

# --- الاستيرادات المحدثة ---
from .base_agent import BaseAgent, AgentState
from core.llm_service import llm_service
# الأدوات المساعدة يمكن تفعيلها لاحقًا إذا كانت مطلوبة
# from ..tools.text_processing_tools import TextProcessor
# from ..tools.analysis_tools import LiteraryAnalyzer, StyleAnalyzer

logger = logging.getLogger(__name__)

# Enum classes can be moved to a shared data_models file later
class CriticismLevel:
    GENTLE = "لطيف"
    CONSTRUCTIVE = "بناء"
    DETAILED = "مفصل"

class LiteraryCriticAgent(BaseAgent):
    """
    وكيل التحرير والنقد الأدبي المتخصص.
    يقوم بتقييم أنواع مختلفة من المحتوى الإبداعي وتقديم ملاحظات بناءة.
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "literary_critic_agent",
            name="الناقد الأدبي",
            description="يقدم نقدًا أدبيًا دقيقًا وبناءً للنصوص والأفكار والمخططات."
        )
        self.criticism_criteria = {
            "idea": ["originality", "feasibility", "engagement_potential", "depth"],
            "blueprint": ["coherence", "pacing", "character_arc_clarity", "plot_strength"],
            "chapter": ["prose_quality", "emotional_impact", "dialogue_realism", "flow"]
        }
        logger.info("LiteraryCriticAgent initialized and connected to the live LLM service.")

    # --- الدوال العامة لواجهة النقد ---
    
    def review_idea(self, idea_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        يراجع فكرة قصة ويعطي تقييمًا وملاحظات.
        (تم تكييفها من `idea_critic_agent.py` الأصلي)
        """
        logger.info(f"Critiquing idea: '{idea_content.get('premise', 'N/A')}'")
        issues: List[str] = []
        score = 10.0

        premise = idea_content.get("premise", "")
        if "تاريخ مزيف" in premise or "اكتشاف سر" in premise:
            score -= 2.0
            issues.append("الفكرة تحتوي على عناصر شائعة (مثل التاريخ المزيف). حاول إيجاد زاوية جديدة.")
        if len(premise.split()) < 10:
            score -= 1.5
            issues.append("الفكرة الأساسية موجزة جدًا وتحتاج إلى تفاصيل أكثر لتحديد إمكانية تطويرها.")
        if "منظمة سرية" not in premise and "مطارد" not in premise:
            score -= 1.0
            issues.append("الفكرة تفتقر إلى عنصر صراع أو تشويق واضح لجذب القارئ.")

        return {
            "overall_score": max(min(score, 10.0), 0.0),
            "issues": issues, # سيتم استخدامها كـ feedback
        }
        
    def review_blueprint(self, blueprint_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        يراجع مخطط قصة (StoryBlueprint) ويعطي تقييمًا.
        (تم تكييفها من `blueprint_critic_agent.py` الأصلي)
        """
        logger.info(f"Critiquing blueprint for: '{blueprint_content.get('introduction', '')[:30]}...'")
        issues: List[str] = []
        score = 10.0

        if not blueprint_content.get("introduction") or len(blueprint_content.get("introduction", "").split()) < 15:
            issues.append("المقدمة قصيرة جدًا أو سطحية.")
            score -= 1.5
        if len(blueprint_content.get("chapters", [])) < 3:
            issues.append("عدد الفصول قليل جدًا (أقل من 3).")
            score -= 2.0
        
        # يمكن إضافة المزيد من الفحوصات هنا

        return {
            "overall_score": score,
            "issues": issues,
        }

    async def review_chapter(self, chapter_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        مراجعة شاملة لفصل مكتوب. تستخدم الـ LLM لتقييم متعدد الأبعاد.
        """
        logger.info(f"Performing comprehensive critique on chapter: '{chapter_content.get('title', 'Untitled')}'")
        text_to_review = chapter_content.get("chapter_content", "")
        if not text_to_review:
            return {"overall_score": 0.0, "issues": ["المحتوى فارغ."]}

        prompt = self._build_critique_prompt(
            text_to_review,
            context=f"هذا الفصل بعنوان '{chapter_content.get('title')}' ويهدف إلى إيصال شعور بـ'{chapter_content.get('emotional_focus', 'N/A')}'."
        )
        
        response = await llm_service.generate_json_response(prompt, temperature=0.4)

        if "error" in response:
            logger.error(f"LLM critique failed: {response.get('details')}")
            # في حالة الفشل، نرجع تقييمًا افتراضيًا
            return {"overall_score": 5.0, "issues": ["فشل الناقد الآلي في تقييم النص."]}
        
        return response

    # --- دالة بناء الـ Prompt ---

    def _build_critique_prompt(self, text_to_review: str, context: str) -> str:
        """
        يبني prompt مفصلاً ليقوم الـ LLM بدور الناقد الأدبي.
        """
        return f"""
مهمتك: أنت ناقد أدبي عربي محترف وخبير. قم بتقييم النص التالي بدقة وموضوعية.
**سياق النص:** {context}

**النص للمراجعة:**
---
{text_to_review}
---

**تعليمات النقد:**
1.  اقرأ النص بعناية.
2.  قم بتقييم النص بناءً على المعايير التالية، مع إعطاء كل معيار درجة من 1 إلى 10.
3.  اكتب نقاط القوة الرئيسية (2-3 نقاط).
4.  اكتب أهم نقاط الضعف التي تحتاج إلى تحسين (2-3 نقاط)، واجعلها ملاحظات قابلة للتنفيذ.
5.  احسب درجة إجمالية (overall_score) كمتوسط لدرجات المعايير.

أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يتبع الرد المخطط التالي تمامًا:
{{
  "scores": {{
    "prose_quality": "float // جودة النثر واللغة والأسلوب.",
    "emotional_impact": "float // مدى قدرة النص على إثارة المشاعر وتحقيق التركيز العاطفي المطلوب.",
    "plot_progression": "float // مدى مساهمة النص في دفع أحداث القصة إلى الأمام.",
    "character_consistency": "float // مدى اتساق تصرفات وأقوال الشخصيات مع ملفاتها المعروفة."
  }},
  "strengths": [
    "string // نقطة قوة واضحة ومحددة.",
    "string // نقطة قوة أخرى."
  ],
  "issues": [
    "string // مشكلة قابلة للتنفيذ (مثال: 'الحوار يبدو جافًا، حاول إضافة المزيد من المشاعر').",
    "string // مشكلة أخرى."
  ],
  "overall_score": "float // المتوسط المحسوب للدرجات في 'scores'."
}}
"""

# --- قسم الاختبار المحدّث ---
async def main_test():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود.")
        return

    critic_agent = LiteraryCriticAgent()
    
    # --- 1. اختبار نقد فكرة ---
    print("\n--- 🧪 TEST 1: Critiquing a story idea ---")
    bad_idea = {"premise": "رجل يكتشف سرا."}
    critique_result = critic_agent.review_idea(bad_idea)
    print(f"Critique for a weak idea: {critique_result}")
    assert critique_result['overall_score'] < 8.0

    good_idea = {"premise": "في عالم صحراوي، تكتشف منظمة سرية أن الماء ليس عنصراً طبيعياً بل هو دم كائن فضائي قديم، ويطاردون آخر شخص يعرف الحقيقة."}
    critique_result = critic_agent.review_idea(good_idea)
    print(f"Critique for a strong idea: {critique_result}")
    assert critique_result['overall_score'] >= 8.0

    # --- 2. اختبار نقد فصل كامل (باستخدام LLM) ---
    print("\n--- 🧪 TEST 2: Critiquing a full chapter via LLM ---")
    sample_chapter_content = {
        "title": "الفصل 1: الرسالة الغامضة",
        "chapter_content": "تحت سماء القاهرة الرمادية، وقف علي يراقب المارة. لم يكن يشعر ببرودة الهواء بقدر ما كان يشعر ببرودة روحه الفارغة. رائحة الشواء المنبعثة من مطعم قريب لم تعد تثير شهيته، بل ذكرته فقط بموائد الطعام الدافئة التي تركها خلفه. أمسك بالرسالة القديمة في جيبه، ملمسها الخشن كان بمثابة مرساة تربطه بعالم يكاد ينساه. كانت غربته صحراء لا تنتهي، وكانت هذه الرسالة بئر الماء الوحيد في أفقه.",
        "emotional_focus": "الغربة"
    }

    try:
        chapter_critique = await critic_agent.review_chapter(sample_chapter_content)
        print("✅ LLM-based critique successful!")
        print(json.dumps(chapter_critique, indent=2, ensure_ascii=False))
        assert "overall_score" in chapter_critique
        assert "issues" in chapter_critique
    except Exception as e:
        print(f"❌ LLM-based critique failed: {e}")

if __name__ == "__main__":
    # هذا الكود الآن يتطلب تعريف الفئة الأساسية BaseAgent بشكل صحيح
    # سنفترض أن `agents/base_agent.py` موجود ويعمل
    asyncio.run(main_test())
