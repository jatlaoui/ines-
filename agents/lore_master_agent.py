# agents/lore_master_agent.py (وكيل جديد)
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_agent import BaseAgent
# يفترض أن هذا الوكيل لديه وصول إلى قاعدة البيانات أو إلى مخرجات المهام المجمعة
from ..core.core_database import core_db # كمثال للوصول المباشر
from ..core.core_orchestrator import CoreOrchestrator # للحصول على حالة التنفيذ

logger = logging.getLogger("LoreMasterAgent")

class LoreMasterAgent(BaseAgent):
    """
    وكيل "سيد المعارف" (LoreMaster).
    متخصص في تجميع وتنظيم وتحليل كل المعرفة المتراكمة خلال
    عملية الكتابة لإنتاج "الكتاب المقدس للقصة" (Story Bible).
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id or "lore_master",
            name="سيد المعارف",
            description="ينظم المعرفة السردية وينشئ الكتاب المقدس للقصة."
        )

    async def generate_story_bible(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يجمع كل البيانات من سير عمل مكتمل وينشئ الكتاب المقدس للقصة.
        'context' يجب أن يحتوي على:
        - execution: كائن تنفيذ سير العمل المكتمل.
        - format: الصيغة المطلوبة (e.g., "markdown", "json").
        """
        execution = context.get("execution")
        output_format = context.get("format", "markdown")

        if not execution:
            return {"status": "error", "message": "A completed workflow execution object is required."}

        logger.info(f"LoreMaster: Generating '{output_format}' Story Bible for execution ID '{execution['id']}'...")
        
        # 1. استخلاص وتجميع البيانات من حالة التنفيذ
        story_data = self._extract_data_from_execution(execution)

        # 2. بناء الكتاب المقدس بالصيغة المطلوبة
        if output_format == "markdown":
            story_bible_content = self._build_markdown_bible(story_data)
        elif output_format == "json":
            story_bible_content = story_data
        else:
            return {"status": "error", "message": f"Unsupported format: {output_format}"}

        return {
            "status": "success",
            "content": {"story_bible": story_bible_content, "format": output_format},
            "summary": "The Story Bible has been successfully generated."
        }

    def _extract_data_from_execution(self, execution: Dict) -> Dict:
        """يستخلص وينظم البيانات من مخرجات المهام المختلفة."""
        logger.info("Extracting and organizing data from all workflow tasks...")
        
        # هذا منطق تجميع معقد، سأقوم بتبسيطه هنا
        # في نظام حقيقي، سيمر على `execution['task_outputs']`
        
        # محاكاة للبيانات المجمعة
        character_profiles = [
            {"name": "مبروك", "role": "البطل", "psych_profile": "يسعى للاعتراف، آلية دفاعه السخرية.", "arc": "يتحرر من قيمة الأشياء المادية."},
            {"name": "زهرة", "role": "زوجة البطل", "psych_profile": "واقعية، قلقة، تمثل صوت الضمير.", "arc": "تساعد مبروك على رؤية الحقيقة."},
            {"name": "الهادي", "role": "الخصم", "psych_profile": "انتهازي، يؤمن بقوة المال.", "arc": "يمثل الحداثة السلبية التي تفشل في النهاية."}
        ]
        
        timeline = [
            {"event": "مبروك يحصل على الشهادة", "chapter": 1},
            {"event": "مبروك يواجه البيروقراطية", "chapter": 1},
            {"event": "مبروك يلتقي بالهادي", "chapter": 2},
            {"event": "مبروك يتنازل ويدفع للمعتمد", "chapter": 2},
            {"event": "مبروك يمزق الشهادة", "chapter": 3}
        ]
        
        fact_database = {
            ("الشهادة", "الحالة"): "بدون قيمة مادية",
            ("مبروك", "الهدف الأولي"): "الحصول على الترقية",
            ("الهادي", "الهدف"): "شراء أراضي الدوار"
        }
        
        themes_and_symbols = {
            "الكرسي": "رمز للسلطة الفارغة والمنصب.",
            "الشهادة": "رمز للقيمة الزائفة والاعتراف الرسمي.",
            "الموضوع الرئيسي": "صراع بين القيم الأصيلة والانتهازية المادية."
        }

        return {
            "project_title": execution["name"].replace("Execution: ", ""),
            "character_profiles": character_profiles,
            "event_timeline": timeline,
            "world_facts": fact_database,
            "themes_and_symbols": themes_and_symbols,
            "generation_date": datetime.now().isoformat()
        }

    def _build_markdown_bible(self, data: Dict) -> str:
        """يبني الكتاب المقدس بصيغة Markdown."""
        logger.info("Building Markdown version of the Story Bible...")
        
        # --- صفحة العنوان ---
        md = f"# الكتاب المقدس للقصة: {data['project_title']}\n"
        md += f"**تاريخ الإنشاء:** {data['generation_date']}\n\n"
        md += "---\n\n"

        # --- قسم الشخصيات ---
        md += "## 1. ملفات الشخصيات\n\n"
        for char in data["character_profiles"]:
            md += f"### 1.1. {char['name']} ({char['role']})\n"
            md += f"- **الملف النفسي:** {char['psych_profile']}\n"
            md += f"- **قوس التطور:** {char['arc']}\n\n"
        md += "---\n\n"

        # --- قسم الجدول الزمني ---
        md += "## 2. الجدول الزمني للأحداث الرئيسية\n\n"
        for event in data["event_timeline"]:
            md += f"- **(الفصل {event['chapter']}):** {event['event']}\n"
        md += "\n---\n\n"

        # --- قسم حقائق العالم ---
        md += "## 3. الحقائق الثابتة (قوانين العالم)\n\n"
        for (sub, pred), obj in data["world_facts"].items():
            md += f"- **حقيقة:** {sub} **{pred}** هو/هي **'{obj}'**.\n"
        md += "\n---\n\n"

        # --- قسم المواضيع والرموز ---
        md += "## 4. المواضيع والرموز الرئيسية\n\n"
        for symbol, meaning in data["themes_and_symbols"].items():
            md += f"- **{symbol}:** {meaning}\n"
        
        return md.strip()

    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.generate_story_bible(context)

# إنشاء مثيل وحيد
lore_master_agent = LoreMasterAgent()
