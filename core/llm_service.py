# core/llm_service.py (Simplified for Gemini Free Tier)
import logging
import os
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger("LLMService")

class LLMService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ LLM Service initialized with Gemini 1.5 Flash (Free Tier Compliant).")

    async def generate_text_response(self, prompt: str, temperature: float = 0.7) -> str:
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(temperature=temperature)
            )
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini API call: {e}")
            return f"Error: LLM call failed. Details: {e}"

    async def generate_json_response(self, prompt: str, temperature: float = 0.2) -> Dict:
        json_prompt = f"{prompt}\n\nتنبيه: يجب أن يكون الرد بصيغة JSON صالحة فقط، بدون أي نص إضافي قبله أو بعده."
        try:
            response_text = await self.generate_text_response(json_prompt, temperature)
            import json
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                raise ValueError("No valid JSON object found in the response.")
        except Exception as e:
            logger.error(f"Error parsing JSON from Gemini response: {e}")
            return {"error": "Failed to parse JSON response.", "details": str(e)}

# إنشاء مثيل وحيد
llm_service = LLMService()
