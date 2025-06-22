# agents/fusion_synthesizer_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..core.llm_service import llm_service
# هذا الوكيل سيستدعي وكلاء آخرين لتحليل المصادر
from .soul_profiler_agent import soul_profiler_agent
from .blueprint_architect_agent import blueprint_architect
from .fusion_arbitrator_agent import fusion_arbitrator_agent

logger = logging.getLogger("FusionSynthesizerAgent")

class FusionSynthesizerAgent(BaseAgent):
    """
    وكيل "الاندماج والتخليق السردي".
    متخصص في تحليل ودمج عملين أو أكثر لإنتاج عمل إبداعي جديد.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "fusion_synthesizer",
            name="مُخلِّق السرد الفائق",
            description="يدمج بين عوالم وشخصيات وأساليب مختلفة لخلق أعمال جديدة."
        )

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        يعالج مهام الاندماج المختلفة: التحليل، التخليق، أو التحكيم.
        """
        task_type = context.get("fusion_task_type")
        if not task_type:
            return {"status": "error", "message": "Fusion task type is required."}

        if task_type == "analyze_compatibility":
            return await self.analyze_compatibility(context)
        elif task_type == "synthesize_narrative":
            return await self.synthesize_narrative(context)
        else:
            return {"status": "error", "message": f"Unknown fusion task type: {task_type}"}

    async def analyze_compatibility(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        يحلل مصدرين أو أكثر ويقيم درجة التوافق بينهما.
        'context' يجب أن يحتوي على:
        - sources: قائمة من القواميس، كل قاموس يحتوي على 'type' و 'content'.
        """
        sources = context.get("sources", [])
        if len(sources) < 2:
            return {"status": "error", "message": "At least two sources are required for compatibility analysis."}

        logger.info(f"Analyzing compatibility between {len(sources)} narrative sources...")
        
        # 1. تحليل الهوية السردية لكل مصدر
        narrative_identities = []
        for src in sources:
            # استخدام SoulProfiler لتحليل الأسلوب والشخصيات والمواضيع
            identity = await soul_profiler_agent.process_task({"text_content": src["content"]})
            narrative_identities.append(identity.get("profile", {}))

        # 2. تقييم التوافق باستخدام LLM
        prompt = self._build_compatibility_prompt(narrative_identities)
        compatibility_report = await llm_service.generate_json_response(prompt, temperature=0.2)

        return {
            "status": "success",
            "content": {
                "narrative_identities": narrative_identities,
                "compatibility_report": compatibility_report
            },
            "summary": "Compatibility analysis complete."
        }

    def _build_compatibility_prompt(self, identities: List[Dict]) -> str:
        identities_text = "\n\n---\n\n".join([str(identity) for identity in identities])
        return f"""
مهمتك: أنت ناقد أدبي وخبير في نظرية السرد المقارن. لديك الهويات السردية لعدة أعمال أدبية.

**الهويات السردية للمصادر:**
{identities_text}

**المطلوب:**
1.  **احسب "درجة التوافق" (compatibility_score)** بين هذه الأعمال (من 0.0 إلى 1.0)، حيث 1.0 يعني توافقًا تامًا.
2.  **حدد "نقاط التوتر" (tension_points):** العناصر التي قد تتعارض بشدة (مثل قيم الشخصيات، قوانين العالم).
3.  **حدد "نقاط الانسجام" (harmony_points):** العناصر المشتركة التي يمكن أن تكون أساسًا للدمج (مثل المواضيع المتشابهة).
4.  **اقترح "استراتيجية الدمج المثلى" (optimal_fusion_strategy):** (مثال: "دمج شخصية من المصدر أ في عالم المصدر ب"، "كتابة قصة جديدة تجمع بين أسلوب أ وموضوع ب").

أرجع ردك **حصريًا** بتنسيق JSON.
"""

    async def synthesize_narrative(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        يقوم بعملية التخليق الفعلية بناءً على مخطط الاندماج.
        'context' يجب أن يحتوي على:
        - fusion_blueprint: مخطط الاندماج الذي يحدد الاستراتيجية.
        - narrative_identities: الهويات السردية للمصادر.
        """
        blueprint = context.get("fusion_blueprint")
        identities = context.get("narrative_identities")

        if not blueprint or not identities:
            return {"status": "error", "message": "Fusion blueprint and narrative identities are required."}
            
        logger.info(f"Synthesizing new narrative based on strategy: '{blueprint.get('fusion_strategy')}'")

        # بناء الـ prompt النهائي للتخليق
        prompt = self._build_synthesis_prompt(blueprint, identities)
        synthesized_text = await llm_service.generate_text_response(prompt, temperature=0.8)

        # التحكيم الأولي في جودة المخرج
        arbitration_report = await fusion_arbitrator_agent.process_task({"synthesized_narrative": synthesized_text})

        return {
            "status": "success",
            "content": {
                "synthesized_narrative": synthesized_text,
                "initial_arbitration": arbitration_report.get("content")
            },
            "summary": "Narrative synthesis and initial arbitration complete."
        }

    def _build_synthesis_prompt(self, blueprint: Dict, identities: List[Dict]) -> str:
        # هذا الـ prompt هو قلب العملية الإبداعية، وسيكون معقدًا جدًا
        # يعتمد على تفاصيل المخطط. هذا مثال مبسط.
        strategy = blueprint.get("fusion_strategy", "No strategy defined.")
        
        return f"""
مهمتك: أنت روائي تجريبي عبقري، قادر على دمج عوالم وأساليب مختلفة في عمل فني واحد متماسك.

**الهويات السردية للمصادر:**
{identities}

**مخطط واستراتيجية الاندماج المطلوبة:**
{strategy}

**المطلوب:**
اكتب الآن الفصل الأول من هذا العمل الهجين. يجب أن يكون النص الناتج متماسكًا، ومبدعًا، ويحترم استراتيجية الدمج المحددة. اكتب باللغة العربية الفصحى وبأسلوب أدبي رفيع.

**الفصل الأول:**
"""

# إنشاء مثيل وحيد
fusion_synthesizer_agent = FusionSynthesizerAgent()
