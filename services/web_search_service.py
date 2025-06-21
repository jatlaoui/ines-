# services/web_search_service.py (النسخة الإبداعية)

import logging
import asyncio
from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup
from newspaper import Article # مكتبة متخصصة لاستخلاص المقالات
from core.llm_service import llm_service

logger = logging.getLogger("WebSearchService")

class WebSearchService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=20, follow_redirects=True, http2=True)
        logger.info("Intelligent Web Explorer initialized.")

    async def _fetch_and_parse(self, url: str) -> str:
        """يجلب المحتوى ويحلله بذكاء."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()

            # استخدام newspaper3k أولاً لأنها أكثر ذكاءً في تحديد المحتوى الرئيسي
            try:
                article = Article(url)
                article.download(input_html=response.content)
                article.parse()
                if len(article.text) > 500: # إذا نجحت في استخلاص محتوى جيد
                    logger.info(f"Successfully scraped with newspaper3k from {url}")
                    return article.title + "\n\n" + article.text
            except Exception as e:
                logger.warning(f"newspaper3k failed for {url}: {e}. Falling back to BeautifulSoup.")

            # الخطة البديلة: BeautifulSoup للتنظيف اليدوي
            soup = BeautifulSoup(response.content, 'html.parser')
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            
            body = soup.find('body')
            return body.get_text(separator='\n', strip=True) if body else ""

        except Exception as e:
            logger.error(f"Failed to fetch content from {url}. Error: {e}")
            return ""

    def _filter_forum_noise(self, text: str) -> str:
        """يزيل الضوضاء الشائعة في المنتديات."""
        noise_patterns = [
            r'رد مع اقتباس', r'مشاهدة ملفه الشخصي', r'إرسال رسالة خاصة',
            r'البحث عن كل مشاركات', r'^\s*الكاتب:.*', r'^\s*تاريخ التسجيل:.*',
            r'^\s*المشاركات:.*', r'\[.*\]', r'مشاركة\s+#\d+'
        ]
        for pattern in noise_patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE)
        
        lines = text.split('\n')
        # إزالة الأسطر القصيرة جدًا أو الفارغة
        clean_lines = [line for line in lines if len(line.split()) > 3]
        return "\n".join(clean_lines)

    async def get_inspiration_from_url(self, url: str) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية الجديدة: تجلب، تنظف، وتلخص المحتوى من رابط للإلهام.
        """
        logger.info(f"Seeking inspiration from URL: {url}")
        
        raw_content = await self._fetch_and_parse(url)
        if not raw_content or len(raw_content) < 200:
            return {"status": "error", "message": "Content is too short or could not be fetched."}
            
        cleaned_content = self._filter_forum_noise(raw_content)
        
        # تلخيص المحتوى للحصول على الجوهر فقط
        summary_prompt = f"""
مهمتك: أنت باحث أدبي. قم بقراءة النص التالي واستخلاص جوهره في 3 نقاط رئيسية. ركز على المواضيع، المشاعر، والصور الشعرية المتكررة.
---
{cleaned_content[:4000]} 
---
أرجع ردك في شكل نص عادي.
"""
        summary = await llm_service.generate_text_response(summary_prompt, temperature=0.3)

        return {
            "status": "success",
            "data": {
                "url": url,
                "summary": summary,
                "full_text_for_analysis": cleaned_content # نمرر النص الكامل للتحليل العميق
            }
        }

# إنشاء مثيل وحيد
web_inspiration_service = WebSearchService()
