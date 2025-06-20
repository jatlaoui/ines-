# poem_composer_agent.py
"""
PoemComposerAgent (كاتب القصائد)
الغرض: توليد قصائد أدبية بأساليب شعرية متنوعة.
"""
import logging
import json
from typing import Dict, Any, Optional, List

logger = logging.getLogger("PoemComposerAgent")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [PoemComposer] - %(levelname)s - %(message)s')

class MockLLMPoetryService:
    async def generate_poem(self, prompt: str) -> str:
        mock_poem = {
            "content": {
                "title": "غربةٌ بينَ الأسلاك",
                "style": "شعر حر",
                "theme": "الوحدة الرقمية",
                "lines": [
                    "بينَ شاشاتٍ لا تعرفني،",
                    "أمدُّ يدي إلى ضوءٍ لا يدفئني،",
                    "وصوتي يعودُ كأصداءٍ باردة،",
                    "كأنني تائهٌ في صحراءِ الشبكات..."
                ]
            }
        }
        return json.dumps(mock_poem, ensure_ascii=False)

class PoemComposerAgent:
    def __init__(self, llm_service=None):
        self.llm = llm_service or MockLLMPoetryService()
        logger.info("PoemComposerAgent initialized.")

    async def generate_poem(self, context: Dict[str, Any], feedback: Optional[List[str]] = None) -> Dict[str, Any]:
        logger.info(f"Generating poem for theme: {context.get('theme_hint', 'غير محدد')}")
        prompt = self._build_prompt(context, feedback)
        response_json = await self.llm.generate_poem(prompt)
        try:
            return json.loads(response_json)
        except Exception as e:
            logger.error(f"Failed to parse poem: {e}")
            return {"error": "Parsing error in poem generation"}

    def _build_prompt(self, context: Dict[str, Any], feedback: Optional[List[str]] = None) -> str:
        theme = context.get("theme_hint", "مفتوح")
        style = context.get("style_hint", "شعر حر")

        feedback_block = "\n".join(f"- {fb}" for fb in feedback) if feedback else ""

        return f"""
        اكتب قصيدة بأسلوب {style} عن الموضوع التالي: "{theme}".
        {feedback_block}
        يجب أن تتضمن القصيدة:
        - عنوان
        - الأسلوب المستخدم
        - الموضوع
        - قائمة من الأسطر الشعرية
        
        أرجع الرد بتنسيق JSON يحتوي على:
        "title", "style", "theme", "lines" (list of strings)
        """
