# apollo_orchestrator.py (الإصدار المحدث مع دعم مهام متعددة)
import logging
from typing import Any, Callable, Dict, List, Optional
import json
import asyncio

# --- استيراد الوكلاء والخدمات ---
# سيتم إنشاء مثيلات منها داخل المنسق
from blueprint_architect_agent import BlueprintArchitectAgent
from chapter_composer_agent import ChapterComposerAgent
from literary_critic_agent import LiteraryCriticAgent
from blueprint_critic_agent import BlueprintCriticAgent
from idea_generator_agent import IdeaGeneratorAgent
from idea_critic_agent import IdeaCriticAgent
from poem_composer_agent import PoemComposerAgent
from poetry_critic_agent import PoetryCriticAgent

from refinement_service import RefinementService

# --- إعداد التسجيل (Logger) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    """
    المايسترو "أبولو" - المنسق الرئيسي للعمليات الإبداعية.
    يستخدم سجل مهام مرن وخدمة تحسين عامة لتنسيق عمل الوكلاء.
    """
    def __init__(self):
        """
        تهيئة أبولو وسجل المهام.
        """
        # --- سجل المهام (Task Registry) ---
        self._task_registry = self._build_task_registry()
        logger.info(f"Apollo initialized with a Task Registry of {len(self._task_registry)} tasks.")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """
        يبني ويهيئ سجل المهام الذي يربط كل مهمة بوكلائها.
        هذا هو "دليل الهاتف" الذي يستخدمه أبولو.
        """
        # إنشاء مثيلات من الوكلاء لاستخدامها في السجل
        # في نظام حقيقي، قد يتم حقن هذه التبعيات (Dependency Injection)
        idea_generator = IdeaGeneratorAgent()
        idea_critic = IdeaCriticAgent()
        blueprint_architect = BlueprintArchitectAgent(kb={}) # يحتاج kb وهمية للتهيئة
        blueprint_critic = BlueprintCriticAgent()
        chapter_composer = ChapterComposerAgent()
        literary_critic = LiteraryCriticAgent()
        poem_composer = PoemComposerAgent()
        poem_critic = PoetryCriticAgent()

        return {
            "generate_idea": {
                "description": "توليد وتطوير فكرة قصة إبداعية.",
                "creator_agent": idea_generator,
                "creator_fn_name": "generate_idea",
                "critic_agent": idea_critic,
                "critic_fn_name": "review_idea",
                "default_threshold": 7.0
            },
            "generate_blueprint": {
                "description": "بناء مخطط رواية مفصل.",
                "creator_agent": blueprint_architect,
                "creator_fn_name": "generate_blueprint",
                "critic_agent": blueprint_critic,
                "critic_fn_name": "review_blueprint",
                "default_threshold": 8.0
            },
            "generate_chapter": {
                "description": "كتابة فصل روائي كامل مع مراجعته.",
                "creator_agent": chapter_composer,
                "creator_fn_name": "write_chapter",
                "critic_agent": literary_critic,
                "critic_fn_name": "review_chapter",
                "default_threshold": 8.0
            },
            "generate_poem": {
                "description": "توليد قصيدة بناءً على موضوع معين.",
                "creator_agent": poem_composer,
                "creator_fn_name": "generate_poem",
                "critic_agent": poem_critic,
                "critic_fn_name": "review_poem",
                "default_threshold": 7.5
            },
        }

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
        
        # 1. البحث عن المهمة في السجل
        task_definition = self._task_registry.get(task_name)
        if not task_definition:
            logger.error(f"Task '{task_name}' is not defined in the registry.")
            raise ValueError(f"Task '{task_name}' is not defined in the registry.")

        # 2. إعداد خدمة التحسين بالوكلاء المناسبين
        creator_agent = task_definition["creator_agent"]
        critic_agent = task_definition["critic_agent"]
        
        # الحصول على الدوال من الوكلاء باستخدام أسمائها المسجلة
        try:
            creator_fn = getattr(creator_agent, task_definition["creator_fn_name"])
            critic_fn = getattr(critic_agent, task_definition["critic_fn_name"])
        except AttributeError as e:
            logger.error(f"Function not found on agent for task '{task_name}': {e}")
            raise AttributeError(f"Misconfigured task '{task_name}': {e}")

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

# --- مثال اختبار جديد لاختبار مرونة السجل ---
if __name__ == "__main__":
    from blueprint_architect_agent import ChapterOutline # للتوافق
    
    async def main_test():
        orchestrator = ApolloOrchestrator()
        
        # --- اختبار مهمة كتابة الفصل ---
        print("\n" + "="*80)
        print("🧪 TEST 1: RUNNING 'generate_chapter' TASK")
        print("="*80)
        sample_outline = ChapterOutline(
            title="الفصل 1: الرسالة الغامضة", summary="ملخص...", emotional_focus="أمل حذر", 
            key_events=["حدث1","حدث2"], character_arcs={"علي":"ينتقل..."}
        )
        final_chapter_result = await orchestrator.run_refinable_task(
            task_name="generate_chapter",
            initial_context=sample_outline,
            user_config={"quality_threshold": 8.5}
        )
        print("\n--- ✅ نتيجة مهمة كتابة الفصل النهائية ---")
        print(json.dumps(final_chapter_result, ensure_ascii=False, indent=2))
        
        # --- اختبار مهمة كتابة قصيدة ---
        print("\n" + "="*80)
        print("🧪 TEST 2: RUNNING 'generate_poem' TASK")
        print("="*80)
        poem_config = {
            "theme_hint": "الوحدة في المدينة الرقمية",
            "style_hint": "شعر حر",
            "quality_threshold": 7.0
        }
        final_poem_result = await orchestrator.run_refinable_task(
            task_name="generate_poem",
            initial_context=poem_config, # السياق الأولي هنا هو إعدادات القصيدة
            user_config=poem_config
        )
        print("\n--- ✅ نتيجة مهمة كتابة القصيدة النهائية ---")
        print(json.dumps(final_poem_result, ensure_ascii=False, indent=2))

    asyncio.run(main_test())
