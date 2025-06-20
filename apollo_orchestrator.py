# core/apollo_orchestrator.py
"""
ApolloOrchestrator (المايسترو أبولو) - الإصدار الكامل
المنسق الرئيسي للعمليات الإبداعية، مع تسجيل كامل لجميع الوكلاء المتخصصين.
"""
import logging
from typing import Any, Callable, Dict, List, Optional
import json
import asyncio

# --- استيراد جميع الوكلاء والخدمات ---
# نفترض أن هذه الملفات موجودة في مجلد `agents` أو `core`
from agents.base_agent import BaseAgent
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.idea_critic_agent import IdeaCriticAgent
from agents.blueprint_architect_agent import BlueprintArchitectAgent
from agents.blueprint_critic_agent import BlueprintCriticAgent
from agents.chapter_composer_agent import ChapterComposerAgent
from agents.literary_critic_agent import LiteraryCriticAgent
from agents.poem_composer_agent import PoemComposerAgent
from agents.poetry_critic_agent import PoetryCriticAgent
from agents.forensic_logic_agent import ForensicLogicAgent
from agents.forensic_critic_agent import ForensicCriticAgent
from agents.cultural_maestro_agent import CulturalMaestroAgent
from agents.psychological_profiler_agent import PsychologicalProfilerAgent
from agents.social_conflict_mapper_agent import SocialConflictMapperAgent
from agents.dream_symbol_interpreter_agent import DreamSymbolInterpreterAgent
from agents.creative_chaos_agent import CreativeChaosAgent
from agents.frailty_injector_agent import AuthenticFrailtyInjectorAgent

