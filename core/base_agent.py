# core/base_agent.py (Single Source of Truth)
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
        self.agent_id = agent_id or self.__class__.__name__
        self.name = name
        self.description = description
        logger.info(f"Agent '{self.name}' ({self.agent_id}) initialized.")

    @abstractmethod
    async def process_task(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        الطريقة المجردة لمعالجة المهام. يجب على كل وكيل متخصص تنفيذها.
        هذا يضمن أن جميع الوكلاء لديهم نقطة دخول موحدة.
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
