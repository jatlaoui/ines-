# agents/creative_chaos_agent.py
"""
CreativeChaosAgent (وكيل الفوضى المبدعة)
يقوم بإدخال "ضوضاء إبداعية" محسوبة لكسر الأنماط وتوليد أفكار غير متوقعة.
"""
import logging
import random
from typing import Dict, Any, List, Optional

from .base_agent import BaseAgent

logger = logging.getLogger("CreativeChaosAgent")

class CreativeChaosAgent(BaseAgent):
    """
    وكيل متخصص في توليد اقتراحات إبداعية غير متوقعة.
    """
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="مُحدث الفوضى المبدعة",
            description="يكسر الأنماط المتوقعة ويقترح روابط ومفاهيم غير تقليدية."
        )
        self.creativity_techniques = [
            self._juxtapose_concepts,
            self._invert_expectation,
            self._introduce_random_element,
            self._change_perspective
        ]
        logger.info("CreativeChaosAgent initialized.")

    async def generate_disruptive_ideas(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        """
        الوظيفة الرئيسية: يولد مجموعة من الأفكار "المزعزعة" بناءً على السياق.
        'context' يجب أن يحتوي على 'knowledge_base'.
        """
        knowledge_base = context.get("knowledge_base")
        if not knowledge_base:
            raise ValueError("KnowledgeBase is required for generating disruptive ideas.")

        num_ideas = context.get("num_ideas", 3)
        logger.info(f"Generating {num_ideas} disruptive ideas...")

        disruptive_ideas = []
        for _ in range(num_ideas):
            # اختيار تقنية إبداعية عشوائية
            technique = random.choice(self.creativity_techniques)
            idea = technique(knowledge_base)
            disruptive_ideas.append(idea)
        
        return {
            "content": disruptive_ideas,
            "summary": f"تم توليد {len(disruptive_ideas)} فكرة غير تقليدية."
        }

    def _juxtapose_concepts(self, kb: Dict[str, Any]) -> Dict[str, str]:
        """تقنية الربط بين مفهومين لا علاقة لهما ببعض."""
        entities = kb.get("entities", [])
        if len(entities) < 2:
            return {"technique": "Juxtaposition", "idea": "لا توجد كيانات كافية للربط."}
        
        entity1, entity2 = random.sample(entities, 2)
        idea = f"ماذا لو كانت '{entity1['name']}' ({entity1['type']}) هي في الحقيقة رمز لـ '{entity2['name']}' ({entity2['type']})؟"
        
        return {"technique": "Juxtaposition (ربط المفاهيم)", "idea": idea}

    def _invert_expectation(self, kb: Dict[str, Any]) -> Dict[str, str]:
        """تقنية عكس التوقعات."""
        relationships = kb.get("relationship_graph", [])
        if not relationships:
            return {"technique": "Inversion", "idea": "لا توجد علاقات لتحليلها."}
        
        rel = random.choice(relationships)
        source, target, relation = rel['source'], rel['target'], rel['relation']
        
        inversion_map = {
            "يحب": "يكره في الخفاء",
            "يثق في": "يخطط لخيانة",
            "يساعد": "يساعد لتحقيق مصلحة خفية"
        }
        inverted_relation = inversion_map.get(relation, f"يفعل عكس '{relation}'")
        
        idea = f"ماذا لو كانت العلاقة الظاهرية '{source} {relation} {target}' تخفي حقيقة معاكسة: '{source} {inverted_relation} {target}'؟"

        return {"technique": "Inversion (عكس التوقعات)", "idea": idea}

    def _introduce_random_element(self, kb: Dict[str, Any]) -> Dict[str, str]:
        """تقنية إدخال عنصر عشوائي."""
        random_elements = ["عاصفة رملية مفاجئة", "طفل غامض يظهر من العدم", "اكتشاف أداة تكنولوجية قديمة", "مرض غريب ينتشر"]
        random_event = random.choice(random_elements)
        
        main_char = next((e['name'] for e in kb.get("entities", []) if e.get('type') == 'character'), None)
        if not main_char:
            return {"technique": "Random Element", "idea": "لا توجد شخصية رئيسية لإدخال الحدث عليها."}

        idea = f"في أكثر اللحظات هدوءًا، كيف سيغير '{random_event}' مسار حياة '{main_char}' وكل شيء حوله؟"

        return {"technique": "Random Element (عنصر عشوائي)", "idea": idea}
        
    def _change_perspective(self, kb: Dict[str, Any]) -> Dict[str, str]:
        """تقنية تغيير منظور السرد."""
        entities = kb.get("entities", [])
        secondary_char = next((e['name'] for e in entities if e.get('importance_score', 0) < 7 and e.get('type') == 'character'), None)
        inanimate_object = next((e['name'] for e in entities if e.get('type') == 'object'), None)

        if secondary_char:
            idea = f"ماذا لو تم سرد الفصل التالي بالكامل من وجهة نظر الشخصية الثانوية '{secondary_char}'؟ ماذا سترى هي وما الذي ستكشفه؟"
        elif inanimate_object:
            idea = f"ماذا لو تم سرد مشهد واحد من 'وجهة نظر' الكائن '{inanimate_object}'؟ ماذا شهد هذا الكائن الصامت؟"
        else:
            idea = "ماذا لو تم سرد القصة من منظور حيوان أو كائن غير متوقع في المشهد؟"

        return {"technique": "Perspective Shift (تغيير المنظور)", "idea": idea}
