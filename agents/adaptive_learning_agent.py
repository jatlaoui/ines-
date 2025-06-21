# agents/adaptive_learning_agent.py
import logging
from typing import Dict, Any, List, Optional
from difflib import ndiff
from .base_agent import BaseAgent

logger = logging.getLogger("AdaptiveLearningAgent")

class AdaptiveLearningAgent(BaseAgent):
    """
    وكيل متخصص في التعلم من تعديلات المستخدم لتخصيص تجربة الكتابة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "adaptive_learning_agent",
            name="المتعلم التكيفي",
            description="يتعلم من أسلوب المستخدم ويخصص مخرجات النظام."
        )
        # سيتم تخزين ملفات تعريف المستخدمين في قاعدة البيانات الرئيسية
        # هنا سنحاكيها في الذاكرة
        self.user_style_profiles: Dict[str, Dict[str, Any]] = {}
        logger.info("✅ Adaptive Learning Agent initialized.")

    def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """الحصول على ملف تعريف المستخدم أو إنشاؤه."""
        if user_id not in self.user_style_profiles:
            self.user_style_profiles[user_id] = {
                "sentence_length_preference": "medium", # short, medium, long
                "vocabulary_preference": "balanced",  # simple, balanced, rich
                "preferred_verbs": [],
                "preferred_adjectives": []
            }
        return self.user_style_profiles[user_id]

    async def analyze_user_edit(self, user_id: str, original_text: str, edited_text: str):
        """
        يحلل الفرق بين النص الأصلي والمعدل لتحديث ملف تعريف أسلوب المستخدم.
        """
        profile = self._get_user_profile(user_id)
        
        # 1. تحليل طول الجمل
        original_avg_len = np.mean([len(s.split()) for s in original_text.split('.')])
        edited_avg_len = np.mean([len(s.split()) for s in edited_text.split('.')])

        if edited_avg_len < original_avg_len * 0.8:
            profile["sentence_length_preference"] = "short"
        elif edited_avg_len > original_avg_len * 1.2:
            profile["sentence_length_preference"] = "long"
        
        # 2. تحليل الكلمات المضافة والمحذوفة
        diff = ndiff(original_text.split(), edited_text.split())
        added_words = [d[2:] for d in diff if d.startswith('+ ')]

        # يمكن هنا تحليل أنواع الكلمات المضافة (صفات، أفعال) لتحديد تفضيلات المفردات
        # هذا مجرد مثال بسيط
        if len(added_words) > 5:
            profile["vocabulary_preference"] = "rich"
        
        logger.info(f"User '{user_id}' profile updated based on edit analysis.")
        # في نظام حقيقي، سيتم حفظ هذا التحديث في core_database
        self.user_style_profiles[user_id] = profile

    async def get_style_directives(self, user_id: str) -> List[str]:
        """
        ترجمة ملف تعريف المستخدم إلى توجيهات واضحة لوكلاء الكتابة.
        """
        profile = self._get_user_profile(user_id)
        directives = ["Write in literary Arabic."]

        if profile["sentence_length_preference"] == "short":
            directives.append("Use short, impactful sentences.")
        elif profile["sentence_length_preference"] == "long":
            directives.append("Use longer, more descriptive sentences.")
        
        if profile["vocabulary_preference"] == "rich":
            directives.append("Employ a rich and varied vocabulary.")
        elif profile["vocabulary_preference"] == "simple":
            directives.append("Use clear and simple vocabulary.")
            
        return directives

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """معالجة مهام التعلم."""
        task_type = context.get("type")
        user_id = context.get("user_id")

        if not user_id:
            return {"status": "error", "message": "User ID is required."}

        if task_type == "analyze_edit":
            await self.analyze_user_edit(user_id, context["original_text"], context["edited_text"])
            return {"status": "success", "message": "User profile updated."}
        elif task_type == "get_directives":
            directives = await self.get_style_directives(user_id)
            return {"status": "success", "directives": directives}
        
        return {"status": "error", "message": f"Unknown task type: {task_type}"}

# إنشاء مثيل وحيد
adaptive_learner = AdaptiveLearningAgent()
