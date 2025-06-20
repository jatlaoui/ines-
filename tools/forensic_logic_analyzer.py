# tools/forensic_logic_analyzer.py
"""
Forensic Logic Analyzer
أداة متخصصة لضمان الدقة الإجرائية في روايات الجريمة والغموض.
"""
import logging
import re
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger("ForensicLogicAnalyzer")

class EvidenceType(Enum):
    PHYSICAL = "مادي"
    BIOLOGICAL = "بيولوجي"
    DIGITAL = "رقمي"
    TESTIMONIAL = "شهادة"

class CrimeType(Enum):
    MURDER = "جريمة قتل"
    THEFT = "سرقة"
    FRAUD = "احتيال"

class ForensicLogicAnalyzer:
    """
    أداة لتحليل المنطق الجنائي في النصوص السردية.
    """
    def __init__(self):
        self.procedural_checklist = {
            CrimeType.MURDER: [
                "تأمين مسرح الجريمة", "استدعاء الطبيب الشرعي", "توثيق الأدلة",
                "جمع العينات البيولوجية", "البحث عن سلاح الجريمة"
            ],
            CrimeType.THEFT: [
                "فحص نقاط الدخول والخروج", "البحث عن بصمات", "جرد المسروقات",
                "مراجعة كاميرات المراقبة"
            ]
        }
        logger.info("ForensicLogicAnalyzer initialized.")

    async def analyze(self, content: str, context: Dict, options: Dict) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: تقوم بتحليل شامل للمنطق الجنائي في النص.
        """
        logger.info("Performing forensic logic analysis...")
        
        crime_type = await self._identify_crime_type(content)
        evidence_map = await self._extract_evidence(content)
        timeline = await self._construct_timeline(content)
        inconsistencies = await self._detect_logical_inconsistencies(timeline, evidence_map)
        procedural_errors = await self._detect_procedural_errors(content, crime_type)
        
        analysis = {
            "crime_type": crime_type.value,
            "evidence_count": len(evidence_map),
            "timeline_events": len(timeline),
            "inconsistencies_count": len(inconsistencies),
            "procedural_errors_count": len(procedural_errors),
            "evidence_map": evidence_map,
            "timeline": timeline,
            "inconsistencies": inconsistencies,
            "procedural_errors": procedural_errors
        }

        # محاكاة لتقييم الثقة
        confidence_score = 0.9 - (len(inconsistencies) * 0.1) - (len(procedural_errors) * 0.1)
        
        return {
            "analysis": analysis,
            "confidence_score": max(0, confidence_score),
            "recommendations": self._generate_recommendations(analysis),
            "visual_data": {} # يمكن إضافة بيانات للرسم البياني هنا
        }

    async def _identify_crime_type(self, text: str) -> CrimeType:
        """تحديد نوع الجريمة من النص."""
        text_lower = text.lower()
        if any(kw in text_lower for kw in ["قتل", "جثة", "مقتول"]):
            return CrimeType.MURDER
        if any(kw in text_lower for kw in ["سرقة", "لص", "مسروقات"]):
            return CrimeType.THEFT
        if any(kw in text_lower for kw in ["احتيال", "تزوير", "نصب"]):
            return CrimeType.FRAUD
        return CrimeType.MURDER # Default

    async def _extract_evidence(self, text: str) -> Dict[str, Any]:
        """استخلاص الأدلة المذكورة في النص."""
        evidence_map = {}
        patterns = {
            "سكين": EvidenceType.PHYSICAL,
            "بصمات": EvidenceType.PHYSICAL,
            "دم": EvidenceType.BIOLOGICAL,
            "رسالة": EvidenceType.PHYSICAL,
            "كاميرا مراقبة": EvidenceType.DIGITAL,
            "شهادة جار": EvidenceType.TESTIMONIAL,
        }
        for evidence, ev_type in patterns.items():
            if evidence in text:
                evidence_map[evidence] = {"type": ev_type.value, "status": "موجود في مسرح الجريمة"}
        return evidence_map

    async def _construct_timeline(self, text: str) -> List[str]:
        """بناء خط زمني بسيط للأحداث."""
        events = re.findall(r"في (.*?): (.*?)\.", text)
        if not events:
            return ["منتصف الليل: سماع صراخ", "الصباح التالي: اكتشاف الجريمة"]
        return [f"{time}: {event}" for time, event in events]

    async def _detect_logical_inconsistencies(self, timeline: List, evidence: Dict) -> List[str]:
        """كشف التناقضات المنطقية."""
        errors = []
        if "سكين" in evidence and "بصمات" not in evidence:
            errors.append("تم العثور على سكين ولكن لم يتم ذكر البحث عن بصمات عليه.")
        if len(timeline) > 1 and "الصباح التالي" in timeline[1] and "منتصف الليل" in timeline[0]:
            pass # منطقي
        else:
            errors.append("تسلسل زمني غير واضح أو غير منطقي.")
        return errors

    async def _detect_procedural_errors(self, text: str, crime_type: CrimeType) -> List[str]:
        """كشف الأخطاء الإجرائية في التحقيق."""
        errors = []
        checklist = self.procedural_checklist.get(crime_type, [])
        for procedure in checklist:
            if procedure not in text:
                errors.append(f"خطأ إجرائي: لم يتم ذكر '{procedure}'.")
        return errors
        
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """توليد توصيات لتحسين الحبكة الجنائية."""
        recs = []
        if analysis["inconsistencies"]:
            recs.append("قم بمعالجة التناقضات المنطقية لزيادة واقعية القصة.")
        if analysis["procedural_errors"]:
            recs.append("أضف التفاصيل الإجرائية الصحيحة لجعل التحقيق أكثر مصداقية.")
        recs.append("فكر في إضافة 'دليل مضلل' (Red Herring) لزيادة التشويق.")
        return recs
