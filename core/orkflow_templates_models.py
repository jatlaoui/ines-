# core/workflow_templates_models.py
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class TaskType(Enum):
    # قائمة شاملة بكل أنواع المهام الممكنة في النظام
    CUSTOM_AGENT_TASK = "custom_agent_task"
    GENERATE_IDEAS = "generate_ideas"
    BUILD_BLUEPRINT = "build_blueprint"
    GENERATE_CHAPTER = "generate_chapter"
    DYNAMIC_REPLAN = "dynamic_replan"
    CHECK_CONSISTENCY = "check_consistency"
    VALIDATE_DIALECT = "validate_dialect"
    MERGE_DATA = "merge_data"
    FINISH_WORKFLOW = "finish_workflow"
    # ... إضافة بقية الأنواع

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class WorkflowTask(BaseModel):
    id: str
    name: str
    task_type: TaskType
    input_data: Dict = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    # حقول إضافية للمهام التكرارية
    is_loop: bool = False
    loop_over: Optional[str] = None # e.g., "{{task_id.output.key}}"

class WorkflowTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    tasks: List[WorkflowTask]
