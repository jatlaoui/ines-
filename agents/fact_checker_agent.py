# agents/fact_checker_agent.py (وكيل جديد يدمج الأدوات)
import logging
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent
from ..tools.witness_extractor_tool import WitnessExtractorTool # نفترض وجود هذه الأداة
from ..services.web_search_service import web_inspiration_service # خدمة البحث
from ..core.llm_service import llm_service

logger = logging.getLogger("FactCheckerAgent")

class FactCheckerAgent(BaseAgent):
    """
    وكيل متخصص في التحقق من الحقائق والمصداقية.
    يستخلص الادعاءات من النص ويتحقق منها عبر البحث في الويب.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "fact_checker",
            name="مدقق الحقائق",
            description="يتحقق من صحة الادعاءات الواردة في النصوص عبر مصادر خارجية."
        )
        self.extractor = WitnessExtractorTool() # أداة استخلاص الادعاءات
        self.search_service = web_inspiration_service

    async def verify_text_credibility(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يتحقق من مصداقية نص معين.
        """
        text_content = context.get("text_content")
        if not text_content:
            return {"status": "error", "message": "Text content is required."}

        logger.info("Fact Checker: Verifying text credibility...")

        # 1. استخلاص الادعاءات القابلة للتحقق
        # في نظام حقيقي، ستكون هذه دالة متخصصة في WitnessExtractorTool
        claims = self._extract_verifiable_claims(text_content)
        if not claims:
            return {"status": "success", "content": {"credibility_score": 0.8, "verified_claims": []}, "summary": "No verifiable claims found."}

        # 2. التحقق من كل ادعاء
        verified_claims = []
        for claim in claims:
            verification_result = await self._cross_reference_claim(claim)
            verified_claims.append(verification_result)
        
        # 3. حساب درجة المصداقية الإجمالية
        overall_score = self._calculate_overall_credibility(verified_claims)

        return {
            "status": "success",
            "content": {"credibility_score": overall_score, "verified_claims": verified_claims},
            "summary": f"Credibility assessment complete with a score of {overall_score:.2f}."
        }

    def _extract_verifiable_claims(self, text: str) -> List[str]:
        """(محاكاة) يستخلص الادعاءات التي يمكن التحقق منها."""
        # مثال: "في عام 1992، تم تمرير قانون يسمح ببيع الأراضي"
        claims = []
        if "عام 1992" in text and "قانون" in text:
            claims.append("تم تمرير قانون بيع الأراضي في تونس عام 1992")
        return claims

    async def _cross_reference_claim(self, claim: str) -> Dict:
        """يتحقق من صحة ادعاء واحد عبر البحث."""
        logger.info(f"Cross-referencing claim: '{claim}'")
        # في نظام حقيقي، سنقوم بالبحث الفعلي
        # search_results = await self.search_service.search(claim)
        
        # محاكاة لنتيجة البحث
        # لنفترض أننا وجدنا مصدرًا موثوقًا يؤكد الادعاء
        is_supported = True
        supporting_sources = ["الرائد الرسمي للجمهورية التونسية، 1992"]
        
        return {
            "claim": claim,
            "is_supported": is_supported,
            "supporting_sources": supporting_sources
        }

    def _calculate_overall_credibility(self, verified_claims: List[Dict]) -> float:
        if not verified_claims:
            return 0.8 # درجة افتراضية إذا لم تكن هناك ادعاءات
        
        supported_count = sum(1 for claim in verified_claims if claim["is_supported"])
        return supported_count / len(verified_claims)

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.verify_text_credibility(context)

# إنشاء مثيل وحيد
fact_checker_agent = FactCheckerAgent()
