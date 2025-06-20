# apollo_orchestrator.py (الإصدار المحدث مع Task Registry و run_task)
import asyncio
import logging
from typing import Any, Dict, List, Optional

# استيراد الوكلاء والخدمات
from blueprint_architect_agent import BlueprintArchitectAgent # مثال
from chapter_composer_agent import ChapterComposerAgent
from literary_critic_agent import LiteraryCriticAgent
# ... استيراد بقية الوكلاء

from refinement_service import RefinementService

# ... (بقية الكود الأساسي لـ ApolloOrchestrator كما هو) ...

class ApolloOrchestrator:
    def __init__(self):
        # ... (نفس التهيئة السابقة) ...
        
        # --- الخطوة 2.1: بناء سجل المهام (Task Registry) ---
        self._task_registry = self._build_task_registry()
        logger.info(f"Task Registry initialized with {len(self._task_registry)} tasks.")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """
        يبني ويهيئ سجل المهام الذي يربط كل مهمة بوكلائها.
        """
        # إنشاء مثيلات من الوكلاء لاستخدامها في السجل
        # في نظام حقيقي، قد يتم حقن هذه التبعيات (Dependency Injection)
        chapter_composer = ChapterComposerAgent()
        literary_critic = LiteraryCriticAgent()
        blueprint_architect = BlueprintArchitectAgent(kb={}) # يحتاج kb وهمية للتهيئة
        # blueprint_critic = BlueprintCriticAgent() # وكيل ناقد للمخططات (سيتم بناؤه لاحقًا)

        return {
            "generate_chapter": {
                "description": "كتابة فصل روائي كامل مع مراجعته.",
                "creator_agent": chapter_composer,
                "creator_fn_name": "write_chapter", # اسم الدالة داخل الوكيل
                "critic_agent": literary_critic,
                "critic_fn_name": "review_chapter",
                "default_threshold": 8.0
            },
            "generate_blueprint": {
                "description": "بناء مخطط رواية مفصل.",
                "creator_agent": blueprint_architect,
                "creator_fn_name": "generate_blueprint",
                # نفترض مؤقتًا أن الناقد الأدبي يمكنه مراجعة المخططات أيضًا
                "critic_agent": literary_critic, 
                "critic_fn_name": "review_blueprint", # سنحتاج لإضافة هذه الدالة للناقد
                "default_threshold": 7.5
            },
            # ... يمكن إضافة مهام أخرى هنا مثل "generate_idea"
        }

    # --- الخطوة 2.2: بناء دالة run_task العامة ---
    async def run_refinable_task(
        self,
        task_name: str,
        initial_context: Any,
        user_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        يشغل أي مهمة إبداعية تتطلب دورة تحسين.
        """
        logger.info(f"Received request to run task: '{task_name}'")
        
        # 1. البحث عن المهمة في السجل
        task_definition = self._task_registry.get(task_name)
        if not task_definition:
            raise ValueError(f"Task '{task_name}' is not defined in the registry.")

        # 2. إعداد خدمة التحسين بالوكلاء المناسبين
        creator_agent = task_definition["creator_agent"]
        critic_agent = task_definition["critic_agent"]
        
        # الحصول على الدوال من الوكلاء باستخدام أسمائها
        creator_fn = getattr(creator_agent, task_definition["creator_fn_name"])
        critic_fn = getattr(critic_agent, task_definition["critic_fn_name"])

        # 3. إعداد إعدادات التحسين (دمج الإعدادات الافتراضية مع إعدادات المستخدم)
        config = user_config or {}
        quality_threshold = config.get("quality_threshold", task_definition["default_threshold"])
        max_cycles = config.get("max_refinement_cycles", 2)
        
        refinement_service = RefinementService(
            creator_fn=creator_fn,
            critique_fn=critic_fn,
            quality_threshold=quality_threshold,
            max_refinement_cycles=max_cycles
        )

        # 4. تشغيل دورة التحسين
        logger.info(f"Starting refinement service for '{task_name}' with threshold {quality_threshold}...")
        result = await refinement_service.refine(context=initial_context)
        
        # 5. إرجاع النتيجة النهائية
        logger.info(f"Task '{task_name}' finished with a final score of {result.get('final_score'):.1f}")
        return result
    
    # ... (بقية دوال أبولو كما هي) ...

# --- مثال اختبار جديد ---
async def main_test():
    # محاكاة مخطط فصل
    from blueprint_architect_agent import ChapterOutline
    sample_outline = ChapterOutline(
        title="الفصل 1: الرسالة الغامضة", summary="ملخص...", emotional_focus="أمل حذر", 
        key_events=["حدث1","حدث2"], character_arcs={"علي":"ينتقل..."}
    )

    # إنشاء المنسق
    orchestrator = ApolloOrchestrator()

    # محاكاة استدعاء من خلال واجهة API
    final_chapter_result = await orchestrator.run_refinable_task(
        task_name="generate_chapter",
        initial_context=sample_outline,
        user_config={"quality_threshold": 8.5} # يمكن للمستخدم تعديل العتبة
    )

    print("\n--- ✅ نتيجة المهمة النهائية (كتابة الفصل) ---")
    print(json.dumps(final_chapter_result, ensure_ascii=False, indent=2))
    
# --- ملاحظة مهمة ---
# لتشغيل هذا المثال، سنحتاج إلى إضافة دالة وهمية `review_blueprint` إلى LiteraryCriticAgent
class LiteraryCriticAgent:
    # ...
    def review_blueprint(self, blueprint_content: Any) -> Dict[str, Any]:
        # محاكاة بسيطة لنقد المخطط
        logger.info("[Critic] Reviewing blueprint...")
        return {
            "overall_score": 8.0,
            "issues": ["المخطط جيد لكنه يفتقر إلى حبكة فرعية."]
        }

if __name__ == "__main__":
    import json # Add this import for the test
    asyncio.run(main_test())
