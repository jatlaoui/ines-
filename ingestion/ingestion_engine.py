# ingestion/ingestion_engine.py (V2 - PDF Enabled)
"""
Multimedia Ingestion Engine
محرك متخصص في استيعاب أنواع مختلفة من المدخلات وتحويلها إلى نص نظيف.
V2: يستخدم Gemini File API لمعالجة ملفات PDF مباشرة.
"""
import logging
import base64
from typing import Dict, Any, Optional
from enum import Enum
import httpx
from bs4 import BeautifulSoup

# استيراد الخدمات والعميل الأساسي
from core.llm_service import llm_service # لم يعد ضروريًا هنا مباشرة ولكن جيد للاستمرارية

# نحتاج إلى العميل الأساسي لـ genai للوصول إلى File API
import google.generativeai as genai

logger = logging.getLogger("IngestionEngine")

class InputType(Enum):
    RAW_TEXT = "نص مباشر"
    URL = "رابط ويب"
    PDF_FILE_PATH = "مسار ملف PDF" # أصبحنا نتعامل مع المسارات
    AUDIO_FILE = "ملف صوتي"

class IngestionResult:
    """نتيجة عملية الاستيعاب."""
    def __init__(self, success: bool, text_content: str = "", metadata: Optional[Dict] = None, error: Optional[str] = None):
        self.success = success
        self.text_content = text_content
        self.metadata = metadata or {}
        self.error = error

class MultimediaIngestionEngine:
    """
    محرك استيعاب المدخلات متعدد الوسائط (V2).
    """
    def __init__(self):
        # لم نعد بحاجة لخدمات PDF خارجية، سنستخدم Gemini مباشرة
        logger.info("✅ Multimedia Ingestion Engine (V2) Initialized with Gemini File API capabilities.")

    async def ingest(self, source: str, input_type: InputType, options: Optional[Dict] = None) -> IngestionResult:
        """
        الوظيفة الرئيسية: تستوعب مصدرًا وتحوله إلى نص.
        """
        logger.info(f"Ingesting source of type: {input_type.value}")
        
        try:
            if input_type == InputType.RAW_TEXT:
                return await self._ingest_raw_text(source)
            elif input_type == InputType.URL:
                return await self._ingest_url(source)
            elif input_type == InputType.PDF_FILE_PATH:
                # 'source' هنا هو مسار الملف المحلي
                return await self._ingest_pdf(source)
            elif input_type == InputType.AUDIO_FILE:
                return await self._ingest_audio(source)
            else:
                raise ValueError(f"نوع المدخل غير مدعوم: {input_type}")

        except Exception as e:
            logger.error(f"Failed to ingest source. Type: {input_type.value}, Error: {e}", exc_info=True)
            return IngestionResult(success=False, error=str(e))

    async def _ingest_raw_text(self, text: str) -> IngestionResult:
        """استيعاب نص مباشر."""
        if not text or not text.strip():
            return IngestionResult(success=False, error="النص المدخل فارغ.")
        
        metadata = {
            "source_type": InputType.RAW_TEXT.value,
            "char_count": len(text),
            "word_count": len(text.split())
        }
        return IngestionResult(success=True, text_content=text, metadata=metadata)

    async def _ingest_url(self, url: str) -> IngestionResult:
        """استيعاب محتوى من رابط ويب."""
        logger.info(f"Fetching content from URL: {url}")
        try:
            async with httpx.AsyncClient() as client:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = await client.get(url, headers=headers, timeout=15, follow_redirects=True)
                response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()
            text = soup.get_text(separator='\n', strip=True)
            title = soup.title.string if soup.title else "بدون عنوان"
            metadata = {"source_type": InputType.URL.value, "source_url": url, "title": title}
            return IngestionResult(success=True, text_content=text, metadata=metadata)
        except httpx.RequestException as e:
            raise IOError(f"فشل في جلب المحتوى من الرابط: {e}")

    async def _ingest_pdf(self, file_path: str) -> IngestionResult:
        """[مُعدَّل] استيعاب محتوى من ملف PDF باستخدام File API."""
        uploaded_file = None
        try:
            logger.info(f"Uploading PDF '{file_path}' using Gemini File API...")
            # 1. تحميل الملف
            uploaded_file = genai.upload_file(path=file_path)
            
            # التأكد من أن الملف في حالة جاهزية
            while uploaded_file.state.name == "PROCESSING":
                await asyncio.sleep(2) # انتظار لمدة ثانيتين
                uploaded_file = genai.get_file(name=uploaded_file.name)
            
            if uploaded_file.state.name == "FAILED":
                raise ValueError(f"File processing failed: {uploaded_file.uri}")

            logger.info(f"File uploaded successfully. URI: {uploaded_file.uri}. Extracting content...")
            
            # 2. استخلاص النص باستخدام النموذج
            prompt = "استخلص النص الكامل من ملف PDF المرفق بدقة. حافظ على بنية الفقرات."
            response = llm_service.model.generate_content([prompt, uploaded_file])
            text_content = response.text
            
            metadata = {
                "source_type": InputType.PDF_FILE_PATH.value,
                "file_name": uploaded_file.display_name,
                "file_uri": uploaded_file.uri,
                "mime_type": uploaded_file.mime_type
            }
            
            return IngestionResult(success=True, text_content=text_content, metadata=metadata)
        
        except Exception as e:
            logger.error(f"Error during PDF ingestion with File API: {e}", exc_info=True)
            return IngestionResult(success=False, error=f"فشل استخلاص PDF: {e}")
        
        finally:
            # 3. (اختياري) حذف الملف بعد المعالجة لتنظيف الموارد
            if uploaded_file:
                genai.delete_file(name=uploaded_file.name)
                logger.info(f"Cleaned up uploaded file: {uploaded_file.name}")


    async def _ingest_audio(self, source: str) -> IngestionResult:
        """(مستقبلي) استيعاب محتوى من ملف صوتي."""
        logger.warning("Audio ingestion is not implemented yet.")
        return IngestionResult(success=False, error="ميزة تحويل الصوت إلى نص قيد التطوير.")
        
# إنشاء مثيل وحيد من المحرك
ingestion_engine = MultimediaIngestionEngine()
