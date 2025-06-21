# core/apollo_orchestrator.py (النسخة النهائية مع البحث الهجين والذاكرة الدائمة)

import logging
import json
import asyncio
from typing import Any, Dict, List, Optional

# --- استيراد الخدمات الأساسية المفعّلة ---
from core.llm_service import llm_service
from core.database_service import db_service # خدمة قاعدة البيانات السحابية
from core.refinement_service import RefinementService
# خدمة البحث في الويب (سنقوم بمحاكاتها الآن، ويمكن استبدالها بـ Tavily أو Searper لاحقًا)
from services.web_search_service import web_search_service 

# --- استيراد الوكلاء ---
# نستورد الكلاسات فقط، لأننا سننشئ المثيلات ديناميكيًا
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.blueprint_architect_agent import BlueprintArchitectAgent
from agents.chapter_composer_agent import ChapterComposerAgent
from agents.literary_critic_agent import LiteraryCriticAgent
from agents.psychological_profiler_agent import PsychologicalProfilerAgent
from agents.cultural_maestro_agent import CulturalMaestroAgent

# --- إعدادات التسجيل ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s')
logger = logging.getLogger("ApolloOrchestrator")

class ApolloOrchestrator:
    """
    المايسترو "أبولو" - المنسق المركزي لمجتمع الوكلاء.
    يدير المهام، وينسق بين الوكلاء، ويستخدم بروتوكول بحث هجين (قاعدة بيانات + ويب)
    لضمان أفضل النتائج الممكنة.
    """
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self._task_registry: Dict[str, Dict[str, Any]] = {}
        self.is_initialized = False

    async def initialize(self):
        """
        تهيئة المنسق. يتم فصلها عن __init__ للسماح بالعمليات غير المتزامنة.
        سيقوم بجلب الوكلاء من قاعدة البيانات أو إنشائهم إذا لم يكونوا موجودين.
        """
        if self.is_initialized:
            return

        logger.info("🚀 Initializing Apollo Orchestrator...")
        
        # 1. جلب الوكلاء من قاعدة البيانات
        agents_from_db = await db_service.get_all_agents()
        
        if agents_from_db.get("status") == "success" and agents_from_db.get("data"):
            logger.info(f"Found {len(agents_from_db['data'])} agents in the database. Loading them...")
            for agent_data in agents_from_db['data']:
                # (منطق متقدم لإعادة إنشاء الكائنات من البيانات، سيتم تبسيطه الآن)
                self.agents[agent_data['name']] = globals()[agent_data['class_name']]()
        else:
            # 2. إذا كانت قاعدة البيانات فارغة، قم بإنشاء الوكلاء الافتراضيين وحفظهم
            logger.info("No agents found in DB. Creating and registering default agents...")
            await self._create_and_register_default_agents()
            
        # 3. بناء سجل المهام بناءً على الوكلاء المتاحين
        self._task_registry = self._build_task_registry()
        
        self.is_initialized = True
        logger.info(f"✅ Apollo Orchestrator initialized successfully. Registered tasks: {list(self._task_registry.keys())}")

    async def _create_and_register_default_agents(self):
        """
        ينشئ الوكلاء الافتراضيين ويحفظهم في قاعدة البيانات السحابية.
        """
        default_agents_classes = {
            "مولد الأفكار": IdeaGeneratorAgent,
            "مهندس المخططات": BlueprintArchitectAgent,
            "مؤلف الفصول": ChapterComposerAgent,
            "الناقد الأدبي": LiteraryCriticAgent,
            "المحلل النفسي للشخصيات": PsychologicalProfilerAgent,
            "الخبير الثقافي": CulturalMaestroAgent,
        }

        for name, agent_class in default_agents_classes.items():
            agent_instance = agent_class()
            self.agents[name] = agent_instance
            
            agent_data_to_save = {
                "agent_id": agent_instance.id,
                "name": agent_instance.name,
                "description": agent_instance.description,
                "class_name": agent_instance.__class__.__name__,
                "capabilities": json.dumps(agent_instance.get_capabilities())
            }
            await db_service.add_agent(agent_data_to_save)

    def _build_task_registry(self) -> Dict[str, Dict[str, Any]]:
        """يبني سجل المهام بناءً على الوكلاء الذين تم تحميلهم."""
        return {
            "analyze_psychological_profile": {
                "handler_agent": self.agents.get("المحلل النفسي للشخصيات"),
                "handler_fn_name": "create_profile",
            },
            "enrich_text_culturally": {
                "handler_agent": self.agents.get("الخبير الثقافي"),
                "handler_fn_name": "enrich_text",
            },
            "generate_idea": {
                "creator_agent": self.agents.get("مولد الأفكار"),
                "creator_fn_name": "generate_idea",
                "critic_agent": self.agents.get("الناقد الأدبي"),
                "critic_fn_name": "review_idea",
                "default_threshold": 7.0
            },
            "develop_blueprint": {
                "creator_agent": self.agents.get("مهندس المخططات"),
                "creator_fn_name": "create_blueprint",
                "critic_agent": self.agents.get("الناقد الأدبي"),
                "critic_fn_name": "review_blueprint",
                "default_threshold": 7.5
            },
            "compose_chapter": {
                "creator_agent": self.agents.get("مؤلف الفصول"),
                "creator_fn_name": "write_chapter",
                "critic_agent": self.agents.get("الناقد الأدبي"),
                "critic_fn_name": "review_chapter",
                "default_threshold": 8.0
            },
        }
    
    async def _jit_research(self, topic: str) -> Dict[str, Any]:
        """
        بروتوكول البحث الوقتي (Just-in-Time Research).
        يبحث في الويب عند الحاجة لبناء قاعدة معرفة مؤقتة.
        """
        logger.info(f"🧠 JIT Research Protocol activated for topic: '{topic}'")
        
        # الخطوة 1: البحث في الويب
        search_results = await web_search_service.search(f"معلومات مفصلة عن {topic}")
        if not search_results or search_results.get("status") != "success":
            logger.warning("Web search failed or returned no results.")
            return {"error": "Web search failed."}
            
        # الخطوة 2: تحليل أهم نتيجة لبناء قاعدة معرفة مؤقتة
        # (في نظام حقيقي، قد نحلل أفضل 3 نتائج)
        top_result_content = search_results.get("data", [{}])[0].get("content", "")
        if not top_result_content:
            logger.warning("No content found in top web search result.")
            return {"error": "No content in web search results."}

        # استخدام وكيل تحليل السياق (الذي يجب أن يكون متاحًا)
        from engines.advanced_context_engine import AdvancedContextEngine
        context_engine = AdvancedContextEngine()
        
        logger.info("Building temporary KnowledgeBase from web content...")
        temp_kb = await context_engine.analyze_text(top_result_content)
        
        return {"status": "success", "knowledge_base": temp_kb.dict()}

    async def run_task(self, task_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        المنفذ العام الموحد. يدير دورة المهمة الكاملة، بما في ذلك البحث الهجين.
        """
        if not self.is_initialized:
            await self.initialize()

        logger.info(f"▶️ Received task: '{task_name}' with context keys: {list(context.keys())}")
        
        # --- بروتوكول البحث الهجين ---
        if context.get("requires_deep_knowledge") and not context.get("knowledge_base"):
            topic = context.get("topic")
            # 1. البحث في الذاكرة الدائمة (Supabase)
            db_knowledge = await db_service.get_knowledge(topic)
            
            if db_knowledge.get("status") == "success":
                logger.info(f"Found knowledge for '{topic}' in permanent memory (Supabase).")
                context["knowledge_base"] = db_knowledge["data"]
            else:
                # 2. إذا لم تكن موجودة، ابحث في الويب
                logger.info(f"No permanent knowledge for '{topic}'. Initiating JIT web research...")
                web_knowledge = await self._jit_research(topic)
                if web_knowledge.get("status") == "success":
                    context["knowledge_base"] = web_knowledge["knowledge_base"]
                    # (اختياري) يمكن إضافة منطق لحفظ هذه المعرفة الجديدة في Supabase للوصول إليها لاحقًا
                    # await db_service.save_knowledge(topic, web_knowledge["knowledge_base"])
        
        # --- تنفيذ المهمة ---
        task_def = self._task_registry.get(task_name)
        if not task_def:
            raise ValueError(f"Task '{task_name}' not found.")

        # التحقق من وجود الوكلاء المطلوبين
        for key in ["handler_agent", "creator_agent", "critic_agent"]:
            if key in task_def and not task_def[key]:
                 raise RuntimeError(f"Agent for '{key}' in task '{task_name}' is not available.")
        
        # تنفيذ المهام القابلة للتحسين
        if "creator_fn_name" in task_def:
            refinement_service = RefinementService(
                creator_fn=getattr(task_def["creator_agent"], task_def["creator_fn_name"]),
                critique_fn=getattr(task_def["critic_agent"], task_def["critic_fn_name"]),
                quality_threshold=task_def.get("default_threshold", 8.0)
            )
            return await refinement_service.refine(context)
        
        # تنفيذ المهام التحليلية المباشرة
        elif "handler_fn_name" in task_def:
            return await getattr(task_def["handler_agent"], task_def["handler_fn_name"])(context)
            
        else:
            raise NotImplementedError(f"Task type for '{task_name}' is not implemented.")

# --- إنشاء مثيل وحيد ---
apollo = ApolloOrchestrator()

# --- قسم الاختبار ---
async def main_test():
    # تأكد من أن متغيرات البيئة لـ GEMINI و SUPABASE معينة
    logger.info("\n" + "="*80)
    logger.info("🎭 Apollo Orchestrator - Hybrid Knowledge & Creative Cycle Test 🎭")
    logger.info("="*80)
    
    # تهيئة المنسق (مهم جدًا)
    await apollo.initialize()

    # --- اختبار مهمة تتطلب معرفة عميقة ---
    logger.info("\n--- TESTING TASK WITH DEEP KNOWLEDGE REQUIREMENT ---")
    
    # السياق يحدد الموضوع وأنه يحتاج معرفة، لكنه لا يوفرها
    context_for_research = {
        "topic": "صالح بن يوسف",
        "requires_deep_knowledge": True
    }
    
    # نتوقع من أبولو أن يقوم بالبحث الوقتي (JIT Research)
    blueprint_result = await apollo.run_task(
        task_name="develop_blueprint",
        context=context_for_research
    )
    
    if blueprint_result.get("status") == "success":
        logger.info("✅ Blueprint created successfully using JIT web research!")
        # طباعة ملخص فقط
        bp_content = blueprint_result.get("final_content", {}).get("blueprint", {})
        print(f"  - Blueprint Introduction: {bp_content.get('introduction', 'N/A')[:100]}...")
        print(f"  - Number of Chapters: {len(bp_content.get('chapters', []))}")
    else:
        logger.error(f"❌ Failed to create blueprint with JIT research. Result: {blueprint_result}")

if __name__ == "__main__":
    asyncio.run(main_test())
