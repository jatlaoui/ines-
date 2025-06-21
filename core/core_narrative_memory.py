# core/core_narrative_memory.py
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import numpy as np

# في نظام حقيقي، سنستخدم قاعدة بيانات متخصصة مثل ChromaDB أو FAISS
# هنا، سنحاكيها باستخدام قاموس و list في الذاكرة.

logger = logging.getLogger("CoreNarrativeMemory")

@dataclass
class MemoryEntry:
    """يمثل إدخالاً واحدًا في الذاكرة السردية."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "generic"  # (e.g., 'plot_point', 'character_update', 'emotional_beat')
    content: str = ""
    embedding: Optional[List[float]] = None # Vector embedding
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class CoreNarrativeMemory:
    """
    الذاكرة السردية المركزية للنظام.
    تخزن الأحداث والتطورات الرئيسية كـ "متجهات دلالية" (Embeddings)
    لتوفير سياق ذكي وطويل المدى للوكلاء.
    """
    def __init__(self):
        self._memory_bank: Dict[str, MemoryEntry] = {}
        logger.info("✅ Core Narrative Memory initialized.")

    def _generate_embedding(self, text: str) -> List[float]:
        """
        (محاكاة) توليد متجه دلالي للنص.
        في نظام حقيقي، سيتم استدعاء نموذج embedding متخصص.
        """
        # محاكاة بسيطة تعتمد على طول النص كمتجه
        np.random.seed(len(text))
        return np.random.rand(128).tolist()

    def add_entry(self, entry_type: str, content: str, metadata: Dict[str, Any] = None):
        """
        إضافة إدخال جديد إلى الذاكرة.
        """
        embedding = self._generate_embedding(content)
        entry = MemoryEntry(
            type=entry_type,
            content=content,
            embedding=embedding,
            metadata=metadata or {}
        )
        self._memory_bank[entry.id] = entry
        logger.info(f"🧠 New memory entry added: [Type: {entry_type}] - '{content[:50]}...'")

    def query(self, query_text: str, top_k: int = 5) -> List[MemoryEntry]:
        """
        (محاكاة) استعلام الذاكرة للعثور على الإدخالات الأكثر صلة.
        """
        if not self._memory_bank:
            return []

        query_embedding = np.array(self._generate_embedding(query_text))
        
        # حساب التشابه (Cosine Similarity) مع كل الإدخالات
        similarities = []
        for entry in self._memory_bank.values():
            entry_embedding = np.array(entry.embedding)
            # حساب التشابه بين متجه الاستعلام ومتجه الإدخال
            sim = np.dot(query_embedding, entry_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(entry_embedding))
            similarities.append((entry, sim))

        # ترتيب النتائج حسب التشابه وإرجاع أفضلها
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return [entry for entry, sim in similarities[:top_k]]

    def get_full_chronology(self) -> List[MemoryEntry]:
        """إرجاع كل الإدخالات مرتبة زمنياً."""
        return sorted(self._memory_bank.values(), key=lambda x: x.timestamp)
        
    def clear(self):
        """مسح الذاكرة (لبدء مشروع جديد)."""
        self._memory_bank.clear()
        logger.info("Core Narrative Memory has been cleared.")

# إنشاء مثيل وحيد للذاكرة يمكن استيراده في أي مكان
narrative_memory = CoreNarrativeMemory()
