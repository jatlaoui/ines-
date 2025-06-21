# engines/creative_layer_engine.py
import logging
from typing import Dict, Any, List

logger = logging.getLogger("CreativeLayerEngine")

class CreativeLayerEngine:
    def __init__(self):
        # ... (بقية التهيئة) ...
        self._tunisian_sensory_libraries = self._load_tunisian_sensory_data()
        logger.info("CreativeLayerEngine initialized with Tunisian Sensory Libraries.")

    def _load_tunisian_sensory_data(self) -> Dict[str, Dict[str, List[str]]]:
        """تحميل المكتبات الحسية التونسية."""
        return {
            "cafe": {
                "smells": ["رائحة القهوة التركي بالزهر", "دخان الشيشة بنكهة التفاح", "رائحة النعناع الطازج"],
                "sounds": ["صوت فناجين القهوة على الصينية النحاسية", "صوت زهر النرد على الطاولة", "همسات الزبائن", "صوت أغنية قديمة لفنان تونسي"],
                "sights": ["ضوء خافت يتسلل من المشربية", "فسيفساء زرقاء على الجدران", "كراسي من الخيزران", "دخان الشيشة المتصاعد"]
            },
            "souk": {
                "smells": ["رائحة البهارات (كمون، فلفل أحمر)", "رائحة الجلد الطبيعي من المصنوعات", "عطر الياسمين من الباعة"],
                "sounds": ["صوت الباعة ينادون على بضاعتهم", "ضجيج الدراجات النارية في الأزقة الضيقة", "صوت المطارق من ورش النحاسين"],
                "sights": ["ألوان زاهية للتوابل المعروضة", "الضوء والظل يتراقصان في الأزقة المسقوفة", "مصابيح نحاسية تلمع"]
            }
        }
    
    async def generate_tunisian_sensory_details(self, location_type: str, num_details: int = 3) -> Dict[str, List[str]]:
        """
        يولد تفاصيل حسية من مكتبة تونسية محددة.
        """
        logger.info(f"Generating Tunisian sensory details for location: '{location_type}'")
        
        library = self._tunisian_sensory_libraries.get(location_type)
        if not library:
            return {}
            
        details = {}
        for sense, options in library.items():
            if options:
                # اختيار عينة عشوائية
                import random
                sample_size = min(num_details, len(options))
                details[sense] = random.sample(options, sample_size)
        
        return details

    # ... (بقية دوال المحرك كما هي) ...
