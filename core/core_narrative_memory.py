# core/core_narrative_memory.py (V2 - Embeddings Powered)
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np
import pandas as pd

# استيراد خدمة LLM لتوليد المتجهات
import google.generativeai as genai
from google.generativeai.types import EmbedContentConfig, TaskType

logger = logging.getLogger("CoreNarrativeMemory")

class MemoryEntry:
    # ... (يمكن تبسيطها أو استخدام قاموس مباشرة)
    def __init__(self, entry_type: str, content: str, metadata: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.type = entry_type
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        # سيتم إضافة المتجه لاحقًا

class CoreNarrativeMemory:
    """
    الذاكرة السردية المركزية (V2).
    تستخدم Gemini Embeddings لتوفير سياق ذكي وطويل المدى.
    """
    def __init__(self):
        self.embedding_model = 'models/embedding-001'
        # استخدام Pandas DataFrame كمحاكاة لقاعدة بيانات متجهة (Vector DB)
        self.memory_df = pd.DataFrame(columns=['id', 'type', 'content', 'metadata', 'timestamp', 'embedding'])
        logger.info("✅ Core Narrative Memory (V2) initialized with in-memory DataFrame.")

    def _generate_embedding(self, text: str, task_type: TaskType) -> List[float]:
        """
        تولد متجهًا دلاليًا للنص باستخدام Gemini API.
        """
        try:
            # استخدام task_type الصحيح للحصول على أفضل النتائج
            response = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type=task_type
            )
            return response['embedding']
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return []

    def add_entry(self, entry_type: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        تضيف إدخالاً جديدًا إلى الذاكرة، مع توليد متجه دلالي له.
        """
        if not content:
            return

        entry = MemoryEntry(entry_type, content, metadata)
        # توليد المتجه كـ 'document' لأنه سيتم البحث فيه لاحقًا
        embedding = self._generate_embedding(content, TaskType.RETRIEVAL_DOCUMENT)
        
        if not embedding:
            logger.warning(f"Could not generate embedding for entry. Skipping add.")
            return

        new_entry_df = pd.DataFrame([{
            'id': entry.id,
            'type': entry.type,
            'content': entry.content,
            'metadata': entry.metadata,
            'timestamp': entry.timestamp,
            'embedding': embedding
        }])
        
        self.memory_df = pd.concat([self.memory_df, new_entry_df], ignore_index=True)
        logger.info(f"🧠 New memory entry added: [ID: {entry.id}, Type: {entry.type}]")

    def query(self, query_text: str, top_k: int = 3, entry_type_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        تستعلم الذاكرة باستخدام البحث الدلالي للعثور على الإدخالات الأكثر صلة.
        """
        if self.memory_df.empty:
            return []

        # توليد متجه للسؤال
        query_embedding = self._generate_embedding(query_text, TaskType.RETRIEVAL_QUERY)
        if not query_embedding:
            return []

        # تصفية قاعدة البيانات حسب نوع الإدخال إذا تم تحديده
        target_df = self.memory_df
        if entry_type_filter:
            target_df = self.memory_df[self.memory_df['type'] == entry_type_filter]

        if target_df.empty:
            return []

        # حساب الضرب النقطي (Dot Product) للعثور على التشابه
        dot_products = np.dot(np.stack(target_df['embedding']), query_embedding)
        
        # الحصول على مؤشرات أفضل النتائج
        # نستخدم argpartition للحصول على أفضل k بكفاءة
        # إذا كان عدد النتائج أقل من k، نأخذ كل النتائج
        num_results = min(top_k, len(dot_products))
        indices = np.argpartition(dot_products, -num_results)[-num_results:]
        
        # ترتيب النتائج حسب درجة التشابه
        results_df = target_df.iloc[indices]
        results_df['similarity'] = dot_products[indices]
        results_df = results_df.sort_values(by='similarity', ascending=False)
        
        return results_df.to_dict('records')

    def get_full_chronology(self) -> List[Dict[str, Any]]:
        """ترجع كل الإدخالات مرتبة زمنياً."""
        return self.memory_df.sort_values(by='timestamp').to_dict('records')
        
    def clear(self):
        """تمسح الذاكرة (لبدء مشروع جديد)."""
        self.memory_df = pd.DataFrame(columns=['id', 'type', 'content', 'metadata', 'timestamp', 'embedding'])
        logger.info("Core Narrative Memory has been cleared.")

# إنشاء مثيل وحيد للذاكرة
narrative_memory = CoreNarrativeMemory()
