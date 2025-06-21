# agents/narrative_constructor_agent.py
import logging
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from engines.creative_layer_engine import CreativeLayerEngine # نفترض وجوده
from tools.tunisian_dialogue_gallery import TunisianDialogueGallery

logger = logging.getLogger("NarrativeConstructorAgent")

class NarrativeConstructorAgent(BaseAgent):
    """
    وكيل بناء المشاهد السردية، ينسق بين المحركات والأدوات الأخرى.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="باني المشاهد السردية",
            description="ينسق بين المحركات المختلفة لبناء مشاهد كاملة."
        )
        self.creative_engine = CreativeLayerEngine()
        self.dialogue_gallery = TunisianDialogueGallery()

    async def construct_play_scene(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يبني مشهدًا مسرحيًا كاملاً.
        """
        scene_outline = context.get("scene_outline") # مخطط المشهد
        if not scene_outline:
            raise ValueError("مخطط المشهد مطلوب.")
            
        logger.info(f"Constructing play scene: '{scene_outline.get('title')}'")

        # 1. طلب الوصف الحسي للمكان
        location = scene_outline.get("location", "cafe")
        sensory_details = await self.creative_engine.generate_tunisian_sensory_details(location)

        # 2. طلب الحوارات
        dialogues = []
        for interaction in scene_outline.get("interactions", []):
            dialogue_line = self.dialogue_gallery.generate_dialogue(
                character_archetype=interaction["character_archetype"],
                topic=interaction["topic"],
                mood=interaction["mood"]
            )
            dialogues.append({"character": interaction["character_name"], "line": dialogue_line})

        # 3. تجميع المشهد
        scene_script = self._assemble_scene(sensory_details, dialogues, scene_outline)

        return {
            "content": {"scene_script": scene_script},
            "summary": "تم بناء مشهد مسرحي متكامل."
        }
        
    def _assemble_scene(self, sensory: Dict, dialogues: List[Dict], outline: Dict) -> str:
        """يقوم بتجميع المشهد في الصيغة المسرحية."""
        
        script = f"### {outline.get('title', 'مشهد جديد')} ###\n\n"
        
        # الوصف الافتتاحي
        opening_desc = f"[المكان: {outline.get('location_name', 'مقهى تونسي')}. "
        if sensory.get("sights"):
            opening_desc += f"{sensory['sights'][0]}. "
        if sensory.get("sounds"):
            opening_desc += f"{sensory['sounds'][0]}. "
        if sensory.get("smells"):
            opening_desc += f"{sensory['smells'][0]}. "
        script += opening_desc.strip() + "]\n\n"

        # الحوار
        for dialogue_entry in dialogues:
            script += f"{dialogue_entry['character'].upper()}:\n"
            script += f"{dialogue_entry['line']}\n\n"
            
        return script
