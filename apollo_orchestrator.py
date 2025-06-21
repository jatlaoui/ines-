# core/apollo_orchestrator.py (النسخة النهائية والمفعّلة)

import logging
from typing import Any, Dict, List, Optional

# استيراد الوكلاء المفعّلين
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.blueprint_architect_agent import BlueprintArchitectAgent
from agents.chapter_composer_agent import ChapterComposerAgent
from agents.literary_critic_agent import LiteraryCriticAgent
from agents.psychological_profiler_agent import PsychologicalProfilerAgent
from agents.cultural_maestro_agent import CulturalMaestroAgent
# استيراد الخدمات الأساسية
from core.refinement_service import RefinementService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    """
    المايسترو "أبولو" - ينسق بين الوكلاء لتنفيذ المهام الإبداعية والتحليلية.
    """
    def __init__(self):
        # تهيئة جميع الوكلاء عند بدء التشغيل
        self.agents = {
            "idea_generator": IdeaGeneratorAgent(),
            "blueprint_architect": BlueprintArchitectAgent(),
            "chapter_composer": ChapterComposerAgent(),
            "literary_critic": LiteraryCriticAgent(),
            "psychological_profiler": PsychologicalProfilerAgent(),
            "cultural_maestro": CulturalMaestroAgent(),
        }
        self._task_registry = self._build_task_registry()
        logger.info(f"🚀 Apollo Orchestrator initialized. Registered tasks: {list(self._task_registry.keys())}")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """يبني سجل المهام الذي يربط كل مهمة بوكلائها ودوالها."""
        return {
            # --- مهام تحليلية (مباشرة) ---
            "create_psychological_profile": {
                "description": "إنشاء ملف نفسي عميق لشخصية.",
                "task_type": "analysis",
                "handler": self.agents["psychological_profiler"].create_profile,
            },
            "enrich_text_culturally": {
                "description": "إثراء نص بلمسات ثقافية أصيلة.",
                "task_type": "analysis",
                "handler": self.agents["cultural_maestro"].enrich_text,
            },
            
            # --- مهام إبداعية قابلة للتحسين ---
            "generate_idea": {
                "description": "توليد فكرة رواية جديدة مع دورة نقد وتحسين.",
                "task_type": "refinable_creation",
                "creator_fn": self.agents["idea_generator"].generate_idea,
                "critic_fn": self.agents["literary_critic"].review_idea,
                "default_threshold": 7.0
            },
            "develop_blueprint": {
                "description": "تحويل قاعدة معرفة إلى مخطط سردي متكامل.",
                "task_type": "refinable_creation",
                "creator_fn": self.agents["blueprint_architect"].create_blueprint,
                "critic_fn": self.agents["literary_critic"].review_blueprint,
                "default_threshold": 7.5
            },
            "compose_chapter": {
                "description": "كتابة فصل روائي كامل.",
                "task_type": "refinable_creation",
                "creator_fn": self.agents["chapter_composer"].write_chapter,
                "critic_fn": self.agents["literary_critic"].review_chapter,
                "default_threshold": 8.0
            },
        }

    async def run_task(self, task_name: str, context: Dict[str, Any], user_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """المنفذ العام الموحد: يشغل أي مهمة مسجلة حسب نوعها."""
        logger.info(f"▶️ Running task: '{task_name}'")
        task_def = self._task_registry.get(task_name)
        if not task_def:
            raise ValueError(f"Task '{task_name}' not found in registry.")

        task_type = task_def.get("task_type")
        config = user_config or {}

        if task_type == "analysis":
            return await task_def["handler"](context)
        
        elif task_type == "refinable_creation":
            refinement_service = RefinementService(
                creator_fn=task_def["creator_fn"],
                critique_fn=task_def["critic_fn"],
                quality_threshold=config.get("quality_threshold", task_def["default_threshold"]),
                max_refinement_cycles=config.get("max_cycles", 1) # دورة تحسين واحدة كافتراضي
            )
            return await refinement_service.refine(context=context)
            
        else:
            raise ValueError(f"Unsupported task type: '{task_type}'")

# --- إنشاء مثيل وحيد ---
apollo = ApolloOrchestrator()
