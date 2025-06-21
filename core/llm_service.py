# core/llm_service.py

import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# --- إعدادات أساسية ---
load_dotenv() # لتحميل المتغيرات من ملف .env
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
logger = logging.getLogger("LLM_Service")

class LLMService:
    """
    خدمة مركزية للتفاعل مع نماذج اللغة الكبيرة (Gemini API).
    """
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-pro-latest"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("مفتاح Gemini API غير موجود. يرجى إضافته في ملف .env باسم GEMINI_API_KEY")

        genai.configure(api_key=self.api_key)
        
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"✅ LLM Service initialized with model: {model_name}")

    async def generate_json_response(self, prompt: str, temperature: float = 0.5) -> Dict[str, Any]:
        """
        يستدعي الـ LLM ويتوقع استجابة بتنسيق JSON.
        """
        logger.info(f"▶️ Sending JSON request to LLM (temp={temperature}). Prompt starts with: '{prompt[:200].replace('\n', ' ')}...'")
        
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                response_mime_type="application/json"
            )
            
            response = await self.model.generate_content_async(
                prompt, 
                generation_config=generation_config
            )
            
            if not response.parts:
                logger.error("❌ LLM returned an empty response.")
                return {"error": "LLM returned an empty response."}

            json_data = json.loads(response.text)
            logger.info(f"✅ Received valid JSON response from LLM.")
            return json_data

        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to decode JSON from LLM response. Error: {e}")
            logger.debug(f"Raw response text: {getattr(response, 'text', 'N/A')}")
            return {"error": "JSONDecodeError", "details": str(e), "raw_response": getattr(response, 'text', 'N/A')}
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred while calling the LLM: {e}")
            return {"error": "LLM_API_Call_Failed", "details": str(e)}

    async def generate_text_response(self, prompt: str, temperature: float = 0.7) -> str:
        """
        يستدعي الـ LLM ويتوقع استجابة نصية عادية.
        """
        logger.info(f"▶️ Sending Text request to LLM (temp={temperature}). Prompt starts with: '{prompt[:200].replace('\n', ' ')}...'")
        try:
            response = await self.model.generate_content_async(prompt, temperature=temperature)
            logger.info(f"✅ Received text response from LLM.")
            return response.text
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred while calling the LLM: {e}")
            return f"Error: {e}"

# --- إنشاء مثيل وحيد يمكن استيراده في أي مكان في المشروع ---
llm_service = LLMService()
