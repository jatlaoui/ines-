# apollo_orchestrator.py (الإصدار المحدث لتضمين ناقد المخططات)
import json
# ... (بقية الاستيرادات كما هي) ...

from blueprint_architect_agent import BlueprintArchitectAgent
from chapter_composer_agent import ChapterComposerAgent
from literary_critic_agent import LiteraryCriticAgent
from blueprint_critic_agent import BlueprintCriticAgent # <-- الإضافة الجديدة

# ...

class ApolloOrchestrator:
    def __init__(self):
        # ... (نفس التهيئة السابقة) ...
        self._task_registry = self._build_task_registry()
        # ...

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """
        تحديث سجل المهام ليشمل الناقد الجديد.
        """
        chapter_composer = ChapterComposerAgent()
        literary_critic = LiteraryCriticAgent()
        blueprint_architect = BlueprintArchitectAgent(kb={})
        blueprint_critic = BlueprintCriticAgent() # <-- إنشاء مثيل من الناقد الجديد

        return {
            "generate_chapter": {
                # ... (كما هو) ...
            },
            "generate_blueprint": {
                "description": "بناء مخطط رواية مفصل.",
                "creator_agent": blueprint_architect,
                "creator_fn_name": "generate_blueprint",
                "critic_agent": blueprint_critic, # <-- التحديث هنا
                "critic_fn_name": "review_blueprint", # <-- التحديث هنا
                "default_threshold": 8.0 # يمكن تعديل العتبة لهذه المهمة
            },
        }

    # ... (run_refinable_task والدوال الأخرى تبقى كما هي تمامًا) ...

# --- مثال اختبار جديد ---
async def main_test():
    # محاكاة KnowledgeBase
    from advanced_context_engine import KnowledgeBase, Entity, EntityContext, Relationship, EmotionalArcPoint
    sample_kb = KnowledgeBase(
        entities=[Entity(name='علي', type='character', description='', importance_score=9, context=EntityContext(role_in_text='البطل'))],
        relationship_graph=[Relationship(source='علي', target='زينب', relation='يخون')],
        emotional_arc=[EmotionalArcPoint(emotion='قلق', intensity=4, timestamp=10), EmotionalArcPoint(emotion='خوف', intensity=8, timestamp=50)],
        historical_context={}
    )
    
    orchestrator = ApolloOrchestrator()

    print("\n--- بدء مهمة بناء المخطط مع دورة التحسين ---")
    final_blueprint_result = await orchestrator.run_refinable_task(
        task_name="generate_blueprint",
        initial_context=sample_kb, # الآن نمرر كائن KB كاملاً
        user_config={"quality_threshold": 8.5}
    )

    print("\n--- ✅ نتيجة المهمة النهائية (مخطط القصة) ---")
    print(json.dumps(final_blueprint_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    import asyncio
    # ملاحظة: يجب تعديل BlueprintArchitectAgent ليأخذ KnowledgeBase ككائن
    # وتعديل المثال الرئيسي ليتوافق
    asyncio.run(main_test())
