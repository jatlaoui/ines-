"""
النواة الموحدة الوحيدة لإدارة سير العمل والوكلاء
تطبيق المرحلة الأولى من التحسينات المنهجية - نظام موحد وبسيط وقوي
"""

import asyncio
import logging
import json
import uuid
from typing import Dict, Any, List, Optional, Tuple, Callable, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
import traceback

# الاستيراد من الأنظمة الموحدة فقط
from core_database import core_db, WorkflowStatus, TaskStatus
from core_auth import core_auth, UserSession, require_auth

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskType(Enum):
    """أنواع المهام المدعومة"""
    # مهام الوكلاء الأساسية
    ANALYZE_NOVEL = "analyze_novel"
    GENERATE_IDEAS = "generate_ideas"
    BUILD_BLUEPRINT = "build_blueprint"
    GENERATE_CHAPTER = "generate_chapter"
    REFINE_TEXT = "refine_text"
    CHECK_CONSISTENCY = "check_consistency"
    GENERATE_REPORT = "generate_report"
    
    # مهام التحكم والمنطق
    CONDITION = "condition"
    MERGE_DATA = "merge_data"
    TRANSFORM_DATA = "transform_data"
    SAVE_TO_PROJECT = "save_to_project"
    CUSTOM_AGENT_TASK = "custom_agent_task"
    
    # مهام الشاهد
    WITNESS_UPLOAD = "witness_upload"
    WITNESS_EXTRACT = "witness_extract"
    WITNESS_ANALYZE = "witness_analyze"
    WITNESS_INTEGRATE = "witness_integrate"
    WITNESS_EVALUATE = "witness_evaluate"
    
    # مهام الاندماج السردي الفائق
    FUSION_CREATE_PROJECT = "fusion_create_project"
    FUSION_ANALYZE_NARRATIVE = "fusion_analyze_narrative"
    FUSION_ASSESS_COMPATIBILITY = "fusion_assess_compatibility"
    FUSION_CREATE_BLUEPRINT = "fusion_create_blueprint"
    FUSION_SYNTHESIZE_NARRATIVE = "fusion_synthesize_narrative"
    FUSION_ARBITRATE_QUALITY = "fusion_arbitrate_quality"
    FUSION_REFINE_SYNTHESIS = "fusion_refine_synthesis"
    FUSION_FINALIZE_PROJECT = "fusion_finalize_project"

class TaskPriority(Enum):
    """أولوية المهام"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    """حالة المهمة"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

@dataclass
class WorkflowTask:
    """مهمة في سير العمل"""
    id: str
    name: str
    task_type: TaskType
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    agent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowTemplate:
    """قالب سير العمل"""
    id: str
    name: str
    description: str
    version: str
    category: str
    tasks: List[WorkflowTask]
    is_public: bool = False
    author_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass  
