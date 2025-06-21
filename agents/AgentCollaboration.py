#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
نظام الوكلاء المتعاونين والحوارات الداخلية (AgentCollaboration)
=============================================================

نظام متقدم يتيح للوكلاء التعاون وإجراء حوارات داخلية لحل المشكلات المعقدة
وتحسين نوعية المخرجات من خلال العمل الجماعي.

المميزات:
- محادثات مباشرة بين الوكلاء
- مؤتمرات متعددة الوكلاء لاتخاذ القرارات
- عصف ذهني جماعي
- تقسيم المهام آلياً بين الوكلاء
- تصويت الوكلاء على الخيارات المختلفة
"""

import os
import json
import time
import copy
import logging
import uuid
import asyncio
import threading
from typing import Dict, List, Any, Tuple, Optional, Union, Callable
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# استيراد المكتبات الداخلية
from ..llm_service import get_llm_response, get_llm_response_async
from ..database import get_db_connection
from ..agents.base_agent import BaseAgent
from .AdvancedArbitrator import get_arbitrator

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/agent_collaboration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AgentCollaboration")

class AgentCollaboration:
    """
    نظام الوكلاء المتعاونين والحوارات الداخلية
    """
    
    def __init__(self, config: Dict = None):
        """
        تهيئة نظام التعاون بين الوكلاء
        
        Args:
            config: إعدادات النظام (اختياري)
        """
        self.config = config or {}
        self.available_agents = {}
        self.active_sessions = {}
        self.conversation_history = {}
        self.task_assignments = {}
        self.arbitrator = get_arbitrator()
        
        # تهيئة قاعدة البيانات
        self.db = get_db_connection()
        self._init_database()
        
        # تهيئة التزامن
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.lock = threading.Lock()
        
        logger.info("تم تهيئة نظام الوكلاء المتعاونين")
    
    def _init_database(self):
        """
        تهيئة جداول قاعدة البيانات اللازمة
        """
        cursor = self.db.cursor()
        
        # جدول جلسات التعاون
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS collaboration_sessions (
            id TEXT PRIMARY KEY,
            topic TEXT,
            goal TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT
        )
        ''')
        
        # جدول الرسائل في الجلسات
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS collaboration_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            agent_id TEXT,
            message_type TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT,
            FOREIGN KEY (session_id) REFERENCES collaboration_sessions(id)
        )
        ''')
        
        # جدول توزيع المهام
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            task_id TEXT,
            agent_id TEXT,
            task_description TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            result TEXT,
            FOREIGN KEY (session_id) REFERENCES collaboration_sessions(id)
        )
        ''')
        
        # جدول تصويت الوكلاء
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            topic TEXT,
            agent_id TEXT,
            option_id TEXT,
            vote_value INTEGER,
            reasoning TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES collaboration_sessions(id)
        )
        ''')
        
        self.db.commit()
        logger.info("تم تهيئة جداول قاعدة البيانات لنظام الوكلاء المتعاونين")
    
    def register_agent(self, agent_id: str, agent_instance: BaseAgent, agent_type: str, capabilities: List[str]) -> bool:
        """
        تسجيل وكيل في نظام التعاون
        
        Args:
            agent_id: معرف الوكيل
            agent_instance: نسخة من الوكيل
            agent_type: نوع الوكيل
            capabilities: قدرات الوكيل
            
        Returns:
            نجاح العملية
        """
        logger.info(f"تسجيل الوكيل {agent_id} من النوع {agent_type}")
        
        with self.lock:
            if agent_id in self.available_agents:
                logger.warning(f"الوكيل {agent_id} مسجل بالفعل")
                return False
            
            self.available_agents[agent_id] = {
                "instance": agent_instance,
                "type": agent_type,
                "capabilities": capabilities,
                "status": "available",
                "current_session": None,
                "registered_at": datetime.now().isoformat()
            }
            
            logger.info(f"تم تسجيل الوكيل {agent_id} بنجاح")
            return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        إلغاء تسجيل وكيل من نظام التعاون
        
        Args:
            agent_id: معرف الوكيل
            
        Returns:
            نجاح العملية
        """
        logger.info(f"إلغاء تسجيل الوكيل {agent_id}")
        
        with self.lock:
            if agent_id not in self.available_agents:
                logger.warning(f"الوكيل {agent_id} غير مسجل")
                return False
            
            # التحقق من عدم وجود الوكيل في جلسة نشطة
            agent_info = self.available_agents[agent_id]
            if agent_info["current_session"] and agent_info["current_session"] in self.active_sessions:
                logger.warning(f"لا يمكن إلغاء تسجيل الوكيل {agent_id} لأنه في جلسة نشطة")
                return False
            
            del self.available_agents[agent_id]
            logger.info(f"تم إلغاء تسجيل الوكيل {agent_id} بنجاح")
            return True
    
    def create_collaboration_session(self, topic: str, goal: str, agent_ids: List[str] = None, 
                                    metadata: Dict = None) -> Dict:
        """
        إنشاء جلسة تعاون بين الوكلاء
        
        Args:
            topic: موضوع الجلسة
            goal: هدف الجلسة
            agent_ids: قائمة بمعرفات الوكلاء المشاركين (اختياري)
            metadata: بيانات وصفية إضافية (اختياري)
            
        Returns:
            معلومات الجلسة
        """
        logger.info(f"إنشاء جلسة تعاون جديدة: {topic}")
        
        # إنشاء معرف فريد للجلسة
        session_id = str(uuid.uuid4())
        
        # إذا لم يتم تحديد الوكلاء، استخدام جميع الوكلاء المتاحين
        if not agent_ids:
            agent_ids = list(self.available_agents.keys())
        
        # التحقق من توفر الوكلاء
        available_agent_ids = []
        for agent_id in agent_ids:
            if agent_id in self.available_agents and self.available_agents[agent_id]["status"] == "available":
                available_agent_ids.append(agent_id)
                
                # تحديث حالة الوكيل
                with self.lock:
                    self.available_agents[agent_id]["status"] = "in_session"
                    self.available_agents[agent_id]["current_session"] = session_id
        
        if not available_agent_ids:
            logger.error("لا يوجد وكلاء متاحين للمشاركة في الجلسة")
            return {
                "status": "error",
                "message": "لا يوجد وكلاء متاحين للمشاركة في الجلسة",
                "session_id": None
            }
        
        # إنشاء الجلسة
        metadata = metadata or {}
        metadata["agent_ids"] = available_agent_ids
        
        session_info = {
            "id": session_id,
            "topic": topic,
            "goal": goal,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "agents": available_agent_ids,
            "metadata": metadata
        }
        
        # تخزين الجلسة في الذاكرة
        with self.lock:
            self.active_sessions[session_id] = session_info
            self.conversation_history[session_id] = []
        
        # تخزين الجلسة في قاعدة البيانات
        self._store_session(session_id, topic, goal, "active", json.dumps(metadata))
        
        # إضافة رسالة ترحيب للنظام
        system_message = {
            "agent_id": "system",
            "message_type": "system",
            "content": f"بدأت جلسة التعاون: {topic}. الهدف: {goal}",
            "timestamp": datetime.now().isoformat()
        }
        
        self.add_message_to_session(session_id, system_message)
        
        logger.info(f"تم إنشاء جلسة التعاون {session_id} بنجاح مع {len(available_agent_ids)} وكلاء")
        
        return {
            "status": "success",
            "message": "تم إنشاء جلسة التعاون بنجاح",
            "session_id": session_id,
            "session_info": session_info
        }
    
    def close_collaboration_session(self, session_id: str, summary: str = None) -> Dict:
        """
        إغلاق جلسة تعاون
        
        Args:
            session_id: معرف الجلسة
            summary: ملخص نتائج الجلسة (اختياري)
            
        Returns:
            معلومات الإغلاق
        """
        logger.info(f"إغلاق جلسة التعاون {session_id}")
        
        with self.lock:
            if session_id not in self.active_sessions:
                logger.warning(f"الجلسة {session_id} غير موجودة")
                return {
                    "status": "error",
                    "message": "الجلسة غير موجودة",
                    "session_id": session_id
                }
            
            session_info = self.active_sessions[session_id]
            
            # إنشاء ملخص إذا لم يتم تقديمه
            if not summary:
                conversation = self.get_session_messages(session_id)
                summary = self._generate_session_summary(session_id, conversation)
            
            # تحديث حالة الوكلاء
            for agent_id in session_info["agents"]:
                if agent_id in self.available_agents:
                    self.available_agents[agent_id]["status"] = "available"
                    self.available_agents[agent_id]["current_session"] = None
            
            # إضافة رسالة إغلاق للنظام
            system_message = {
                "agent_id": "system",
                "message_type": "system",
                "content": f"انتهت جلسة التعاون: {session_info['topic']}. الملخص: {summary}",
                "timestamp": datetime.now().isoformat()
            }
            
            self.add_message_to_session(session_id, system_message)
            
            # تحديث حالة الجلسة
            session_info["status"] = "closed"
            session_info["updated_at"] = datetime.now().isoformat()
            session_info["summary"] = summary
            
            # تحديث قاعدة البيانات
            self._update_session_status(session_id, "closed")
            
            # نقل الجلسة من النشطة إلى المغلقة
            del self.active_sessions[session_id]
        
        logger.info(f"تم إغلاق جلسة التعاون {session_id} بنجاح")
        
        return {
            "status": "success",
            "message": "تم إغلاق جلسة التعاون بنجاح",
            "session_id": session_id,
            "summary": summary
        }
    
    def add_message_to_session(self, session_id: str, message: Dict) -> Dict:
        """
        إضافة رسالة إلى جلسة التعاون
        
        Args:
            session_id: معرف الجلسة
            message: الرسالة
            
        Returns:
            معلومات العملية
        """
        if session_id not in self.active_sessions:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return {
                "status": "error",
                "message": "الجلسة غير موجودة",
                "session_id": session_id
            }
        
        # التحقق من صحة الرسالة
        required_fields = ["agent_id", "content"]
        for field in required_fields:
            if field not in message:
                logger.warning(f"الحقل {field} مفقود في الرسالة")
                return {
                    "status": "error",
                    "message": f"الحقل {field} مفقود في الرسالة",
                    "session_id": session_id
                }
        
        # إضافة الوقت إذا لم يكن موجوداً
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().isoformat()
        
        # إضافة نوع الرسالة إذا لم يكن موجوداً
        if "message_type" not in message:
            message["message_type"] = "chat"
        
        # إضافة البيانات الوصفية إذا لم تكن موجودة
        if "metadata" not in message:
            message["metadata"] = {}
        
        # تخزين الرسالة في الذاكرة
        with self.lock:
            self.conversation_history[session_id].append(message)
        
        # تخزين الرسالة في قاعدة البيانات
        self._store_message(
            session_id,
            message["agent_id"],
            message["message_type"],
            message["content"],
            json.dumps(message.get("metadata", {}))
        )
        
        logger.info(f"تمت إضافة رسالة من الوكيل {message['agent_id']} إلى الجلسة {session_id}")
        
        return {
            "status": "success",
            "message": "تمت إضافة الرسالة بنجاح",
            "session_id": session_id,
            "message_id": len(self.conversation_history[session_id]) - 1
        }
    
    def get_session_messages(self, session_id: str, limit: int = None, 
                            agent_id: str = None, message_type: str = None) -> List[Dict]:
        """
        الحصول على رسائل جلسة التعاون
        
        Args:
            session_id: معرف الجلسة
            limit: عدد الرسائل (اختياري)
            agent_id: تصفية حسب معرف الوكيل (اختياري)
            message_type: تصفية حسب نوع الرسالة (اختياري)
            
        Returns:
            قائمة بالرسائل
        """
        if session_id not in self.conversation_history:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return []
        
        messages = self.conversation_history[session_id]
        
        # تطبيق التصفية
        if agent_id:
            messages = [msg for msg in messages if msg["agent_id"] == agent_id]
        
        if message_type:
            messages = [msg for msg in messages if msg.get("message_type") == message_type]
        
        # تطبيق الحد
        if limit and limit > 0:
            messages = messages[-limit:]
        
        return messages
    
    def send_direct_message(self, session_id: str, from_agent_id: str, 
                           to_agent_id: str, content: str, metadata: Dict = None) -> Dict:
        """
        إرسال رسالة مباشرة من وكيل إلى وكيل آخر
        
        Args:
            session_id: معرف الجلسة
            from_agent_id: معرف الوكيل المرسل
            to_agent_id: معرف الوكيل المستقبل
            content: محتوى الرسالة
            metadata: بيانات وصفية إضافية (اختياري)
            
        Returns:
            معلومات العملية
        """
        logger.info(f"إرسال رسالة مباشرة من {from_agent_id} إلى {to_agent_id} في الجلسة {session_id}")
        
        if session_id not in self.active_sessions:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return {
                "status": "error",
                "message": "الجلسة غير موجودة",
                "session_id": session_id
            }
        
        # التحقق من وجود الوكيلين في الجلسة
        session_info = self.active_sessions[session_id]
        if from_agent_id not in session_info["agents"]:
            logger.warning(f"الوكيل المرسل {from_agent_id} غير موجود في الجلسة")
            return {
                "status": "error",
                "message": "الوكيل المرسل غير موجود في الجلسة",
                "session_id": session_id
            }
        
        if to_agent_id not in session_info["agents"]:
            logger.warning(f"الوكيل المستقبل {to_agent_id} غير موجود في الجلسة")
            return {
                "status": "error",
                "message": "الوكيل المستقبل غير موجود في الجلسة",
                "session_id": session_id
            }
        
        # إنشاء الرسالة
        metadata = metadata or {}
        metadata["direct_message"] = True
        metadata["to_agent_id"] = to_agent_id
        
        message = {
            "agent_id": from_agent_id,
            "message_type": "direct",
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }
        
        # إضافة الرسالة إلى الجلسة
        result = self.add_message_to_session(session_id, message)
        
        if result["status"] == "success":
            logger.info(f"تم إرسال رسالة مباشرة من {from_agent_id} إلى {to_agent_id} بنجاح")
        
        return result
    
    def start_brainstorming(self, session_id: str, topic: str, duration_minutes: int = 5, 
                           max_ideas_per_agent: int = 5) -> Dict:
        """
        بدء جلسة عصف ذهني بين الوكلاء
        
        Args:
            session_id: معرف الجلسة
            topic: موضوع العصف الذهني
            duration_minutes: مدة الجلسة بالدقائق (اختياري)
            max_ideas_per_agent: الحد الأقصى للأفكار لكل وكيل (اختياري)
            
        Returns:
            نتائج العصف الذهني
        """
        logger.info(f"بدء جلسة عصف ذهني حول {topic} في الجلسة {session_id}")
        
        if session_id not in self.active_sessions:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return {
                "status": "error",
                "message": "الجلسة غير موجودة",
                "session_id": session_id
            }
        
        # الحصول على الوكلاء المشاركين
        session_info = self.active_sessions[session_id]
        agent_ids = session_info["agents"]
        
        # إضافة رسالة بدء العصف الذهني
        system_message = {
            "agent_id": "system",
            "message_type": "system",
            "content": f"بدأت جلسة العصف الذهني حول: {topic}. المدة: {duration_minutes} دقائق.",
            "timestamp": datetime.now().isoformat()
        }
        
        self.add_message_to_session(session_id, system_message)
        
        # جمع الأفكار من كل وكيل
        all_ideas = []
        futures = {}
        
        with ThreadPoolExecutor(max_workers=len(agent_ids)) as executor:
            for agent_id in agent_ids:
                if agent_id in self.available_agents:
                    agent_info = self.available_agents[agent_id]
                    futures[agent_id] = executor.submit(
                        self._generate_agent_ideas,
                        agent_id,
                        agent_info,
                        topic,
                        session_id,
                        max_ideas_per_agent
                    )
        
        # جمع النتائج
        for agent_id, future in futures.items():
            try:
                agent_ideas = future.result()
                all_ideas.extend(agent_ideas)
                
                # إضافة رسالة بأفكار الوكيل
                idea_message = {
                    "agent_id": agent_id,
                    "message_type": "brainstorm",
                    "content": f"أفكاري حول {topic}:\n" + "\n".join([f"- {idea}" for idea in agent_ideas]),
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "ideas": agent_ideas,
                        "topic": topic
                    }
                }
                
                self.add_message_to_session(session_id, idea_message)
                
            except Exception as e:
                logger.error(f"خطأ في جمع أفكار الوكيل {agent_id}: {str(e)}")
        
        # تحليل وتلخيص الأفكار
        summary = self._summarize_brainstorming(all_ideas, topic)
        
        # إضافة رسالة ملخص العصف الذهني
        summary_message = {
            "agent_id": "system",
            "message_type": "summary",
            "content": f"ملخص نتائج العصف الذهني حول {topic}:\n{summary['summary']}",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "ideas_count": len(all_ideas),
                "top_ideas": summary["top_ideas"],
                "categories": summary["categories"]
            }
        }
        
        self.add_message_to_session(session_id, summary_message)
        
        logger.info(f"اكتملت جلسة العصف الذهني في الجلسة {session_id} مع {len(all_ideas)} فكرة")
        
        return {
            "status": "success",
            "message": "اكتملت جلسة العصف الذهني بنجاح",
            "session_id": session_id,
            "ideas_count": len(all_ideas),
            "all_ideas": all_ideas,
            "summary": summary
        }
    
    def distribute_tasks(self, session_id: str, tasks: List[Dict], auto_assign: bool = True) -> Dict:
        """
        توزيع المهام على الوكلاء في جلسة
        
        Args:
            session_id: معرف الجلسة
            tasks: قائمة بالمهام
            auto_assign: توزيع المهام تلقائياً (اختياري)
            
        Returns:
            نتائج توزيع المهام
        """
        logger.info(f"توزيع {len(tasks)} مهام في الجلسة {session_id}")
        
        if session_id not in self.active_sessions:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return {
                "status": "error",
                "message": "الجلسة غير موجودة",
                "session_id": session_id
            }
        
        # الحصول على الوكلاء المشاركين
        session_info = self.active_sessions[session_id]
        agent_ids = session_info["agents"]
        
        if not agent_ids:
            logger.warning(f"لا يوجد وكلاء في الجلسة {session_id}")
            return {
                "status": "error",
                "message": "لا يوجد وكلاء في الجلسة",
                "session_id": session_id
            }
        
        if not tasks:
            logger.warning("قائمة المهام فارغة")
            return {
                "status": "error",
                "message": "قائمة المهام فارغة",
                "session_id": session_id
            }
        
        # تهيئة توزيع المهام للجلسة
        with self.lock:
            if session_id not in self.task_assignments:
                self.task_assignments[session_id] = {}
        
        assignments = []
        
        # إذا كان التوزيع تلقائياً، تعيين المهام للوكلاء المناسبين
        if auto_assign:
            agent_capabilities = {
                agent_id: self.available_agents[agent_id]["capabilities"]
                for agent_id in agent_ids
                if agent_id in self.available_agents
            }
            
            assignments = self._auto_assign_tasks(tasks, agent_capabilities)
        else:
            # استخدام التعيينات المحددة مسبقاً في المهام
            for task in tasks:
                if "assigned_to" in task and task["assigned_to"] in agent_ids:
                    assignments.append({
                        "task_id": task.get("id", str(uuid.uuid4())),
                        "agent_id": task["assigned_to"],
                        "task_description": task.get("description", ""),
                        "priority": task.get("priority", 5),
                        "deadline": task.get("deadline")
                    })
                else:
                    logger.warning(f"لا يمكن تعيين المهمة {task.get('id', 'غير معروف')} لأن الوكيل غير محدد أو غير موجود في الجلسة")
        
        if not assignments:
            logger.warning(f"لم يتم تعيين أي مهام في الجلسة {session_id}")
            return {
                "status": "error",
                "message": "لم يتم تعيين أي مهام",
                "session_id": session_id
            }
        
        # تخزين التعيينات
        for assignment in assignments:
            task_id = assignment["task_id"]
            agent_id = assignment["agent_id"]
            
            # تخزين في الذاكرة
            with self.lock:
                self.task_assignments[session_id][task_id] = {
                    "task_id": task_id,
                    "agent_id": agent_id,
                    "task_description": assignment["task_description"],
                    "status": "assigned",
                    "assigned_at": datetime.now().isoformat(),
                    "priority": assignment.get("priority", 5),
                    "deadline": assignment.get("deadline"),
                    "result": None
                }
            
            # تخزين في قاعدة البيانات
            self._store_task_assignment(
                session_id,
                task_id,
                agent_id,
                assignment["task_description"],
                "assigned"
            )
            
            # إرسال رسالة للوكيل بالمهمة
            task_message = {
                "agent_id": "system",
                "message_type": "task_assignment",
                "content": f"تم تعيين مهمة للوكيل {agent_id}: {assignment['task_description']}",
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "task_id": task_id,
                    "agent_id": agent_id,
                    "priority": assignment.get("priority", 5),
                    "deadline": assignment.get("deadline")
                }
            }
            
            self.add_message_to_session(session_id, task_message)
        
        logger.info(f"تم توزيع {len(assignments)} مهام في الجلسة {session_id}")
        
        return {
            "status": "success",
            "message": "تم توزيع المهام بنجاح",
            "session_id": session_id,
            "assignments": assignments
        }
    
    def submit_task_result(self, session_id: str, task_id: str, agent_id: str, result: Dict) -> Dict:
        """
        تقديم نتيجة مهمة
        
        Args:
            session_id: معرف الجلسة
            task_id: معرف المهمة
            agent_id: معرف الوكيل
            result: نتيجة المهمة
            
        Returns:
            معلومات العملية
        """
        logger.info(f"تقديم نتيجة المهمة {task_id} من الوكيل {agent_id} في الجلسة {session_id}")
        
        if session_id not in self.active_sessions:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return {
                "status": "error",
                "message": "الجلسة غير موجودة",
                "session_id": session_id
            }
        
        if session_id not in self.task_assignments or task_id not in self.task_assignments[session_id]:
            logger.warning(f"المهمة {task_id} غير موجودة في الجلسة {session_id}")
            return {
                "status": "error",
                "message": "المهمة غير موجودة في الجلسة",
                "session_id": session_id,
                "task_id": task_id
            }
        
        task_info = self.task_assignments[session_id][task_id]
        
        if task_info["agent_id"] != agent_id:
            logger.warning(f"الوكيل {agent_id} غير مسؤول عن المهمة {task_id}")
            return {
                "status": "error",
                "message": "الوكيل غير مسؤول عن المهمة",
                "session_id": session_id,
                "task_id": task_id
            }
        
        # تحديث حالة المهمة
        with self.lock:
            self.task_assignments[session_id][task_id]["status"] = "completed"
            self.task_assignments[session_id][task_id]["completed_at"] = datetime.now().isoformat()
            self.task_assignments[session_id][task_id]["result"] = result
        
        # تحديث قاعدة البيانات
        self._update_task_status(
            session_id,
            task_id,
            "completed",
            json.dumps(result)
        )
        
        # إضافة رسالة بنتيجة المهمة
        result_message = {
            "agent_id": agent_id,
            "message_type": "task_result",
            "content": f"نتيجة المهمة {task_id}: {result.get('summary', 'مكتملة')}",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "task_id": task_id,
                "result": result
            }
        }
        
        self.add_message_to_session(session_id, result_message)
        
        logger.info(f"تم تقديم نتيجة المهمة {task_id} بنجاح")
        
        return {
            "status": "success",
            "message": "تم تقديم نتيجة المهمة بنجاح",
            "session_id": session_id,
            "task_id": task_id
        }
    
    def start_voting(self, session_id: str, topic: str, options: List[Dict], 
                    deadline_seconds: int = 60) -> Dict:
        """
        بدء تصويت بين الوكلاء
        
        Args:
            session_id: معرف الجلسة
            topic: موضوع التصويت
            options: خيارات التصويت
            deadline_seconds: مهلة التصويت بالثواني (اختياري)
            
        Returns:
            نتائج عملية بدء التصويت
        """
        logger.info(f"بدء تصويت حول {topic} في الجلسة {session_id}")
        
        if session_id not in self.active_sessions:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return {
                "status": "error",
                "message": "الجلسة غير موجودة",
                "session_id": session_id
            }
        
        # الحصول على الوكلاء المشاركين
        session_info = self.active_sessions[session_id]
        agent_ids = session_info["agents"]
        
        if not options or len(options) < 2:
            logger.warning("خيارات التصويت غير كافية")
            return {
                "status": "error",
                "message": "يجب توفير خيارين على الأقل للتصويت",
                "session_id": session_id
            }
        
        # إضافة معرفات للخيارات إذا لم تكن موجودة
        for option in options:
            if "id" not in option:
                option["id"] = str(uuid.uuid4())
        
        # إنشاء سجل التصويت
        voting_id = str(uuid.uuid4())
        voting_info = {
            "id": voting_id,
            "session_id": session_id,
            "topic": topic,
            "options": options,
            "started_at": datetime.now().isoformat(),
            "deadline": (datetime.now() + datetime.timedelta(seconds=deadline_seconds)).isoformat(),
            "status": "active",
            "votes": {},
            "results": None
        }
        
        # تخزين سجل التصويت
        with self.lock:
            if "votings" not in self.active_sessions[session_id]:
                self.active_sessions[session_id]["votings"] = {}
            
            self.active_sessions[session_id]["votings"][voting_id] = voting_info
        
        # إضافة رسالة بدء التصويت
        voting_message = {
            "agent_id": "system",
            "message_type": "voting_start",
            "content": f"بدأ تصويت حول: {topic}. المهلة: {deadline_seconds} ثانية.",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "voting_id": voting_id,
                "options": options,
                "deadline_seconds": deadline_seconds
            }
        }
        
        self.add_message_to_session(session_id, voting_message)
        
        # جمع أصوات الوكلاء
        futures = {}
        
        with ThreadPoolExecutor(max_workers=len(agent_ids)) as executor:
            for agent_id in agent_ids:
                if agent_id in self.available_agents:
                    agent_info = self.available_agents[agent_id]
                    futures[agent_id] = executor.submit(
                        self._collect_agent_vote,
                        agent_id,
                        agent_info,
                        topic,
                        options,
                        session_id,
                        voting_id
                    )
        
        # جمع الأصوات
        votes = {}
        for agent_id, future in futures.items():
            try:
                vote_result = future.result()
                votes[agent_id] = vote_result
                
                # تخزين الصوت في قاعدة البيانات
                self._store_vote(
                    session_id,
                    topic,
                    agent_id,
                    vote_result["option_id"],
                    vote_result["vote_value"],
                    vote_result["reasoning"]
                )
                
                # إضافة رسالة بصوت الوكيل
                vote_message = {
                    "agent_id": agent_id,
                    "message_type": "vote",
                    "content": f"صوتي في موضوع '{topic}': {vote_result['reasoning']}",
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "voting_id": voting_id,
                        "option_id": vote_result["option_id"],
                        "vote_value": vote_result["vote_value"]
                    }
                }
                
                self.add_message_to_session(session_id, vote_message)
                
            except Exception as e:
                logger.error(f"خطأ في جمع صوت الوكيل {agent_id}: {str(e)}")
        
        # تحديث سجل التصويت بالنتائج
        with self.lock:
            voting_info = self.active_sessions[session_id]["votings"][voting_id]
            voting_info["votes"] = votes
            voting_info["status"] = "completed"
            
            # حساب النتائج
            results = self._calculate_voting_results(votes, options)
            voting_info["results"] = results
        
        # إضافة رسالة بنتائج التصويت
        results_message = {
            "agent_id": "system",
            "message_type": "voting_results",
            "content": f"نتائج التصويت حول '{topic}':\n{results['summary']}",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "voting_id": voting_id,
                "results": results
            }
        }
        
        self.add_message_to_session(session_id, results_message)
        
        logger.info(f"اكتمل التصويت {voting_id} في الجلسة {session_id}")
        
        return {
            "status": "success",
            "message": "اكتمل التصويت بنجاح",
            "session_id": session_id,
            "voting_id": voting_id,
            "results": results
        }
    
    def run_agent_conference(self, session_id: str, topic: str, moderator_id: str = None, 
                            rounds: int = 3, max_time_minutes: int = 10) -> Dict:
        """
        إجراء مؤتمر بين الوكلاء لمناقشة موضوع
        
        Args:
            session_id: معرف الجلسة
            topic: موضوع المؤتمر
            moderator_id: معرف الوكيل المدير (اختياري)
            rounds: عدد جولات النقاش (اختياري)
            max_time_minutes: الحد الأقصى للوقت بالدقائق (اختياري)
            
        Returns:
            نتائج المؤتمر
        """
        logger.info(f"بدء مؤتمر حول {topic} في الجلسة {session_id}")
        
        if session_id not in self.active_sessions:
            logger.warning(f"الجلسة {session_id} غير موجودة")
            return {
                "status": "error",
                "message": "الجلسة غير موجودة",
                "session_id": session_id
            }
        
        # الحصول على الوكلاء المشاركين
        session_info = self.active_sessions[session_id]
        agent_ids = session_info["agents"]
        
        if len(agent_ids) < 2:
            logger.warning(f"عدد الوكلاء غير كافٍ في الجلسة {session_id}")
            return {
                "status": "error",
                "message": "يجب وجود وكيلين على الأقل للمؤتمر",
                "session_id": session_id
            }
        
        # إذا لم يتم تحديد المدير، اختيار وكيل عشوائياً
        if not moderator_id or moderator_id not in agent_ids:
            moderator_id = agent_ids[0]
        
        # إضافة رسالة بدء المؤتمر
        conference_id = str(uuid.uuid4())
        start_message = {
            "agent_id": "system",
            "message_type": "conference_start",
            "content": f"بدأ مؤتمر الوكلاء حول: {topic}. المدير: {moderator_id}. عدد الجولات: {rounds}.",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "conference_id": conference_id,
                "moderator_id": moderator_id,
                "rounds": rounds,
                "max_time_minutes": max_time_minutes
            }
        }
        
        self.add_message_to_session(session_id, start_message)
        
        # إجراء جولات النقاش
        conference_messages = []
        
        for round_num in range(1, rounds + 1):
            logger.info(f"جولة المؤتمر {round_num}/{rounds}")
            
            # رسالة بدء الجولة
            round_start = {
                "agent_id": "system",
                "message_type": "conference_round",
                "content": f"جولة المؤتمر {round_num}/{rounds}: {topic}",
                "timestamp": datetime.now().isoformat()
            }
            
            self.add_message_to_session(session_id, round_start)
            conference_messages.append(round_start)
            
            # جمع تعليقات الوكلاء في هذه الجولة
            round_messages = []
            
            # تعليق المدير أولاً
            if round_num == 1:
                moderator_prompt = f"أنت مدير مؤتمر الوكلاء حول '{topic}'. قم بتقديم الموضوع وطرح الأسئلة الرئيسية للنقاش."
                moderator_context = {
                    "role": "moderator",
                    "round": round_num,
                    "session_id": session_id,
                    "conference_id": conference_id
                }
            else:
                # استخراج تعليقات الجولة السابقة
                previous_comments = [
                    msg for msg in conference_messages 
                    if msg.get("message_type") == "conference_comment" and 
                    msg.get("metadata", {}).get("round") == round_num - 1
                ]
                
                moderator_prompt = f"""
                أنت مدير مؤتمر الوكلاء حول '{topic}'. 
                هذه الجولة رقم {round_num} من {rounds}.
                
                تعليقات الجولة السابقة:
                {json.dumps([
                    {"agent": msg["agent_id"], "comment": msg["content"]} 
                    for msg in previous_comments
                ], ensure_ascii=False)}
                
                قم بتلخيص النقاط الرئيسية وطرح أسئلة للجولة الحالية.
                """
                
                moderator_context = {
                    "role": "moderator",
                    "round": round_num,
                    "session_id": session_id,
                    "conference_id": conference_id,
                    "previous_comments": previous_comments
                }
            
            # الحصول على تعليق المدير
            moderator_comment = self._get_agent_conference_comment(
                moderator_id, 
                self.available_agents[moderator_id], 
                topic, 
                moderator_prompt, 
                moderator_context
            )
            
            if moderator_comment:
                moderator_message = {
                    "agent_id": moderator_id,
                    "message_type": "conference_comment",
                    "content": moderator_comment,
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "conference_id": conference_id,
                        "round": round_num,
                        "role": "moderator"
                    }
                }
                
                self.add_message_to_session(session_id, moderator_message)
                conference_messages.append(moderator_message)
                round_messages.append(moderator_message)
            
            # جمع تعليقات باقي الوكلاء
            participant_ids = [agent_id for agent_id in agent_ids if agent_id != moderator_id]
            
            # استخدام التزامن لجمع التعليقات
            futures = {}
            
            with ThreadPoolExecutor(max_workers=len(participant_ids)) as executor:
                for agent_id in participant_ids:
                    if agent_id in self.available_agents:
                        agent_info = self.available_agents[agent_id]
                        
                        # إنشاء سياق الوكيل
                        context = {
                            "role": "participant",
                            "round": round_num,
                            "session_id": session_id,
                            "conference_id": conference_id,
                            "moderator_comment": moderator_comment,
                            "previous_messages": round_messages
                        }
                        
                        prompt = f"""
                        أنت مشارك في مؤتمر الوكلاء حول '{topic}'. 
                        هذه الجولة رقم {round_num} من {rounds}.
                        
                        تعليق المدير:
                        {moderator_comment}
                        
                        قدم وجهة نظرك أو إجابتك على الأسئلة المطروحة.
                        """
                        
                        futures[agent_id] = executor.submit(
                            self._get_agent_conference_comment,
                            agent_id,
                            agent_info,
                            topic,
                            prompt,
                            context
                        )
            
            # جمع التعليقات
            for agent_id, future in futures.items():
                try:
                    comment = future.result()
                    
                    if comment:
                        agent_message = {
                            "agent_id": agent_id,
                            "message_type": "conference_comment",
                            "content": comment,
                            "timestamp": datetime.now().isoformat(),
                            "metadata": {
                                "conference_id": conference_id,
                                "round": round_num,
                                "role": "participant"
                            }
                        }
                        
                        self.add_message_to_session(session_id, agent_message)
                        conference_messages.append(agent_message)
                        round_messages.append(agent_message)
                    
                except Exception as e:
                    logger.error(f"خطأ في الحصول على تعليق الوكيل {agent_id}: {str(e)}")
        
        # تلخيص نتائج المؤتمر
        summary = self._generate_conference_summary(conference_id, conference_messages, topic)
        
        # إضافة رسالة ملخص المؤتمر
        summary_message = {
            "agent_id": "system",
            "message_type": "conference_summary",
            "content": f"ملخص مؤتمر الوكلاء حول '{topic}':\n{summary['summary']}",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "conference_id": conference_id,
                "summary": summary
            }
        }
        
        self.add_message_to_session(session_id, summary_message)
        
        logger.info(f"اكتمل مؤتمر الوكلاء {conference_id} في الجلسة {session_id}")
        
        return {
            "status": "success",
            "message": "اكتمل مؤتمر الوكلاء بنجاح",
            "session_id": session_id,
            "conference_id": conference_id,
            "summary": summary
        }
    
    def get_available_agents(self) -> Dict:
        """
        الحصول على قائمة الوكلاء المتاحين
        
        Returns:
            قائمة الوكلاء المتاحين
        """
        agents_info = {}
        
        for agent_id, agent_info in self.available_agents.items():
            agents_info[agent_id] = {
                "type": agent_info["type"],
                "capabilities": agent_info["capabilities"],
                "status": agent_info["status"],
                "current_session": agent_info["current_session"],
                "registered_at": agent_info["registered_at"]
            }
        
        return {
            "count": len(agents_info),
            "agents": agents_info
        }
    
    def get_active_sessions(self) -> Dict:
        """
        الحصول على قائمة الجلسات النشطة
        
        Returns:
            قائمة الجلسات النشطة
        """
        sessions_info = {}
        
        for session_id, session_info in self.active_sessions.items():
            sessions_info[session_id] = {
                "topic": session_info["topic"],
                "goal": session_info["goal"],
                "status": session_info["status"],
                "created_at": session_info["created_at"],
                "updated_at": session_info["updated_at"],
                "agents_count": len(session_info["agents"])
            }
        
        return {
            "count": len(sessions_info),
            "sessions": sessions_info
        }
    
    def _store_session(self, session_id: str, topic: str, goal: str, status: str, metadata: str) -> int:
        """
        تخزين جلسة في قاعدة البيانات
        
        Args:
            session_id: معرف الجلسة
            topic: موضوع الجلسة
            goal: هدف الجلسة
            status: حالة الجلسة
            metadata: البيانات الوصفية
            
        Returns:
            معرف السجل
        """
        cursor = self.db.cursor()
        
        cursor.execute("""
        INSERT INTO collaboration_sessions 
        (id, topic, goal, status, metadata)
        VALUES (?, ?, ?, ?, ?)
        """, (session_id, topic, goal, status, metadata))
        
        self.db.commit()
        
        return cursor.lastrowid
    
    def _update_session_status(self, session_id: str, status: str) -> bool:
        """
        تحديث حالة جلسة في قاعدة البيانات
        
        Args:
            session_id: معرف الجلسة
            status: الحالة الجديدة
            
        Returns:
            نجاح العملية
        """
        cursor = self.db.cursor()
        
        cursor.execute("""
        UPDATE collaboration_sessions 
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (status, session_id))
        
        self.db.commit()
        
        return cursor.rowcount > 0
    
    def _store_message(self, session_id: str, agent_id: str, message_type: str, 
                      content: str, metadata: str) -> int:
        """
        تخزين رسالة في قاعدة البيانات
        
        Args:
            session_id: معرف الجلسة
            agent_id: معرف الوكيل
            message_type: نوع الرسالة
            content: محتوى الرسالة
            metadata: البيانات الوصفية
            
        Returns:
            معرف السجل
        """
        cursor = self.db.cursor()
        
        cursor.execute("""
        INSERT INTO collaboration_messages 
        (session_id, agent_id, message_type, content, metadata)
        VALUES (?, ?, ?, ?, ?)
        """, (session_id, agent_id, message_type, content, metadata))
        
        self.db.commit()
        
        return cursor.lastrowid
    
    def _store_task_assignment(self, session_id: str, task_id: str, agent_id: str, 
                              task_description: str, status: str) -> int:
        """
        تخزين تعيين مهمة في قاعدة البيانات
        
        Args:
            session_id: معرف الجلسة
            task_id: معرف المهمة
            agent_id: معرف الوكيل
            task_description: وصف المهمة
            status: حالة المهمة
            
        Returns:
            معرف السجل
        """
        cursor = self.db.cursor()
        
        cursor.execute("""
        INSERT INTO task_assignments 
        (session_id, task_id, agent_id, task_description, status)
        VALUES (?, ?, ?, ?, ?)
        """, (session_id, task_id, agent_id, task_description, status))
        
        self.db.commit()
        
        return cursor.lastrowid
    
    def _update_task_status(self, session_id: str, task_id: str, status: str, result: str = None) -> bool:
        """
        تحديث حالة مهمة في قاعدة البيانات
        
        Args:
            session_id: معرف الجلسة
            task_id: معرف المهمة
            status: الحالة الجديدة
            result: نتيجة المهمة (اختياري)
            
        Returns:
            نجاح العملية
        """
        cursor = self.db.cursor()
        
        if status == "completed":
            cursor.execute("""
            UPDATE task_assignments 
            SET status = ?, completed_at = CURRENT_TIMESTAMP, result = ?
            WHERE session_id = ? AND task_id = ?
            """, (status, result, session_id, task_id))
        else:
            cursor.execute("""
            UPDATE task_assignments 
            SET status = ?
            WHERE session_id = ? AND task_id = ?
            """, (status, session_id, task_id))
        
        self.db.commit()
        
        return cursor.rowcount > 0
    
    def _store_vote(self, session_id: str, topic: str, agent_id: str, option_id: str, 
                   vote_value: int, reasoning: str) -> int:
        """
        تخزين صوت في قاعدة البيانات
        
        Args:
            session_id: معرف الجلسة
            topic: موضوع التصويت
            agent_id: معرف الوكيل
            option_id: معرف الخيار
            vote_value: قيمة الصوت
            reasoning: سبب التصويت
            
        Returns:
            معرف السجل
        """
        cursor = self.db.cursor()
        
        cursor.execute("""
        INSERT INTO agent_votes 
        (session_id, topic, agent_id, option_id, vote_value, reasoning)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, topic, agent_id, option_id, vote_value, reasoning))
        
        self.db.commit()
        
        return cursor.lastrowid
    
    def _generate_agent_ideas(self, agent_id: str, agent_info: Dict, topic: str, 
                             session_id: str, max_ideas: int = 5) -> List[str]:
        """
        توليد أفكار من وكيل
        
        Args:
            agent_id: معرف الوكيل
            agent_info: معلومات الوكيل
            topic: موضوع العصف الذهني
            session_id: معرف الجلسة
            max_ideas: الحد الأقصى للأفكار
            
        Returns:
            قائمة بالأفكار
        """
        logger.info(f"توليد أفكار من الوكيل {agent_id} حول {topic}")
        
        # الحصول على تاريخ المحادثة للسياق
        conversation_history = self.get_session_messages(session_id, limit=10)
        
        # إنشاء نص تاريخ المحادثة
        history_text = ""
        for msg in conversation_history:
            sender = msg["agent_id"]
            content = msg["content"]
            history_text += f"{sender}: {content}\n\n"
        
        # إنشاء موجه للوكيل
        prompt = f"""
        أنت وكيل ذكي يدعى {agent_id} وتشارك في جلسة عصف ذهني حول الموضوع: "{topic}".
        
        سياق المحادثة:
        {history_text}
        
        مهمتك هي إنتاج {max_ideas} أفكار إبداعية ومبتكرة حول الموضوع المطروح.
        قم بإنتاج أفكار متنوعة وفريدة ومفيدة.
        
        أنتج الأفكار بتنسيق JSON كما يلي:
        {{
            "ideas": [
                "الفكرة الأولى هنا",
                "الفكرة الثانية هنا",
                ...
            ],
            "reasoning": "شرح موجز لمنهجية توليد الأفكار"
        }}
        """
        
        try:
            # الحصول على الاستجابة من نموذج اللغة
            response = get_llm_response(
                prompt,
                temperature=0.8,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            # تحليل الاستجابة
            ideas_data = json.loads(response)
            
            if "ideas" in ideas_data and isinstance(ideas_data["ideas"], list):
                ideas = ideas_data["ideas"]
                
                # تسجيل الأفكار المولدة
                logger.info(f"تم توليد {len(ideas)} أفكار من الوكيل {agent_id}")
                
                return ideas
            else:
                logger.warning(f"استجابة غير صالحة من الوكيل {agent_id}")
                return []
            
        except Exception as e:
            logger.error(f"خطأ في توليد أفكار من الوكيل {agent_id}: {str(e)}")
            return []
    
    def _summarize_brainstorming(self, ideas: List[str], topic: str) -> Dict:
        """
        تلخيص نتائج العصف الذهني
        
        Args:
            ideas: قائمة بالأفكار
            topic: موضوع العصف الذهني
            
        Returns:
            ملخص العصف الذهني
        """
        logger.info(f"تلخيص {len(ideas)} فكرة حول {topic}")
        
        if not ideas:
            return {
                "summary": "لم يتم توليد أي أفكار.",
                "top_ideas": [],
                "categories": {}
            }
        
        # إنشاء موجه للتلخيص
        prompt = f"""
        أنت مستشار تلخيص محترف. قم بتحليل وتلخيص الأفكار التالية التي تم توليدها خلال جلسة عصف ذهني حول الموضوع: "{topic}".
        
        الأفكار:
        {json.dumps(ideas, ensure_ascii=False)}
        
        قم بإنشاء:
        1. ملخص موجز للأفكار (3-5 جمل)
        2. اختيار أفضل 3-5 أفكار
        3. تصنيف الأفكار إلى فئات
        
        أعد الإجابة بتنسيق JSON كما يلي:
        {{
            "summary": "ملخص موجز للأفكار",
            "top_ideas": ["الفكرة الأولى", "الفكرة الثانية", ...],
            "categories": {{
                "الفئة الأولى": ["الفكرة 1", "الفكرة 2", ...],
                "الفئة الثانية": ["الفكرة 3", "الفكرة 4", ...],
                ...
            }}
        }}
        """
        
        try:
            # الحصول على الاستجابة من نموذج اللغة
            response = get_llm_response(
                prompt,
                temperature=0.4,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # تحليل الاستجابة
            summary_data = json.loads(response)
            
            # التحقق من وجود الحقول المطلوبة
            if not all(key in summary_data for key in ["summary", "top_ideas", "categories"]):
                logger.warning("استجابة غير مكتملة من نموذج اللغة")
                
                # إنشاء بيانات افتراضية
                summary_data = {
                    "summary": "تم توليد مجموعة متنوعة من الأفكار حول الموضوع.",
                    "top_ideas": ideas[:5] if len(ideas) > 5 else ideas,
                    "categories": {"أفكار عامة": ideas}
                }
            
            logger.info(f"تم تلخيص العصف الذهني بنجاح: {len(summary_data['top_ideas'])} أفكار رئيسية، {len(summary_data['categories'])} فئات")
            
            return summary_data
            
        except Exception as e:
            logger.error(f"خطأ في تلخيص العصف الذهني: {str(e)}")
            
            # إرجاع بيانات افتراضية في حالة الخطأ
            return {
                "summary": "تم توليد مجموعة من الأفكار حول الموضوع.",
                "top_ideas": ideas[:5] if len(ideas) > 5 else ideas,
                "categories": {"أفكار عامة": ideas}
            }
    
    def _auto_assign_tasks(self, tasks: List[Dict], agent_capabilities: Dict) -> List[Dict]:
        """
        توزيع المهام تلقائياً على الوكلاء المناسبين
        
        Args:
            tasks: قائمة بالمهام
            agent_capabilities: قدرات الوكلاء
            
        Returns:
            قائمة بتعيينات المهام
        """
        logger.info(f"توزيع {len(tasks)} مهام تلقائياً")
        
        assignments = []
        
        for task in tasks:
            task_id = task.get("id", str(uuid.uuid4()))
            task_description = task.get("description", "")
            task_requirements = task.get("requirements", [])
            task_priority = task.get("priority", 5)
            
            # حساب ملاءمة كل وكيل للمهمة
            agent_scores = {}
            
            for agent_id, capabilities in agent_capabilities.items():
                # حساب نقاط الملاءمة
                score = 0
                
                # زيادة النقاط لكل متطلب متوافق
                for req in task_requirements:
                    if req in capabilities:
                        score += 2
                
                # زيادة النقاط لكل قدرة إضافية قد تكون مفيدة
                for cap in capabilities:
                    if cap not in task_requirements:
                        score += 0.5
                
                agent_scores[agent_id] = score
            
            # اختيار الوكيل الأكثر ملاءمة
            if agent_scores:
                best_agent_id = max(agent_scores, key=agent_scores.get)
                
                # إضافة التعيين
                assignment = {
                    "task_id": task_id,
                    "agent_id": best_agent_id,
                    "task_description": task_description,
                    "priority": task_priority,
                    "deadline": task.get("deadline")
                }
                
                assignments.append(assignment)
                
                logger.info(f"تم تعيين المهمة {task_id} للوكيل {best_agent_id} بدرجة ملاءمة {agent_scores[best_agent_id]}")
            else:
                logger.warning(f"لم يتم العثور على وكيل مناسب للمهمة {task_id}")
        
        return assignments
    
    def _collect_agent_vote(self, agent_id: str, agent_info: Dict, topic: str, 
                           options: List[Dict], session_id: str, voting_id: str) -> Dict:
        """
        جمع صوت من وكيل
        
        Args:
            agent_id: معرف الوكيل
            agent_info: معلومات الوكيل
            topic: موضوع التصويت
            options: خيارات التصويت
            session_id: معرف الجلسة
            voting_id: معرف التصويت
            
        Returns:
            نتيجة التصويت
        """
        logger.info(f"جمع صوت من الوكيل {agent_id} في التصويت {voting_id}")
        
        # الحصول على تاريخ المحادثة للسياق
        conversation_history = self.get_session_messages(session_id, limit=10)
        
        # إنشاء نص تاريخ المحادثة
        history_text = ""
        for msg in conversation_history:
            sender = msg["agent_id"]
            content = msg["content"]
            history_text += f"{sender}: {content}\n\n"
        
        # إنشاء نص خيارات التصويت
        options_text = ""
        for i, option in enumerate(options):
            options_text += f"{i+1}. {option['id']}: {option.get('description', option.get('text', ''))}\n"
        
        # إنشاء موجه للوكيل
        prompt = f"""
        أنت وكيل ذكي يدعى {agent_id} وتشارك في تصويت حول الموضوع: "{topic}".
        
        سياق المحادثة:
        {history_text}
        
        الخيارات المتاحة للتصويت:
        {options_text}
        
        مهمتك هي:
        1. تقييم كل خيار بمقياس من 1 إلى 10
        2. اختيار الخيار الأفضل من وجهة نظرك
        3. شرح سبب اختيارك
        
        أعد الإجابة بتنسيق JSON كما يلي:
        {{
            "option_id": "معرف الخيار المختار",
            "vote_value": 10,
            "reasoning": "شرح سبب اختيارك لهذا الخيار",
            "other_options": {{
                "معرف الخيار 1": 5,
                "معرف الخيار 2": 8,
                ...
            }}
        }}
        """
        
        try:
            # الحصول على الاستجابة من نموذج اللغة
            response = get_llm_response(
                prompt,
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            # تحليل الاستجابة
            vote_data = json.loads(response)
            
            # التحقق من صحة البيانات
            if "option_id" not in vote_data or "vote_value" not in vote_data:
                logger.warning(f"استجابة غير صالحة من الوكيل {agent_id}")
                
                # إنشاء صوت افتراضي
                return {
                    "option_id": options[0]["id"],
                    "vote_value": 5,
                    "reasoning": "لم أتمكن من تحديد خيار واضح."
                }
            
            # التحقق من وجود الخيار
            option_exists = any(opt["id"] == vote_data["option_id"] for opt in options)
            if not option_exists:
                logger.warning(f"الوكيل {agent_id} صوت لخيار غير موجود: {vote_data['option_id']}")
                
                # استخدام أول خيار كبديل
                vote_data["option_id"] = options[0]["id"]
                vote_data["reasoning"] += " (تم تصحيح الخيار تلقائياً)"
            
            logger.info(f"تم جمع صوت من الوكيل {agent_id}: {vote_data['option_id']} ({vote_data['vote_value']})")
            
            return vote_data
            
        except Exception as e:
            logger.error(f"خطأ في جمع صوت من الوكيل {agent_id}: {str(e)}")
            
            # إرجاع صوت افتراضي في حالة الخطأ
            return {
                "option_id": options[0]["id"],
                "vote_value": 5,
                "reasoning": f"حدث خطأ أثناء التصويت: {str(e)}"
            }
    
    def _calculate_voting_results(self, votes: Dict, options: List[Dict]) -> Dict:
        """
        حساب نتائج التصويت
        
        Args:
            votes: أصوات الوكلاء
            options: خيارات التصويت
            
        Returns:
            نتائج التصويت
        """
        logger.info(f"حساب نتائج التصويت مع {len(votes)} أصوات")
        
        # تهيئة نتائج الخيارات
        option_results = {option["id"]: {"votes": 0, "score": 0, "avg_score": 0} for option in options}
        
        # حساب النتائج
        for agent_id, vote in votes.items():
            option_id = vote["option_id"]
            vote_value = vote["vote_value"]
            
            if option_id in option_results:
                option_results[option_id]["votes"] += 1
                option_results[option_id]["score"] += vote_value
        
        # حساب المتوسطات
        for option_id, result in option_results.items():
            if result["votes"] > 0:
                result["avg_score"] = result["score"] / result["votes"]
        
        # تحديد الخيار الفائز
        if option_results:
            # الترتيب حسب عدد الأصوات ثم متوسط الدرجة
            winner_id = max(option_results, key=lambda x: (option_results[x]["votes"], option_results[x]["avg_score"]))
            
            # الحصول على تفاصيل الخيار الفائز
            winner_details = next((opt for opt in options if opt["id"] == winner_id), {})
            
            # إنشاء ملخص النتائج
            total_votes = sum(result["votes"] for result in option_results.values())
            
            summary = f"""
            نتائج التصويت:
            - إجمالي الأصوات: {total_votes}
            - الخيار الفائز: {winner_details.get('description', winner_id)}
            - عدد أصوات الفائز: {option_results[winner_id]['votes']} ({option_results[winner_id]['votes']*100/total_votes:.1f}%)
            - متوسط درجة الفائز: {option_results[winner_id]['avg_score']:.1f}/10
            """
            
            return {
                "winner": {
                    "id": winner_id,
                    "details": winner_details,
                    "votes": option_results[winner_id]["votes"],
                    "avg_score": option_results[winner_id]["avg_score"]
                },
                "option_results": option_results,
                "total_votes": total_votes,
                "summary": summary
            }
        else:
            return {
                "winner": None,
                "option_results": {},
                "total_votes": 0,
                "summary": "لم يتم التصويت."
            }
    
    def _get_agent_conference_comment(self, agent_id: str, agent_info: Dict, 
                                     topic: str, prompt: str, context: Dict) -> str:
        """
        الحصول على تعليق وكيل في المؤتمر
        
        Args:
            agent_id: معرف الوكيل
            agent_info: معلومات الوكيل
            topic: موضوع المؤتمر
            prompt: موجه الوكيل
            context: سياق التعليق
            
        Returns:
            تعليق الوكيل
        """
        logger.info(f"طلب تعليق من الوكيل {agent_id} في المؤتمر حول {topic}")
        
        try:
            # الحصول على الاستجابة من نموذج اللغة
            response = get_llm_response(
                prompt,
                temperature=0.5,
                max_tokens=800
            )
            
            logger.info(f"تم استلام تعليق من الوكيل {agent_id}: {len(response)} حرف")
            
            return response
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على تعليق من الوكيل {agent_id}: {str(e)}")
            return f"اعتذر، لم أتمكن من المشاركة بشكل صحيح في هذه الجولة. ({str(e)})"
    
    def _generate_conference_summary(self, conference_id: str, messages: List[Dict], topic: str) -> Dict:
        """
        إنشاء ملخص لمؤتمر الوكلاء
        
        Args:
            conference_id: معرف المؤتمر
            messages: رسائل المؤتمر
            topic: موضوع المؤتمر
            
        Returns:
            ملخص المؤتمر
        """
        logger.info(f"إنشاء ملخص لمؤتمر الوكلاء {conference_id} حول {topic}")
        
        # استخراج تعليقات الوكلاء
        comments = []
        for msg in messages:
            if msg.get("message_type") == "conference_comment":
                comments.append({
                    "agent_id": msg["agent_id"],
                    "content": msg["content"],
                    "round": msg.get("metadata", {}).get("round", 0),
                    "role": msg.get("metadata", {}).get("role", "participant")
                })
        
        if not comments:
            logger.warning(f"لا توجد تعليقات في المؤتمر {conference_id}")
            return {
                "summary": "لم يتم العثور على تعليقات في المؤتمر.",
                "key_points": [],
                "decisions": [],
                "agent_contributions": {}
            }
        
        # إنشاء موجه للتلخيص
        prompt = f"""
        أنت مستشار تلخيص محترف. قم بتحليل وتلخيص المؤتمر التالي بين الوكلاء حول الموضوع: "{topic}".
        
        تعليقات المؤتمر:
        {json.dumps(comments, ensure_ascii=False, indent=2)}
        
        قم بإنشاء:
        1. ملخص شامل للمؤتمر (5-7 جمل)
        2. النقاط الرئيسية التي تمت مناقشتها
        3. القرارات أو التوصيات التي تم التوصل إليها
        4. تقييم لمساهمة كل وكيل في المؤتمر
        
        أعد الإجابة بتنسيق JSON كما يلي:
        {{
            "summary": "ملخص شامل للمؤتمر",
            "key_points": ["النقطة الرئيسية 1", "النقطة الرئيسية 2", ...],
            "decisions": ["القرار 1", "القرار 2", ...],
            "agent_contributions": {{
                "agent_id_1": {{
                    "contribution_level": "عالي/متوسط/منخفض",
                    "strengths": ["نقطة قوة 1", "نقطة قوة 2"],
                    "insights": ["رؤية 1", "رؤية 2"]
                }},
                ...
            }}
        }}
        """
        
        try:
            # الحصول على الاستجابة من نموذج اللغة
            response = get_llm_response(
                prompt,
                temperature=0.4,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # تحليل الاستجابة
            summary_data = json.loads(response)
            
            # التحقق من وجود الحقول المطلوبة
            if not all(key in summary_data for key in ["summary", "key_points", "decisions", "agent_contributions"]):
                logger.warning("استجابة غير مكتملة من نموذج اللغة")
                
                # إنشاء بيانات افتراضية
                summary_data = {
                    "summary": f"تم إجراء مؤتمر بين الوكلاء حول {topic}.",
                    "key_points": ["تمت مناقشة الموضوع من عدة جوانب"],
                    "decisions": [],
                    "agent_contributions": {}
                }
            
            logger.info(f"تم إنشاء ملخص لمؤتمر الوكلاء: {len(summary_data['key_points'])} نقاط رئيسية، {len(summary_data['decisions'])} قرارات")
            
            return summary_data
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء ملخص المؤتمر: {str(e)}")
            
            # إرجاع بيانات افتراضية في حالة الخطأ
            return {
                "summary": f"تم إجراء مؤتمر بين الوكلاء حول {topic}.",
                "key_points": ["تمت مناقشة الموضوع من عدة جوانب"],
                "decisions": [],
                "agent_contributions": {}
            }
    
    def _generate_session_summary(self, session_id: str, messages: List[Dict]) -> str:
        """
        إنشاء ملخص لجلسة التعاون
        
        Args:
            session_id: معرف الجلسة
            messages: رسائل الجلسة
            
        Returns:
            ملخص الجلسة
        """
        logger.info(f"إنشاء ملخص لجلسة التعاون {session_id}")
        
        if not messages:
            return "لم يتم العثور على رسائل في الجلسة."
        
        # الحصول على معلومات الجلسة
        session_info = self.active_sessions.get(session_id, {})
        topic = session_info.get("topic", "موضوع غير معروف")
        goal = session_info.get("goal", "هدف غير معروف")
        
        # إنشاء موجه للتلخيص
        prompt = f"""
        أنت مستشار تلخيص محترف. قم بتلخيص الجلسة التالية بين الوكلاء.
        
        موضوع الجلسة: {topic}
        هدف الجلسة: {goal}
        
        الرسائل:
        {json.dumps([{
            "agent": msg["agent_id"],
            "type": msg.get("message_type", "chat"),
            "content": msg["content"]
        } for msg in messages[-30:]], ensure_ascii=False)}
        
        قم بإنشاء ملخص موجز (7-10 جمل) يتضمن:
        1. أهم النقاط التي تمت مناقشتها
        2. النتائج الرئيسية
        3. الخطوات التالية إن وجدت
        """
        
        try:
            # الحصول على الاستجابة من نموذج اللغة
            response = get_llm_response(
                prompt,
                temperature=0.4,
                max_tokens=800
            )
            
            logger.info(f"تم إنشاء ملخص لجلسة التعاون: {len(response)} حرف")
            
            return response
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء ملخص الجلسة: {str(e)}")
            return f"تم إجراء جلسة تعاون حول {topic} بهدف {goal}. تضمنت الجلسة {len(messages)} رسالة."


# تهيئة نظام التعاون عند استيراد الوحدة
collaboration_system = AgentCollaboration()

def get_collaboration_system():
    """
    الحصول على نسخة من نظام التعاون بين الوكلاء
    
    Returns:
        نظام التعاون بين الوكلاء
    """
    return collaboration_system


# وظائف مساعدة للاستخدام المباشر

def create_collaboration_session(topic: str, goal: str, agent_ids: List[str] = None, 
                                metadata: Dict = None) -> Dict:
    """
    إنشاء جلسة تعاون بين الوكلاء
    
    Args:
        topic: موضوع الجلسة
        goal: هدف الجلسة
        agent_ids: قائمة بمعرفات الوكلاء المشاركين (اختياري)
        metadata: بيانات وصفية إضافية (اختياري)
        
    Returns:
        معلومات الجلسة
    """
    return collaboration_system.create_collaboration_session(topic, goal, agent_ids, metadata)

def start_brainstorming(session_id: str, topic: str, duration_minutes: int = 5, 
                       max_ideas_per_agent: int = 5) -> Dict:
    """
    بدء جلسة عصف ذهني بين الوكلاء
    
    Args:
        session_id: معرف الجلسة
        topic: موضوع العصف الذهني
        duration_minutes: مدة الجلسة بالدقائق (اختياري)
        max_ideas_per_agent: الحد الأقصى للأفكار لكل وكيل (اختياري)
        
    Returns:
        نتائج العصف الذهني
    """
    return collaboration_system.start_brainstorming(session_id, topic, duration_minutes, max_ideas_per_agent)

def run_agent_conference(session_id: str, topic: str, moderator_id: str = None, 
                        rounds: int = 3, max_time_minutes: int = 10) -> Dict:
    """
    إجراء مؤتمر بين الوكلاء لمناقشة موضوع
    
    Args:
        session_id: معرف الجلسة
        topic: موضوع المؤتمر
        moderator_id: معرف الوكيل المدير (اختياري)
        rounds: عدد جولات النقاش (اختياري)
        max_time_minutes: الحد الأقصى للوقت بالدقائق (اختياري)
        
    Returns:
        نتائج المؤتمر
    """
    return collaboration_system.run_agent_conference(session_id, topic, moderator_id, rounds, max_time_minutes)


if __name__ == "__main__":
    # اختبار النظام
    print("اختبار نظام الوكلاء المتعاونين والحوارات الداخلية")
    
    # تسجيل بعض الوكلاء للاختبار
    from ..agents.base_agent import BaseAgent
    
    # إنشاء وكلاء وهمية
    agent1 = BaseAgent(agent_id="idea_generator", agent_name="مولد الأفكار")
    agent2 = BaseAgent(agent_id="chapter_composer", agent_name="كاتب الفصول")
    agent3 = BaseAgent(agent_id="literary_critic", agent_name="الناقد الأدبي")
    
    # تسجيل الوكلاء
    collaboration_system.register_agent(
        "idea_generator",
        agent1,
        "idea_generator",
        ["brainstorming", "idea_creation", "creative_thinking"]
    )
    
    collaboration_system.register_agent(
        "chapter_composer",
        agent2,
        "chapter_composer",
        ["writing", "storytelling", "character_development"]
    )
    
    collaboration_system.register_agent(
        "literary_critic",
        agent3,
        "literary_critic",
        ["analysis", "feedback", "quality_assessment"]
    )
    
    # إنشاء جلسة تعاون
    session_result = create_collaboration_session(
        "تطوير شخصية البطل في الرواية",
        "تحديد أفضل طريقة لتطوير شخصية البطل عبر أحداث الرواية"
    )
    
    print("تم إنشاء جلسة:", session_result)
    
    if session_result["status"] == "success":
        session_id = session_result["session_id"]
        
        # بدء عصف ذهني
        brainstorm_result = start_brainstorming(
            session_id,
            "طرق تطوير شخصية البطل بشكل مقنع"
        )
        
        print("نتائج العصف الذهني:", brainstorm_result)
        
        # إجراء مؤتمر بين الوكلاء
        conference_result = run_agent_conference(
            session_id,
            "اختيار أفضل مسار لتطور البطل",
            moderator_id="literary_critic",
            rounds=2
        )
        
        print("نتائج المؤتمر:", conference_result)
        
        # إغلاق الجلسة
        close_result = collaboration_system.close_collaboration_session(session_id)
        print("تم إغلاق الجلسة:", close_result)