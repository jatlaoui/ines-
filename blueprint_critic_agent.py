# blueprint_critic_agent.py
"""
BlueprintCriticAgent (ناقد المخططات)
الغرض: مراجعة وتقييم المخططات السردية (StoryBlueprints) لضمان جودتها وتماسكها.
"""
from typing import Dict, Any, List
import logging

# استيراد النماذج اللازمة
from blueprint_architect_agent import StoryBlueprint, ChapterOutline

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [BlueprintCritic] - %(levelname)s - %(message)s')
logger = logging.getLogger("BlueprintCriticAgent")

class BlueprintCriticAgent:
    """
    وكيل متخصص في نقد المخططات السردية.
    """
    def __init__(self):
        # يمكن إضافة إعدادات مستقبلية هنا
        logger.info("BlueprintCriticAgent initialized.")
        
    def review_blueprint(self, blueprint: StoryBlueprint) -> Dict[str, Any]:
        """
        يراجع مخطط سردي من نوع StoryBlueprint ويعطي تقييمًا وملاحظات.
        """
        logger.info(f"[BlueprintCritic] Reviewing blueprint for '{blueprint.introduction[:30]}...'")

        issues: List[str] = []
        strengths: List[str] = []

        # 1. تقييم المقدمة
        if not blueprint.introduction or len(blueprint.introduction.split()) < 15:
            issues.append("المقدمة قصيرة جدًا أو سطحية. يجب أن توضح الصراع الرئيسي والشخصيات بشكل أفضل.")
        else:
            strengths.append("المقدمة تضع أساسًا جيدًا للقصة.")

        # 2. تقييم عدد الفصول
        if len(blueprint.chapters) < 3:
            issues.append("عدد الفصول قليل جدًا (أقل من 3). قد تكون الحبكة غير متطورة بما فيه الكفاية.")
        elif len(blueprint.chapters) > 15: # تم تحديثه ليكون أكثر منطقية
             strengths.append(f"هيكل الفصول مفصل ({len(blueprint.chapters)} فصل)، مما يسمح بتطور عميق.")

        # 3. تقييم الفجوات العاطفية
        emotional_gaps = [
            chap.title for chap in blueprint.chapters if "محايد" in chap.emotional_focus
        ]
        if emotional_gaps:
            issues.append(f"الفصول التالية تفتقر إلى تركيز عاطفي واضح: {', '.join(emotional_gaps)}. يجب تحديد المشاعر السائدة.")
        else:
            strengths.append("جميع الفصول لها تركيز عاطفي واضح، مما يعزز رحلة القارئ.")
            
        # 4. تقييم الخاتمة
        if not blueprint.conclusion or len(blueprint.conclusion.split()) < 15:
            issues.append("الخاتمة ضعيفة أو غير موجودة. يجب أن تقدم حلاً مرضيًا للصراع الرئيسي.")
        else:
            strengths.append("الخاتمة تقدم إغلاقًا مناسبًا للقصة.")

        # حساب التقييم بناءً على عدد المشاكل
        # كل مشكلة تقلل التقييم
        score = 9.5 - len(issues) * 1.0 
        score = max(min(score, 10.0), 3.0) # ضمان أن التقييم بين 3 و 9.5

        return {
            "overall_score": score,
            "issues": issues, # سيتم استخدامها كـ feedback
            "strengths": strengths
        }