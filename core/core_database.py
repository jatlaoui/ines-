"""
قاعدة البيانات الموحدة المحسنة للنظام الذكي للكتابة العربية
تطبيق المرحلة الأولى من التحسينات - بنية مبسطة وقوية
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from enum import Enum
from dataclasses import dataclass, asdict

DATABASE_FILE = 'unified_writing_system.db'

class ProjectStatus(Enum):
    """حالات المشروع"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class WorkflowStatus(Enum):
    """حالات سير العمل"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskStatus(Enum):
    """حالة المهمة"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class CoreDatabase:
    """قاعدة البيانات الأساسية المحسنة"""
    
    def __init__(self, database_file: str = DATABASE_FILE):
        self.database_file = database_file
        self._init_database()
    
    def get_connection(self):
        """إنشاء اتصال جديد بقاعدة البيانات"""
        conn = sqlite3.connect(self.database_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        """تهيئة قاعدة البيانات الموحدة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # تفعيل المفاتيح الخارجية
        cursor.execute('PRAGMA foreign_keys = ON;')
        
        # === الجداول الأساسية ===
        self._create_core_tables(cursor)
        
        # === جداول الاندماج السردي الفائق ===
        self._create_fusion_tables(cursor)
        
        # === فهارس الأداء ===
        self._create_indexes(cursor)
        
        conn.commit()
        conn.close()
    
    def _create_core_tables(self, cursor):
        """إنشاء الجداول الأساسية المحسنة"""
        
        # === جدول المستخدمين والمصادقة ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT,
                role TEXT DEFAULT 'user',
                display_name TEXT,
                preferences TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # جدول جلسات المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                token_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL,
                last_activity TEXT DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول المشاريع المحسن ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'draft',
                genre TEXT,
                target_length TEXT,
                current_stage INTEGER DEFAULT 1,
                progress_percentage REAL DEFAULT 0.0,
                word_count INTEGER DEFAULT 0,
                chapter_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        # جدول بيانات المشروع المرنة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                data_key TEXT NOT NULL,
                data_value TEXT NOT NULL,
                data_type TEXT DEFAULT 'json',
                stage_number INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE,
                UNIQUE(project_id, data_key)
            )
        ''')
        
        # === جداول سير العمل المحسنة ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_templates (
                template_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                version TEXT DEFAULT '1.0',
                category TEXT DEFAULT 'user',
                template_data TEXT NOT NULL,
                created_by TEXT NOT NULL,
                is_public BOOLEAN DEFAULT FALSE,
                usage_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_executions (
                execution_id TEXT PRIMARY KEY,
                template_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                current_task_index INTEGER DEFAULT 0,
                progress_percentage REAL DEFAULT 0.0,
                context_data TEXT DEFAULT '{}',
                result_data TEXT,
                error_message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                started_at TEXT,
                completed_at TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (template_id) REFERENCES workflow_templates (template_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_tasks (
                task_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                name TEXT NOT NULL,
                task_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                task_order INTEGER NOT NULL,
                input_data TEXT DEFAULT '{}',
                output_data TEXT,
                dependencies TEXT DEFAULT '[]',
                error_message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                started_at TEXT,
                completed_at TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (execution_id) REFERENCES workflow_executions (execution_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول الوكلاء المبسط ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                agent_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                version TEXT DEFAULT '1.0',
                description TEXT,
                status TEXT DEFAULT 'active',
                capabilities TEXT DEFAULT '[]',
                configuration TEXT DEFAULT '{}',
                performance_stats TEXT DEFAULT '{}',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_interactions (
                interaction_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                user_id TEXT,
                project_id TEXT,
                task_type TEXT NOT NULL,
                input_data TEXT DEFAULT '{}',
                output_data TEXT DEFAULT '{}',
                execution_time REAL,
                status TEXT DEFAULT 'completed',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES agents (agent_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE SET NULL,
                FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE SET NULL
            )
        ''')
        
        # === جدول الشاهد المبسط ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS witness_sources (
                witness_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source_type TEXT DEFAULT 'text',
                file_path TEXT,
                analysis_data TEXT DEFAULT '{}',
                extracted_elements TEXT DEFAULT '{}',
                status TEXT DEFAULT 'uploaded',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                analyzed_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_witnesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                witness_id TEXT NOT NULL,
                integration_type TEXT DEFAULT 'reference',
                usage_notes TEXT,
                linked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE,
                FOREIGN KEY (witness_id) REFERENCES witness_sources (witness_id) ON DELETE CASCADE,
                UNIQUE(project_id, witness_id)
            )
        ''')
        
        # === جدول التحليلات المبسط ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT DEFAULT '{}',
                project_id TEXT,
                session_id TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE SET NULL
            )
        ''')
        
        # === جدول الإعدادات العامة ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL,
                setting_type TEXT DEFAULT 'string',
                description TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def _create_fusion_tables(self, cursor):
        """إنشاء جداول الاندماج السردي الفائق"""
        
        # === جدول مشاريع الاندماج ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fusion_projects (
                fusion_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                fusion_type TEXT NOT NULL, -- character_merge, plot_weave, style_blend, world_fusion
                status TEXT DEFAULT 'planning', -- planning, analyzing, synthesizing, reviewing, completed
                source_count INTEGER DEFAULT 0,
                target_length INTEGER,
                compatibility_score REAL,
                estimated_success_rate REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول مصادر الاندماج ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fusion_sources (
                source_id TEXT PRIMARY KEY,
                fusion_id TEXT NOT NULL,
                source_type TEXT NOT NULL, -- project, file, external
                source_reference TEXT NOT NULL, -- project_id or file_path
                source_title TEXT,
                narrative_identity TEXT, -- JSON للهوية السردية المستخرجة
                weight REAL DEFAULT 1.0, -- وزن المصدر في الدمج
                analysis_results TEXT, -- JSON لنتائج التحليل
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fusion_id) REFERENCES fusion_projects (fusion_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول قوالب الاندماج ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fusion_blueprints (
                blueprint_id TEXT PRIMARY KEY,
                fusion_id TEXT NOT NULL,
                blueprint_name TEXT NOT NULL,
                fusion_strategy TEXT NOT NULL, -- complete, gradual, selective
                source_weights TEXT NOT NULL, -- JSON للأوزان
                narrative_structure TEXT, -- JSON للبنية السردية
                character_mapping TEXT, -- JSON لخرائط الشخصيات
                plot_integration TEXT, -- JSON لتكامل الحبكة
                style_balance TEXT, -- JSON لتوازن الأسلوب
                quality_targets TEXT, -- JSON لأهداف الجودة
                fusion_parameters TEXT, -- JSON لمعاملات الدمج
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fusion_id) REFERENCES fusion_projects (fusion_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول عمليات التخليق ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS synthesis_sessions (
                session_id TEXT PRIMARY KEY,
                fusion_id TEXT NOT NULL,
                blueprint_id TEXT NOT NULL,
                status TEXT DEFAULT 'pending', -- pending, running, paused, completed, failed
                progress_percentage REAL DEFAULT 0.0,
                current_step TEXT,
                total_steps INTEGER DEFAULT 10,
                synthesized_content TEXT, -- المحتوى المُخلق
                synthesis_metadata TEXT DEFAULT '{}', -- بيانات وصفية للتخليق
                started_at TEXT,
                completed_at TEXT,
                error_log TEXT,
                FOREIGN KEY (fusion_id) REFERENCES fusion_projects (fusion_id) ON DELETE CASCADE,
                FOREIGN KEY (blueprint_id) REFERENCES fusion_blueprints (blueprint_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول تقييمات المحكم ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS arbitration_results (
                arbitration_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                fusion_id TEXT NOT NULL,
                quality_metrics TEXT NOT NULL, -- JSON لمقاييس الجودة
                detected_issues TEXT, -- JSON للمشاكل المكتشفة
                recommendations TEXT, -- JSON للتوصيات
                improvement_suggestions TEXT, -- JSON لاقتراحات التحسين
                approval_status TEXT NOT NULL, -- approved, needs_revision, major_revision
                confidence_level REAL NOT NULL,
                arbitrator_version TEXT DEFAULT '1.0.0',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES synthesis_sessions (session_id) ON DELETE CASCADE,
                FOREIGN KEY (fusion_id) REFERENCES fusion_projects (fusion_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول تاريخ النسخ ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS synthesis_versions (
                version_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                version_number INTEGER NOT NULL,
                content TEXT NOT NULL,
                quality_score REAL,
                changes_summary TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES synthesis_sessions (session_id) ON DELETE CASCADE
            )
        ''')
        
        # === جدول إحصائيات الاندماج ===
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fusion_analytics (
                analytics_id TEXT PRIMARY KEY,
                fusion_id TEXT NOT NULL,
                event_type TEXT NOT NULL, -- compatibility_assessment, synthesis_start, quality_check, etc.
                event_data TEXT, -- JSON للبيانات
                metrics TEXT, -- JSON للمقاييس
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fusion_id) REFERENCES fusion_projects (fusion_id) ON DELETE CASCADE
            )
        ''')
    
    def _create_indexes(self, cursor):
        """إنشاء الفهارس لتحسين الأداء"""
        indexes = [
            # فهارس المستخدمين
            'CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);',
            'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);',
            'CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);',
            'CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active);',
            
            # فهارس المشاريع
            'CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);',
            'CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);',
            'CREATE INDEX IF NOT EXISTS idx_projects_updated ON projects(updated_at);',
            'CREATE INDEX IF NOT EXISTS idx_project_data_project ON project_data(project_id);',
            'CREATE INDEX IF NOT EXISTS idx_project_data_key ON project_data(data_key);',
            
            # فهارس سير العمل
            'CREATE INDEX IF NOT EXISTS idx_workflows_user ON workflow_executions(user_id);',
            'CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflow_executions(status);',
            'CREATE INDEX IF NOT EXISTS idx_workflows_created ON workflow_executions(created_at);',
            'CREATE INDEX IF NOT EXISTS idx_tasks_execution ON workflow_tasks(execution_id);',
            'CREATE INDEX IF NOT EXISTS idx_tasks_status ON workflow_tasks(status);',
            
            # فهارس الوكلاء
            'CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(type);',
            'CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);',
            'CREATE INDEX IF NOT EXISTS idx_interactions_agent ON agent_interactions(agent_id);',
            'CREATE INDEX IF NOT EXISTS idx_interactions_user ON agent_interactions(user_id);',
            
            # فهارس الشاهد
            'CREATE INDEX IF NOT EXISTS idx_witness_user ON witness_sources(user_id);',
            'CREATE INDEX IF NOT EXISTS idx_witness_status ON witness_sources(status);',
            'CREATE INDEX IF NOT EXISTS idx_project_witnesses_project ON project_witnesses(project_id);',
            
            # فهارس التحليلات
            'CREATE INDEX IF NOT EXISTS idx_analytics_user ON user_analytics(user_id);',
            'CREATE INDEX IF NOT EXISTS idx_analytics_type ON user_analytics(event_type);',
            'CREATE INDEX IF NOT EXISTS idx_analytics_time ON user_analytics(timestamp);',
            
            # فهارس الاندماج السردي الفائق
            'CREATE INDEX IF NOT EXISTS idx_fusion_projects_user ON fusion_projects(user_id);',
            'CREATE INDEX IF NOT EXISTS idx_fusion_projects_status ON fusion_projects(status);',
            'CREATE INDEX IF NOT EXISTS idx_fusion_projects_type ON fusion_projects(fusion_type);',
            'CREATE INDEX IF NOT EXISTS idx_fusion_sources_fusion ON fusion_sources(fusion_id);',
            'CREATE INDEX IF NOT EXISTS idx_fusion_sources_type ON fusion_sources(source_type);',
            'CREATE INDEX IF NOT EXISTS idx_fusion_blueprints_fusion ON fusion_blueprints(fusion_id);',
            'CREATE INDEX IF NOT EXISTS idx_synthesis_sessions_fusion ON synthesis_sessions(fusion_id);',
            'CREATE INDEX IF NOT EXISTS idx_synthesis_sessions_status ON synthesis_sessions(status);',
            'CREATE INDEX IF NOT EXISTS idx_arbitration_fusion ON arbitration_results(fusion_id);',
            'CREATE INDEX IF NOT EXISTS idx_arbitration_approval ON arbitration_results(approval_status);',
            'CREATE INDEX IF NOT EXISTS idx_synthesis_versions_session ON synthesis_versions(session_id);',
            'CREATE INDEX IF NOT EXISTS idx_fusion_analytics_fusion ON fusion_analytics(fusion_id);',
            'CREATE INDEX IF NOT EXISTS idx_fusion_analytics_type ON fusion_analytics(event_type);'
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
    
    # === وظائف المستخدمين ===
    
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """إنشاء مستخدم جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        user_id = user_data.get('user_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO users (user_id, username, email, password_hash, role, display_name, preferences)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            user_data.get('username'),
            user_data.get('email'),
            user_data.get('password_hash'),
            user_data.get('role', 'user'),
            user_data.get('display_name'),
            json.dumps(user_data.get('preferences', {}))
        ))
        
        conn.commit()
        conn.close()
        return user_id
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            user_dict = dict(user)
            user_dict['preferences'] = json.loads(user_dict.get('preferences', '{}'))
            return user_dict
        return None
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """تحديث بيانات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clause = []
        values = []
        
        for key, value in update_data.items():
            if key in ['username', 'email', 'password_hash', 'role', 'display_name', 'last_login', 'is_active']:
                set_clause.append(f"{key} = ?")
                values.append(value)
            elif key == 'preferences':
                set_clause.append("preferences = ?")
                values.append(json.dumps(value))
        
        if not set_clause:
            conn.close()
            return False
        
        values.append(user_id)
        
        cursor.execute(f'''
            UPDATE users SET {', '.join(set_clause)} WHERE user_id = ?
        ''', values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # === وظائف الجلسات ===
    
    def create_session(self, session_data: Dict[str, Any]) -> str:
        """إنشاء جلسة جديدة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        session_id = session_data.get('session_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO user_sessions 
            (session_id, user_id, token_hash, expires_at, ip_address, user_agent, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            session_data['user_id'],
            session_data['token_hash'],
            session_data['expires_at'],
            session_data.get('ip_address'),
            session_data.get('user_agent'),
            json.dumps(session_data.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات الجلسة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.*, u.role FROM user_sessions s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.session_id = ? AND s.is_active = 1
        ''', (session_id,))
        
        session = cursor.fetchone()
        conn.close()
        
        if session:
            session_dict = dict(session)
            session_dict['metadata'] = json.loads(session_dict.get('metadata', '{}'))
            return session_dict
        return None
    
    def update_session_activity(self, session_id: str) -> bool:
        """تحديث نشاط الجلسة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions SET last_activity = CURRENT_TIMESTAMP
            WHERE session_id = ?
        ''', (session_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def deactivate_session(self, session_id: str) -> bool:
        """إلغاء تفعيل الجلسة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions SET is_active = 0 WHERE session_id = ?
        ''', (session_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # === وظائف المشاريع ===
    
    def create_project(self, project_data: Dict[str, Any]) -> str:
        """إنشاء مشروع جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        project_id = project_data.get('project_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO projects 
            (project_id, user_id, title, description, status, genre, target_length, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            project_data['user_id'],
            project_data['title'],
            project_data.get('description', ''),
            project_data.get('status', 'draft'),
            project_data.get('genre'),
            project_data.get('target_length'),
            json.dumps(project_data.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
        return project_id
    
    def get_project(self, project_id: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات المشروع"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT * FROM projects WHERE project_id = ? AND user_id = ?
            ''', (project_id, user_id))
        else:
            cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
        
        project = cursor.fetchone()
        
        if not project:
            conn.close()
            return None
        
        project_dict = dict(project)
        project_dict['metadata'] = json.loads(project_dict.get('metadata', '{}'))
        
        # الحصول على بيانات المشروع المرتبطة
        cursor.execute('''
            SELECT data_key, data_value, data_type, stage_number
            FROM project_data WHERE project_id = ?
        ''', (project_id,))
        
        project_data = cursor.fetchall()
        project_dict['data'] = {}
        
        for data_row in project_data:
            key = data_row['data_key']
            value = data_row['data_value']
            data_type = data_row['data_type']
            
            if data_type == 'json':
                try:
                    value = json.loads(value)
                except:
                    pass
            
            project_dict['data'][key] = {
                'value': value,
                'type': data_type,
                'stage': data_row['stage_number']
            }
        
        conn.close()
        return project_dict
    
    def update_project(self, project_id: str, update_data: Dict[str, Any], user_id: str = None) -> bool:
        """تحديث بيانات المشروع"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # تحديث الجدول الرئيسي
        main_fields = ['title', 'description', 'status', 'genre', 'target_length', 
                      'current_stage', 'progress_percentage', 'word_count', 'chapter_count']
        
        set_clause = ['updated_at = CURRENT_TIMESTAMP']
        values = []
        
        for field in main_fields:
            if field in update_data:
                set_clause.append(f"{field} = ?")
                values.append(update_data[field])
        
        if 'metadata' in update_data:
            set_clause.append("metadata = ?")
            values.append(json.dumps(update_data['metadata']))
        
        if set_clause:
            values.append(project_id)
            if user_id:
                values.append(user_id)
                where_clause = "project_id = ? AND user_id = ?"
            else:
                where_clause = "project_id = ?"
            
            cursor.execute(f'''
                UPDATE projects SET {', '.join(set_clause)} WHERE {where_clause}
            ''', values)
        
        # تحديث البيانات المرتبطة
        if 'data' in update_data:
            for key, value_info in update_data['data'].items():
                if isinstance(value_info, dict):
                    value = value_info.get('value')
                    data_type = value_info.get('type', 'json')
                    stage = value_info.get('stage')
                else:
                    value = value_info
                    data_type = 'json'
                    stage = None
                
                if data_type == 'json':
                    value = json.dumps(value)
                
                cursor.execute('''
                    INSERT OR REPLACE INTO project_data 
                    (project_id, data_key, data_value, data_type, stage_number, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (project_id, key, value, data_type, stage))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user_projects(self, user_id: str, status_filter: str = None) -> List[Dict[str, Any]]:
        """الحصول على مشاريع المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status_filter:
            cursor.execute('''
                SELECT * FROM projects WHERE user_id = ? AND status = ?
                ORDER BY updated_at DESC
            ''', (user_id, status_filter))
        else:
            cursor.execute('''
                SELECT * FROM projects WHERE user_id = ?
                ORDER BY updated_at DESC
            ''', (user_id,))
        
        projects = cursor.fetchall()
        conn.close()
        
        result = []
        for project in projects:
            project_dict = dict(project)
            project_dict['metadata'] = json.loads(project_dict.get('metadata', '{}'))
            result.append(project_dict)
        
        return result
    
    def delete_project(self, project_id: str, user_id: str) -> bool:
        """حذف مشروع"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM projects WHERE project_id = ? AND user_id = ?
        ''', (project_id, user_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # === وظائف سير العمل ===
    
    def save_workflow_template(self, template_data: Dict[str, Any]) -> str:
        """حفظ قالب سير عمل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        template_id = template_data.get('template_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT OR REPLACE INTO workflow_templates
            (template_id, name, description, version, category, template_data, created_by, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            template_id,
            template_data['name'],
            template_data.get('description', ''),
            template_data.get('version', '1.0'),
            template_data.get('category', 'user'),
            json.dumps(template_data.get('template_data', {})),
            template_data['created_by'],
            template_data.get('is_public', False)
        ))
        
        conn.commit()
        conn.close()
        return template_id
    
    def get_workflow_templates(self, user_id: str = None, category: str = None) -> List[Dict[str, Any]]:
        """الحصول على قوالب سير العمل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        where_conditions = []
        params = []
        
        if user_id:
            where_conditions.append("(is_public = 1 OR created_by = ?)")
            params.append(user_id)
        else:
            where_conditions.append("is_public = 1")
        
        if category:
            where_conditions.append("category = ?")
            params.append(category)
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        cursor.execute(f'''
            SELECT * FROM workflow_templates 
            WHERE {where_clause}
            ORDER BY usage_count DESC, created_at DESC
        ''', params)
        
        templates = cursor.fetchall()
        conn.close()
        
        result = []
        for template in templates:
            template_dict = dict(template)
            template_dict['template_data'] = json.loads(template_dict.get('template_data', '{}'))
            result.append(template_dict)
        
        return result
    
    def save_workflow_execution(self, execution_data: Dict[str, Any]) -> str:
        """حفظ تنفيذ سير عمل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        execution_id = execution_data.get('execution_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT OR REPLACE INTO workflow_executions
            (execution_id, template_id, user_id, name, status, current_task_index, 
             progress_percentage, context_data, result_data, error_message, 
             started_at, completed_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            execution_id,
            execution_data.get('template_id'),
            execution_data['user_id'],
            execution_data['name'],
            execution_data.get('status', 'pending'),
            execution_data.get('current_task_index', 0),
            execution_data.get('progress_percentage', 0.0),
            json.dumps(execution_data.get('context_data', {})),
            json.dumps(execution_data.get('result_data')) if execution_data.get('result_data') else None,
            execution_data.get('error_message'),
            execution_data.get('started_at'),
            execution_data.get('completed_at'),
            json.dumps(execution_data.get('metadata', {}))
        ))
        
        # حفظ المهام
        if 'tasks' in execution_data:
            for i, task in enumerate(execution_data['tasks']):
                cursor.execute('''
                    INSERT OR REPLACE INTO workflow_tasks
                    (task_id, execution_id, name, task_type, status, task_order,
                     input_data, output_data, dependencies, error_message,
                     started_at, completed_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    task.get('task_id', f"{execution_id}_task_{i}"),
                    execution_id,
                    task['name'],
                    task['task_type'],
                    task.get('status', 'pending'),
                    i,
                    json.dumps(task.get('input_data', {})),
                    json.dumps(task.get('output_data')) if task.get('output_data') else None,
                    json.dumps(task.get('dependencies', [])),
                    task.get('error_message'),
                    task.get('started_at'),
                    task.get('completed_at'),
                    json.dumps(task.get('metadata', {}))
                ))
        
        conn.commit()
        conn.close()
        return execution_id
    
    def get_workflow_execution(self, execution_id: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """الحصول على تنفيذ سير عمل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT * FROM workflow_executions 
                WHERE execution_id = ? AND user_id = ?
            ''', (execution_id, user_id))
        else:
            cursor.execute('''
                SELECT * FROM workflow_executions WHERE execution_id = ?
            ''', (execution_id,))
        
        execution = cursor.fetchone()
        
        if not execution:
            conn.close()
            return None
        
        execution_dict = dict(execution)
        execution_dict['context_data'] = json.loads(execution_dict.get('context_data', '{}'))
        execution_dict['metadata'] = json.loads(execution_dict.get('metadata', '{}'))
        
        if execution_dict.get('result_data'):
            execution_dict['result_data'] = json.loads(execution_dict['result_data'])
        
        # الحصول على المهام
        cursor.execute('''
            SELECT * FROM workflow_tasks 
            WHERE execution_id = ? ORDER BY task_order
        ''', (execution_id,))
        
        tasks = cursor.fetchall()
        execution_dict['tasks'] = []
        
        for task in tasks:
            task_dict = dict(task)
            task_dict['input_data'] = json.loads(task_dict.get('input_data', '{}'))
            task_dict['dependencies'] = json.loads(task_dict.get('dependencies', '[]'))
            task_dict['metadata'] = json.loads(task_dict.get('metadata', '{}'))
            
            if task_dict.get('output_data'):
                task_dict['output_data'] = json.loads(task_dict['output_data'])
            
            execution_dict['tasks'].append(task_dict)
        
        conn.close()
        return execution_dict
    
    def get_user_workflow_executions(self, user_id: str, status_filter: str = None) -> List[Dict[str, Any]]:
        """الحصول على تنفيذات سير العمل للمستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status_filter:
            cursor.execute('''
                SELECT execution_id, name, status, progress_percentage, created_at, started_at, completed_at
                FROM workflow_executions 
                WHERE user_id = ? AND status = ?
                ORDER BY created_at DESC
            ''', (user_id, status_filter))
        else:
            cursor.execute('''
                SELECT execution_id, name, status, progress_percentage, created_at, started_at, completed_at
                FROM workflow_executions 
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
        
        executions = cursor.fetchall()
        conn.close()
        
        return [dict(execution) for execution in executions]
    
    # === وظائف التحليلات ===
    
    def log_user_event(self, user_id: str, event_type: str, event_data: Dict[str, Any] = None, 
                      project_id: str = None, session_id: str = None) -> str:
        """تسجيل حدث المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        event_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO user_analytics 
            (user_id, event_type, event_data, project_id, session_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            event_type,
            json.dumps(event_data or {}),
            project_id,
            session_id
        ))
        
        conn.commit()
        conn.close()
        return event_id
    
    def get_user_analytics(self, user_id: str, event_type: str = None, 
                          days_back: int = 30) -> List[Dict[str, Any]]:
        """الحصول على تحليلات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if event_type:
            cursor.execute('''
                SELECT * FROM user_analytics 
                WHERE user_id = ? AND event_type = ?
                AND datetime(timestamp) >= datetime('now', '-{} days')
                ORDER BY timestamp DESC
            '''.format(days_back), (user_id, event_type))
        else:
            cursor.execute('''
                SELECT * FROM user_analytics 
                WHERE user_id = ?
                AND datetime(timestamp) >= datetime('now', '-{} days')
                ORDER BY timestamp DESC
            '''.format(days_back), (user_id,))
        
        events = cursor.fetchall()
        conn.close()
        
        result = []
        for event in events:
            event_dict = dict(event)
            event_dict['event_data'] = json.loads(event_dict.get('event_data', '{}'))
            result.append(event_dict)
        
        return result
    
    # === وظائف الشاهد ===
    
    def save_witness_source(self, witness_data: Dict[str, Any]) -> str:
        """حفظ مصدر شاهد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        witness_id = witness_data.get('witness_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT OR REPLACE INTO witness_sources
            (witness_id, user_id, title, content, source_type, file_path, 
             analysis_data, extracted_elements, status, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            witness_id,
            witness_data['user_id'],
            witness_data['title'],
            witness_data['content'],
            witness_data.get('source_type', 'text'),
            witness_data.get('file_path'),
            json.dumps(witness_data.get('analysis_data', {})),
            json.dumps(witness_data.get('extracted_elements', {})),
            witness_data.get('status', 'uploaded'),
            witness_data.get('analyzed_at')
        ))
        
        conn.commit()
        conn.close()
        return witness_id
    
    def get_witness_source(self, witness_id: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """الحصول على مصدر شاهد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT * FROM witness_sources WHERE witness_id = ? AND user_id = ?
            ''', (witness_id, user_id))
        else:
            cursor.execute('''
                SELECT * FROM witness_sources WHERE witness_id = ?
            ''', (witness_id,))
        
        witness = cursor.fetchone()
        conn.close()
        
        if witness:
            witness_dict = dict(witness)
            witness_dict['analysis_data'] = json.loads(witness_dict.get('analysis_data', '{}'))
            witness_dict['extracted_elements'] = json.loads(witness_dict.get('extracted_elements', '{}'))
            return witness_dict
        return None
    
    def get_user_witnesses(self, user_id: str) -> List[Dict[str, Any]]:
        """الحصول على مصادر الشاهد للمستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT witness_id, title, source_type, status, created_at, analyzed_at
            FROM witness_sources WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        witnesses = cursor.fetchall()
        conn.close()
        
        return [dict(witness) for witness in witnesses]
    
    def link_witness_to_project(self, project_id: str, witness_id: str, 
                               integration_type: str = 'reference', usage_notes: str = None) -> bool:
        """ربط شاهد بمشروع"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO project_witnesses
            (project_id, witness_id, integration_type, usage_notes)
            VALUES (?, ?, ?, ?)
        ''', (project_id, witness_id, integration_type, usage_notes))
        
        conn.commit()
        conn.close()
        return True
    
    def get_project_witnesses(self, project_id: str) -> List[Dict[str, Any]]:
        """الحصول على شهود المشروع"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pw.*, ws.title, ws.source_type, ws.status
            FROM project_witnesses pw
            JOIN witness_sources ws ON pw.witness_id = ws.witness_id
            WHERE pw.project_id = ?
            ORDER BY pw.linked_at DESC
        ''', (project_id,))
        
        witnesses = cursor.fetchall()
        conn.close()
        
        return [dict(witness) for witness in witnesses]
    
    # === وظائف النظام ===
    
    def set_system_setting(self, key: str, value: Any, setting_type: str = 'string', description: str = None):
        """تعيين إعداد النظام"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if setting_type == 'json':
            value = json.dumps(value)
        
        cursor.execute('''
            INSERT OR REPLACE INTO system_settings
            (setting_key, setting_value, setting_type, description, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (key, str(value), setting_type, description))
        
        conn.commit()
        conn.close()
    
    def get_system_setting(self, key: str, default=None):
        """الحصول على إعداد النظام"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT setting_value, setting_type FROM system_settings WHERE setting_key = ?
        ''', (key,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            value = result['setting_value']
            setting_type = result['setting_type']
            
            if setting_type == 'json':
                try:
                    return json.loads(value)
                except:
                    return default
            elif setting_type == 'int':
                try:
                    return int(value)
                except:
                    return default
            elif setting_type == 'float':
                try:
                    return float(value)
                except:
                    return default
            elif setting_type == 'bool':
                return value.lower() in ('true', '1', 'yes')
            else:
                return value
        
        return default
    
    # === وظائف الصيانة ===
    
    def cleanup_expired_sessions(self):
        """تنظيف الجلسات المنتهية الصلاحية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions SET is_active = 0 
            WHERE datetime(expires_at) < datetime('now')
        ''')
        
        cleaned_count = cursor.rowcount
        conn.commit()
        conn.close()
        return cleaned_count
    
    def get_database_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # إحصائيات الجداول
        tables = [
            'users', 'user_sessions', 'projects', 'project_data',
            'workflow_templates', 'workflow_executions', 'workflow_tasks',
            'agents', 'agent_interactions', 'witness_sources', 'project_witnesses',
            'user_analytics', 'system_settings'
        ]
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) as count FROM {table}')
            count = cursor.fetchone()['count']
            stats[f'{table}_count'] = count
        
        # حجم قاعدة البيانات
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        size_result = cursor.fetchone()
        stats['database_size_bytes'] = size_result['size'] if size_result else 0
        
        conn.close()
        return stats
    
    # === وظائف سير العمل إضافية ===
    
    def save_workflow_template(self, template):
        """حفظ كائن قالب سير العمل"""
        from dataclasses import asdict
        
        template_dict = asdict(template)
        template_dict['template_id'] = template.id
        template_dict['created_by'] = template.author_id
        template_dict['template_data'] = {
            'tasks': [asdict(task) for task in template.tasks],
            'metadata': template.metadata
        }
        
        return self.save_workflow_template(template_dict)
    
    def update_workflow_execution(self, execution):
        """تحديث كائن تنفيذ سير العمل"""
        from dataclasses import asdict
        
        execution_dict = asdict(execution)
        execution_dict['execution_id'] = execution.id
        execution_dict['template_id'] = execution.template_id
        execution_dict['status'] = execution.status.value if hasattr(execution.status, 'value') else execution.status
        execution_dict['tasks'] = [asdict(task) for task in execution.tasks]
        
        # تحويل التواريخ
        if execution.started_at:
            execution_dict['started_at'] = execution.started_at.isoformat()
        if execution.completed_at:
            execution_dict['completed_at'] = execution.completed_at.isoformat()
        
        return self.save_workflow_execution(execution_dict)
    
    def get_workflow_execution_status(self, execution_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على حالة تنفيذ سير عمل"""
        execution = self.get_workflow_execution(execution_id, user_id)
        if not execution:
            return None
        
        return {
            'id': execution['execution_id'],
            'name': execution['name'],
            'status': execution['status'],
            'progress_percentage': execution['progress_percentage'],
            'current_task_index': execution['current_task_index'],
            'total_tasks': len(execution.get('tasks', [])),
            'created_at': execution['created_at'],
            'started_at': execution.get('started_at'),
            'completed_at': execution.get('completed_at'),
            'error_message': execution.get('error_message')
        }
    
    def delete_workflow_template(self, template_id: str) -> bool:
        """حذف قالب سير عمل"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM workflow_templates WHERE template_id = ?', (template_id,))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
            
        except Exception as e:
            print(f"خطأ في حذف قالب سير العمل: {e}")
            return False
    
    # === وظائف الاندماج السردي الفائق ===
    
    def create_fusion_project(self, fusion_data: Dict[str, Any]) -> str:
        """إنشاء مشروع اندماج سردي جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fusion_id = fusion_data.get('fusion_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO fusion_projects 
            (fusion_id, user_id, title, description, fusion_type, target_length, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            fusion_id,
            fusion_data['user_id'],
            fusion_data['title'],
            fusion_data.get('description', ''),
            fusion_data['fusion_type'],
            fusion_data.get('target_length'),
            json.dumps(fusion_data.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
        return fusion_id
    
    def add_fusion_source(self, source_data: Dict[str, Any]) -> str:
        """إضافة مصدر لمشروع الاندماج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        source_id = source_data.get('source_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO fusion_sources 
            (source_id, fusion_id, source_type, source_reference, source_title, 
             narrative_identity, weight, analysis_results)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            source_id,
            source_data['fusion_id'],
            source_data['source_type'],
            source_data['source_reference'],
            source_data.get('source_title', ''),
            json.dumps(source_data.get('narrative_identity', {})),
            source_data.get('weight', 1.0),
            json.dumps(source_data.get('analysis_results', {}))
        ))
        
        # تحديث عدد المصادر في المشروع
        cursor.execute('''
            UPDATE fusion_projects 
            SET source_count = (
                SELECT COUNT(*) FROM fusion_sources WHERE fusion_id = ?
            ), updated_at = CURRENT_TIMESTAMP
            WHERE fusion_id = ?
        ''', (source_data['fusion_id'], source_data['fusion_id']))
        
        conn.commit()
        conn.close()
        return source_id
    
    def create_fusion_blueprint(self, blueprint_data: Dict[str, Any]) -> str:
        """إنشاء مخطط اندماج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        blueprint_id = blueprint_data.get('blueprint_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO fusion_blueprints 
            (blueprint_id, fusion_id, blueprint_name, fusion_strategy, source_weights,
             narrative_structure, character_mapping, plot_integration, style_balance,
             quality_targets, fusion_parameters)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            blueprint_id,
            blueprint_data['fusion_id'],
            blueprint_data['blueprint_name'],
            blueprint_data['fusion_strategy'],
            json.dumps(blueprint_data['source_weights']),
            json.dumps(blueprint_data.get('narrative_structure', {})),
            json.dumps(blueprint_data.get('character_mapping', {})),
            json.dumps(blueprint_data.get('plot_integration', {})),
            json.dumps(blueprint_data.get('style_balance', {})),
            json.dumps(blueprint_data.get('quality_targets', {})),
            json.dumps(blueprint_data.get('fusion_parameters', {}))
        ))
        
        conn.commit()
        conn.close()
        return blueprint_id
    
    def create_synthesis_session(self, session_data: Dict[str, Any]) -> str:
        """إنشاء جلسة تخليق"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        session_id = session_data.get('session_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO synthesis_sessions 
            (session_id, fusion_id, blueprint_id, total_steps, synthesis_metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            session_id,
            session_data['fusion_id'],
            session_data['blueprint_id'],
            session_data.get('total_steps', 10),
            json.dumps(session_data.get('synthesis_metadata', {}))
        ))
        
        conn.commit()
        conn.close()
        return session_id
    
    def update_synthesis_progress(self, session_id: str, progress_data: Dict[str, Any]) -> bool:
        """تحديث تقدم جلسة التخليق"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clause = []
        values = []
        
        if 'progress_percentage' in progress_data:
            set_clause.append('progress_percentage = ?')
            values.append(progress_data['progress_percentage'])
        
        if 'current_step' in progress_data:
            set_clause.append('current_step = ?')
            values.append(progress_data['current_step'])
        
        if 'status' in progress_data:
            set_clause.append('status = ?')
            values.append(progress_data['status'])
        
        if 'synthesized_content' in progress_data:
            set_clause.append('synthesized_content = ?')
            values.append(progress_data['synthesized_content'])
        
        if 'error_log' in progress_data:
            set_clause.append('error_log = ?')
            values.append(progress_data['error_log'])
        
        if progress_data.get('status') == 'completed':
            set_clause.append('completed_at = CURRENT_TIMESTAMP')
        elif progress_data.get('status') == 'running' and 'started_at' not in progress_data:
            set_clause.append('started_at = CURRENT_TIMESTAMP')
        
        if not set_clause:
            conn.close()
            return False
        
        values.append(session_id)
        
        cursor.execute(f'''
            UPDATE synthesis_sessions SET {', '.join(set_clause)} WHERE session_id = ?
        ''', values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def save_arbitration_result(self, arbitration_data: Dict[str, Any]) -> str:
        """حفظ نتيجة التحكيم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        arbitration_id = arbitration_data.get('arbitration_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO arbitration_results 
            (arbitration_id, session_id, fusion_id, quality_metrics, detected_issues,
             recommendations, improvement_suggestions, approval_status, confidence_level,
             arbitrator_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            arbitration_id,
            arbitration_data['session_id'],
            arbitration_data['fusion_id'],
            json.dumps(arbitration_data['quality_metrics']),
            json.dumps(arbitration_data.get('detected_issues', [])),
            json.dumps(arbitration_data.get('recommendations', [])),
            json.dumps(arbitration_data.get('improvement_suggestions', [])),
            arbitration_data['approval_status'],
            arbitration_data['confidence_level'],
            arbitration_data.get('arbitrator_version', '1.0.0')
        ))
        
        conn.commit()
        conn.close()
        return arbitration_id
    
    def save_synthesis_version(self, version_data: Dict[str, Any]) -> str:
        """حفظ إصدار من المحتوى المُخلق"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        version_id = version_data.get('version_id', str(uuid.uuid4()))
        
        # الحصول على رقم الإصدار التالي
        cursor.execute('''
            SELECT COALESCE(MAX(version_number), 0) + 1 
            FROM synthesis_versions WHERE session_id = ?
        ''', (version_data['session_id'],))
        
        next_version = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO synthesis_versions 
            (version_id, session_id, version_number, content, quality_score, changes_summary)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            version_id,
            version_data['session_id'],
            next_version,
            version_data['content'],
            version_data.get('quality_score'),
            version_data.get('changes_summary', '')
        ))
        
        conn.commit()
        conn.close()
        return version_id
    
    def log_fusion_analytics(self, analytics_data: Dict[str, Any]) -> str:
        """تسجيل أحداث التحليلات للاندماج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        analytics_id = analytics_data.get('analytics_id', str(uuid.uuid4()))
        
        cursor.execute('''
            INSERT INTO fusion_analytics 
            (analytics_id, fusion_id, event_type, event_data, metrics)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            analytics_id,
            analytics_data['fusion_id'],
            analytics_data['event_type'],
            json.dumps(analytics_data.get('event_data', {})),
            json.dumps(analytics_data.get('metrics', {}))
        ))
        
        conn.commit()
        conn.close()
        return analytics_id
    
    def get_fusion_project(self, fusion_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على مشروع اندماج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM fusion_projects WHERE fusion_id = ?
        ''', (fusion_id,))
        
        project = cursor.fetchone()
        conn.close()
        
        if project:
            project_dict = dict(project)
            project_dict['metadata'] = json.loads(project_dict.get('metadata', '{}'))
            return project_dict
        return None
    
    def get_fusion_sources(self, fusion_id: str) -> List[Dict[str, Any]]:
        """الحصول على مصادر مشروع الاندماج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM fusion_sources WHERE fusion_id = ? ORDER BY created_at
        ''', (fusion_id,))
        
        sources = cursor.fetchall()
        conn.close()
        
        source_list = []
        for source in sources:
            source_dict = dict(source)
            source_dict['narrative_identity'] = json.loads(source_dict.get('narrative_identity', '{}'))
            source_dict['analysis_results'] = json.loads(source_dict.get('analysis_results', '{}'))
            source_list.append(source_dict)
        
        return source_list
    
    def get_fusion_projects_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """الحصول على مشاريع الاندماج للمستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM fusion_projects 
            WHERE user_id = ? 
            ORDER BY updated_at DESC
        ''', (user_id,))
        
        projects = cursor.fetchall()
        conn.close()
        
        project_list = []
        for project in projects:
            project_dict = dict(project)
            project_dict['metadata'] = json.loads(project_dict.get('metadata', '{}'))
            project_list.append(project_dict)
        
        return project_list
    
    def get_synthesis_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على جلسة تخليق"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM synthesis_sessions WHERE session_id = ?
        ''', (session_id,))
        
        session = cursor.fetchone()
        conn.close()
        
        if session:
            session_dict = dict(session)
            session_dict['synthesis_metadata'] = json.loads(session_dict.get('synthesis_metadata', '{}'))
            return session_dict
        return None
    
    def get_latest_arbitration(self, fusion_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على آخر نتيجة تحكيم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM arbitration_results 
            WHERE fusion_id = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        ''', (fusion_id,))
        
        arbitration = cursor.fetchone()
        conn.close()
        
        if arbitration:
            arb_dict = dict(arbitration)
            arb_dict['quality_metrics'] = json.loads(arb_dict.get('quality_metrics', '{}'))
            arb_dict['detected_issues'] = json.loads(arb_dict.get('detected_issues', '[]'))
            arb_dict['recommendations'] = json.loads(arb_dict.get('recommendations', '[]'))
            arb_dict['improvement_suggestions'] = json.loads(arb_dict.get('improvement_suggestions', '[]'))
            return arb_dict
        return None
    
    def update_fusion_compatibility(self, fusion_id: str, compatibility_score: float, 
                                  success_rate: float) -> bool:
        """تحديث درجة التوافق والنجاح المتوقع"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE fusion_projects 
            SET compatibility_score = ?, estimated_success_rate = ?, updated_at = CURRENT_TIMESTAMP
            WHERE fusion_id = ?
        ''', (compatibility_score, success_rate, fusion_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_fusion_project(self, fusion_id: str) -> bool:
        """حذف مشروع اندماج (مع جميع البيانات المرتبطة)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # حذف المشروع (سيحذف البيانات المرتبطة تلقائياً بسبب CASCADE)
            cursor.execute('DELETE FROM fusion_projects WHERE fusion_id = ?', (fusion_id,))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
            
        except Exception as e:
            print(f"خطأ في حذف مشروع الاندماج: {e}")
            return False

# إنشاء المثيل الوحيد
core_db = CoreDatabase()
