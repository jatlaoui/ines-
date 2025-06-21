# agents/idea_generator_agent.py (النسخة المفعّلة)

import asyncio
import logging
import random
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

# --- الاستيرادات المحدثة ---
from .base_agent import BaseAgent, AgentState  # نفترض أن BaseAgent موجود في نفس المجلد
from core.llm_service import llm_service      # استيراد خدمة LLM الحقيقية
# أدوات التحليل والمعالجة يمكن تركها للمستقبل أو استخدامها إذا كانت جاهزة
# from ..tools.text_processing_tools import TextProcessor
# from ..tools.analysis_tools import CreativityAnalyzer

logger = logging.getLogger(__name__)

class IdeaGeneratorAgent(BaseAgent):
    """
    وكيل توليد الأفكار الإبداعية.
    مهمته الرئيسية هي معالجة المهام المتعلقة بتوليد الأفكار عبر استدعاءات LLM.
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        # تم تبسيط التهيئة لتكون أكثر وضوحًا، حيث أن معظم المنطق أصبح في BaseAgent
        super().__init__(
            name="مولد الأفكار الإبداعي",
            persona="مفكر إبداعي متخصص في توليد الأفكار الأدبية المبتكرة والمستوحاة من الثقافة العربية.",
            goals=["توليد أفكار قصص وشخصيات وحبكات مبتكرة"],
            tools=["creative_thinking", "idea_generation", "concept_development"],
            agent_id=agent_id
        )
        logger.info("IdeaGeneratorAgent initialized and connected to the live LLM service.")
    
    def get_capabilities(self) -> List[str]:
        """إرجاع قدرات الوكيل"""
        return [
            "story_ideas", "character_ideas", "plot_twists", "world_building", 
            "theme_exploration", "brainstorming", "idea_expansion", "conflict_generation"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        المعالج الرئيسي للمهام. يوجه كل نوع مهمة إلى الدالة المناسبة.
        """
        try:
            self.update_state(AgentState.WORKING)
            start_time = datetime.now()
            
            task_type = task.get("type")
            if not task_type or task_type not in self.get_capabilities():
                raise ValueError(f"نوع مهمة غير مدعوم أو مفقود: {task_type}")

            logger.info(f"Processing task of type: '{task_type}'")
            
            # --- التوجيه إلى الدالة المناسبة ---
            handler_map = {
                "story_ideas": self._generate_story_ideas,
                "character_ideas": self._generate_character_ideas,
                "plot_twists": self._generate_plot_twists,
                # ... يمكن إضافة بقية المعالجات هنا بنفس الطريقة
            }
            
            handler = handler_map.get(task_type)
            if not handler:
                 raise NotImplementedError(f"Handler for task type '{task_type}' is not implemented yet.")
                 
            # استدعاء المعالج المناسب
            result = await handler(task)
            
            # التأكد من عدم وجود خطأ في الرد
            if result.get("status") == "error":
                raise RuntimeError(f"LLM task failed: {result.get('message')}")
            
            # إضافة بيانات وصفية للنتيجة
            processing_time = (datetime.now() - start_time).total_seconds()
            result["processing_time"] = processing_time
            result["generator_agent_id"] = self.id
            
            self.update_state(AgentState.COMPLETED)
            logger.info(f"Task '{task_type}' completed successfully in {processing_time:.2f}s.")
            
            return result
            
        except Exception as e:
            self.update_state(AgentState.ERROR, context={"error": str(e)})
            logger.error(f"Error processing task '{task.get('type')}' in IdeaGeneratorAgent: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    # --- معالجات المهام المتخصصة ---

    async def _generate_story_ideas(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """يولد مجموعة من أفكار القصص."""
        seed = task_context.get("seed", "")
        options = task_context.get("options", {})
        count = options.get("count", 3)
        creativity_level = options.get("creativity", "moderate")
        genre = options.get("genre", "عام")
        
        prompt = self._build_story_ideas_prompt(seed, count, creativity_level, genre)
        response = await llm_service.generate_json_response(prompt, temperature=0.9)
        
        if "error" in response:
            return {"status": "error", "message": "Failed to get story ideas from LLM.", "details": response}
            
        return {"status": "success", "ideas": response.get("ideas", [])}

    async def _generate_character_ideas(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """يولد مجموعة من مفاهيم الشخصيات."""
        seed = task_context.get("seed", "")
        options = task_context.get("options", {})
        count = options.get("count", 3)
        
        prompt = self._build_character_ideas_prompt(seed, count)
        response = await llm_service.generate_json_response(prompt, temperature=0.8)

        if "error" in response:
            return {"status": "error", "message": "Failed to get character ideas from LLM.", "details": response}
            
        return {"status": "success", "characters": response.get("characters", [])}

    async def _generate_plot_twists(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """يولد مجموعة من المفاجآت في الحبكة."""
        seed = task_context.get("seed", "") # seed هنا يمكن أن يكون ملخص الحبكة
        options = task_context.get("options", {})
        count = options.get("count", 3)
        
        prompt = self._build_plot_twists_prompt(seed, count)
        response = await llm_service.generate_json_response(prompt, temperature=1.0) # حرارة أعلى للإبداع

        if "error" in response:
            return {"status": "error", "message": "Failed to get plot twists from LLM.", "details": response}
            
        return {"status": "success", "twists": response.get("twists", [])}

    # --- دوال بناء الـ Prompts (محسنة لـ Gemini) ---

    def _build_story_ideas_prompt(self, seed: str, count: int, creativity: str, genre: str) -> str:
        creativity_map = {
            "moderate": "أفكار مبتكرة تحترم التقاليد السردية.",
            "bold": "أفكار جريئة وغير متوقعة تكسر القوالب.",
            "experimental": "أفكار تجريبية تتحدى مفهوم القصة نفسه."
        }
        
        return f"""
مهمتك: أنت خبير في توليد الأفكار الأدبية. قم بإنشاء {count} أفكار قصص فريدة بناءً على الإلهام التالي.
**الإلهام الأولي:** "{seed}"
**النوع الأدبي المطلوب:** {genre}
**مستوى الإبداع المطلوب:** {creativity_map.get(creativity, creativity_map['moderate'])}

أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يحتوي الرد على مفتاح واحد هو "ideas"، وقيمته قائمة (list) من الكائنات (objects).
كل كائن في القائمة يجب أن يتبع المخطط التالي:
{{
  "title": "string // عنوان جذاب للفكرة.",
  "premise": "string // الفكرة الأساسية للقصة في جملتين كحد أقصى.",
  "theme": "string // الموضوع الرئيسي الذي تعالجه القصة.",
  "hook": "string // جملة افتتاحية أو سؤال يثير فضول القارئ."
}}
"""

    def _build_character_ideas_prompt(self, seed: str, count: int) -> str:
        return f"""
مهمتك: أنت خبير في تطوير الشخصيات. قم بتصميم {count} شخصية فريدة ومعقدة يمكن أن توجد في قصة تدور حول: "{seed}".
ركز على خلق شخصيات ذات دوافع وصراعات داخلية واضحة.

أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يحتوي الرد على مفتاح واحد هو "characters"، وقيمته قائمة (list) من الكائنات (objects).
كل كائن في القائمة يجب أن يتبع المخطط التالي:
{{
  "name": "string // اسم الشخصية.",
  "archetype": "string // النمط الأصلي للشخصية (مثال: البطل، المرشد، المحتال).",
  "motivation": "string // الدافع الأساسي الذي يحرك الشخصية (ماذا تريد أكثر من أي شيء آخر؟).",
  "conflict": "string // الصراع الداخلي أو الخارجي الرئيسي الذي تواجهه الشخصية."
}}
"""

    def _build_plot_twists_prompt(self, plot_summary: str, count: int) -> str:
        return f"""
مهمتك: أنت كاتب سيناريو محترف وخبير في المفاجآت الدرامية.
بناءً على ملخص الحبكة التالي، قم بتوليد {count} مفاجآت (plot twists) غير متوقعة يمكن أن تغير مسار القصة بالكامل.
**ملخص الحبكة:** "{plot_summary}"

أرجع ردك **حصريًا** بتنسيق JSON صالح. يجب أن يحتوي الرد على مفتاح واحد هو "twists"، وقيمته قائمة (list) من الكائنات (objects).
كل كائن في القائمة يجب أن يتبع المخطط التالي:
{{
  "twist_title": "string // عنوان للمفاجأة (مثال: الخائن غير المتوقع).",
  "description": "string // شرح للمفاجأة وكيف تغير القصة.",
  "impact": "string // التأثير المتوقع على الشخصيات والجمهور."
}}
"""
