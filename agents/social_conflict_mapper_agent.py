# agents/social_conflict_mapper_agent.py (V2 - Functional)
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from ..core.llm_service import llm_service

logger = logging.getLogger("SocialConflictMapperAgent")

class SocialConflictMapperAgent(BaseAgent):
    """
    وكيل مخطط الصراعات الاجتماعية (V2).
    يستخدم LLM لتحليل النصوص وتحديد المجموعات الاجتماعية،
    نقاط التوتر بينها، وديناميكيات القوة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "social_conflict_mapper",
            name="مخطط الصراعات الاجتماعية",
            description="يحلل ويبني الصراعات بين الطبقات والمجموعات الاجتماعية في القصة."
        )
        logger.info("✅ Functional Social Conflict Mapper Agent (V2) Initialized.")
        
    async def map_social_conflicts(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: إنشاء خريطة للصراعات الاجتماعية.
        """
        text_content = context.get("text_content")
        setting_description = context.get("setting_description", "مدينة عربية معاصرة")
        
        if not text_content:
            return {"status": "error", "message": "Text content is required to map conflicts."}
            
        logger.info(f"Mapping social conflicts in setting: '{setting_description}'...")
        
        prompt = self._build_mapping_prompt(text_content, setting_description)
        conflict_map = await llm_service.generate_json_response(prompt, temperature=0.3)

        if "error" in conflict_map:
            return {"status": "error", "message": "LLM call for conflict mapping failed.", "details": conflict_map}

        return {
            "status": "success",
            "content": {"conflict_map": conflict_map},
            "summary": f"Social conflict map generated with {len(conflict_map.get('involved_groups', []))} groups."
        }
        
    def _build_mapping_prompt(self, text: str, setting: str) -> str:
        return f"""
مهمتك: أنت عالم اجتماع ومحلل سياسي، متخصص في بناء الديناميكيات الاجتماعية للسرد الروائي.

**وصف العالم والسياق:**
{setting}

**النص للتحليل (يصف شخصيات وتفاعلات داخل هذا العالم):**
---
{text}
---

**التعليمات:**
بناءً على النص والسياق، قم بإنشاء "خريطة صراع" اجتماعية. أرجع ردك **حصريًا** بتنسيق JSON.
1.  **involved_groups:** حدد أبرز 2-3 مجموعات اجتماعية أو طبقات موجودة في النص (مثال: "الطبقة الأرستقراطية القديمة"، "العمال الكادحون"، "الشباب المثقف الطموح").
2.  **main_conflict:** صف الصراع الرئيسي بين هذه المجموعات في جملة واحدة (مثال: "صراع على النفوذ والموارد بين النخبة التقليدية والتجار الجدد").
3.  **tension_points:** اذكر 3 نقاط توتر محددة تظهر هذا الصراع (مثال: "فجوة الأجور"، "الوصول إلى التعليم"، "التحكم في الأراضي").
4.  **power_dynamics:** صف بإيجاز ديناميكية القوة (من يملك السلطة ومن يسعى إليها).

**خريطة الصراع (JSON):**
"""

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.map_social_conflicts(context)

# إنشاء مثيل وحيد
social_conflict_mapper_agent = SocialConflictMapperAgent()
```**شرح الترقية:** مرة أخرى، بدلاً من الاعتماد على قائمة ثابتة من الطبقات الاجتماعية، يقوم الوكيل الآن بتمرير النص إلى الـ LLM ويطلب منه **استنتاج** المجموعات الاجتماعية والصراعات مباشرة من سياق القصة. هذا يجعله قادرًا على تحليل أي نوع من الصراعات (طبقي، ديني، عرقي، إلخ) بدلاً من أن يكون مقيدًا بما تم تعريفه مسبقًا.

---
### **الخلاصة**
بهذه الترقية، قمنا بسد الفجوة التي حددتها بدقة. لقد حولنا ثلاثة من أهم الوكلاء المتخصصين من مجرد "وظائف وهمية" إلى **أدوات تحليلية حقيقية وقوية** تعتمد على قدرة نماذج اللغة الكبيرة على الاستدلال والتصنيف والتوليد ضمن أطر عمل محددة. نظام "إينيس" الآن أصبح أكثر فعالية بكثير وجاهزًا لإنتاج مخرجات ذات عمق نفسي ومنطقي واجتماعي حقيقي.
