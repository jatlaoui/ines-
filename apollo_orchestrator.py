# core/apollo_orchestrator.py (النسخة المفعّلة والمبسطة)

import logging
import json
import asyncio
from typing import Any, Callable, Dict, List, Optional

# --- استيراد الوكلاء المفعّلين والخدمات الأساسية ---
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.chapter_composer_agent import ChapterComposerAgent
from agents.literary_critic_agent import LiteraryCriticAgent
from agents.blueprint_architect_agent import BlueprintArchitectAgent, StoryBlueprint, ChapterOutline # استيراد نماذج البيانات
from core.refinement_service import RefinementService

# --- إعدادات التسجيل ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    """
    المايسترو "أبولو" - المنسق المركزي للعمليات الإبداعية.
    ينسق بين وكلاء الإنشاء والنقد لتشغيل دورات تحسين متكاملة.
    """
    def __init__(self):
        # تهيئة الوكلاء الذين سنستخدمهم مباشرة.
        self.idea_generator = IdeaGeneratorAgent()
        self.chapter_composer = ChapterComposerAgent()
        self.literary_critic = LiteraryCriticAgent()
        # وكلاء آخرون يمكن إضافتهم هنا عند تفعيلهم
        # self.blueprint_architect = BlueprintArchitectAgent()
        
        self._task_registry = self._build_task_registry()
        logger.info(f"🚀 Apollo Orchestrator initialized. Registered tasks: {list(self._task_registry.keys())}")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """
        يبني سجل المهام الذي يربط كل مهمة بوكلائها ودوالها المناسبة.
        يركز هذا السجل حاليًا على المهام التي تم تفعيلها.
        """
        registry = {
            # مهمة قابلة للتحسين: توليد فكرة
            "generate_idea": {
                "description": "توليد فكرة رواية جديدة مع دورة نقد وتحسين.",
                "creator_agent": self.idea_generator,
                "creator_fn": self.idea_generator.generate_idea,
                "critic_agent": self.literary_critic,
                "critic_fn": self.literary_critic.review_idea, # استخدام دالة نقد الأفكار
                "default_threshold": 7.0
            },
            
            # مهمة قابلة للتحسين: كتابة فصل
            "compose_chapter": {
                "description": "كتابة فصل روائي كامل معزز بالذاكرة الحسية.",
                "creator_agent": self.chapter_composer,
                "creator_fn": self.chapter_composer.write_chapter,
                "critic_agent": self.literary_critic,
                "critic_fn": self.literary_critic.review_chapter, # استخدام دالة نقد الفصول
                "default_threshold": 8.0
            },
            
            # --- مهام مستقبلية يمكن إضافتها عند تفعيل وكلائها ---
            # "develop_blueprint": { ... },
            # "analyze_psychology": { ... },
            # "run_collaborative_session": { ... }
        }
        return registry

    async def run_refinable_task(
        self,
        task_name: str,
        initial_context: Dict[str, Any],
        user_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        المنفذ العام للمهام القابلة للتحسين (Create -> Critique -> Refine).
        """
        logger.info(f"▶️ Received request to run refinable task: '{task_name}'")
        
        task_def = self._task_registry.get(task_name)
        if not task_def:
            logger.error(f"❌ Task '{task_name}' not found in registry.")
            raise ValueError(f"Task '{task_name}' is not a registered refinable task.")

        config = user_config or {}
        
        # إنشاء خدمة التحسين مع الوكلاء والدوال المحددة لهذه المهمة
        refinement_service = RefinementService(
            creator_fn=task_def["creator_fn"],
            critique_fn=task_def["critic_fn"],
            quality_threshold=config.get("quality_threshold", task_def["default_threshold"]),
            max_refinement_cycles=config.get("max_cycles", 2)
        )
        
        logger.info(f"Starting refinement service for '{task_name}'...")
        result = await refinement_service.refine(context=initial_context)
        
        return result

# --- إنشاء مثيل وحيد ---
apollo = ApolloOrchestrator()

# --- قسم الاختبار المتكامل ---
async def main_test():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود. يرجى إضافته في ملف .env")
        return

    logger.info("\n" + "="*80)
    logger.info("🎭 Apollo Orchestrator - Full Creative Cycle Test 🎭")
    logger.info("="*80)

    # --- 1. توليد فكرة أولية وتحسينها ---
    logger.info("\n--- STEP 1: Generating and Refining a Story Idea ---")
    idea_context = {
        "genre_hint": "خيال علمي فلسفي",
        "theme_hint": "الذاكرة والهوية"
    }
    idea_result = await apollo.run_refinable_task(
        task_name="generate_idea",
        initial_context=idea_context,
        user_config={"max_cycles": 1} # دورة تحسين واحدة فقط للفكرة
    )
    
    if idea_result.get("status") != "success":
        logger.error("Failed to generate an idea. Aborting test.")
        print(json.dumps(idea_result, indent=2, ensure_ascii=False))
        return

    final_idea = idea_result.get("final_content", {}).get("content", {})
    logger.info(f"✅ Idea generation complete! Final Score: {idea_result.get('final_score'):.2f}")
    print("Final Idea:", json.dumps(final_idea, indent=2, ensure_ascii=False))

    # --- 2. بناء مخطط فصل وهمي (لأن وكيل المخططات لم يتم تفعيله بعد) ---
    logger.info("\n--- STEP 2: Mocking a Chapter Outline based on the Idea ---")
    mock_chapter_outline = ChapterOutline(
        title="الفصل الأول: الصدى المفقود",
        summary=f"نقدم البطل، 'كاي'، وهو فني ذاكرة يعيش في مدينة 'نيو-بابل'. يبدأ في الشك في ذكرياته الخاصة بعد أن يجد قطعة أثرية لا تتوافق مع تاريخه الرسمي. الفكرة الأساسية هي: {final_idea.get('premise')}",
        emotional_focus="القلق والفضول",
        key_events=["كاي يقوم بعمله اليومي في 'أرشيف الذاكرة'", "يكتشف القطعة الأثرية الغامضة", "يواجه خللاً في ذاكرته لأول مرة"],
        character_arcs={"كاي": "ينتقل من الثقة المطلقة بالنظام إلى الشك والبحث عن الحقيقة."}
    )
    print("Mock Chapter Outline created.")

    # --- 3. كتابة الفصل الأول وتحسينه ---
    logger.info("\n--- STEP 3: Composing and Refining the First Chapter ---")
    chapter_context = {"chapter_outline": mock_chapter_outline}
    
    chapter_result = await apollo.run_refinable_task(
        task_name="compose_chapter",
        initial_context=chapter_context,
        user_config={"quality_threshold": 8.5, "max_cycles": 2}
    )
    
    if chapter_result.get("status") != "success":
        logger.error("Failed to compose the chapter.")
        print(json.dumps(chapter_result, indent=2, ensure_ascii=False))
        return
        
    final_chapter = chapter_result.get("final_content", {})
    logger.info(f"✅ Chapter composition complete! Final Score: {chapter_result.get('final_score'):.2f}")
    logger.info(f"Refinement cycles used: {chapter_result.get('refinement_cycles_used')}")
    
    print("\n--- Final Chapter Content ---")
    print(final_chapter.get("chapter_content"))
    print("\n--- Final Critique ---")
    print(json.dumps(chapter_result.get("final_critique"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main_test())
