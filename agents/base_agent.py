"""
الفئة الأساسية للوكلاء في النظام الذكي للكتابة العربية
توفر البنية الأساسية لجميع الوكلاء المتخصصين
"""

import uuid
import json
import logging
import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import traceback

# إعداد التسجيل
logger = logging.getLogger(__name__)

class AgentState(Enum):
    """حالات الوكيل"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"

class MessageType(Enum):
    """أنواع الرسائل بين الوكلاء"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"
    STATUS_UPDATE = "status_update"

@dataclass
class AgentMessage:
    """رسالة بين الوكلاء"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    receiver_id: str = ""
    message_type: MessageType = MessageType.REQUEST
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 1  # 1 = عادي، 2 = مهم، 3 = عاجل
    requires_response: bool = False
    correlation_id: Optional[str] = None  # ربط الرسائل ببعضها

@dataclass
class AgentMemory:
    """ذاكرة الوكيل لتخزين المعلومات والسياق"""
    short_term: Dict[str, Any] = field(default_factory=dict)
    long_term: Dict[str, Any] = field(default_factory=dict)
    context_stack: List[Dict[str, Any]] = field(default_factory=list)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    learned_patterns: Dict[str, Any] = field(default_factory=dict)
    
    def add_to_context(self, context: Dict[str, Any]):
        """إضافة سياق جديد"""
        self.context_stack.append({
            "timestamp": datetime.now().isoformat(),
            "data": context
        })
        # الاحتفاظ بآخر 10 سياقات فقط
        if len(self.context_stack) > 10:
            self.context_stack = self.context_stack[-10:]
    
    def get_current_context(self) -> Dict[str, Any]:
        """الحصول على السياق الحالي"""
        return self.context_stack[-1]["data"] if self.context_stack else {}
    
    def remember(self, key: str, value: Any, duration: str = "short"):
        """تذكر معلومة معينة"""
        if duration == "short":
            self.short_term[key] = {
                "value": value,
                "timestamp": datetime.now().isoformat()
            }
        else:
            self.long_term[key] = {
                "value": value,
                "timestamp": datetime.now().isoformat()
            }
    
    def recall(self, key: str, duration: str = "short") -> Any:
        """استدعاء معلومة محفوظة"""
        memory_store = self.short_term if duration == "short" else self.long_term
        return memory_store.get(key, {}).get("value")

@dataclass
class AgentGoal:
    """هدف الوكيل"""
    id: str
    description: str
    priority: int
    status: str = "pending"  # pending, in_progress, completed, failed
    deadline: Optional[datetime] = None
    success_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

class BaseAgent(ABC):
    """الفئة الأساسية لجميع الوكلاء في النظام"""
    
    def __init__(
        self,
        name: str,
        persona: str,
        goals: List[str],
        tools: List[str],
        agent_id: Optional[str] = None
    ):
        self.id = agent_id or str(uuid.uuid4())
        self.name = name
        self.persona = persona
        self.goals = [AgentGoal(id=str(uuid.uuid4()), description=goal, priority=1) 
                     for goal in goals]
        self.tools = tools
        self.state = AgentState.IDLE
        self.memory = AgentMemory()
        self.message_queue: List[AgentMessage] = []
        self.communication_handlers: Dict[str, Callable] = {}
        self.error_count = 0
        self.max_retries = 3
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_response_time": 0,
            "total_processing_time": 0
        }
        
        # تسجيل إنشاء الوكيل
        logger.info(f"تم إنشاء الوكيل {self.name} (ID: {self.id})")
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة مهمة محددة - يجب تنفيذها في كل وكيل"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """إرجاع قائمة بقدرات الوكيل"""
        pass
    
    async def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """استقبال ومعالجة رسالة من وكيل آخر"""
        try:
            self.message_queue.append(message)
            self.last_activity = datetime.now()
            
            logger.info(f"الوكيل {self.name} استلم رسالة من {message.sender_id}")
            
            # معالجة الرسالة حسب نوعها
            if message.message_type == MessageType.REQUEST:
                return await self._handle_request(message)
            elif message.message_type == MessageType.NOTIFICATION:
                await self._handle_notification(message)
            elif message.message_type == MessageType.STATUS_UPDATE:
                await self._handle_status_update(message)
            elif message.message_type == MessageType.ERROR:
                await self._handle_error_message(message)
                
            return None
            
        except Exception as e:
            logger.error(f"خطأ في معالجة الرسالة في الوكيل {self.name}: {str(e)}")
            self.error_count += 1
            return self._create_error_response(message, str(e))
    
    async def send_message(
        self,
        receiver_id: str,
        content: Dict[str, Any],
        message_type: MessageType = MessageType.REQUEST,
        requires_response: bool = False
    ) -> AgentMessage:
        """إرسال رسالة إلى وكيل آخر"""
        message = AgentMessage(
            sender_id=self.id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content,
            requires_response=requires_response
        )
        
        logger.info(f"الوكيل {self.name} يرسل رسالة إلى {receiver_id}")
        return message
    
    async def _handle_request(self, message: AgentMessage) -> Optional[AgentMessage]:
        """معالجة طلب من وكيل آخر"""
        try:
            self.state = AgentState.WORKING
            
            # معالجة الطلب
            result = await self.process_task(message.content)
            
            # إنشاء رد
            response = AgentMessage(
                sender_id=self.id,
                receiver_id=message.sender_id,
                message_type=MessageType.RESPONSE,
                content={"result": result, "status": "success"},
                correlation_id=message.id
            )
            
            self.state = AgentState.COMPLETED
            self.performance_metrics["tasks_completed"] += 1
            
            return response
            
        except Exception as e:
            self.state = AgentState.ERROR
            self.performance_metrics["tasks_failed"] += 1
            logger.error(f"خطأ في معالجة الطلب في الوكيل {self.name}: {str(e)}")
            return self._create_error_response(message, str(e))
    
    async def _handle_notification(self, message: AgentMessage):
        """معالجة إشعار من وكيل آخر"""
        # حفظ الإشعار في الذاكرة
        self.memory.add_to_context({
            "type": "notification",
            "from": message.sender_id,
            "content": message.content
        })
        
        logger.info(f"الوكيل {self.name} تلقى إشعار: {message.content}")
    
    async def _handle_status_update(self, message: AgentMessage):
        """معالجة تحديث حالة من وكيل آخر"""
        self.memory.remember(
            f"status_{message.sender_id}",
            message.content,
            "short"
        )
        
        logger.info(f"تحديث حالة من {message.sender_id}: {message.content}")
    
    async def _handle_error_message(self, message: AgentMessage):
        """معالجة رسالة خطأ من وكيل آخر"""
        logger.error(f"خطأ من الوكيل {message.sender_id}: {message.content}")
        
        # حفظ الخطأ للتعلم من الأخطاء
        self.memory.remember(
            f"error_{message.sender_id}_{datetime.now().isoformat()}",
            message.content,
            "long"
        )
    
    def _create_error_response(self, original_message: AgentMessage, error: str) -> AgentMessage:
        """إنشاء رد خطأ"""
        return AgentMessage(
            sender_id=self.id,
            receiver_id=original_message.sender_id,
            message_type=MessageType.ERROR,
            content={
                "error": error,
                "original_message_id": original_message.id,
                "agent_name": self.name
            },
            correlation_id=original_message.id
        )
    
    def update_state(self, new_state: AgentState, context: Optional[Dict[str, Any]] = None):
        """تحديث حالة الوكيل"""
        old_state = self.state
        self.state = new_state
        self.last_activity = datetime.now()
        
        if context:
            self.memory.add_to_context(context)
        
        logger.info(f"الوكيل {self.name} غير حالته من {old_state.value} إلى {new_state.value}")
    
    def add_goal(self, description: str, priority: int = 1, deadline: Optional[datetime] = None):
        """إضافة هدف جديد للوكيل"""
        goal = AgentGoal(
            id=str(uuid.uuid4()),
            description=description,
            priority=priority,
            deadline=deadline
        )
        self.goals.append(goal)
        logger.info(f"تم إضافة هدف جديد للوكيل {self.name}: {description}")
    
    def complete_goal(self, goal_id: str, success: bool = True):
        """إكمال هدف معين"""
        for goal in self.goals:
            if goal.id == goal_id:
                goal.status = "completed" if success else "failed"
                logger.info(f"تم إكمال الهدف {goal.description} للوكيل {self.name}")
                break
    
    def get_status(self) -> Dict[str, Any]:
        """الحصول على حالة الوكيل الحالية"""
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state.value,
            "goals": [asdict(goal) for goal in self.goals],
            "message_queue_size": len(self.message_queue),
            "error_count": self.error_count,
            "performance_metrics": self.performance_metrics,
            "last_activity": self.last_activity.isoformat(),
            "memory_summary": {
                "short_term_items": len(self.memory.short_term),
                "long_term_items": len(self.memory.long_term),
                "context_depth": len(self.memory.context_stack)
            }
        }
    
    def reset_state(self):
        """إعادة تعيين حالة الوكيل"""
        self.state = AgentState.IDLE
        self.error_count = 0
        self.message_queue.clear()
        logger.info(f"تم إعادة تعيين حالة الوكيل {self.name}")
    
    def learn_from_interaction(self, interaction_data: Dict[str, Any]):
        """التعلم من التفاعلات السابقة"""
        # حفظ نمط التفاعل
        pattern_key = f"interaction_{datetime.now().isoformat()}"
        self.memory.learned_patterns[pattern_key] = interaction_data
        
        # تحديث المقاييس
        if "response_time" in interaction_data:
            current_avg = self.performance_metrics["average_response_time"]
            new_time = interaction_data["response_time"]
            task_count = self.performance_metrics["tasks_completed"]
            
            if task_count > 0:
                self.performance_metrics["average_response_time"] = (
                    (current_avg * (task_count - 1) + new_time) / task_count
                )
    
    async def cleanup(self):
        """تنظيف موارد الوكيل"""
        logger.info(f"تنظيف موارد الوكيل {self.name}")
        self.state = AgentState.IDLE
        # احتفظ بالذاكرة الطويلة المدى فقط
        self.memory.short_term.clear()
        self.memory.context_stack.clear()
        self.message_queue.clear()

# فئة مساعدة للإدارة المتقدمة للوكلاء
class AgentManager:
    """مدير الوكلاء للتحكم في دورة حياة الوكلاء والتنسيق بينهم"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_broker: List[AgentMessage] = []
        self.agent_relationships: Dict[str, List[str]] = {}
        
    def register_agent(self, agent: BaseAgent):
        """تسجيل وكيل جديد"""
        self.agents[agent.id] = agent
        self.agent_relationships[agent.id] = []
        logger.info(f"تم تسجيل الوكيل {agent.name} في المدير")
    
    def unregister_agent(self, agent_id: str):
        """إلغاء تسجيل وكيل"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            asyncio.create_task(agent.cleanup())
            del self.agents[agent_id]
            del self.agent_relationships[agent_id]
            logger.info(f"تم إلغاء تسجيل الوكيل {agent.name}")
    
    async def route_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """توجيه الرسائل بين الوكلاء"""
        if message.receiver_id in self.agents:
            receiver = self.agents[message.receiver_id]
            return await receiver.receive_message(message)
        else:
            logger.error(f"الوكيل المستقبل غير موجود: {message.receiver_id}")
            return None
    
    def get_all_agents_status(self) -> Dict[str, Dict[str, Any]]:
        """الحصول على حالة جميع الوكلاء"""
        return {agent_id: agent.get_status() for agent_id, agent in self.agents.items()}
    
    def find_agent_by_capability(self, capability: str) -> List[BaseAgent]:
        """البحث عن الوكلاء بناءً على قدرة معينة"""
        matching_agents = []
        for agent in self.agents.values():
            if capability in agent.get_capabilities():
                matching_agents.append(agent)
        return matching_agents

# مثيل المدير العام للوكلاء
global_agent_manager = AgentManager()
