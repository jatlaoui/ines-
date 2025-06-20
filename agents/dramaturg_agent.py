# agents/dramaturg_agent.py
"""
DramaturgAgent (وكيل البناء الدرامي)
يقوم بتحويل فكرة أولية إلى مخطط درامي متكامل للمسرحيات.
"""
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent

logger = logging.getLogger("DramaturgAgent")

class DramaturgAgent(BaseAgent):
    """
    وكيل متخصص في تصميم الهيكل الدرامي للمسرحيات.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="الكاتب الدرامي (Dramaturg)",
            description="يصمم الهيكل العام للمسرحية، الفصول، والصراع المركزي."
        )

    async def generate_dramatic_blueprint(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يأخذ فكرة أولية وينتج "مخططًا دراميًا".
        """
        initial_idea = context.get("idea")
        if not initial_idea:
            raise ValueError("الفكرة الأولية مطلوبة لبناء المخطط الدرامي.")
            
        logger.info(f"Generating dramatic blueprint for idea: '{initial_idea.get('premise')}'")

        # محاكاة لعملية بناء المخطط باستخدام LLM
        # الـ Prompt سيطلب من النموذج تحديد البنية ثلاثية الفصول، الرمز، والسؤال الدرامي
        
        dramatic_blueprint = {
            "title": initial_idea.get("title", "مسرحية بدون عنوان"),
            "dramatic_question": "من سيملأ الفراغ الذي تركه غياب السلطة الأخلاقية، وهل هذا الفراغ يجب أن يُملأ أصلاً؟",
            "central_symbol": "الكرسي الفارغ: يرمز للسلطة، المسؤولية، والفراغ القيمي.",
            "acts": [
                {
                    "act_number": 1,
                    "title": "الفصل الأول: الفراغ",
                    "summary": "تقديم الشخصيات والصراع الأولي بعد حدث جلل (موت العمدة). يتم تعريف رؤى كل من 'الهادي' (الحداثة المادية) و 'مبروك' (التقاليد).",
                    "key_events": ["الإعلان عن موت العمدة", "أول مواجهة فكرية بين الهادي ومبروك", "ظهور الكرسي الفارغ كرمز مركزي."]
                },
                {
                    "act_number": 2,
                    "title": "الفصل الثاني: الانتهازيون",
                    "summary": "تصاعد الصراع بدخول أطراف خارجية (فتحي والمعتمد) تستغل الموقف لمصالحها. تضع الشخصيات الرئيسية في مواجهة 'نقطة اللاعودة'.",
                    "key_events": ["وصول فتحي وعرضه المغري", "قرار المعتمد الذي يصب في مصلحة الهادي", "مبروك يشعر بالعزلة والخذلان."]
                },
                {
                    "act_number": 3,
                    "title": "الفصل الثالث: الكلمة الأخيرة",
                    "summary": "الوصول إلى الذروة حيث يتم الكشف عن النوايا الحقيقية. كلمة شخصية حكيمة (عزيزة) تعيد تعريف معنى 'الكرسي' والصراع بأكمله. الخاتمة تترك الجمهور مع سؤال تأملي.",
                    "key_events": ["المواجهة النهائية بين جميع الأطراف", "كلمة عزيزة التي تغير منظور الجميع", "المشهد الأخير: تغطية الكرسي بقماش أبيض."]
                }
            ]
        }
        
        return {
            "content": dramatic_blueprint,
            "summary": "تم إنشاء مخطط درامي متكامل ثلاثي الفصول."
        }
