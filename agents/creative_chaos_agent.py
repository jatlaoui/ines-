# agents/creative_chaos_agent.py
import logging
import random
from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent

logger = logging.getLogger("CreativeChaosAgent")

class CreativeChaosAgent(BaseAgent):
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            name="مُحدث الفوضى المبدعة",
            description="يكسر الأنماط المتوقعة ويقترح روابط ومفاهيم غير تقليدية."
        )
        self.creativity_techniques = [
            self._juxtapose_concepts, self._invert_expectation,
            self._introduce_random_element, self._change_perspective
        ]

    async def generate_disruptive_ideas(self, context: Dict[str, Any], feedback: Optional[Any] = None) -> Dict[str, Any]:
        knowledge_base = context.get("knowledge_base")
        if not knowledge_base:
            raise ValueError("KnowledgeBase is required.")
            
        num_ideas = context.get("num_ideas", 3)
        logger.info(f"Generating {num_ideas} disruptive ideas...")
        
        disruptive_ideas = [random.choice(self.creativity_techniques)(knowledge_base) for _ in range(num_ideas)]
        
        return {"content": disruptive_ideas, "summary": f"تم توليد {len(disruptive_ideas)} فكرة غير تقليدية."}

    def _juxtapose_concepts(self, kb: Dict[str, Any]) -> Dict[str, str]:
        entities = kb.get("entities", [])
        if len(entities) < 2: return {"technique": "Juxtaposition", "idea": "لا توجد كيانات كافية."}
        e1, e2 = random.sample(entities, 2)
        return {"technique": "ربط المفاهيم", "idea": f"ماذا لو كانت '{e1['name']}' رمزًا لـ '{e2['name']}'؟"}

    def _invert_expectation(self, kb: Dict[str, Any]) -> Dict[str, str]:
        rels = kb.get("relationship_graph", [])
        if not rels: return {"technique": "Inversion", "idea": "لا توجد علاقات لتحليلها."}
        rel = random.choice(rels)
        inversion = {"يحب": "يكره", "يثق في": "يخون", "يساعد": "يستغل"}
        inv_rel = inversion.get(rel['relation'], f"عكس '{rel['relation']}'")
        return {"technique": "عكس التوقعات", "idea": f"ماذا لو كانت علاقة '{rel['source']}' بـ '{rel['target']}' تخفي '{inv_rel}'؟"}

    def _introduce_random_element(self, kb: Dict[str, Any]) -> Dict[str, str]:
        elements = ["عاصفة مفاجئة", "طفل غامض", "اكتشاف أثري"]
        return {"technique": "عنصر عشوائي", "idea": f"كيف سيغير '{random.choice(elements)}' كل شيء؟"}
        
    def _change_perspective(self, kb: Dict[str, Any]) -> Dict[str, str]:
        s_char = next((e['name'] for e in kb.get("entities", []) if e.get('importance_score', 0) < 7), None)
        return {"technique": "تغيير المنظور", "idea": f"ماذا لو تم سرد الفصل التالي من وجهة نظر '{s_char or 'شخصية ثانوية'}'؟"}
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
