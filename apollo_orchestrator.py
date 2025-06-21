# core/apollo_orchestrator.py (الإصدار المحدث بالكامل)
import logging
import json
import asyncio
from typing import Any, Callable, Dict, List, Optional

# --- استيراد البنية التحتية والوكلاء الجدد والأقوياء ---
# استيراد الفئة الأساسية الجديدة والمدير
from agents.base_agent import BaseAgent, AgentManager, AgentState

# استيراد وكلاء متخصصين من الملفات الجديدة
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.blueprint_architect_agent import BlueprintArchitectAgent
from agents.chapter_composer_agent import ChapterComposerAgent
from agents.literary_critic_agent import LiteraryCriticAgent
from agents.psychological_profiler_agent import PsychologicalProfilerAgent
from agents.cultural_maestro_agent import CulturalMaestroAgent
from agents.dream_symbol_interpreter_agent import DreamSymbolInterpreterAgent
from agents.social_conflict_mapper_agent import SocialConflictMapperAgent

# استيراد الأنظمة المتقدمة (الوكلاء الفوقيين Meta-Agents)
from agents.AdvancedArbitrator import AdvancedArbitrator
from agents.AgentCollaboration import AgentCollaboration

# استيراد الخدمات الأساسية
from core.refinement_service import RefinementService

# --- إعدادات التسجيل ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    """
    المايسترو "أبولو" - المنسق المركزي لمجتمع الوكلاء.
    يدير تسجيل الوكلاء، وتوجيه المهام، وتنسيق العمليات الإبداعية المعقدة.
    """
    def __init__(self):
        self.agent_manager = AgentManager()
        self.collaboration_system = AgentCollaboration()
        self.arbitrator = AdvancedArbitrator()
        
        self._task_registry = self._build_task_registry()
        logger.info(f"🚀 Apollo Orchestrator initialized with a powerful Agent Society.")
        logger.info(f"Registered Tasks: {list(self._task_registry.keys())}")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """
        يبني ويهيئ سجل المهام الذي يربط كل مهمة بوكلائها وأنظمتها.
        """
        # --- إنشاء وتسجيل جميع الوكلاء ---
        agents_to_register = [
            IdeaGeneratorAgent(),
            BlueprintArchitectAgent(),
            ChapterComposerAgent(),
            LiteraryCriticAgent(),
            PsychologicalProfilerAgent(),
            CulturalMaestroAgent(),
            DreamSymbolInterpreterAgent(),
            SocialConflictMapperAgent(),
            # يمكن إضافة المزيد من الوكلاء هنا
        ]
        
        for agent in agents_to_register:
            # نفترض أن كل وكيل لديه خصائص name و capabilities
            self.agent_manager.register_agent(agent)
            self.collaboration_system.register_agent(
                agent.id, agent, agent.name, agent.get_capabilities()
            )

        registry = {
            # --- 1. مهام التحليل العميق (Analysis Tasks) ---
            "analyze_psychological_profile": {
                "description": "إنشاء ملف نفسي عميق لشخصية.",
                "task_type": "analysis",
                "handler_agent_name": "المحلل النفسي للشخصيات",
                "handler_fn_name": "create_character_profile"
            },
            "analyze_cultural_elements": {
                "description": "تحليل العناصر الثقافية في نص.",
                "task_type": "analysis",
                "handler_agent_name": "الخبير الثقافي",
                "handler_fn_name": "enhance_cultural_authenticity" # نفترض أن هذه الدالة تقوم بالتحليل أيضًا
            },
            "map_social_conflicts": {
                "description": "بناء خريطة للصراعات الاجتماعية في السرد.",
                "task_type": "analysis",
                "handler_agent_name": "مخطط الصراعات الاجتماعية",
                "handler_fn_name": "map_social_conflicts"
            },
            "interpret_dreams_and_symbols": {
                "description": "تفسير الأحلام والرموز في نص.",
                "task_type": "analysis",
                "handler_agent_name": "مفسر الأحلام والرموز",
                "handler_fn_name": "generate_symbolic_dream"
            },
            
            # --- 2. مهام الإنشاء القابلة للتحسين (Refinable Creation Tasks) ---
            "generate_novel_idea": {
                "description": "توليد فكرة رواية جديدة مع دورة نقد وتحسين.",
                "task_type": "refinable_creation",
                "creator_agent_name": "مولد الأفكار الإبداعي",
                "creator_fn_name": "generate_idea",
                "critic_agent_name": "الناقد الأدبي",
                "critic_fn_name": "review_idea", # نفترض وجود دالة نقد للأفكار
                "default_threshold": 7.5
            },
            "develop_story_blueprint": {
                "description": "تحويل فكرة إلى مخطط سردي متكامل.",
                "task_type": "refinable_creation",
                "creator_agent_name": "مهندس المخططات الأدبية",
                "creator_fn_name": "generate_blueprint", # نفترض وجود هذه الدالة
                "critic_agent_name": "ناقد المخططات", # نفترض وجود ناقد متخصص
                "critic_fn_name": "review_blueprint",
                "default_threshold": 8.0
            },
            
            # --- 3. مهام تعاونية (Collaborative Tasks) ---
            "collaborative_brainstorming": {
                "description": "عقد جلسة عصف ذهني جماعي بين الوكلاء.",
                "task_type": "collaborative",
                "handler_system": self.collaboration_system,
                "handler_fn_name": "start_brainstorming"
            },
            
            # --- 4. مهام التحكيم والجودة (Arbitration Tasks) ---
            "arbitrate_content_quality": {
                "description": "تقييم وتصحيح محتوى بواسطة المحكم المتقدم.",
                "task_type": "arbitration",
                "handler_system": self.arbitrator,
                "handler_fn_name": "evaluate_content"
            },
            "correct_content_with_arbitrator": {
                "description": "تصحيح محتوى بشكل متقدم.",
                "task_type": "arbitration",
                "handler_system": self.arbitrator,
                "handler_fn_name": "correct_content"
            }
        }
        
        return registry

    async def run_task(
        self,
        task_name: str,
        context: Dict[str, Any],
        user_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        المنفذ العام الموحد: يشغل أي مهمة مسجلة حسب نوعها.
        """
        logger.info(f"▶️ Running task: '{task_name}'")
        
        task_def = self._task_registry.get(task_name)
        if not task_def:
            raise ValueError(f"Task '{task_name}' not defined in the registry.")

        config = user_config or {}
        task_type = task_def.get("task_type")

        # --- توجيه المهمة حسب نوعها ---
        if task_type == "analysis":
            agent = self.agent_manager.find_agent_by_name(task_def["handler_agent_name"])
            if not agent:
                raise RuntimeError(f"Agent '{task_def['handler_agent_name']}' not found.")
            
            handler_fn = getattr(agent, task_def["handler_fn_name"])
            return await handler_fn(context)

        elif task_type == "refinable_creation":
            creator_agent = self.agent_manager.find_agent_by_name(task_def["creator_agent_name"])
            critic_agent = self.agent_manager.find_agent_by_name(task_def["critic_agent_name"])
            
            if not creator_agent or not critic_agent:
                 raise RuntimeError("Creator or Critic agent not found for task.")

            creator_fn = getattr(creator_agent, task_def["creator_fn_name"])
            critic_fn = getattr(critic_agent, task_def["critic_fn_name"])
            
            refinement_service = RefinementService(
                creator_fn=creator_fn, critique_fn=critic_fn,
                quality_threshold=config.get("quality_threshold", task_def["default_threshold"]),
                max_refinement_cycles=config.get("max_cycles", 2)
            )
            return await refinement_service.refine(context=context)

        elif task_type == "collaborative" or task_type == "arbitration":
            handler_system = task_def["handler_system"]
            handler_fn = getattr(handler_system, task_def["handler_fn_name"])
            # تمرير السياق مباشرة إلى أنظمة التعاون والتحكيم
            return await handler_fn(**context)
            
        else:
            raise ValueError(f"Unsupported task type: '{task_type}'")