from core.refinement_service import RefinementService

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
        # إنشاء مثيلات من جميع الوكلاء
        idea_generator = IdeaGeneratorAgent()
        idea_critic = IdeaCriticAgent()
        blueprint_architect = BlueprintArchitectAgent(kb={})
        blueprint_critic = BlueprintCriticAgent()
        chapter_composer = ChapterComposerAgent()
        literary_critic = LiteraryCriticAgent()
        poem_composer = PoemComposerAgent()
        poem_critic = PoetryCriticAgent()
        forensic_agent = ForensicLogicAgent()
        forensic_critic = ForensicCriticAgent()
        cultural_maestro = CulturalMaestroAgent()
        psychological_profiler = PsychologicalProfilerAgent()
        social_conflict_mapper = SocialConflictMapperAgent()
        dream_interpreter = DreamSymbolInterpreterAgent()
        chaos_agent = CreativeChaosAgent()
        frailty_agent = AuthenticFrailtyInjectorAgent()

        return {
            # --- مهام الكتابة الأساسية ---
            "generate_idea": {
                "description": "توليد وتطوير فكرة قصة إبداعية.",
                "creator_agent": idea_generator, "creator_fn_name": "generate_idea",
                "critic_agent": idea_critic, "critic_fn_name": "review_idea",
                "default_threshold": 7.0
            },
            "generate_blueprint": {
                "description": "بناء مخطط رواية مفصل.",
                "creator_agent": blueprint_architect, "creator_fn_name": "generate_blueprint",
                "critic_agent": blueprint_critic, "critic_fn_name": "review_blueprint",
                "default_threshold": 8.0
            },
            "generate_chapter": {
                "description": "كتابة فصل روائي كامل مع مراجعته.",
                "creator_agent": chapter_composer, "creator_fn_name": "write_chapter",
                "critic_agent": literary_critic, "critic_fn_name": "review_chapter",
                "default_threshold": 8.0
            },
            "generate_poem": {
                "description": "توليد قصيدة بناءً على موضوع معين.",
                "creator_agent": poem_composer, "creator_fn_name": "generate_poem",
                "critic_agent": poem_critic, "critic_fn_name": "review_poem",
                "default_threshold": 7.5
            },

            # --- مهام التحليل المتخصصة ---
            "analyze_crime_narrative": {
                "description": "تحليل نص جريمة لاستخلاص الأدلة والمنطق.",
                "creator_agent": forensic_agent, "creator_fn_name": "analyze_crime_scene",
                "critic_agent": forensic_critic, "critic_fn_name": "review_forensic_analysis",
                "default_threshold": 7.5
            },
            "enhance_cultural_authenticity": {
                "description": "إثراء النص بعناصر ثقافية وتراثية أصيلة.",
                "creator_agent": cultural_maestro, "creator_fn_name": "enhance_cultural_authenticity",
                "critic_agent": literary_critic, "critic_fn_name": "review_chapter",
                "default_threshold": 8.0
            },
            "create_psychological_profile": {
                "description": "بناء ملف نفسي عميق لشخصية.",
                "creator_agent": psychological_profiler, "creator_fn_name": "create_character_profile",
                "critic_agent": literary_critic, "critic_fn_name": "review_character_depth",
                "default_threshold": 8.5
            },
            "map_social_conflicts": {
                "description": "تخطيط وتحليل الصراعات الاجتماعية في القصة.",
                "creator_agent": social_conflict_mapper, "creator_fn_name": "map_social_conflicts",
                "critic_agent": blueprint_critic, "critic_fn_name": "review_plot_consistency",
                "default_threshold": 7.5
            },
            "generate_symbolic_dream": {
                "description": "توليد حلم رمزي يعمق القصة.",
                "creator_agent": dream_interpreter, "creator_fn_name": "generate_symbolic_dream",
                "critic_agent": literary_critic, "critic_fn_name": "review_symbolism",
                "default_threshold": 7.0
            },

            # --- مهام الإبداع المتقدم ---
            "generate_disruptive_ideas": {
                "description": "توليد أفكار غير متوقعة لكسر الجمود الإبداعي.",
                "creator_agent": chaos_agent, "creator_fn_name": "generate_disruptive_ideas",
                "critic_agent": idea_critic, "critic_fn_name": "review_idea_originality",
                "default_threshold": 6.0
            },
            "humanize_text": {
                "description": "إضافة لمسة من الضعف الإنساني والواقعية على النص.",
                "creator_agent": frailty_agent, "creator_fn_name": "humanize_text",
                "critic_agent": literary_critic, "critic_fn_name": "review_authenticity",
                "default_threshold": 8.0
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
        
        task_definition = self._task_registry.get(task_name)
        if not task_definition:
            logger.error(f"Task '{task_name}' is not defined in the registry.")
            raise ValueError(f"Task '{task_name}' is not defined in the registry.")

        creator_agent = task_definition["creator_agent"]
        critic_agent = task_definition["critic_agent"]
        
        try:
            creator_fn = getattr(creator_agent, task_definition["creator_fn_name"])
            # نفترض وجود دوال النقد بأسماء متوقعة في الوكلاء النقاد
            critic_fn = getattr(critic_agent, task_definition["critic_fn_name"])
        except AttributeError as e:
            logger.error(f"Function not found on agent for task '{task_name}': {e}")
            raise AttributeError(f"Misconfigured task '{task_name}': The function name in the registry does not exist on the agent. {e}")

        config = user_config or {}
        quality_threshold = config.get("quality_threshold", task_definition["default_threshold"])
        max_cycles = config.get("max_refinement_cycles", 2)
        
        refinement_service = RefinementService(
            creator_fn=creator_fn,
            critique_fn=critic_fn,
            quality_threshold=quality_threshold,
            max_refinement_cycles=max_cycles
        )

        logger.info(f"Starting refinement service for '{task_name}' with threshold {quality_threshold}...")
        result = await refinement_service.refine(context=initial_context)
        
        logger.info(f"Task '{task_name}' finished with a final score of {result.get('final_score'):.1f}")
        return result

# إنشاء مثيل وحيد من أبولو يمكن استيراده في أي مكان
apollo = ApolloOrchestrator()

# --- مثال اختبار جديد لاختبار مرونة السجل ---
if __name__ == "__main__":
    # هذا القسم يتطلب وجود جميع ملفات الوكلاء والنقاد في المسار الصحيح
    
    async def main_test():
        orchestrator = apollo
        
        # --- اختبار مهمة توليد فكرة ---
        print("\n" + "="*80)
        print("🧪 TEST: RUNNING 'generate_idea' TASK")
        print("="*80)
        idea_config = {
            "genre_hint": "خيال علمي",
            "theme_hint": "الذكاء الاصطناعي والوعي",
        }
        try:
            final_idea_result = await orchestrator.run_refinable_task(
                task_name="generate_idea",
                initial_context=idea_config,
                user_config={"quality_threshold": 7.5}
            )
            print("\n--- ✅ نتيجة مهمة توليد الفكرة النهائية ---")
            print(json.dumps(final_idea_result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"--- ❌ فشل اختبار توليد الفكرة --- \n {e}")

        # --- اختبار مهمة تحليل الجريمة ---
        print("\n" + "="*80)
        print("🧪 TEST: RUNNING 'analyze_crime_narrative' TASK")
        print("="*80)
        crime_config = {
            "text_content": "وجد المحقق جثة الهالك في الغرفة. بجانبها، كان هناك سكين ملطخ بالدماء ونافذة مكسورة. شهود قالوا إنهم سمعوا صراخًا حوالي منتصف الليل.",
        }
        try:
            final_crime_analysis = await orchestrator.run_refinable_task(
                task_name="analyze_crime_narrative",
                initial_context=crime_config,
            )
            print("\n--- ✅ نتيجة مهمة تحليل الجريمة النهائية ---")
            print(json.dumps(final_crime_analysis, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"--- ❌ فشل اختبار تحليل الجريمة --- \n {e}")
    
    # إضافة مسار المجلد الحالي للسماح بالاستيرادات
    import sys
    sys.path.append('.')

    asyncio.run(main_test())