class WorkflowExecution:
    """تنفيذ سير العمل"""
    id: str
    template_id: str
    user_id: str
    name: str
    status: WorkflowStatus
    current_task_index: int = 0
    progress_percentage: float = 0.0
    tasks: List[WorkflowTask] = field(default_factory=list)
    context_data: Dict[str, Any] = field(default_factory=dict)
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class CoreOrchestrator:
    """النواة الموحدة لإدارة سير العمل والوكلاء"""
    
    def __init__(self):
        self.running_workflows: Dict[str, WorkflowExecution] = {}
        self.task_handlers: Dict[TaskType, Callable] = {}
        self.workflow_templates: Dict[str, WorkflowTemplate] = {}
        self._init_default_handlers()
        self._load_default_templates()
    
    def _init_default_handlers(self):
        """تهيئة معالجات المهام الافتراضية"""
        self.task_handlers = {
            TaskType.ANALYZE_NOVEL: self._handle_analyze_novel,
            TaskType.GENERATE_IDEAS: self._handle_generate_ideas,
            TaskType.BUILD_BLUEPRINT: self._handle_build_blueprint,
            TaskType.GENERATE_CHAPTER: self._handle_generate_chapter,
            TaskType.REFINE_TEXT: self._handle_refine_text,
            TaskType.CHECK_CONSISTENCY: self._handle_check_consistency,
            TaskType.GENERATE_REPORT: self._handle_generate_report,
            TaskType.CONDITION: self._handle_condition,
            TaskType.MERGE_DATA: self._handle_merge_data,
            TaskType.TRANSFORM_DATA: self._handle_transform_data,
            TaskType.SAVE_TO_PROJECT: self._handle_save_to_project,
            TaskType.CUSTOM_AGENT_TASK: self._handle_custom_agent_task,
            TaskType.WITNESS_UPLOAD: self._handle_witness_upload,
            TaskType.WITNESS_EXTRACT: self._handle_witness_extract,
            TaskType.WITNESS_ANALYZE: self._handle_witness_analyze,
            TaskType.WITNESS_INTEGRATE: self._handle_witness_integrate,
            TaskType.WITNESS_EVALUATE: self._handle_witness_evaluate,
        }
    
    def _load_default_templates(self):
        """تحميل قوالب سير العمل الافتراضية"""
        # قالب الرحلة الأساسية
        basic_journey = WorkflowTemplate(
            id="basic_novel_journey",
            name="رحلة كتابة الرواية الأساسية",
            description="سير العمل الأساسي لكتابة رواية كاملة",
            version="1.0",
            category="basic",
            tasks=[
                WorkflowTask(
                    id="task_1",
                    name="تحليل المصدر",
                    task_type=TaskType.ANALYZE_NOVEL,
                    input_data={"source_type": "user_input"},
                    dependencies=[]
                ),
                WorkflowTask(
                    id="task_2", 
                    name="توليد الأفكار",
                    task_type=TaskType.GENERATE_IDEAS,
                    input_data={"count": 5, "creativity_level": "high"},
                    dependencies=["task_1"]
                ),
                WorkflowTask(
                    id="task_3",
                    name="بناء المخطط",
                    task_type=TaskType.BUILD_BLUEPRINT,
                    input_data={"structure_type": "three_act"},
                    dependencies=["task_2"]
                ),
                WorkflowTask(
                    id="task_4",
                    name="كتابة الفصول", 
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"chapters_count": 12},
                    dependencies=["task_3"]
                ),
                WorkflowTask(
                    id="task_5",
                    name="المراجعة النهائية",
                    task_type=TaskType.CHECK_CONSISTENCY,
                    input_data={"check_type": "full"},
                    dependencies=["task_4"]
                )
            ]
        )
        
        # قالب مع الشاهد
        witness_journey = WorkflowTemplate(
            id="witness_enhanced_journey",
            name="رحلة كتابة معززة بالشاهد", 
            description="سير عمل متقدم يدمج ميزة الشاهد",
            version="1.0",
            category="advanced",
            tasks=[
                WorkflowTask(
                    id="task_1",
                    name="رفع مصادر الشاهد",
                    task_type=TaskType.WITNESS_UPLOAD,
                    input_data={"auto_extract": True},
                    dependencies=[]
                ),
                WorkflowTask(
                    id="task_2",
                    name="استخراج المحتوى",
                    task_type=TaskType.WITNESS_EXTRACT,
                    input_data={"extract_mode": "comprehensive"},
                    dependencies=["task_1"]
                ),
                WorkflowTask(
                    id="task_3",
                    name="تحليل النص الأصلي",
                    task_type=TaskType.ANALYZE_NOVEL,
                    input_data={"include_witness": True},
                    dependencies=["task_2"]
                ),
                WorkflowTask(
                    id="task_4",
                    name="توليد أفكار محسنة",
                    task_type=TaskType.GENERATE_IDEAS,
                    input_data={"use_witness": True, "count": 7},
                    dependencies=["task_3"]
                ),
                WorkflowTask(
                    id="task_5",
                    name="بناء مخطط متقدم",
                    task_type=TaskType.BUILD_BLUEPRINT,
                    input_data={"witness_integration": True},
                    dependencies=["task_4"]
                )
            ]
        )
        
        # قالب مخصص سريع
        quick_chapter = WorkflowTemplate(
            id="quick_chapter_generation",
            name="توليد فصل سريع",
            description="قالب سريع لتوليد فصل واحد",
            version="1.0", 
            category="quick",
            tasks=[
                WorkflowTask(
                    id="task_1",
                    name="توليد فصل",
                    task_type=TaskType.GENERATE_CHAPTER,
                    input_data={"quick_mode": True},
                    dependencies=[]
                ),
                WorkflowTask(
                    id="task_2",
                    name="تحسين النص",
                    task_type=TaskType.REFINE_TEXT,
                    input_data={"refinement_level": "moderate"},
                    dependencies=["task_1"]
                )
            ]
        )
        
        self.workflow_templates = {
            basic_journey.id: basic_journey,
            witness_journey.id: witness_journey,
            quick_chapter.id: quick_chapter
        }
    
    # === إدارة قوالب سير العمل ===
    
    def create_workflow_template(self, template_data: Dict[str, Any], user_session: UserSession) -> str:
        """إنشاء قالب سير عمل جديد"""
        try:
            template_id = str(uuid.uuid4())
            
            # تحويل مهام من dict إلى WorkflowTask objects
            tasks = []
            for task_data in template_data.get('tasks', []):
                task = WorkflowTask(
                    id=task_data.get('id', str(uuid.uuid4())),
                    name=task_data['name'],
                    task_type=TaskType(task_data['task_type']),
                    input_data=task_data.get('input_data', {}),
                    dependencies=task_data.get('dependencies', []),
                    priority=TaskPriority(task_data.get('priority', TaskPriority.NORMAL.value)),
                    metadata=task_data.get('metadata', {})
                )
                tasks.append(task)
            
            template = WorkflowTemplate(
                id=template_id,
                name=template_data['name'],
                description=template_data.get('description', ''),
                version=template_data.get('version', '1.0'),
                category=template_data.get('category', 'user_created'),
                tasks=tasks,
                is_public=template_data.get('is_public', False),
                author_id=user_session.user_id,
                tags=template_data.get('tags', []),
                metadata=template_data.get('metadata', {})
            )
            
            # حفظ في الذاكرة
            self.workflow_templates[template_id] = template
            
            # حفظ في قاعدة البيانات
            core_db.save_workflow_template(template)
            
            logger.info(f"تم إنشاء قالب سير العمل: {template.name} (ID: {template_id})")
            return template_id
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء قالب سير العمل: {str(e)}")
            raise
    
    def get_workflow_templates(self, user_session: UserSession, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """الحصول على قوالب سير العمل المتاحة"""
        try:
            templates = []
            for template in self.workflow_templates.values():
                # فحص الأذونات - القوالب العامة أو المملوكة للمستخدم
                if template.is_public or template.author_id == user_session.user_id:
                    # تصفية حسب الفئة إذا طُلبت
                    if not category or template.category == category:
                        template_dict = asdict(template)
                        # تحويل التواريخ إلى strings
                        template_dict['created_at'] = template.created_at.isoformat()
                        # تحويل المهام
                        template_dict['tasks'] = [asdict(task) for task in template.tasks]
                        templates.append(template_dict)
            
            return templates
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على قوالب سير العمل: {str(e)}")
            return []
    
    def delete_workflow_template(self, template_id: str, user_session: UserSession) -> bool:
        """حذف قالب سير عمل"""
        try:
            if template_id not in self.workflow_templates:
                return False
            
            template = self.workflow_templates[template_id]
            
            # فحص الأذونات
            if template.author_id != user_session.user_id and user_session.role.value != 'admin':
                raise PermissionError("ليس لديك صلاحية لحذف هذا القالب")
            
            # حذف من الذاكرة
            del self.workflow_templates[template_id]
            
            # حذف من قاعدة البيانات
            core_db.delete_workflow_template(template_id)
            
            logger.info(f"تم حذف قالب سير العمل: {template_id}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في حذف قالب سير العمل: {str(e)}")
            return False
    
    # === تنفيذ سير العمل ===
    
    def start_workflow(self, template_id: str, context_data: Dict[str, Any], user_session: UserSession) -> str:
        """بدء تنفيذ سير عمل من قالب"""
        try:
            if template_id not in self.workflow_templates:
                raise ValueError(f"قالب سير العمل غير موجود: {template_id}")
            
            template = self.workflow_templates[template_id]
            execution_id = str(uuid.uuid4())
            
            # إنشاء نسخ من مهام القالب
            execution_tasks = []
            for task in template.tasks:
                execution_task = WorkflowTask(
                    id=task.id,
                    name=task.name,
                    task_type=task.task_type,
                    input_data=task.input_data.copy(),
                    dependencies=task.dependencies.copy(),
                    priority=task.priority,
                    metadata=task.metadata.copy()
                )
                execution_tasks.append(execution_task)
            
            # إنشاء تنفيذ سير العمل
            execution = WorkflowExecution(
                id=execution_id,
                template_id=template_id,
                user_id=user_session.user_id,
                name=f"تنفيذ {template.name}",
                status=WorkflowStatus.PENDING,
                tasks=execution_tasks,
                context_data=context_data,
                metadata={
                    'template_name': template.name,
                    'template_version': template.version
                }
            )
            
            # حفظ في الذاكرة
            self.running_workflows[execution_id] = execution
            
            # حفظ في قاعدة البيانات
            core_db.save_workflow_execution(execution)
            
            logger.info(f"تم بدء تنفيذ سير العمل: {execution.name} (ID: {execution_id})")
            
            # بدء التنفيذ الفعلي في الخلفية
            asyncio.create_task(self._execute_workflow(execution_id))
            
            return execution_id
            
        except Exception as e:
            logger.error(f"خطأ في بدء سير العمل: {str(e)}")
            raise
    
    async def _execute_workflow(self, execution_id: str):
        """تنفيذ سير العمل الفعلي"""
        try:
            execution = self.running_workflows[execution_id]
            execution.status = WorkflowStatus.RUNNING
            execution.started_at = datetime.now()
            
            # تحديث قاعدة البيانات
            core_db.update_workflow_execution(execution)
            
            logger.info(f"بدء تنفيذ سير العمل: {execution.name}")
            
            # تنفيذ المهام بناءً على التبعيات
            completed_tasks = set()
            total_tasks = len(execution.tasks)
            
            while len(completed_tasks) < total_tasks:
                # البحث عن المهام الجاهزة للتنفيذ
                ready_tasks = []
                for task in execution.tasks:
                    if (task.status == TaskStatus.PENDING and 
                        all(dep in completed_tasks for dep in task.dependencies)):
                        ready_tasks.append(task)
                
                if not ready_tasks:
                    # تحقق من وجود مهام عالقة
                    pending_tasks = [t for t in execution.tasks if t.status == TaskStatus.PENDING]
                    if pending_tasks:
                        error_msg = f"مهام عالقة في التبعيات: {[t.name for t in pending_tasks]}"
                        raise RuntimeError(error_msg)
                    break
                
                # تنفيذ المهام الجاهزة
                for task in ready_tasks:
                    try:
                        await self._execute_task(task, execution)
                        completed_tasks.add(task.id)
                        
                        # تحديث التقدم
                        execution.progress_percentage = (len(completed_tasks) / total_tasks) * 100
                        execution.current_task_index = len(completed_tasks)
                        
                        # تحديث قاعدة البيانات
                        core_db.update_workflow_execution(execution)
                        
                    except Exception as task_error:
                        logger.error(f"خطأ في المهمة {task.name}: {str(task_error)}")
                        task.status = TaskStatus.FAILED
                        task.error_message = str(task_error)
                        
                        # فشل سير العمل إذا فشلت مهمة أساسية
                        execution.status = WorkflowStatus.FAILED
                        execution.error_message = f"فشلت المهمة: {task.name}"
                        core_db.update_workflow_execution(execution)
                        return
            
            # إكمال سير العمل بنجاح
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.now()
            execution.progress_percentage = 100.0
            
            # تجميع النتائج النهائية
            execution.result_data = self._compile_workflow_results(execution)
            
            # تحديث قاعدة البيانات
            core_db.update_workflow_execution(execution)
            
            logger.info(f"اكتمل تنفيذ سير العمل: {execution.name}")
            
        except Exception as e:
            logger.error(f"خطأ في تنفيذ سير العمل {execution_id}: {str(e)}")
            execution = self.running_workflows[execution_id]
            execution.status = WorkflowStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.now()
            core_db.update_workflow_execution(execution)
    
    async def _execute_task(self, task: WorkflowTask, execution: WorkflowExecution):
        """تنفيذ مهمة واحدة"""
        try:
            logger.info(f"بدء تنفيذ المهمة: {task.name}")
            
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            
            # الحصول على معالج المهمة
            if task.task_type not in self.task_handlers:
                raise ValueError(f"نوع المهمة غير مدعوم: {task.task_type}")
            
            handler = self.task_handlers[task.task_type]
            
            # دمج البيانات من المهام السابقة
            enriched_input = self._enrich_task_input(task, execution)
            
            # تنفيذ المهمة
            result = await handler(enriched_input, execution.context_data)
            
            # حفظ النتيجة
            task.output_data = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            logger.info(f"اكتملت المهمة: {task.name}")
            
        except Exception as e:
            logger.error(f"خطأ في تنفيذ المهمة {task.name}: {str(e)}")
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.completed_at = datetime.now()
            raise
    
    def _enrich_task_input(self, task: WorkflowTask, execution: WorkflowExecution) -> Dict[str, Any]:
        """إثراء مدخلات المهمة بنتائج المهام السابقة"""
        enriched_input = task.input_data.copy()
        
        # إضافة نتائج المهام التي تعتمد عليها
        for dep_id in task.dependencies:
            dep_task = next((t for t in execution.tasks if t.id == dep_id), None)
            if dep_task and dep_task.output_data:
                enriched_input[f"from_{dep_id}"] = dep_task.output_data
        
        # إضافة السياق العام
        enriched_input["execution_context"] = execution.context_data
        enriched_input["execution_id"] = execution.id
        
        return enriched_input
    
    def _compile_workflow_results(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """تجميع النتائج النهائية لسير العمل"""
        results = {
            "execution_summary": {
                "total_tasks": len(execution.tasks),
                "completed_tasks": len([t for t in execution.tasks if t.status == TaskStatus.COMPLETED]),
                "failed_tasks": len([t for t in execution.tasks if t.status == TaskStatus.FAILED]),
                "execution_time": (execution.completed_at - execution.started_at).total_seconds() if execution.started_at and execution.completed_at else 0
            },
            "task_results": {}
        }
        
        # تجميع نتائج كل مهمة
        for task in execution.tasks:
            results["task_results"][task.id] = {
                "name": task.name,
                "status": task.status.value,
                "output_data": task.output_data,
                "error_message": task.error_message
            }
        
        return results
    
    # === معالجات المهام الأساسية ===
    
    async def _handle_analyze_novel(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج تحليل الرواية"""
        # محاكاة المعالجة (سيتم استبدالها بالوكلاء الحقيقيين)
        await asyncio.sleep(1)  # محاكاة وقت المعالجة
        
        return {
            "analysis_type": "comprehensive",
            "themes": ["الحب", "الصراع", "النمو الشخصي"],
            "characters_count": 5,
            "estimated_chapters": 12,
            "writing_style": "سردي تقليدي",
            "complexity_level": "متوسط"
        }
    
    async def _handle_generate_ideas(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج توليد الأفكار"""
        await asyncio.sleep(1)
        
        count = input_data.get('count', 5)
        ideas = []
        
        for i in range(count):
            ideas.append({
                "id": f"idea_{i+1}",
                "title": f"فكرة رقم {i+1}",
                "description": f"وصف تفصيلي للفكرة رقم {i+1}",
                "genre": "دراما",
                "complexity": "متوسط",
                "estimated_length": "متوسط"
            })
        
        return {
            "generated_ideas": ideas,
            "total_count": count,
            "generation_method": "ai_assisted"
        }
    
    async def _handle_build_blueprint(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج بناء المخطط"""
        await asyncio.sleep(1)
        
        return {
            "structure_type": input_data.get('structure_type', 'three_act'),
            "total_chapters": 12,
            "chapters": [
                {"number": i+1, "title": f"الفصل {i+1}", "description": f"وصف الفصل {i+1}"}
                for i in range(12)
            ],
            "character_arcs": ["تطور البطل", "الصراع الداخلي", "القرار النهائي"],
            "plot_points": ["الحدث المحرك", "نقطة التحول", "الذروة", "الحل"]
        }
    
    async def _handle_generate_chapter(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج توليد الفصل"""
        await asyncio.sleep(2)
        
        return {
            "chapter_content": "محتوى الفصل المولد...",
            "word_count": 2500,
            "writing_time": "45 دقيقة",
            "quality_score": 8.5
        }
    
    async def _handle_refine_text(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج تحسين النص"""
        await asyncio.sleep(1)
        
        return {
            "refined_text": "النص المحسن...",
            "improvements": ["تحسين الأسلوب", "إضافة تفاصيل", "تصحيح الأخطاء"],
            "quality_improvement": 15
        }
    
    async def _handle_check_consistency(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج فحص التماسك"""
        await asyncio.sleep(1)
        
        return {
            "consistency_score": 9.2,
            "issues_found": [],
            "suggestions": ["تحسين انتقالات الفصول"],
            "overall_quality": "ممتاز"
        }
    
    async def _handle_generate_report(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج توليد التقرير"""
        await asyncio.sleep(1)
        
        return {
            "report_type": "comprehensive",
            "total_words": 30000,
            "chapters_completed": 12,
            "quality_metrics": {"style": 8.5, "plot": 9.0, "characters": 8.8},
            "estimated_reading_time": "3 ساعات"
        }
    
    async def _handle_condition(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج الشروط المنطقية"""
        condition = input_data.get('condition', True)
        return {"condition_result": condition}
    
    async def _handle_merge_data(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج دمج البيانات"""
        merged_data = {}
        for key, value in input_data.items():
            if isinstance(value, dict):
                merged_data.update(value)
        return {"merged_data": merged_data}
    
    async def _handle_transform_data(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج تحويل البيانات"""
        # تطبيق تحويلات البيانات
        return {"transformed_data": input_data}
    
    async def _handle_save_to_project(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج حفظ في المشروع"""
        project_id = context.get('project_id')
        if project_id:
            # حفظ البيانات في المشروع
            return {"saved": True, "project_id": project_id}
        return {"saved": False, "error": "معرف المشروع مفقود"}
    
    async def _handle_custom_agent_task(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج المهام المخصصة"""
        # تنفيذ مهمة مخصصة
        return {"custom_result": "تم تنفيذ المهمة المخصصة"}
    
    # === معالجات مهام الشاهد ===
    
    async def _handle_witness_upload(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج رفع ملفات الشاهد"""
        await asyncio.sleep(1)
        return {"uploaded_files": [], "total_size": 0}
    
    async def _handle_witness_extract(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج استخراج محتوى الشاهد"""
        await asyncio.sleep(1)
        return {"extracted_content": "", "metadata": {}}
    
    async def _handle_witness_analyze(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج تحليل محتوى الشاهد"""
        await asyncio.sleep(1)
        return {"analysis_results": {}, "insights": []}
    
    async def _handle_witness_integrate(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج دمج نتائج الشاهد"""
        await asyncio.sleep(1)
        return {"integrated_data": {}, "integration_quality": 0.8}
    
    async def _handle_witness_evaluate(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """معالج تقييم نتائج الشاهد"""
        await asyncio.sleep(1)
        return {"evaluation_score": 8.5, "recommendations": []}
    
    # === واجهات الاستعلام ===
    
    def get_workflow_status(self, execution_id: str, user_session: UserSession) -> Optional[Dict[str, Any]]:
        """الحصول على حالة تنفيذ سير العمل"""
        try:
            if execution_id in self.running_workflows:
                execution = self.running_workflows[execution_id]
                
                # فحص الأذونات
                if execution.user_id != user_session.user_id and user_session.role.value != 'admin':
                    return None
                
                return {
                    "id": execution.id,
                    "name": execution.name,
                    "status": execution.status.value,
                    "progress_percentage": execution.progress_percentage,
                    "current_task_index": execution.current_task_index,
                    "total_tasks": len(execution.tasks),
                    "created_at": execution.created_at.isoformat(),
                    "started_at": execution.started_at.isoformat() if execution.started_at else None,
                    "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
                    "error_message": execution.error_message,
                    "current_task": execution.tasks[execution.current_task_index].name if execution.current_task_index < len(execution.tasks) else None
                }
            
            # البحث في قاعدة البيانات
            return core_db.get_workflow_execution_status(execution_id, user_session.user_id)
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على حالة سير العمل: {str(e)}")
            return None
    
    def get_user_workflows(self, user_session: UserSession, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """الحصول على جميع سير العمل للمستخدم"""
        try:
            workflows = []
            
            # من الذاكرة
            for execution in self.running_workflows.values():
                if execution.user_id == user_session.user_id:
                    if not status_filter or execution.status.value == status_filter:
                        workflows.append({
                            "id": execution.id,
                            "name": execution.name,
                            "status": execution.status.value,
                            "progress_percentage": execution.progress_percentage,
                            "created_at": execution.created_at.isoformat()
                        })
            
            # من قاعدة البيانات
            db_workflows = core_db.get_user_workflow_executions(user_session.user_id, status_filter)
            workflows.extend(db_workflows)
            
            return workflows
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على سير العمل للمستخدم: {str(e)}")
            return []
    
    def cancel_workflow(self, execution_id: str, user_session: UserSession) -> bool:
        """إلغاء تنفيذ سير عمل"""
        try:
            if execution_id in self.running_workflows:
                execution = self.running_workflows[execution_id]
                
                # فحص الأذونات
                if execution.user_id != user_session.user_id and user_session.role.value != 'admin':
                    return False
                
                # إلغاء سير العمل
                execution.status = WorkflowStatus.CANCELLED
                execution.completed_at = datetime.now()
                
                # تحديث قاعدة البيانات
                core_db.update_workflow_execution(execution)
                
                logger.info(f"تم إلغاء سير العمل: {execution_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"خطأ في إلغاء سير العمل: {str(e)}")
            return False
    
    # === وظائف الاندماج السردي الفائق ===
    
    async def create_fusion_project(self, project_data: Dict[str, Any], 
                                   user_session: UserSession) -> Dict[str, Any]:
        """إنشاء مشروع اندماج سردي جديد"""
        try:
            # إضافة معرف المستخدم
            project_data['user_id'] = user_session.user_id
            
            # إنشاء المشروع في قاعدة البيانات
            fusion_id = core_db.create_fusion_project(project_data)
            
            # تسجيل الحدث
            core_db.log_fusion_analytics({
                'fusion_id': fusion_id,
                'event_type': 'project_created',
                'event_data': {
                    'fusion_type': project_data.get('fusion_type'),
                    'title': project_data.get('title')
                }
            })
            
            logger.info(f"تم إنشاء مشروع اندماج جديد: {fusion_id}")
            
            return {
                'status': 'success',
                'fusion_id': fusion_id,
                'message': 'تم إنشاء مشروع الاندماج بنجاح'
            }
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء مشروع الاندماج: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'فشل في إنشاء مشروع الاندماج'
            }
    
    async def orchestrate_narrative_fusion(self, fusion_id: str, user_session: UserSession,
                                          progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """تنسيق عملية الاندماج السردي الكاملة"""
        try:
            logger.info(f"بدء تنسيق الاندماج السردي: {fusion_id}")
            
            # التحقق من وجود المشروع وصلاحية المستخدم
            project = core_db.get_fusion_project(fusion_id)
            if not project or project['user_id'] != user_session.user_id:
                return {
                    'status': 'error',
                    'error': 'unauthorized_or_not_found',
                    'message': 'المشروع غير موجود أو غير مسموح'
                }
            
            # الحصول على المصادر
            sources = core_db.get_fusion_sources(fusion_id)
            if len(sources) < 2:
                return {
                    'status': 'error',
                    'error': 'insufficient_sources',
                    'message': 'يجب توفير مصدرين على الأقل للاندماج'
                }
            
            # استيراد الأدوات المطلوبة
            from tools.hyper_narrative_synthesizer_tool import HyperNarrativeSynthesizerTool
            from agents.fusion_arbitrator_agent import FusionArbitratorAgent
            
            synthesizer = HyperNarrativeSynthesizerTool()
            arbitrator = FusionArbitratorAgent()
            
            def update_progress(step: int, total: int, description: str):
                progress = (step / total) * 100
                if progress_callback:
                    progress_callback(progress, description)
                logger.info(f"التقدم {step}/{total}: {description}")
            
            # الخطوة 1: تحليل الهويات السردية
            update_progress(1, 8, "تحليل الهويات السردية للمصادر")
            narrative_identities = []
            
            for source in sources:
                # محاكاة النص (في التطبيق الفعلي سيتم استرجاعه من المصدر)
                source_text = f"نص تجريبي من المصدر: {source['source_title']}"
                identity = await synthesizer.analyze_narrative_identity(
                    source_text, source['source_title']
                )
                narrative_identities.append(identity)
            
            # الخطوة 2: تقييم التوافق
            update_progress(2, 8, "تقييم التوافق بين المصادر")
            compatibility = await synthesizer.assess_compatibility(narrative_identities)
            
            # تحديث درجة التوافق في قاعدة البيانات
            core_db.update_fusion_compatibility(
                fusion_id, 
                compatibility.compatibility_score,
                compatibility.estimated_success_rate
            )
            
            # الخطوة 3: إنشاء مخطط التخليق
            update_progress(3, 8, "إنشاء مخطط التخليق الأمثل")
            
            from tools.hyper_narrative_synthesizer_tool import SynthesisBlueprint
            blueprint = SynthesisBlueprint(
                blueprint_id=str(uuid.uuid4()),
                fusion_type=project['fusion_type'],
                source_weights={source['source_id']: source['weight'] for source in sources},
                narrative_structure={'type': 'three_act'},
                character_mapping={},
                plot_integration={},
                style_balance={'balanced': True},
                quality_targets={'overall': 0.8},
                estimated_length=project.get('target_length', 5000),
                fusion_parameters={'mode': 'adaptive'}
            )
            
            # حفظ المخطط في قاعدة البيانات
            blueprint_id = core_db.create_fusion_blueprint({
                'blueprint_id': blueprint.blueprint_id,
                'fusion_id': fusion_id,
                'blueprint_name': f"مخطط_{project['title']}",
                'fusion_strategy': compatibility.optimal_fusion_strategy,
                'source_weights': blueprint.source_weights,
                'narrative_structure': blueprint.narrative_structure,
                'character_mapping': blueprint.character_mapping,
                'plot_integration': blueprint.plot_integration,
                'style_balance': blueprint.style_balance,
                'quality_targets': blueprint.quality_targets,
                'fusion_parameters': blueprint.fusion_parameters
            })
            
            # الخطوة 4: إنشاء جلسة التخليق
            update_progress(4, 8, "تحضير جلسة التخليق")
            
            session_id = core_db.create_synthesis_session({
                'fusion_id': fusion_id,
                'blueprint_id': blueprint_id,
                'total_steps': 10,
                'synthesis_metadata': {
                    'compatibility_score': compatibility.compatibility_score,
                    'fusion_type': project['fusion_type']
                }
            })
            
            # الخطوة 5: تنفيذ التخليق السردي
            update_progress(5, 8, "تنفيذ التخليق السردي")
            
            # تحديث حالة الجلسة
            core_db.update_synthesis_progress(session_id, {
                'status': 'running',
                'current_step': 'synthesis_in_progress'
            })
            
            def synthesis_progress_callback(progress: float, step_name: str):
                core_db.update_synthesis_progress(session_id, {
                    'progress_percentage': 50 + (progress * 0.3),  # 50-80%
                    'current_step': step_name
                })
                update_progress(5, 8, f"التخليق: {step_name}")
            
            synthesis_result = await synthesizer.synthesize_narrative(
                narrative_identities, blueprint, synthesis_progress_callback
            )
            
            # الخطوة 6: التحكيم والتقييم
            update_progress(6, 8, "تحكيم وتقييم الجودة")
            
            arbitration = await arbitrator.arbitrate_fusion(
                synthesis_result['synthesized_narrative'],
                [f"مصدر_{i}" for i in range(len(sources))],  # محاكاة
                synthesis_result['metadata']
            )
            
            # حفظ نتائج التحكيم
            core_db.save_arbitration_result({
                'session_id': session_id,
                'fusion_id': fusion_id,
                'quality_metrics': asdict(arbitration.quality_metrics),
                'detected_issues': [asdict(issue) for issue in arbitration.detected_issues],
                'recommendations': arbitration.recommendations,
                'improvement_suggestions': arbitration.improvement_suggestions,
                'approval_status': arbitration.approval_status,
                'confidence_level': arbitration.confidence_level
            })
            
            # الخطوة 7: حفظ النسخة النهائية
            update_progress(7, 8, "حفظ النسخة النهائية")
            
            core_db.save_synthesis_version({
                'session_id': session_id,
                'content': synthesis_result['synthesized_narrative'],
                'quality_score': arbitration.quality_metrics.overall_quality,
                'changes_summary': 'النسخة الأولى من التخليق'
            })
            
            # الخطوة 8: إنهاء العملية
            update_progress(8, 8, "إكمال عملية الاندماج")
            
            # تحديث حالة الجلسة
            final_status = 'completed' if arbitration.approval_status == 'approved' else 'needs_revision'
            core_db.update_synthesis_progress(session_id, {
                'status': final_status,
                'progress_percentage': 100.0,
                'synthesized_content': synthesis_result['synthesized_narrative'],
                'current_step': 'completed'
            })
            
            # تسجيل الحدث النهائي
            core_db.log_fusion_analytics({
                'fusion_id': fusion_id,
                'event_type': 'fusion_completed',
                'event_data': {
                    'session_id': session_id,
                    'approval_status': arbitration.approval_status,
                    'quality_score': arbitration.quality_metrics.overall_quality
                },
                'metrics': {
                    'compatibility_score': compatibility.compatibility_score,
                    'overall_quality': arbitration.quality_metrics.overall_quality,
                    'issues_count': len(arbitration.detected_issues)
                }
            })
            
            logger.info(f"تم إكمال الاندماج السردي: {fusion_id}")
            
            return {
                'status': 'success',
                'session_id': session_id,
                'arbitration_id': arbitration.arbitration_id,
                'synthesis_result': synthesis_result,
                'arbitration_result': {
                    'approval_status': arbitration.approval_status,
                    'overall_quality': arbitration.quality_metrics.overall_quality,
                    'issues_count': len(arbitration.detected_issues),
                    'confidence_level': arbitration.confidence_level
                },
                'message': 'تم إكمال عملية الاندماج السردي بنجاح'
            }
            
        except Exception as e:
            logger.error(f"خطأ في تنسيق الاندماج السردي: {str(e)}")
            logger.error(traceback.format_exc())
            
            # تحديث حالة الجلسة في حالة الخطأ
            if 'session_id' in locals():
                core_db.update_synthesis_progress(session_id, {
                    'status': 'failed',
                    'error_log': str(e)
                })
            
            return {
                'status': 'error',
                'error': str(e),
                'message': 'فشل في عملية الاندماج السردي'
            }
    
    def get_fusion_projects(self, user_session: UserSession) -> List[Dict[str, Any]]:
        """الحصول على مشاريع الاندماج للمستخدم"""
        try:
            projects = core_db.get_fusion_projects_by_user(user_session.user_id)
            return projects
        except Exception as e:
            logger.error(f"خطأ في استرجاع مشاريع الاندماج: {str(e)}")
            return []
    
    def get_fusion_project_details(self, fusion_id: str, user_session: UserSession) -> Optional[Dict[str, Any]]:
        """الحصول على تفاصيل مشروع اندماج"""
        try:
            project = core_db.get_fusion_project(fusion_id)
            if project and project['user_id'] == user_session.user_id:
                # إضافة المصادر
                project['sources'] = core_db.get_fusion_sources(fusion_id)
                # إضافة آخر تقييم
                project['latest_arbitration'] = core_db.get_latest_arbitration(fusion_id)
                return project
            return None
        except Exception as e:
            logger.error(f"خطأ في استرجاع تفاصيل مشروع الاندماج: {str(e)}")
            return None
    
    def add_fusion_source(self, fusion_id: str, source_data: Dict[str, Any], 
                         user_session: UserSession) -> Dict[str, Any]:
        """إضافة مصدر لمشروع الاندماج"""
        try:
            # التحقق من صلاحية المستخدم
            project = core_db.get_fusion_project(fusion_id)
            if not project or project['user_id'] != user_session.user_id:
                return {
                    'status': 'error',
                    'error': 'unauthorized',
                    'message': 'غير مسموح بالوصول لهذا المشروع'
                }
            
            source_data['fusion_id'] = fusion_id
            source_id = core_db.add_fusion_source(source_data)
            
            logger.info(f"تم إضافة مصدر جديد: {source_id}")
            
            return {
                'status': 'success',
                'source_id': source_id,
                'message': 'تم إضافة المصدر بنجاح'
            }
            
        except Exception as e:
            logger.error(f"خطأ في إضافة مصدر الاندماج: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'فشل في إضافة المصدر'
            }
    
    async def assess_fusion_compatibility(self, fusion_id: str, user_session: UserSession) -> Dict[str, Any]:
        """تقييم التوافق بين مصادر الاندماج"""
        try:
            # التحقق من صلاحية المستخدم
            project = core_db.get_fusion_project(fusion_id)
            if not project or project['user_id'] != user_session.user_id:
                return {
                    'status': 'error',
                    'error': 'unauthorized',
                    'message': 'غير مسموح بالوصول لهذا المشروع'
                }
            
            sources = core_db.get_fusion_sources(fusion_id)
            if len(sources) < 2:
                return {
                    'status': 'error',
                    'error': 'insufficient_sources',
                    'message': 'يجب توفير مصدرين على الأقل للتقييم'
                }
            
            # استيراد أداة التخليق
            from tools.hyper_narrative_synthesizer_tool import HyperNarrativeSynthesizerTool
            synthesizer = HyperNarrativeSynthesizerTool()
            
            # تحليل الهويات السردية (محاكاة)
            narrative_identities = []
            for source in sources:
                # في التطبيق الفعلي سيتم استرجاع النص الحقيقي
                sample_text = f"نص تجريبي من {source['source_title']}"
                identity = await synthesizer.analyze_narrative_identity(sample_text, source['source_title'])
                narrative_identities.append(identity)
            
            # تقييم التوافق
            compatibility = await synthesizer.assess_compatibility(narrative_identities)
            
            # تحديث المشروع
            core_db.update_fusion_compatibility(
                fusion_id,
                compatibility.compatibility_score,
                compatibility.estimated_success_rate
            )
            
            # تسجيل الحدث
            core_db.log_fusion_analytics({
                'fusion_id': fusion_id,
                'event_type': 'compatibility_assessment',
                'metrics': {
                    'compatibility_score': compatibility.compatibility_score,
                    'success_rate': compatibility.estimated_success_rate,
                    'tension_points': len(compatibility.tension_points),
                    'harmony_points': len(compatibility.harmony_points)
                }
            })
            
            return {
                'status': 'success',
                'compatibility_score': compatibility.compatibility_score,
                'estimated_success_rate': compatibility.estimated_success_rate,
                'optimal_strategy': compatibility.optimal_fusion_strategy,
                'tension_points': len(compatibility.tension_points),
                'harmony_points': len(compatibility.harmony_points),
                'recommendations': compatibility.fusion_recommendations,
                'risk_factors': compatibility.risk_factors,
                'message': 'تم تقييم التوافق بنجاح'
            }
            
        except Exception as e:
            logger.error(f"خطأ في تقييم التوافق: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'فشل في تقييم التوافق'
            }
    
    async def start_narrative_synthesis(self, fusion_id: str, blueprint_data: Dict[str, Any],
                                       user_session: UserSession) -> Dict[str, Any]:
        """بدء عملية التخليق السردي"""
        try:
            # التحقق من صلاحية المستخدم
            project = core_db.get_fusion_project(fusion_id)
            if not project or project['user_id'] != user_session.user_id:
                return {
                    'status': 'error',
                    'error': 'unauthorized',
                    'message': 'غير مسموح بالوصول لهذا المشروع'
                }
            
            # إنشاء مخطط التخليق
            blueprint_data['fusion_id'] = fusion_id
            blueprint_id = core_db.create_fusion_blueprint(blueprint_data)
            
            # إنشاء جلسة التخليق
            session_id = core_db.create_synthesis_session({
                'fusion_id': fusion_id,
                'blueprint_id': blueprint_id,
                'synthesis_metadata': {
                    'started_by': user_session.user_id,
                    'fusion_type': project['fusion_type']
                }
            })
            
            logger.info(f"تم بدء جلسة التخليق: {session_id}")
            
            return {
                'status': 'success',
                'session_id': session_id,
                'blueprint_id': blueprint_id,
                'message': 'تم بدء عملية التخليق بنجاح'
            }
            
        except Exception as e:
            logger.error(f"خطأ في بدء التخليق السردي: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'فشل في بدء عملية التخليق'
            }
    
    def get_synthesis_progress(self, session_id: str, user_session: UserSession) -> Dict[str, Any]:
        """الحصول على تقدم عملية التخليق"""
        try:
            session = core_db.get_synthesis_session(session_id)
            if not session:
                return {
                    'status': 'error',
                    'error': 'session_not_found',
                    'message': 'جلسة التخليق غير موجودة'
                }
            
            # التحقق من صلاحية المستخدم
            project = core_db.get_fusion_project(session['fusion_id'])
            if not project or project['user_id'] != user_session.user_id:
                return {
                    'status': 'error',
                    'error': 'unauthorized',
                    'message': 'غير مسموح بالوصول لهذه الجلسة'
                }
            
            return {
                'status': 'success',
                'session': session,
                'message': 'تم استرجاع حالة التخليق بنجاح'
            }
            
        except Exception as e:
            logger.error(f"خطأ في استرجاع تقدم التخليق: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'فشل في استرجاع حالة التخليق'
            }
    
    def get_arbitration_results(self, fusion_id: str, user_session: UserSession) -> Optional[Dict[str, Any]]:
        """الحصول على نتائج التحكيم"""
        try:
            # التحقق من صلاحية المستخدم
            project = core_db.get_fusion_project(fusion_id)
            if not project or project['user_id'] != user_session.user_id:
                return None
            
            arbitration = core_db.get_latest_arbitration(fusion_id)
            return arbitration
            
        except Exception as e:
            logger.error(f"خطأ في استرجاع نتائج التحكيم: {str(e)}")
            return None

# إنشاء المثيل الوحيد
core_orchestrator = CoreOrchestrator()

# دوال الواجهة المبسطة
@require_auth
def create_workflow_template(template_data: Dict[str, Any]) -> str:
    """إنشاء قالب سير عمل جديد"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.create_workflow_template(template_data, user_session)

@require_auth  
def get_workflow_templates(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """الحصول على قوالب سير العمل"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.get_workflow_templates(user_session, category)

@require_auth
def start_workflow(template_id: str, context_data: Dict[str, Any]) -> str:
    """بدء تنفيذ سير عمل"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.start_workflow(template_id, context_data, user_session)

@require_auth
def get_workflow_status(execution_id: str) -> Optional[Dict[str, Any]]:
    """الحصول على حالة سير عمل"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.get_workflow_status(execution_id, user_session)

@require_auth
def get_user_workflows(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """الحصول على سير العمل للمستخدم الحالي"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.get_user_workflows(user_session, status_filter)

@require_auth
def cancel_workflow(execution_id: str) -> bool:
    """إلغاء سير عمل"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.cancel_workflow(execution_id, user_session)

# === وظائف الاندماج السردي الفائق ===

@require_auth
def create_fusion_project(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """إنشاء مشروع اندماج سردي جديد"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.create_fusion_project(project_data, user_session)

@require_auth
def orchestrate_narrative_fusion(fusion_id: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
    """تنسيق عملية الاندماج السردي الكاملة"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.orchestrate_narrative_fusion(fusion_id, user_session, progress_callback)

@require_auth 
def get_fusion_projects() -> List[Dict[str, Any]]:
    """الحصول على مشاريع الاندماج للمستخدم"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.get_fusion_projects(user_session)

@require_auth
def get_fusion_project_details(fusion_id: str) -> Optional[Dict[str, Any]]:
    """الحصول على تفاصيل مشروع اندماج"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.get_fusion_project_details(fusion_id, user_session)

@require_auth
def add_fusion_source(fusion_id: str, source_data: Dict[str, Any]) -> Dict[str, Any]:
    """إضافة مصدر لمشروع الاندماج"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.add_fusion_source(fusion_id, source_data, user_session)

@require_auth
def assess_fusion_compatibility(fusion_id: str) -> Dict[str, Any]:
    """تقييم التوافق بين مصادر الاندماج"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.assess_fusion_compatibility(fusion_id, user_session)

@require_auth
def start_narrative_synthesis(fusion_id: str, blueprint_data: Dict[str, Any]) -> Dict[str, Any]:
    """بدء عملية التخليق السردي"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.start_narrative_synthesis(fusion_id, blueprint_data, user_session)

@require_auth
def get_synthesis_progress(session_id: str) -> Dict[str, Any]:
    """الحصول على تقدم عملية التخليق"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.get_synthesis_progress(session_id, user_session)

@require_auth
def get_arbitration_results(fusion_id: str) -> Optional[Dict[str, Any]]:
    """الحصول على نتائج التحكيم"""
    user_session = core_auth.get_current_session()
    return core_orchestrator.get_arbitration_results(fusion_id, user_session)
