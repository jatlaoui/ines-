# core/llm_service.py (V2 - Upgraded with Advanced Features)

import logging
import os
from typing import Dict, Any, Optional, List, Type
import google.generativeai as genai
from google.generativeai.types import GenerationConfig, SafetySetting, HarmCategory, HarmBlockThreshold, Tool
from pydantic import BaseModel
from dotenv import load_dotenv

logger = logging.getLogger("LLMService")

class LLMService:
    """
    خدمة موحدة ومحسّنة (V2) للتفاعل مع Gemini API.
    تدعم الآن: المخرجات المنظمة (Pydantic)، استخدام الأدوات (Tools)،
    وإعدادات السلامة المخصصة.
    """
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")
            
        genai.configure(api_key=api_key)
        # تحديد النموذج الافتراضي
        self.default_model_name = 'gemini-1.5-flash'
        self.model = genai.GenerativeModel(self.default_model_name)
        
        # إعدادات السلامة الافتراضية (متساهلة للمحتوى الأدبي)
        self.default_safety_settings = [
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_NONE),
            SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_NONE),
        ]
        
        logger.info(f"✅ LLM Service (V2) initialized with default model: {self.default_model_name}.")

    async def generate_text_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        يولد نصًا عاديًا. يدعم الآن تعليمات النظام (Role Prompting).
        """
        try:
            config = GenerationConfig(temperature=temperature)
            contents = [prompt]
            
            # بناء كائن النموذج مع تعليمات النظام إذا كانت موجودة
            model_instance = genai.GenerativeModel(
                self.default_model_name,
                system_instruction=system_instruction,
                safety_settings=self.default_safety_settings
            )

            response = await model_instance.generate_content_async(contents, generation_config=config)
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini text generation: {e}")
            return f"Error: LLM call failed. Details: {e}"

    async def generate_structured_response(
        self,
        prompt: str,
        response_model: Type[BaseModel],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2
    ) -> Optional[BaseModel]:
        """
        [جديد] يولد مخرجًا منظمًا ومضمونًا باستخدام Pydantic.
        """
        try:
            # بناء كائن التكوين مع طلب إخراج JSON ومخطط Pydantic
            config = GenerationConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=response_model
            )
            
            # بناء كائن النموذج مع تعليمات النظام
            model_instance = genai.GenerativeModel(
                self.default_model_name,
                system_instruction=system_instruction,
                safety_settings=self.default_safety_settings
            )

            response = await model_instance.generate_content_async([prompt], generation_config=config)
            
            # SDK يقوم بالتحويل إلى كائن Pydantic تلقائيًا
            return response.parsed
        except Exception as e:
            logger.error(f"Error during structured response generation for {response_model.__name__}: {e}", exc_info=True)
            return None

    async def generate_with_tools(
        self,
        prompt: str,
        tools: List[Tool],
        system_instruction: Optional[str] = None,
        temperature: float = 0.1
    ) -> str:
        """
        [جديد] يولد ردًا مع تمكين استخدام الأدوات (مثل بحث جوجل).
        """
        try:
            # بناء كائن النموذج مع الأدوات المتاحة
            model_instance = genai.GenerativeModel(
                self.default_model_name,
                system_instruction=system_instruction,
                tools=tools,
                safety_settings=self.default_safety_settings
            )

            config = GenerationConfig(temperature=temperature)
            response = await model_instance.generate_content_async([prompt], generation_config=config)
            
            # ملاحظة: الردود التي تستخدم الأدوات قد تكون معقدة وتحتاج لتحليل إضافي
            # لكن في حالة بحث جوجل، غالبًا ما يتم دمج النتائج في النص مباشرة
            return response.text
        except Exception as e:
            logger.error(f"Error during tool-based generation: {e}")
            return f"Error: LLM call with tools failed. Details: {e}"

# إنشاء مثيل وحيد ومحسن
llm_service = LLMService()
