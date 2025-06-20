# blueprint_architect_agent.py (الإصدار المحسن)
from typing import Dict, Any, List
from dataclasses import dataclass
import math

@dataclass
class ChapterOutline:
    title: str
    summary: str
    emotional_focus: str  # العاطفة السائدة في هذا الفصل
    key_events: List[str]  # الأحداث الرئيسية المرتبطة بالفصل
    character_arcs: Dict[str, str]  # تطورات شخصية لكل شخصية رئيسية

@dataclass
class StoryBlueprint:
    introduction: str
    chapters: List[ChapterOutline]
    conclusion: str

class BlueprintArchitectAgent:
    """
    وكيل يقوم بتحويل KnowledgeBase إلى مخطط سردي ذكي.
    """
    def __init__(self, kb: Dict[str, Any]):
        self.kb = kb
        self.entities = kb.get('entities', [])
        self.relationships = kb.get('relationship_graph', [])
        self.emotional_arc = kb.get('emotional_arc', [])

    def generate_blueprint(self) -> StoryBlueprint:
        """
        يولد مخططًا سرديًا ذكيًا بناءً على KnowledgeBase.
        """
        num_chapters = self._calculate_optimal_chapters()
        chapter_emotional_segments = self._segment_emotional_arc(num_chapters)
        chapter_events = self._distribute_events_to_chapters(num_chapters)

        chapters = []
        for i in range(num_chapters):
            seg = chapter_emotional_segments[i]
            events = chapter_events[i]

            title = self._generate_chapter_title(i+1, seg, events)
            summary = self._generate_chapter_summary(i+1, seg, events)
            character_arcs = self._map_character_arcs_to_chapter(events)

            chapters.append(ChapterOutline(
                title=title,
                summary=summary,
                emotional_focus=f"الانتقال من {seg['start_emotion']} إلى {seg['end_emotion']}",
                key_events=[e['relation'] for e in events],
                character_arcs=character_arcs
            ))

        intro = self._generate_introduction()
        conclusion = self._generate_conclusion()
        return StoryBlueprint(introduction=intro, chapters=chapters, conclusion=conclusion)

    def _calculate_optimal_chapters(self) -> int:
        complexity = len(self.entities) + len(self.relationships)
        chapters = math.ceil(complexity / 4)
        return min(max(chapters, 3), 12)

    def _segment_emotional_arc(self, num_chapters: int) -> List[Dict[str, Any]]:
        if not self.emotional_arc:
            return [{'start_emotion':'محايد','end_emotion':'محايد','peak_emotion':'محايد','points':[]}] * num_chapters

        segments = []
        points_per = len(self.emotional_arc) / num_chapters
        for i in range(num_chapters):
            start = math.floor(i * points_per)
            end = math.ceil((i+1) * points_per)
            pts = self.emotional_arc[start:end] or [self.emotional_arc[-1]]

            start_emotion = pts[0]['emotion']
            end_emotion = pts[-1]['emotion']
            peak = max(pts, key=lambda p: p['intensity'])

            segments.append({
                'start_emotion': start_emotion,
                'end_emotion': end_emotion,
                'peak_emotion': peak['emotion'],
                'points': pts
            })
        return segments

    def _distribute_events_to_chapters(self, num_chapters: int) -> List[List[Dict[str, Any]]]:
        if not self.relationships:
            return [[] for _ in range(num_chapters)]
        per = math.ceil(len(self.relationships) / num_chapters)
        return [self.relationships[i*per:(i+1)*per] for i in range(num_chapters)]

    def _generate_chapter_title(self, num: int, seg: Dict[str, Any], events: List[Dict[str, Any]]) -> str:
        main = next((e['relation'] for e in events if 'يؤدي إلى' in e['relation']), None)
        return f"الفصل {num}: {main or ('ذروة ' + seg['peak_emotion'])}"

    def _generate_chapter_summary(self, num: int, seg: Dict[str, Any], events: List[Dict[str, Any]]) -> str:
        evs = ", ".join([f"'{e['relation']}'" for e in events]) or 'بدون أحداث رئيسية'
        return (
            f"في هذا الفصل، تتفاعل الأحداث {evs}. "
            f"عاطفيًا، يبدأ بـ '{seg['start_emotion']}', يصل إلى '{seg['peak_emotion']}', وينتهي بـ '{seg['end_emotion']}'."
        )

    def _map_character_arcs_to_chapter(self, events: List[Dict[str, Any]]) -> Dict[str, str]:
        arcs = {}
        chars = {e['name'] for e in self.entities if 'character' in e.get('type', '')}
        for ev in events:
            if ev['source'] in chars:
                arcs[ev['source']] = f"يتطور عبر '{ev['relation']}'"
        return arcs

    def _generate_introduction(self) -> str:
        mains = [e['name'] for e in self.entities if e.get('importance_score',0) > 8]
        conflict = next((r['relation'] for r in self.relationships if 'يؤدي إلى' in r['relation']), 'صراع غير محدد')
        return (
            f"تبدأ حكايتنا مع {', '.join(mains)}, حيث يبرز {conflict} كأساس للصراع."  
        )

    def _generate_conclusion(self) -> str:
        final = self.emotional_arc[-1]['emotion'] if self.emotional_arc else 'نتيجة غير محددة'
        return (
            f"في الختام، تختتم الرحلة بشعور '{final}'، تاركة أثرًا عميقًا لدى القارئ."
        )

# مثال للاستخدام (يبقى كما هو)