# --- إنشاء مثيل وحيد ---
apollo = ApolloOrchestrator()

# --- قسم الاختبار (مُحدَّث بالكامل) ---
async def main_test():
    logger.info("\n" + "="*80)
    logger.info("🎭 Apollo Orchestrator - Advanced Task Execution Test 🎭")
    logger.info("="*80)

    # --- 1. اختبار مهمة تحليل نفسي (Analysis Task) ---
    logger.info("\n--- TEST 1: Psychological Profile Analysis ---")
    try:
        profile_context = {
            "character_name": "خالد",
            "character_description": "شاب انطوائي فقد والده في حادث، ويخاف من الفشل بشدة."
        }
        psych_result = await apollo.run_task(
            task_name="analyze_psychological_profile",
            context=profile_context
        )
        print("✅ Psychological Profile Result:")
        print(json.dumps(psych_result, indent=2, ensure_ascii=False))
    except Exception as e:
        logger.error(f"❌ Psychological analysis failed: {e}", exc_info=True)

    # --- 2. اختبار مهمة التحكيم (Arbitration Task) ---
    logger.info("\n--- TEST 2: Content Arbitration ---")
    try:
        # ملاحظة: هذا يتطلب أن تكون llm_service ودوال قاعدة البيانات مهيأة في AdvancedArbitrator
        # سنقوم بمحاكاة بسيطة للسياق المطلوب
        arbitration_context = {
            "content": "كان النص مليء بالأمل، لكنه يفتقر للحبكة. الشخصية الرئيسية كانت سطحية.",
            "content_type": "chapter",
            "agent_id": "test_writer_agent"
        }
        # arbitrator_result = await apollo.run_task(
        #     task_name="arbitrate_content_quality",
        #     context=arbitration_context
        # )
        # print("✅ Arbitration Result:", arbitrator_result)
        print("ℹ️  Arbitration test skipped (requires live DB/LLM connection).")
    except Exception as e:
        logger.error(f"❌ Arbitration task failed: {e}", exc_info=True)
        
    # --- 3. اختبار مهمة تعاونية (Collaborative Task) ---
    logger.info("\n--- TEST 3: Collaborative Brainstorming ---")
    try:
        # ملاحظة: يتطلب تهيئة الوكلاء في نظام التعاون
        collaboration_context = {
            "session_id": "test_session_001", # يفترض أن يتم إنشاؤها أولاً
            "topic": "كيف يمكن لشخصية انطوائية التغلب على صدمة الماضي؟",
        }
        # collaboration_result = await apollo.run_task(
        #     task_name="collaborative_brainstorming",
        #     context=collaboration_context
        # )
        # print("✅ Collaborative Brainstorming Result:", collaboration_result)
        print("ℹ️  Collaboration test skipped (requires live session setup).")
    except Exception as e:
        logger.error(f"❌ Collaboration task failed: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main_test())
