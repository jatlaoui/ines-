# في خلية الكود الخاصة بـ core/llm_service.py
%%writefile core/llm_service.py
# core/llm_service.py (V2.1 - Corrected Imports)
import logging
import os
from typing import Dict, Any, Optional, List, Type
import google.generativeai as genai
# [تصحيح] استيراد الكائنات مباشرة من المكتبة الرئيسية
from google.generativeai.types import GenerationConfig, HarmCategory, HarmBlockThreshold, Tool 
from pydantic import BaseModel

logger = logging.getLogger("LLMService")

class LLMService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found.")
        genai.configure(api_key=api_key)
        self.default_model_name = 'gemini-1.5-flash'
        self.model = genai.GenerativeModel(self.default_model_name)
        
        # [تصحيح] لم نعد بحاجة لاستيراد SafetySetting، يمكننا إنشاؤها مباشرة
        self.default_safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

    async def generate_text_response(self, prompt: str, system_instruction: Optional[str] = None, temperature: float = 0.7) -> str:
        try:
            config = GenerationConfig(temperature=temperature)
            model_instance = genai.GenerativeModel(
                self.default_model_name, 
                system_instruction=system_instruction, 
                safety_settings=self.default_safety_settings
            )
            response = await model_instance.generate_content_async([prompt], generation_config=config)
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini text generation: {e}")
            return f"Error: LLM call failed. Details: {e}"

    async def generate_structured_response(self, prompt: str, response_model: Type[BaseModel], system_instruction: Optional[str] = None, temperature: float = 0.2) -> Optional[BaseModel]:
        try:
            config = GenerationConfig(
                temperature=temperature, 
                response_mime_type="application/json", 
                response_schema=response_model
            )
            model_instance = genai.GenerativeModel(
                self.default_model_name, 
                system_instruction=system_instruction, 
                safety_settings=self.default_safety_settings
            )
            response = await model_instance.generate_content_async([prompt], generation_config=config)
            
            # في الإصدارات الحديثة، قد يكون المخرج في response.candidates[0].content.parts[0].function_call.args
            # لكن .parsed هي الطريقة الموثوقة
            if hasattr(response, 'parsed') and response.parsed is not None:
                return response.parsed
            else:
                 # محاولة تحليل النص يدويًا كخطة بديلة
                logger.warning("response.parsed was empty, attempting manual JSON parsing from text.")
                import json
                cleaned_text = response.text.strip().lstrip("```json").rstrip("```")
                return response_model.parse_obj(json.loads(cleaned_text))

        except Exception as e:
            logger.error(f"Error during structured response generation for {response_model.__name__}: {e}", exc_info=True)
            return None

# لم نعد ننشئ المثيل هنا، سيتم إنشاؤه في bootstrap
# llm_service = LLMService()
