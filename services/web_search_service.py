# services/web_search_service.py (V3 - Responsible & Respectful)
import logging
import asyncio
import re
import random
import httpx
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin

logger = logging.getLogger("WebSearchService")

class WebSearchService:
    """
    خدمة متقدمة ومسؤولة لجلب وتحليل محتوى الويب.
    مصممة لتكون "مواطنًا صالحًا" على الإنترنت.
    """
    def __init__(self):
        # تعريف هوية العنكبوت بشكل واضح
        self.user_agent = "InesProjectLexiconScraper/1.0 (+http://ines-project.ai/scraper-info)"
        self.client = httpx.AsyncClient(
            headers={'User-Agent': self.user_agent},
            timeout=25,
            follow_redirects=True
        )
        self._robot_parsers: Dict[str, RobotFileParser] = {}
        # ... (نفس قائمة أنماط الضوضاء من الإصدار السابق) ...
        self._forum_noise_patterns = [...]
        logger.info("✅ Responsible Web Search & Scraping Service (V3) Initialized.")

    async def _can_fetch(self, url: str) -> bool:
        """
        [جديد] يتحقق من ملف robots.txt للسماح بالكشط.
        """
        base_url = urljoin(url, '/')
        if base_url not in self._robot_parsers:
            rp = RobotFileParser()
            robots_url = urljoin(base_url, 'robots.txt')
            try:
                response = await self.client.get(robots_url)
                if response.status_code == 200:
                    rp.parse(response.text.splitlines())
                else:
                    # إذا لم يوجد ملف، نفترض أنه مسموح
                    rp.allow_all = True
            except Exception:
                rp.allow_all = True
            self._robot_parsers[base_url] = rp
        
        can_fetch = self._robot_parsers[base_url].can_fetch(self.user_agent, url)
        if not can_fetch:
            logger.warning(f"Scraping disallowed by robots.txt for URL: {url}")
        return can_fetch

    async def scrape_and_clean_url(self, url: str, respect_rules: bool = True) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية للخدمة: تكشط رابطًا بمسؤولية.
        """
        logger.info(f"Responsibly scraping URL: {url}")

        if respect_rules and not await self._can_fetch(url):
            return {"status": "error", "message": f"Access denied by robots.txt for {url}."}

        # [جديد] إضافة تأخير عشوائي وأخلاقي
        delay = random.uniform(3, 8)
        logger.info(f"Waiting for {delay:.2f} seconds before request...")
        await asyncio.sleep(delay)

        try:
            response = await self.client.get(url)
            response.raise_for_status()

            # ... (نفس منطق استخلاص النص باستخدام newspaper3k و BeautifulSoup) ...
            soup = BeautifulSoup(response.text, 'html.parser')
            # ...
            cleaned_text = self._filter_forum_noise(soup.get_text())

            # [جديد] إخفاء هوية البيانات المستخرجة
            anonymized_data = self._anonymize_content(cleaned_text)

            return {
                "status": "success",
                "data": {
                    "url": url,
                    "anonymized_text": anonymized_data["text"],
                    "entities_removed": anonymized_data["removed_count"]
                }
            }
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {url}: {e}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            logger.error(f"General scraping error for {url}: {e}")
            return {"status": "error", "message": "An unexpected error occurred."}

    def _anonymize_content(self, text: str) -> Dict:
        """
        [جديد] يزيل المعلومات الشخصية المحتملة من النص.
        """
        # إزالة الإيميلات وأرقام الهواتف (أمثلة بسيطة)
        anonymized_text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL_REDACTED]', text)
        anonymized_text = re.sub(r'\b\d{8,}\b', '[PHONE_REDACTED]', anonymized_text)
        
        # يمكن استخدام نماذج NER (Named Entity Recognition) لإزالة أسماء الأشخاص والأماكن المحددة
        # هذا يتطلب مكتبة NLP متقدمة.
        
        removed_count = text.count('[EMAIL_REDACTED]') + text.count('[PHONE_REDACTED]')
        return {"text": anonymized_text, "removed_count": removed_count}

    def _filter_forum_noise(self, text: str) -> str:
        # ... (نفس دالة فلترة الضوضاء من الإصدار السابق) ...
        return text

# إنشاء مثيل وحيد
web_search_service = WebSearchService()
