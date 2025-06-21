# agents/narrative_guardian_agent.py
import logging
from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent

logger = logging.getLogger("NarrativeGuardianAgent")

class NarrativeGuardianAgent(BaseAgent):
    """
    وكيل "حارس السرد" - المسؤول عن ضمان الاتساق المنطقي للحقائق
    داخل عالم القصة على المدى الطويل.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "narrative_guardian",
            name="حارس السرد",
            description="يتحقق من الاتساق المنطقي للحقائق والأحداث في الرواية."
        )
        self.fact_database: Dict[Tuple[str, str], Any] = {} # (subject, predicate) -> object
        logger.info("✅ Narrative Guardian Agent initialized.")

    def add_fact(self, subject: str, predicate: str, obj: Any):
        """إضافة حقيقة جديدة إلى قاعدة المعرفة."""
        key = (subject.strip(), predicate.strip())
        if key not in self.fact_database:
            self.fact_database[key] = obj
            logger.info(f"FACT ADDED: ({subject}, {predicate}) -> {obj}")

    def _extract_facts_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        (محاكاة) استخلاص الحقائق من نص.
        في نظام حقيقي، سيستخدم هذا LLM لاستخلاص الحقائق الثلاثية (Subject, Predicate, Object).
        """
        facts = []
        # مثال: "كان لون عيني علي بنياً" -> (علي, لون_العينين, بني)
        if "لون عيني علي" in text and "أزرق" in text:
            facts.append({"subject": "علي", "predicate": "لون_العينين", "object": "أزرق"})
        if "مات مبروك" in text:
            facts.append({"subject": "مبروك", "predicate": "الحالة", "object": "متوفى"})
        return facts

    async def check_consistency(self, text_content: str) -> List[str]:
        """
        الوظيفة الرئيسية: تتحقق من اتساق النص الجديد مع قاعدة الحقائق.
        """
        logger.info("Guardian: Checking text for consistency...")
        
        extracted_facts = self._extract_facts_from_text(text_content)
        inconsistencies: List[str] = []

        for fact in extracted_facts:
            subject, predicate, obj = fact["subject"], fact["predicate"], fact["object"]
            key = (subject, predicate)
            
            if key in self.fact_database:
                known_obj = self.fact_database[key]
                if known_obj != obj:
                    message = (f"Inconsistency detected! The story established that '{subject}' "
                               f"'{predicate}' is '{known_obj}', but the new text states it is '{obj}'.")
                    inconsistencies.append(message)
            else:
                # إذا كانت حقيقة جديدة، أضفها
                self.add_fact(subject, predicate, obj)

        if not inconsistencies:
            logger.info("✅ Guardian: Consistency check passed.")
        else:
            logger.warning(f"Guardian: Found {len(inconsistencies)} inconsistencies.")

        return inconsistencies

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """معالجة مهمة فحص الاتساق."""
        text_to_check = context.get("text_content")
        if not text_to_check:
            return {"status": "error", "message": "No text content provided to check."}

        issues = await self.check_consistency(text_to_check)
        
        return {
            "status": "success" if not issues else "failure",
            "inconsistencies": issues,
        }

    def reset(self):
        """إعادة تعيين قاعدة الحقائق لمشروع جديد."""
        self.fact_database.clear()
        logger.info("Narrative Guardian's fact database has been reset.")

# إنشاء مثيل وحيد
narrative_guardian = NarrativeGuardianAgent()
