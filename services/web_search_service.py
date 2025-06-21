# services/web_search_service.py

import logging

logger = logging.getLogger("WebSearchService")

class WebSearchService:
    async def search(self, query: str) -> dict:
        logger.info(f"Simulating web search for: '{query}'")
        # في نظام حقيقي، ستتصل بـ Tavily أو Google Search API هنا
        
        # محاكاة لنتيجة بحث عن "صالح بن يوسف"
        if "صالح بن يوسف" in query:
            return {
                "status": "success",
                "data": [{
                    "title": "صالح بن يوسف - ويكيبيديا",
                    "url": "https://ar.wikipedia.org/wiki/صالح_بن_يوسف",
                    "content": """
                    صالح بن يوسف كان زعيماً وطنياً تونسياً وأميناً عاماً للحزب الدستوري الجديد. 
                    اختلف بشدة مع الحبيب بورقيبة حول اتفاقيات الاستقلال الداخلي مع فرنسا، 
                    حيث دعا إلى الكفاح المسلح من أجل استقلال كامل. 
                    بلغ الخلاف ذروته في مؤتمر الحزب بصفاقس عام 1955، مما أدى إلى عزله. 
                    اغتيل في ألمانيا عام 1961.
                    """
                }]
            }
        return {"status": "success", "data": []}

web_search_service = WebSearchService()
