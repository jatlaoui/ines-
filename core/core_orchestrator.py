# core/core_orchestrator.py (V7 - Hybrid Supervisor-Apprentice)
import logging
from typing import Dict, Any

# ... (كل الاستيرادات السابقة) ...
from ..agents.apprentice_local_agent import apprentice_local_agent
from ..core.llm_service import llm_service # المشرف (Gemini)
from ..core.local_llm_service import local_llm_service # المتدرب (Jan)

logger = logging.getLogger("CoreOrchestrator-V7")

class CoreOrchestrator:
    """
    المنسق الأساسي الهجين (V7).
    ينفذ بروتوكول CCTD-P لإدارة العلاقة بين المشرف (LLM قوي) والمتدرب (LLM محلي).
    """
    def __init__(self):
        # ... (تسجيل الوكلاء، بما في ذلك apprentice_local_agent) ...
        self.agents = {"apprentice": apprentice_local_agent} # كمثال
        logger.info("✅ Hybrid Supervisor-Apprentice Orchestrator (V7) Initialized.")

    async def execute_hybrid_creative_task(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        [جديد] ينفذ مهمة إبداعية باستخدام بنية المشرف-المتدرب.
        'context' يجب أن يحتوي على:
        - full_project_state: الحالة الكاملة للمشروع.
        - task_description: وصف المهمة الإبداعية (e.g., "كتابة الفصل الخامس").
        """
        full_project_state = context.get("full_project_state")
        task_description = context.get("task_description")
        logger.info(f"--- Starting Hybrid Task: {task_description} ---")

        # --- تفعيل بروتوكول CCTD-P ---

        # الخطوة 1: المتدرب يحضر موجز المهمة
        logger.info("Step 1: Apprentice is preparing the mission brief...")
        briefing_context = {
            "full_project_state": full_project_state,
            "next_task_description": task_description,
            "apprentice_task_type": "prepare_brief"
        }
        brief_result = await self.agents["apprentice"].process_task(briefing_context)
        if brief_result["status"] == "error": return brief_result
        mission_brief = brief_result["content"]["mission_brief"]

        # الخطوة 2: استدعاء المشرف (Gemini) مع السياق المضغوط
        logger.info("Step 2: Supervisor (Gemini) is performing the core creative task...")
        supervisor_prompt = f"""
بناءً على موجز المهمة التالي، اكتب المشهد الإبداعي المحوري المطلوب بأسلوب أدبي رفيع.
---
{mission_brief}
---
المشهد المحوري:
"""
        # استخدام خدمة الـ LLM القوية
        core_scene = await llm_service.generate_text_response(supervisor_prompt, temperature=0.8)
        logger.info("Supervisor has completed the core scene.")

        # الخطوة 3: المتدرب يقوم بتوسيع المشهد وتفصيله
        logger.info("Step 3: Apprentice is expanding and detailing the scene...")
        expansion_context = {
            "core_scene_from_supervisor": core_scene,
            "full_project_state": full_project_state,
            "apprentice_task_type": "expand_scene"
        }
        expansion_result = await self.agents["apprentice"].process_task(expansion_context)
        if expansion_result["status"] == "error": return expansion_result
        full_chapter = expansion_result["content"]["full_chapter"]
        
        logger.info("--- Hybrid Task Completed Successfully ---")
        return {"status": "success", "content": {"final_chapter": full_chapter}}

# ... (بقية الملف)
