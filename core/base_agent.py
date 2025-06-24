# core/base_agent.py (V2 - Simplified & Unified)
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger("BaseAgent")

class BaseAgent(ABC):
    """
    الفئة الأساسية الموحدة (V2) لجميع الوكلاء في النظام.
    توفر بنية أساسية مشتركة وتفرض تنفيذ المهام.
    """
    def __init__(self, agent_id: Optional[str] = None, name: str = "Unnamed Agent", description: str = ""):
        # استخدام اسم الفئة كمعرف افتراضي إذا لم يتم توفيره
        self.agent_id = agent_id or self.__class__.__name__
        self.name = name
        self.description = description
        # لا يتم تسجيل التهيئة هنا، بل في ملفات الوكلاء الفردية لتجنب التكرار.

    @abstractmethod
    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        الطريقة المجردة لمعالجة المهام. يجب على كل وكيل متخصص تنفيذها.
        هذا يضمن أن جميع الوكلاء لديهم نقطة دخول موحدة يمكن للمنسق استدعاؤها.
        
        Args:
            context: قاموس يحتوي على جميع البيانات اللازمة للمهمة.
            **kwargs: أي معلمات إضافية.

        Returns:
            قاموس يحتوي على نتيجة المهمة، يجب أن يتضمن مفتاح 'status' ('success' or 'error').
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """إرجاع معلومات أساسية عن الوكيل."""
        return {
            "id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }
