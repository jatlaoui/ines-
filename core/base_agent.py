# core/base_agent.py
"""
الفئة الأساسية للوكلاء (BaseAgent)
توفر بنية أساسية مشتركة لجميع الوكلاء في النظام.
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class BaseAgent:
    """
    فئة مجردة تمثل الوكيل الأساسي في النظام.
    يجب على كل وكيل متخصص أن يرث من هذه الفئة.
    """
    def __init__(self, agent_id: Optional[str] = None, name: str = "Unnamed Agent", description: str = ""):
        """
        تهيئة الوكيل.
        """
        self.agent_id = agent_id or self.__class__.__name__
        self.name = name
        self.description = description
        logger.info(f"Agent '{self.name}' ({self.agent_id}) initialized.")

    def get_info(self) -> Dict[str, Any]:
        """
        إرجاع معلومات أساسية عن الوكيل.
        """
        return {
            "id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }
