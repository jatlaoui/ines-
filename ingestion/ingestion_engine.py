# ingestion/ingestion_engine.py
"""
Multimedia Ingestion Engine
محرك متخصص في استيعاب أنواع مختلفة من المدخلات وتحويلها إلى نص نظيف.
"""
import logging
from typing import Dict, Any, Optional
from enum import Enum
import requests
from bs4 import BeautifulSoup

# استيراد الأدوات التي بنيناها سابقًا
from tools.advanced_pdf_service import AdvancedPDFService, pdf_service # نفترض أننا نستخدم المثيل الوحيد
# from tools.audio_transcriber import audio_transcriber # أداة مستقبلية لتحويل الصوت لنص

logger = logging.getLogger("IngestionEngine")

class InputType(Enum):
    RAW_TEXT = "نص مباشر"
    URL = "رابط ويب"
    PDF_FILE = "ملف PDF"
    AUDIO_FILE = "ملف صوتي"
    YOUTUBE_URL = "رابط يوتيوب"

class IngestionResult:
    """نتيجة عملية الاستيعاب."""
    def __init__(self, success: bool, text_content: str = "", metadata: Optional[Dict] = None, error: Optional[str] = None):
        self.success = success
        self.text_content = text_content
        self.metadata = metadata or {}
        self.error = error

class MultimediaIngestionEngine:
    """
    محرك استيعاب المدخلات متعدد الوسائط.
    """
    def __init__(self):
        self.pdf_service = pdf_service
        # self.audio_service = audio_transcriber # سيتم تفعيله لاحقًا
        logger.info("Multimedia Ingestion Engine initialized.")

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
            elif input_type == InputType.PDF_FILE:
                # 'source' هنا هو محتوى الملف (bytes)
                return await self._ingest_pdf(source)
            elif input_type == InputType.AUDIO_FILE:
                return await self._ingest_audio(source)
            else:
                raise ValueError(f"نوع المدخل غير مدعوم: {input_type}")

        except Exception as e:
            logger.error(f"Failed to ingest source. Type: {input_type.value}, Error: {e}")
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
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status() # يثير خطأ إذا كانت الاستجابة غير ناجحة

            # استخدام BeautifulSoup لتنظيف واستخلاص النص من HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # إزالة التاغات غير المرغوب فيها (scripts, styles)
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()

            text = soup.get_text(separator='\n', strip=True)
            
            title = soup.title.string if soup.title else "بدون عنوان"

            metadata = {
                "source_type": InputType.URL.value,
                "source_url": url,
                "title": title,
                "char_count": len(text),
                "word_count": len(text.split())
            }
            return IngestionResult(success=True, text_content=text, metadata=metadata)

        except requests.RequestException as e:
            raise IOError(f"فشل في جلب المحتوى من الرابط: {e}")

    async def _ingest_pdf(self, pdf_bytes: bytes) -> IngestionResult:
        """استيعاب محتوى من ملف PDF."""
        if not self.pdf_service:
            return IngestionResult(success=False, error="خدمة معالجة PDF غير متاحة.")

        logger.info("Extracting text from PDF file...")
        # استخدام خدمتنا المتقدمة التي بنيناها
        text, error = self.pdf_service.extract_text_only(pdf_bytes)
        
        if error:
            return IngestionResult(success=False, error=f"فشل استخلاص PDF: {error}")

        info = self.pdf_service.get_pdf_info(pdf_bytes)
        metadata = {
            "source_type": InputType.PDF_FILE.value,
            **info.get("metadata", {})
        }
        
        return IngestionResult(success=True, text_content=text, metadata=metadata)

    async def _ingest_audio(self, audio_bytes: bytes) -> IngestionResult:
        """(مستقبلي) استيعاب محتوى من ملف صوتي."""
        # if not self.audio_service:
        #     return IngestionResult(success=False, error="خدمة تحويل الصوت إلى نص غير متاحة.")
        
        logger.info("Transcribing audio file...")
        # transcript = await self.audio_service.transcribe(audio_bytes)
        # return IngestionResult(success=True, text_content=transcript, metadata=...)
        
        return IngestionResult(success=False, error="ميزة تحويل الصوت إلى نص قيد التطوير.")
        
# إنشاء مثيل وحيد من المحرك
ingestion_engine = MultimediaIngestionEngine()
