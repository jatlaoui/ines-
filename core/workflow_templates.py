# core/workflow_templates.py (V2 - Merged and Expanded)
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field

# --- تعريف نماذج البيانات (كانت في ملف منفصل) ---
class TaskType(str, Enum):
    """
    قائمة شاملة بكل أنواع المهام الممكنة في النظام.
    تستخدمها أثينا لاتخاذ قراراتها.
    """
    # مهام التحليل والتخطيط
    ANALYZE_CONTEXT = "analyze_context"  # مهمة عامة لـ AdvancedContextEngine
    CREATE_PSYCH_PROFILE = "create_psych_profile"
    CREATE_BLUEPRINT = "create_blueprint"
    SUGGEST_SUBPLOTS = "suggest_subplots"
    ANALYZE_PACING = "analyze_pacing"
    
    # مهام الكتابة والإنتاج
    WRITE_CHAPTER = "write_chapter"
    
    # مهام النقد والتحسين
    CRITIQUE_CHAPTER = "critique_chapter"
    CHECK_CONSISTENCY = "check_consistency"
    REFINE_CHAPTER_WITH_FEEDBACK = "refine_chapter_with_feedback"

    # مهام متخصصة ومتقدمة
    INJECT_NARRATIVE_MUTATION = "inject_narrative_mutation" # لـ CreativeChaosAgent
    CORROBORATE_HISTORY = "corroborate_history" # لـ HistoricalCorroborationAgent
    
    # مهام سير العمل
    FINISH_WORKFLOW = "finish_workflow"

class WorkflowTask(BaseModel):
    id: str
    name: str
    task_type: TaskType
    input_data: Dict[str, Any] = Field(default_factory=dict, description="البيانات المحددة لهذه المهمة.")
    dependencies: List[str] = Field(default_factory=list, description="قائمة بمعرفات المهام التي يجب أن تكتمل أولاً.")
    
class WorkflowTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    tasks: List[WorkflowTask]

class WorkflowTemplateManager:
    """
    يدير قوالب سير العمل المحددة مسبقًا في النظام.
    """
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        self._create_templates()

    def _create_templates(self):
        """
        إنشاء قوالب سير العمل. في نظام حقيقي، سيتم تحميلها من قاعدة بيانات أو ملفات.
        """
        # --- قالب كتابة رواية قصيرة ---
        short_novel_template = WorkflowTemplate(
            id="short_novel_v1",
            name="كتابة رواية قصيرة (3 فصول)",
            description="سير عمل أساسي لإنشاء رواية قصيرة من الفكرة إلى المسودة الأولى.",
            category="narrative_writing",
            tasks=[
                WorkflowTask(id="task1", name="تحليل السياق الأولي", task_type=TaskType.ANALYZE_CONTEXT, input_data={"text_content": "{initial_context}"}),
                WorkflowTask(id="task2", name="بناء المخطط السردي", task_type=TaskType.CREATE_BLUEPRINT, dependencies=["task1"]),
                WorkflowTask(id="task3", name="كتابة الفصل الأول", task_type=TaskType.WRITE_CHAPTER, dependencies=["task2"]),
                WorkflowTask(id="task4", name="نقد الفصل الأول", task_type=TaskType.CRITIQUE_CHAPTER, dependencies=["task3"]),
                # ... وهكذا لبقية الفصول ...
            ]
        )
        self.templates[short_novel_template.id] = short_novel_template

    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        return self.templates.get(template_id)

    def list_templates(self) -> List[Dict[str, str]]:
        return [{"id": t.id, "name": t.name, "description": t.description} for t in self.templates.values()]

# إنشاء مثيل وحيد
workflow_template_manager = WorkflowTemplateManager()
