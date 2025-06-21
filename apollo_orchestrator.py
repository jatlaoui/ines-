# core/apollo_orchestrator.py
import logging
from typing import Any, Callable, Dict, List, Optional
import json
import asyncio

# --- استيراد جميع الوكلاء والخدمات ---
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
from agents.dramaturg_agent import DramaturgAgent
from agents.character_arc_agent import CharacterArcAgent
from agents.dialogue_subtext_agent import DialogueSubtextAgent
from agents.staging_director_agent import StagingDirectorAgent
from agents.instructional_designer_agent import InstructionalDesignerAgent
from agents.educational_content_critic import EducationalContentCritic

from core.refinement_service import RefinementService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    def __init__(self):
        self._task_registry = self._build_task_registry()
        logger.info(f"Apollo initialized with a Task Registry of {len(self._task_registry)} tasks.")

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        # إنشاء مثيلات من جميع الوكلاء
        idea_generator, idea_critic = IdeaGeneratorAgent(), IdeaCriticAgent()
        blueprint_architect, blueprint_critic = BlueprintArchitectAgent(kb={}), BlueprintCriticAgent()
        chapter_composer, literary_critic = ChapterComposerAgent(), LiteraryCriticAgent()
        poem_composer, poem_critic = PoemComposerAgent(), PoetryCriticAgent()
        forensic_agent, forensic_critic = ForensicLogicAgent(), ForensicCriticAgent()
        cultural_maestro = CulturalMaestroAgent()
        psychological_profiler = PsychologicalProfilerAgent()
        social_conflict_mapper = SocialConflictMapperAgent()
        dream_interpreter = DreamSymbolInterpreterAgent()
        chaos_agent = CreativeChaosAgent()
        frailty_agent = AuthenticFrailtyInjectorAgent()
        dramaturg, arc_agent = DramaturgAgent(), CharacterArcAgent()
        dialogue_agent, director_agent = DialogueSubtextAgent(), StagingDirectorAgent()
        designer_agent, edu_critic = InstructionalDesignerAgent(), EducationalContentCritic()

        return {
            # --- مهام الكتابة الأساسية ---
            "generate_idea": {"creator_agent": idea_generator, "creator_fn_name": "generate_idea", "critic_agent": idea_critic, "critic_fn_name": "review_idea", "default_threshold": 7.0},
            "generate_blueprint": {"creator_agent": blueprint_architect, "creator_fn_name": "generate_blueprint", "critic_agent": blueprint_critic, "critic_fn_name": "review_blueprint", "default_threshold": 8.0},
            "generate_chapter": {"creator_agent": chapter_composer, "creator_fn_name": "write_chapter", "critic_agent": literary_critic, "critic_fn_name": "review_chapter", "default_threshold": 8.0},
            "generate_poem": {"creator_agent": poem_composer, "creator_fn_name": "generate_poem", "critic_agent": poem_critic, "critic_fn_name": "review_poem", "default_threshold": 7.5},

            # --- مهام كتابة المسرحيات ---
            "generate_dramatic_blueprint": {"creator_agent": dramaturg, "creator_fn_name": "generate_dramatic_blueprint", "critic_agent": blueprint_critic, "critic_fn_name": "review_blueprint", "default_threshold": 8.0},
            "develop_character_arcs": {"creator_agent": arc_agent, "creator_fn_name": "develop_character_arcs", "critic_agent": literary_critic, "critic_fn_name": "review_character_arcs", "default_threshold": 8.0},
            "generate_play_chapter": {"creator_agent": dialogue_agent, "creator_fn_name": "generate_play_chapter", "critic_agent": literary_critic, "critic_fn_name": "review_dialogue", "default_threshold": 8.5},
            "add_staging_directions": {"creator_agent": director_agent, "creator_fn_name": "add_staging_directions", "critic_agent": literary_critic, "critic_fn_name": "review_staging", "default_threshold": 7.5},

            # --- مهام المحتوى التعليمي ---
            "design_curriculum_map": {"creator_agent": designer_agent, "creator_fn_name": "design_curriculum_map", "critic_agent": edu_critic, "critic_fn_name": "review_curriculum_map", "default_threshold": 8.0},
            
            # --- مهام التحليل المتخصصة ---
            "analyze_crime_narrative": {"creator_agent": forensic_agent, "creator_fn_name": "analyze_crime_scene", "critic_agent": forensic_critic, "critic_fn_name": "review_forensic_analysis", "default_threshold": 7.5},
            "enhance_cultural_authenticity": {"creator_agent": cultural_maestro, "creator_fn_name": "enhance_cultural_authenticity", "critic_agent": literary_critic, "critic_fn_name": "review_chapter", "default_threshold": 8.0},
            "create_psychological_profile": {"creator_agent": psychological_profiler, "creator_fn_name": "create_character_profile", "critic_agent": literary_critic, "critic_fn_name": "review_character_depth", "default_threshold": 8.5},
            "map_social_conflicts": {"creator_agent": social_conflict_mapper, "creator_fn_name": "map_social_conflicts", "critic_agent": blueprint_critic, "critic_fn_name": "review_plot_consistency", "default_threshold": 7.5},
            "generate_symbolic_dream": {"creator_agent": dream_interpreter, "creator_fn_name": "generate_symbolic_dream", "critic_agent": literary_critic, "critic_fn_name": "review_symbolism", "default_threshold": 7.0},

            # --- مهام الإبداع المتقدم ---
            "generate_disruptive_ideas": {"creator_agent": chaos_agent, "creator_fn_name": "generate_disruptive_ideas", "critic_agent": idea_critic, "critic_fn_name": "review_idea_originality", "default_threshold": 6.0},
            "humanize_text": {"creator_agent": frailty_agent, "creator_fn_name": "humanize_text", "critic_agent": literary_critic, "critic_fn_name": "review_authenticity", "default_threshold": 8.0},
        }

    async def run_refinable_task(
        self, task_name: str, initial_context: Any, user_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Received request to run task: '{task_name}'")
        
        task_definition = self._task_registry.get(task_name)
        if not task_definition:
            raise ValueError(f"Task '{task_name}' not defined.")

        creator_agent = task_definition["creator_agent"]
        critic_agent = task_definition["critic_agent"]
        
        creator_fn = getattr(creator_agent, task_definition["creator_fn_name"])
        critic_fn = getattr(critic_agent, task_definition["critic_fn_name"])

        config = user_config or {}
        quality_threshold = config.get("quality_threshold", task_definition["default_threshold"])
        max_cycles = config.get("max_refinement_cycles", 2)
        
        refinement_service = RefinementService(
            creator_fn=creator_fn, critique_fn=critic_fn,
            quality_threshold=quality_threshold, max_refinement_cycles=max_cycles
        )

        logger.info(f"Starting refinement for '{task_name}'...")
        result = await refinement_service.refine(context=initial_context)
        
        logger.info(f"Task '{task_name}' finished with score {result.get('final_score'):.1f}")
        return result

apollo = ApolloOrchestrator()
