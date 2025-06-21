# core/apollo_orchestrator.py (الإصدار المحدث مع دعم وكلاء المسرحية التونسية)
import logging
from typing import Any, Callable, Dict, List, Optional
import json
import asyncio

# --- استيراد جميع الوكلاء والخدمات ---
# ... (جميع استيرادات الوكلاء السابقة) ...
from agents.base_agent import BaseAgent
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.idea_critic_agent import IdeaCriticAgent
from agents.narrative_constructor_agent import NarrativeConstructorAgent # <-- وكيل بناء المشاهد الجديد
# ... (بقية الوكلاء) ...

from core.refinement_service import RefinementService
# نفترض وجود ناقد متخصص للمسرحيات أو استخدام الناقد الأدبي العام
from agents.literary_critic_agent import LiteraryCriticAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    """
    المايسترو "أبولو" - المنسق الرئيسي للعمليات الإبداعية.
    """
    def __init__(self):
        self._task_registry = self._build_task_registry()
        logger.info(f"Apollo initialized with a Task Registry of {len(self._task_registry)} tasks.")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """
        يبني ويهيئ سجل المهام الذي يربط كل مهمة بوكلائها.
        """
        # إنشاء مثيلات من جميع الوكلاء
        idea_generator = IdeaGeneratorAgent()
        idea_critic = IdeaCriticAgent()
        narrative_constructor = NarrativeConstructorAgent() # <-- مثيل جديد
        literary_critic = LiteraryCriticAgent()
        # ... (بقية مثيلات الوكلاء)

        registry = {
            # --- مهام الكتابة الأساسية ---
            "generate_idea": {"creator_agent": idea_generator, "creator_fn_name": "generate_idea", "critic_agent": idea_critic, "critic_fn_name": "review_idea", "default_threshold": 7.0},
            # ... (بقية المهام السابقة) ...
        }
        
        # --- إضافة مهمة كتابة المسرحية التونسية المتخصصة ---
        registry["construct_tunisian_play_scene"] = {
            "description": "بناء مشهد مسرحي تونسي كامل باستخدام مكونات متخصصة.",
            "creator_agent": narrative_constructor,
            "creator_fn_name": "construct_play_scene", # الدالة التي بنيناها
            "critic_agent": literary_critic, # يمكن استخدام ناقد عام أو بناء ناقد متخصص للمسرح
            "critic_fn_name": "review_play_scene", # نفترض وجود هذه الدالة في الناقد
            "default_threshold": 8.0
        }
        
        return registry

    async def run_refinable_task(
        self,
        task_name: str,
        initial_context: Any,
        user_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        المنفذ العام: يشغل أي مهمة إبداعية مسجلة وتتطلب دورة تحسين.
        """
        logger.info(f"Received request to run task: '{task_name}'")
        
        task_definition = self._task_registry.get(task_name)
        if not task_definition:
            raise ValueError(f"Task '{task_name}' not defined in the registry.")

        creator_agent = task_definition["creator_agent"]
        critic_agent = task_definition["critic_agent"]
        
        try:
            creator_fn = getattr(creator_agent, task_definition["creator_fn_name"])
            critic_fn = getattr(critic_agent, task_definition["critic_fn_name"])
        except AttributeError as e:
            raise AttributeError(f"Misconfigured task '{task_name}': {e}")

        config = user_config or {}
        quality_threshold = config.get("quality_threshold", task_definition["default_threshold"])
        max_cycles = config.get("max_refinement_cycles", 2)
        
        refinement_service = RefinementService(
            creator_fn=creator_fn, critique_fn=critic_fn,
            quality_threshold=quality_threshold, max_refinement_cycles=max_cycles
        )

        logger.info(f"Starting refinement service for '{task_name}'...")
        result = await refinement_service.refine(context=initial_context)
        
        logger.info(f"Task '{task_name}' finished with a final score of {result.get('final_score'):.1f}")
        return result

# إنشاء مثيل وحيد
apollo = ApolloOrchestrator()

# --- قسم الاختبار (مُحدَّث) ---
if __name__ == "__main__":
    # هذا القسم يتطلب وجود جميع ملفات الوكلاء والنقاد في المسار الصحيح
    
    # إضافة المسار الحالي للسماح بالاستيرادات
    import sys
    sys.path.append('.')
    
    # إضافة دالة نقد وهمية للناقد الأدبي لغرض الاختبار
    def mock_review_play_scene(self, scene_content):
        return {"overall_score": 8.5, "issues": []}
    LiteraryCriticAgent.review_play_scene = mock_review_play_scene

    async def main_test():
        orchestrator = apollo
        
        # --- اختبار مهمة بناء مشهد مسرحي تونسي ---
        print("\n" + "="*80)
        print("🎭 TEST: RUNNING 'construct_tunisian_play_scene' TASK")
        print("="*80)
        
        scene_outline = {
            "title": "مشهد المقهى",
            "location": "cafe",
            "location_name": "مقهى شعبي في تونس العاصمة",
            "interactions": [
                {"character_name": "الحاجة فاطمة", "character_archetype": "al_hajja", "topic": "الزواج", "mood": "قلق"},
                {"character_name": "ابنتها ليلى", "character_archetype": "al_mothaqafa", "topic": "المستقبل", "mood": "ملل"}
            ]
        }
        
        try:
            final_scene_result = await orchestrator.run_refinable_task(
                task_name="construct_tunisian_play_scene",
                initial_context={"scene_outline": scene_outline},
            )
            print("\n--- ✅ نتيجة مهمة بناء المشهد المسرحي ---")
            print(json.dumps(final_scene_result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"--- ❌ فشل اختبار بناء المشهد --- \n {e}")

    asyncio.run(main_test())
