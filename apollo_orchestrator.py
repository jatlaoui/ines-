# core/apollo_orchestrator.py

import logging
import json
import asyncio
from typing import Any, Dict, List, Optional

# --- استيراد الخدمات والوكلاء ---
from core.llm_service import llm_service
from core.refinement_service import RefinementService
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.blueprint_architect_agent import BlueprintArchitectAgent
from agents.chapter_composer_agent import ChapterComposerAgent
from agents.literary_critic_agent import LiteraryCriticAgent
from agents.poem_composer_agent import PoemComposerAgent
from agents.poetry_critic_agent import PoetryCriticAgent
# ... (إضافة استيرادات الوكلاء الآخرين عند تفعيلهم)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    """
    المايسترو "أبولو" - ينسق بين الوكلاء لتنفيذ المهام الإبداعية والتحليلية.
    """
    def __init__(self):
        self.agents = {
            "idea_generator": IdeaGeneratorAgent(),
            "blueprint_architect": BlueprintArchitectAgent(),
            "chapter_composer": ChapterComposerAgent(),
            "literary_critic": LiteraryCriticAgent(),
            "poem_composer": PoemComposerAgent(),
            "poetry_critic": PoetryCriticAgent(),
        }
        self._task_registry = self._build_task_registry()
        logger.info(f"🚀 Apollo Orchestrator initialized. Registered tasks: {list(self._task_registry.keys())}")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """يبني سجل المهام الذي يربط كل مهمة بوكلائها ودوالها."""
        return {
            "generate_idea": {
                "description": "توليد فكرة رواية جديدة مع دورة نقد وتحسين.",
                "creator_fn": self.agents["idea_generator"].generate_idea,
                "critic_fn": self.agents["literary_critic"].review_idea,
                "default_threshold": 7.0
            },
            "develop_blueprint": {
                "description": "تحويل قاعدة معرفة إلى مخطط سردي متكامل.",
                "creator_fn": self.agents["blueprint_architect"].create_blueprint,
                "critic_fn": self.agents["literary_critic"].review_blueprint,
                "default_threshold": 7.5
            },
            "compose_chapter": {
                "description": "كتابة فصل روائي كامل.",
                "creator_fn": self.agents["chapter_composer"].write_chapter,
                "critic_fn": self.agents["literary_critic"].review_chapter,
                "default_threshold": 8.0
            },
            "compose_poem": {
                "description": "كتابة قصيدة شعرية مع دورة نقد.",
                "creator_fn": self.agents["poem_composer"].compose_poem,
                "critic_fn": self.agents["poetry_critic"].review_poem,
                "default_threshold": 7.5
            },
        }

    async def run_refinable_task(self, task_name: str, initial_context: Dict[str, Any], user_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        المنفذ العام للمهام القابلة للتحسين (Create -> Critique -> Refine).
        """
        logger.info(f"▶️ Received request to run refinable task: '{task_name}'")
        
        task_def = self._task_registry.get(task_name)
        if not task_def:
            raise ValueError(f"Task '{task_name}' is not a registered refinable task.")

        config = user_config or {}
        
        refinement_service = RefinementService(
            creator_fn=task_def["creator_fn"],
            critique_fn=task_def["critic_fn"],
            quality_threshold=config.get("quality_threshold", task_def["default_threshold"]),
            max_refinement_cycles=config.get("max_cycles", 1)
        )
        
        logger.info(f"Starting refinement service for '{task_name}'...")
        return await refinement_service.refine(context=initial_context)

# --- إنشاء مثيل وحيد ---
apollo = ApolloOrchestrator()
