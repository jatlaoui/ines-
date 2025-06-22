# services/web_search_service.py (V2 - with Forum Noise Filtering)
import logging
import asyncio
import re
from typing import Dict, Any, List
import httpx
from bs4 import BeautifulSoup
from newspaper import Article

from ..core.llm_service import llm_service

logger = logging.getLogger("WebSearchService")

class WebSearchService:
    """
    خدمة متقدمة لجلب وتحليل محتوى الويب، مع قدرات متخصصة
    لتنظيف بيانات المنتديات والشبكات الاجتماعية.
    """
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=25, follow_redirects=True, http2=True)
        # قائمة بالعبارات والمحددات التي تدل على ضوضاء المنتديات
        self._forum_noise_patterns = [
            r'رد مع اقتباس', r'مشاهدة ملفه الشخصي', r'إرسال رسالة خاصة',
            r'البحث عن كل مشاركات', r'^\s*الكاتب:\s*.*', r'^\s*تاريخ التسجيل:\s*.*',
            r'^\s*المشاركات:\s*.*', r'\[.*\]', r'مشاركة\s+#\d+', r'عدل سابقا من قبل',
            r'تعديل/حذف رسالة', r'إقتباس', r'العودة إلى الأعلى'
        ]
        logger.info("✅ Advanced Web Search & Scraping Service (V2) Initialized.")

    async def _fetch_html(self, url: str) -> Optional[str]:
        """يجلب محتوى HTML الخام من رابط معين."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            logger.error(f"Failed to fetch content from {url}. Error: {e}")
            return None

    def _clean_and_extract_text(self, html_content: str, url: str) -> str:
        """يستخدم طرقًا متعددة لاستخلاص النص النظيف من HTML."""
        # المحاولة الأولى: newspaper3k (ممتازة للمقالات)
        try:
            article = Article(url, language='ar')
            article.download(input_html=html_content)
            article.parse()
            if len(article.text) > 300: # إذا نجحت في استخلاص محتوى جيد
                logger.info(f"Successfully scraped with newspaper3k from {url}")
                return article.title + "\n\n" + article.text
        except Exception:
            logger.warning(f"newspaper3k failed for {url}. Falling back to BeautifulSoup.")

        # الخطة البديلة: BeautifulSoup للتنظيف اليدوي
        soup = BeautifulSoup(html_content, 'html.parser')
        # إزالة التاغات غير المرغوب فيها
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()
        
        body = soup.find('body')
        if not body:
            return ""
            
        return body.get_text(separator='\n', strip=True)

    def _filter_forum_noise(self, text: str) -> str:
        """يزيل الضوضاء الشائعة في المنتديات والتعليقات."""
        clean_text = text
        for pattern in self._forum_noise_patterns:
            clean_text = re.sub(pattern, '', clean_text, flags=re.MULTILINE)
        
        # إزالة الأسطر الفارغة الزائدة
        lines = clean_text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        return "\n".join(non_empty_lines)

    async def scrape_and_clean_url(self, url: str) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية للخدمة: تكشط رابطًا، تستخلص النص، وتنظفه.
        """
        logger.info(f"Scraping and cleaning URL: {url}")
        
        html = await self._fetch_html(url)
        if not html:
            return {"status": "error", "message": "Could not fetch HTML content."}
            
        raw_text = self._clean_and_extract_text(html, url)
        if not raw_text:
            return {"status": "error", "message": "Could not extract text content."}
        
        # تطبيق فلتر خاص بالمنتديات
        if "forum" in url or "vb" in url or "thread" in url:
             logger.info("Forum-like URL detected. Applying noise filter.")
             cleaned_text = self._filter_forum_noise(raw_text)
        else:
            cleaned_text = raw_text

        return {
            "status": "success",
            "data": {
                "url": url,
                "cleaned_text": cleaned_text,
                "original_word_count": len(raw_text.split()),
                "cleaned_word_count": len(cleaned_text.split())
            }
        }

# إنشاء مثيل وحيد
web_search_service = WebSearchService()
