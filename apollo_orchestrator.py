import uuid
import logging
import importlib
import pkgutil
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import asyncio

# --- استيراد المكونات الأساسية (سيتم تطويرها لاحقًا) ---
from .unified_database import unified_db  # تخزين واسترجاع حالة المشاريع
from .intent_analyzer import IntentAnalyzer
from .workflow_manager import WorkflowManager, WorkflowTemplate
from .arbitration_service import ArbitrationService
from .shared_context import SharedContext

# --- إعداد التسجيل (Logger) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Apollo] - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ApolloOrchestrator")

# التحكم في عدد المهام المتزامنة
_workflow_semaphore = asyncio.Semaphore(10)

class ProjectStatus(Enum):
    INITIALIZING = "initializing"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ApolloOrchestrator:
    """
    ماستر أوركستريتور "أبولو" للوكلاء الفنية.
    يحمّل الوكلاء ديناميكيًا من حزمة agents/ ويُدير عملية الكتابة الفنية.
    """

    def __init__(self, agents_package: str = "agents"):
        self.intent_analyzer = IntentAnalyzer()
        self.workflow_manager = WorkflowManager()
        self.arbitrator = ArbitrationService()
        self.active_projects: Dict[str, Dict[str, Any]] = {}
        logger.info("☀️ Apollo Master Orchestrator initialized.")

        # تحميل الوكلاء ديناميكيًا
        self.agent_classes = {}
        self._discover_agents(agents_package)

    def _discover_agents(self, package_name: str):
        """يستكشف كل وحدة في حزمة agents/ ويحمّل فئة Agent موجودة فيها"""
        try:
            package = importlib.import_module(f".{package_name}", package=__name__.split('.')[0])
            for finder, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
                full_name = f"{package.__name__}.{module_name}"
                module = importlib.import_module(full_name)
                if hasattr(module, 'Agent'):
                    cls = getattr(module, 'Agent')
                    self.agent_classes[cls.__name__] = cls
                    logger.info(f"Loaded agent: {cls.__name__}")
        except ModuleNotFoundError:
            logger.warning(f"Agents package '{package_name}' not found.")

    async def start_new_creation(
        self,
        user_id: str,
        user_request: str,
        artistic_form: str  # مثل 'رواية', 'أغنية', 'مسرحية'
    ) -> Dict[str, Any]:
        # التحقق من المدخلات
        if not user_id or not user_request.strip() or not artistic_form:
            return {"success": False, "error": "Invalid inputs."}

        project_id = f"creation_{uuid.uuid4().hex[:8]}"
        logger.info(f"Project {project_id} init for {artistic_form} by user {user_id}")
        self.active_projects[project_id] = {
            "id": project_id,
            "user_id": user_id,
            "form": artistic_form,
            "status": ProjectStatus.INITIALIZING,
            "start_time": datetime.utcnow(),
            "log": []
        }
        unified_db.save_project(self.active_projects[project_id])

        try:
            intent = await self.intent_analyzer.analyze(user_request)
            self._log(project_id, f"Intent: {intent}")

            template: WorkflowTemplate = self.workflow_manager.select_template(intent, artistic_form)
            self._log(project_id, f"Template: {template.name}")

            # تشكيل فريق من الوكلاء المناسبين
            task_force = [self.agent_classes[name]() for name in template.required_agents if name in self.agent_classes]
            self._log(project_id, f"Agents loaded: {[a.__class__.__name__ for a in task_force]}")

            shared_context = SharedContext(project_id)
            await shared_context.initialize(user_request, intent, template)
            self._log(project_id, "SharedContext ready.")

            # إطلاق التنفيذ
            self.active_projects[project_id]['status'] = ProjectStatus.PLANNING
            unified_db.update_status(project_id, ProjectStatus.PLANNING.value)
            asyncio.create_task(self._run_with_semaphore(project_id, template, task_force, shared_context))

            return {"success": True, "project_id": project_id, "form": artistic_form}

        except Exception as e:
            logger.error(f"[{project_id}] init error: {e}")
            self.active_projects[project_id]['status'] = ProjectStatus.FAILED
            unified_db.update_status(project_id, ProjectStatus.FAILED.value)
            return {"success": False, "error": str(e)}

    async def _run_with_semaphore(self, project_id, workflow, agents, context):
        async with _workflow_semaphore:
            await self._execute(project_id, workflow, agents, context)

    async def _execute(
        self,
        project_id: str,
        workflow: WorkflowTemplate,
        agents: List[Any],
        context: SharedContext
    ):
        self._log(project_id, f"Executing {workflow.name}")
        self.active_projects[project_id]['status'] = ProjectStatus.IN_PROGRESS
        unified_db.update_status(project_id, ProjectStatus.IN_PROGRESS.value)

        for task in workflow.tasks:
            try:
                agent = next((a for a in agents if a.can_handle(task['type'])), None)
                if not agent:
                    raise RuntimeError(f"No agent for {task['type']}")
                self._log(project_id, f"Task '{task['name']}' -> {agent.__class__.__name__}")

                result = await agent.execute(task, context)
                await context.update(task['output_key'], result)
                self._log(project_id, f"'{task['name']}' done.")

                if task.get('requires_arbitration'):
                    self.active_projects[project_id]['status'] = ProjectStatus.IN_REVIEW
                    unified_db.update_status(project_id, ProjectStatus.IN_REVIEW.value)
                    report = await self.arbitrator.review(result, context)
                    if not report['approved']:
                        await agent.process_feedback(report)
                        self._log(project_id, f"Feedback sent to {agent.__class__.__name__}")
                    self.active_projects[project_id]['status'] = ProjectStatus.IN_PROGRESS
                    unified_db.update_status(project_id, ProjectStatus.IN_PROGRESS.value)

            except Exception as e:
                logger.error(f"[{project_id}] error: {e}")
                self.active_projects[project_id]['status'] = ProjectStatus.FAILED
                unified_db.update_status(project_id, ProjectStatus.FAILED.value)
                return

        # الانتهاء
        self.active_projects[project_id]['status'] = ProjectStatus.COMPLETED
        self.active_projects[project_id]['end_time'] = datetime.utcnow()
        unified_db.update_status(project_id, ProjectStatus.COMPLETED.value)

        final = await context.get_final_product()
        unified_db.save_final(project_id, final)
        self._log(project_id, "Completed.")

    def get_creation_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        project = unified_db.load_project(project_id) or self.active_projects.get(project_id)
        if not project:
            return None
        return {"project_id": project_id, "status": project.get('status'), "last_log": project.get('log', [])[-1] if project.get('log') else ''}

    def _log(self, project_id: str, msg: str):
        ts = datetime.utcnow().isoformat()
        entry = f"[{ts}] {msg}"
        if project_id in self.active_projects:
            self.active_projects[project_id].setdefault('log', []).append(entry)
            unified_db.append_log(project_id, entry)
        logger.info(f"[{project_id}] {msg}")

# مثيل أبولو الوحيد
apollo = ApolloOrchestrator()
