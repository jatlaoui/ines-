# tools/derja_ninja_scraper.py
import logging
import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

logger = logging.getLogger("DerjaNinjaScraper")

class DerjaNinjaScraperTool:
    """
    أداة متخصصة لكشط واستخلاص البيانات من موقع derja.ninja.
    مصممة لفهم هيكل الموقع واستخراج الكلمات والأمثلة بدقة.
    """
    BASE_URL = "https://derja.ninja"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=20, headers={'User-Agent': 'INES_Project_Scraper/1.0'})
        logger.info("✅ Derja.ninja Scraper Tool Initialized.")

    async def scrape_word_definition(self, word: str) -> Optional[Dict]:
        """
        يكشط صفحة كلمة محددة ويستخلص تعريفاتها وأمثلتها.
        """
        url = f"{self.BASE_URL}/word/{word}"
        logger.info(f"Scraping word definition from: {url}")
        
        try:
            response = await self.client.get(url)
            if response.status_code != 200:
                logger.warning(f"Word '{word}' not found on derja.ninja (Status: {response.status_code}).")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # استخلاص البيانات بناءً على بنية HTML للموقع
            # (ملاحظة: هذه الكلاسات هي أمثلة وقد تتغير)
            definitions_div = soup.find('div', class_='definitions')
            if not definitions_div:
                return None

            entries = []
            for definition_item in definitions_div.find_all('div', class_='definition'):
                meaning_tag = definition_item.find('div', class_='meaning')
                example_tag = definition_item.find('div', class_='example')
                
                meaning = meaning_tag.get_text(strip=True) if meaning_tag else ""
                example = example_tag.get_text(strip=True) if example_tag else ""
                
                # تنظيف المثال من الترجمة الإنجليزية/الفرنسية
                if "Example:" in example:
                    example = example.split("Example:")[1].strip()
                
                entries.append({
                    "meaning": meaning,
                    "example_sentence": example
                })
            
            if not entries:
                return None

            return {
                "word": word,
                "definitions": entries
            }

        except httpx.RequestError as e:
            logger.error(f"Failed to scrape {url}. Error: {e}")
            return None
