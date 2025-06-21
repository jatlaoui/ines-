#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
وكيل التحكيم والتصحيح الذاتي المتقدم (AdvancedArbitrator)
==================================================

وكيل ذكي يقوم بتقييم عمل الوكلاء الآخرين، ومراجعة المخرجات وتصحيح الأخطاء،
وتوفير تغذية راجعة مستمرة لتحسين أداء النظام.

المميزات:
- تقييم النصوص ومخرجات الوكلاء بمقياس من 0-100%
- تحديد الأخطاء اللغوية والمنطقية والسردية
- تقديم اقتراحات تحسين محددة
- بناء حلقات تغذية راجعة بين الوكلاء
- تعلم التفضيلات وتحسين الجودة مع مرور الوقت
"""

import os
import json
import time
import logging
import numpy as np
from typing import Dict, List, Any, Tuple, Optional, Union
from datetime import datetime

# استيراد المكتبات الداخلية
from ..llm_service import get_llm_response
from ..database import get_db_connection
from ..agents.base_agent import BaseAgent

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/advanced_arbitrator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AdvancedArbitrator")

class AdvancedArbitrator:
    """
    وكيل التحكيم والتصحيح الذاتي المتقدم
    """
    
    def __init__(self, config: Dict = None):
        """
        تهيئة وكيل التحكيم المتقدم
        
        Args:
            config: إعدادات الوكيل (اختياري)
        """
        self.config = config or {}
        self.evaluation_history = []
        self.feedback_loops = {}
        self.quality_thresholds = {
            "excellent": 90,
            "good": 75,
            "acceptable": 60,
            "needs_improvement": 40,
            "poor": 20
        }
        self.evaluation_dimensions = {
            "language": 0.20,  # اللغة والأسلوب
            "structure": 0.20,  # البنية والتنظيم
            "creativity": 0.15,  # الإبداع والأفكار
            "coherence": 0.15,  # التماسك والترابط
            "relevance": 0.10,  # الصلة بالموضوع
            "engagement": 0.10,  # جذب القارئ
            "cultural": 0.10   # الملاءمة الثقافية
        }
        
        # تهيئة قاعدة البيانات
        self.db = get_db_connection()
        self._init_database()
        
        logger.info("تم تهيئة وكيل التحكيم المتقدم")
    
    def _init_database(self):
        """
        تهيئة جداول قاعدة البيانات اللازمة
        """
        cursor = self.db.cursor()
        
        # جدول تقييمات المحتوى
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id TEXT,
            agent_id TEXT,
            content_type TEXT,
            evaluation_score REAL,
            evaluation_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول التغذية الراجعة
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback_loops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_agent_id TEXT,
            target_agent_id TEXT,
            feedback_type TEXT,
            feedback_content TEXT,
            applied BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول مقاييس جودة الوكلاء
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_quality_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT,
            metric_name TEXT,
            metric_value REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.db.commit()
        logger.info("تم تهيئة جداول قاعدة البيانات لوكيل التحكيم")
    
    def evaluate_content(self, content: str, content_type: str, content_id: str = None, 
                         agent_id: str = None, detailed: bool = True) -> Dict:
        """
        تقييم محتوى نصي وإنشاء تقرير تقييم مفصل
        
        Args:
            content: النص المراد تقييمه
            content_type: نوع المحتوى (فكرة، فصل، مخطط، الخ)
            content_id: معرف المحتوى (اختياري)
            agent_id: معرف الوكيل المنتج للمحتوى (اختياري)
            detailed: إذا كان يجب إنشاء تقرير مفصل
            
        Returns:
            قاموس يحتوي على نتائج التقييم
        """
        logger.info(f"تقييم محتوى من النوع {content_type}")
        
        if not content or len(content.strip()) < 10:
            return {
                "score": 0,
                "status": "rejected",
                "message": "المحتوى فارغ أو قصير جداً",
                "details": {},
                "suggestions": ["يرجى تقديم محتوى أطول للتقييم"]
            }
        
        # استخدام نموذج اللغة لتقييم المحتوى
        prompt_template = self._get_evaluation_prompt(content, content_type)
        
        try:
            llm_response = get_llm_response(
                prompt_template,
                temperature=0.2,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            evaluation = json.loads(llm_response)
            
            # حساب الدرجة الكلية المرجحة
            total_score = 0
            for dimension, weight in self.evaluation_dimensions.items():
                if dimension in evaluation["scores"]:
                    total_score += evaluation["scores"][dimension] * weight
            
            evaluation["overall_score"] = round(total_score, 2)
            
            # تحديد حالة المحتوى بناءً على العتبات
            if evaluation["overall_score"] >= self.quality_thresholds["excellent"]:
                evaluation["status"] = "excellent"
            elif evaluation["overall_score"] >= self.quality_thresholds["good"]:
                evaluation["status"] = "good"
            elif evaluation["overall_score"] >= self.quality_thresholds["acceptable"]:
                evaluation["status"] = "acceptable"
            elif evaluation["overall_score"] >= self.quality_thresholds["needs_improvement"]:
                evaluation["status"] = "needs_improvement"
            else:
                evaluation["status"] = "poor"
            
            # تخزين التقييم في قاعدة البيانات
            if content_id:
                self._store_evaluation(content_id, agent_id, content_type, 
                                      evaluation["overall_score"], json.dumps(evaluation))
            
            # تسجيل نتيجة التقييم
            logger.info(f"تم تقييم المحتوى بدرجة {evaluation['overall_score']} والحالة {evaluation['status']}")
            
            return evaluation
            
        except Exception as e:
            logger.error(f"خطأ في تقييم المحتوى: {str(e)}")
            return {
                "score": 0,
                "status": "error",
                "message": f"حدث خطأ أثناء التقييم: {str(e)}",
                "details": {},
                "suggestions": ["يرجى المحاولة مرة أخرى"]
            }
    
    def correct_content(self, content: str, evaluation: Dict = None, 
                        content_type: str = "chapter", agent_id: str = None) -> Dict:
        """
        تصحيح المحتوى بناءً على التقييم
        
        Args:
            content: المحتوى الأصلي
            evaluation: نتائج التقييم (إذا كانت متوفرة)
            content_type: نوع المحتوى
            agent_id: معرف الوكيل الذي أنتج المحتوى
            
        Returns:
            قاموس يحتوي على المحتوى المصحح ومعلومات التصحيح
        """
        logger.info(f"تصحيح محتوى من النوع {content_type}")
        
        # إذا لم يتم تقديم تقييم، قم بتقييم المحتوى أولاً
        if not evaluation:
            evaluation = self.evaluate_content(content, content_type, agent_id=agent_id)
        
        # إذا كانت النتيجة ممتازة، لا داعي للتصحيح
        if evaluation["status"] == "excellent":
            return {
                "corrected_content": content,
                "original_content": content,
                "changes_made": False,
                "correction_notes": "المحتوى ممتاز ولا يحتاج إلى تصحيح",
                "evaluation": evaluation
            }
        
        # استخدام نموذج اللغة لتصحيح المحتوى
        prompt_template = self._get_correction_prompt(content, evaluation, content_type)
        
        try:
            llm_response = get_llm_response(
                prompt_template,
                temperature=0.3,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            correction = json.loads(llm_response)
            
            # تقييم المحتوى المصحح للتأكد من تحسنه
            if "corrected_content" in correction and len(correction["corrected_content"]) > 10:
                new_evaluation = self.evaluate_content(
                    correction["corrected_content"], 
                    content_type, 
                    agent_id=agent_id
                )
                
                # إضافة نتائج التقييم الجديد
                correction["new_evaluation"] = new_evaluation
                
                # إذا لم يتحسن التقييم، استخدام المحتوى الأصلي
                if new_evaluation["overall_score"] <= evaluation["overall_score"]:
                    correction["corrected_content"] = content
                    correction["changes_made"] = False
                    correction["correction_notes"] += "\nلم يتم تحسين المحتوى بشكل كافٍ، تم استخدام النسخة الأصلية."
            
            # تسجيل عملية التصحيح
            logger.info(f"تم تصحيح المحتوى من النوع {content_type}")
            
            return correction
            
        except Exception as e:
            logger.error(f"خطأ في تصحيح المحتوى: {str(e)}")
            return {
                "corrected_content": content,
                "original_content": content,
                "changes_made": False,
                "correction_notes": f"حدث خطأ أثناء التصحيح: {str(e)}",
                "evaluation": evaluation
            }
    
    def create_feedback_loop(self, source_agent_id: str, target_agent_id: str, 
                            content_id: str, feedback_type: str, feedback: Dict) -> Dict:
        """
        إنشاء حلقة تغذية راجعة بين وكيلين
        
        Args:
            source_agent_id: معرف الوكيل مصدر التغذية الراجعة
            target_agent_id: معرف الوكيل هدف التغذية الراجعة
            content_id: معرف المحتوى
            feedback_type: نوع التغذية الراجعة (تحسين، تصحيح، اقتراح)
            feedback: محتوى التغذية الراجعة
            
        Returns:
            قاموس يحتوي على معلومات التغذية الراجعة
        """
        logger.info(f"إنشاء حلقة تغذية راجعة من {source_agent_id} إلى {target_agent_id}")
        
        # تخزين التغذية الراجعة في قاعدة البيانات
        feedback_id = self._store_feedback(
            source_agent_id, 
            target_agent_id, 
            feedback_type, 
            json.dumps(feedback)
        )
        
        # إضافة إلى حلقات التغذية الراجعة في الذاكرة
        loop_key = f"{source_agent_id}_{target_agent_id}"
        if loop_key not in self.feedback_loops:
            self.feedback_loops[loop_key] = []
        
        self.feedback_loops[loop_key].append({
            "id": feedback_id,
            "content_id": content_id,
            "feedback_type": feedback_type,
            "feedback": feedback,
            "created_at": datetime.now().isoformat()
        })
        
        return {
            "id": feedback_id,
            "source_agent_id": source_agent_id,
            "target_agent_id": target_agent_id,
            "content_id": content_id,
            "feedback_type": feedback_type,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
    
    def get_agent_quality_metrics(self, agent_id: str, period: str = "all") -> Dict:
        """
        الحصول على مقاييس جودة الوكيل
        
        Args:
            agent_id: معرف الوكيل
            period: الفترة الزمنية للمقاييس (all, month, week, day)
            
        Returns:
            قاموس يحتوي على مقاييس الجودة
        """
        logger.info(f"الحصول على مقاييس جودة الوكيل {agent_id}")
        
        cursor = self.db.cursor()
        
        # تحديد شرط الفترة الزمنية
        time_condition = ""
        if period == "day":
            time_condition = "AND created_at >= datetime('now', '-1 day')"
        elif period == "week":
            time_condition = "AND created_at >= datetime('now', '-7 days')"
        elif period == "month":
            time_condition = "AND created_at >= datetime('now', '-30 days')"
        
        # استعلام مقاييس جودة الوكيل
        cursor.execute(f"""
        SELECT metric_name, AVG(metric_value) as avg_value
        FROM agent_quality_metrics
        WHERE agent_id = ? {time_condition}
        GROUP BY metric_name
        """, (agent_id,))
        
        metrics = {}
        for row in cursor.fetchall():
            metrics[row[0]] = row[1]
        
        # استعلام متوسط نتائج التقييم
        cursor.execute(f"""
        SELECT AVG(evaluation_score) as avg_score
        FROM content_evaluations
        WHERE agent_id = ? {time_condition}
        """, (agent_id,))
        
        avg_score = cursor.fetchone()
        if avg_score and avg_score[0]:
            metrics["average_evaluation_score"] = avg_score[0]
        else:
            metrics["average_evaluation_score"] = 0
        
        # استعلام عدد التقييمات
        cursor.execute(f"""
        SELECT COUNT(*) as eval_count
        FROM content_evaluations
        WHERE agent_id = ? {time_condition}
        """, (agent_id,))
        
        eval_count = cursor.fetchone()
        if eval_count:
            metrics["evaluation_count"] = eval_count[0]
        else:
            metrics["evaluation_count"] = 0
        
        # تصنيف جودة الوكيل
        if metrics["average_evaluation_score"] >= self.quality_thresholds["excellent"]:
            metrics["quality_tier"] = "excellent"
        elif metrics["average_evaluation_score"] >= self.quality_thresholds["good"]:
            metrics["quality_tier"] = "good"
        elif metrics["average_evaluation_score"] >= self.quality_thresholds["acceptable"]:
            metrics["quality_tier"] = "acceptable"
        elif metrics["average_evaluation_score"] >= self.quality_thresholds["needs_improvement"]:
            metrics["quality_tier"] = "needs_improvement"
        else:
            metrics["quality_tier"] = "poor"
        
        return {
            "agent_id": agent_id,
            "period": period,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    
    def update_agent_quality_metric(self, agent_id: str, metric_name: str, metric_value: float) -> bool:
        """
        تحديث مقياس جودة الوكيل
        
        Args:
            agent_id: معرف الوكيل
            metric_name: اسم المقياس
            metric_value: قيمة المقياس
            
        Returns:
            نجاح العملية
        """
        logger.info(f"تحديث مقياس جودة الوكيل {agent_id}: {metric_name} = {metric_value}")
        
        try:
            cursor = self.db.cursor()
            cursor.execute("""
            INSERT INTO agent_quality_metrics (agent_id, metric_name, metric_value)
            VALUES (?, ?, ?)
            """, (agent_id, metric_name, metric_value))
            
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"خطأ في تحديث مقياس جودة الوكيل: {str(e)}")
            return False
    
    def get_agent_improvement_suggestions(self, agent_id: str, content_type: str = None) -> Dict:
        """
        الحصول على اقتراحات لتحسين أداء الوكيل
        
        Args:
            agent_id: معرف الوكيل
            content_type: نوع المحتوى (اختياري)
            
        Returns:
            قاموس يحتوي على اقتراحات التحسين
        """
        logger.info(f"إنشاء اقتراحات تحسين للوكيل {agent_id}")
        
        # الحصول على مقاييس جودة الوكيل
        metrics = self.get_agent_quality_metrics(agent_id)
        
        # الحصول على التقييمات السابقة
        cursor = self.db.cursor()
        
        content_type_condition = ""
        if content_type:
            content_type_condition = f"AND content_type = '{content_type}'"
        
        cursor.execute(f"""
        SELECT evaluation_details
        FROM content_evaluations
        WHERE agent_id = ? {content_type_condition}
        ORDER BY created_at DESC
        LIMIT 10
        """, (agent_id,))
        
        evaluations = []
        for row in cursor.fetchall():
            try:
                eval_data = json.loads(row[0])
                evaluations.append(eval_data)
            except:
                pass
        
        # استخدام نموذج اللغة لإنشاء اقتراحات التحسين
        prompt = f"""
        أنت مستشار تطوير ذكي للوكلاء الاصطناعيين. مهمتك هي تحليل أداء الوكيل وتقديم اقتراحات محددة لتحسين جودة عمله.
        
        معلومات الوكيل:
        - معرف الوكيل: {agent_id}
        - متوسط درجة التقييم: {metrics['metrics'].get('average_evaluation_score', 0):.2f}
        - مستوى الجودة: {metrics['metrics'].get('quality_tier', 'غير معروف')}
        
        التقييمات السابقة:
        {json.dumps(evaluations, ensure_ascii=False, indent=2)}
        
        قم بتحليل نقاط القوة والضعف للوكيل بناءً على التقييمات السابقة، ثم قدم:
        1. قائمة بأهم 3-5 نقاط قوة يجب الحفاظ عليها
        2. قائمة بأهم 3-5 مجالات تحتاج إلى تحسين
        3. اقتراحات محددة وقابلة للتنفيذ لتحسين أداء الوكيل
        4. استراتيجية عامة لتطوير الوكيل على المدى الطويل
        
        أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
        - strengths: قائمة بنقاط القوة
        - improvement_areas: قائمة بمجالات التحسين
        - specific_suggestions: قائمة باقتراحات محددة
        - long_term_strategy: استراتيجية طويلة المدى
        - priority_focus: المجال ذو الأولوية القصوى للتحسين
        """
        
        try:
            llm_response = get_llm_response(
                prompt,
                temperature=0.4,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            suggestions = json.loads(llm_response)
            
            # إضافة معلومات إضافية
            suggestions["agent_id"] = agent_id
            suggestions["metrics"] = metrics["metrics"]
            suggestions["timestamp"] = datetime.now().isoformat()
            
            logger.info(f"تم إنشاء اقتراحات تحسين للوكيل {agent_id}")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء اقتراحات التحسين: {str(e)}")
            return {
                "agent_id": agent_id,
                "error": str(e),
                "strengths": [],
                "improvement_areas": ["لم يتم التمكن من تحليل الأداء بسبب خطأ"],
                "specific_suggestions": ["حاول مرة أخرى لاحقاً"],
                "long_term_strategy": "غير متوفر",
                "priority_focus": "غير متوفر"
            }
    
    def judge_agent_dialogue(self, dialogue: List[Dict], context: Dict = None) -> Dict:
        """
        تقييم حوار بين الوكلاء وتحديد الوكيل الأفضل أداءً
        
        Args:
            dialogue: قائمة برسائل الحوار
            context: سياق الحوار (اختياري)
            
        Returns:
            قاموس يحتوي على نتائج التقييم
        """
        logger.info("تقييم حوار بين الوكلاء")
        
        if not dialogue or len(dialogue) < 2:
            return {
                "status": "error",
                "message": "الحوار قصير جداً للتقييم",
                "best_agent": None,
                "scores": {},
                "reasoning": "لا يوجد حوار كافٍ للتقييم"
            }
        
        # تحضير سياق الحوار
        context_str = ""
        if context:
            context_str = f"""
            سياق الحوار:
            موضوع: {context.get('topic', 'غير محدد')}
            الهدف: {context.get('goal', 'غير محدد')}
            القيود: {context.get('constraints', 'لا توجد قيود')}
            """
        
        # تنسيق الحوار
        dialogue_str = ""
        participating_agents = set()
        
        for i, message in enumerate(dialogue):
            agent_id = message.get("agent_id", "غير معروف")
            content = message.get("content", "")
            participating_agents.add(agent_id)
            
            dialogue_str += f"{agent_id}: {content}\n\n"
        
        # استخدام نموذج اللغة لتقييم الحوار
        prompt = f"""
        أنت قاضٍ محايد ومتخصص في تقييم جودة الحوارات بين الوكلاء الاصطناعيين. مهمتك هي تحليل الحوار وتحديد الوكيل الأفضل أداءً.
        
        {context_str}
        
        الحوار:
        {dialogue_str}
        
        قم بتقييم مساهمة كل وكيل في الحوار بناءً على المعايير التالية:
        1. جودة المحتوى (0-100): مدى دقة وصحة المعلومات المقدمة
        2. الإبداع (0-100): الأفكار المبتكرة والحلول الإبداعية
        3. التعاون (0-100): مدى المساهمة في تقدم الحوار وبناء على أفكار الآخرين
        4. المنطق (0-100): ترابط الأفكار وتسلسلها المنطقي
        5. فائدة المساهمة (0-100): القيمة العملية والفائدة من المساهمات
        
        بناءً على هذه المعايير، حدد الوكيل الأفضل أداءً وشرح سبب اختيارك.
        
        أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
        - scores: قاموس يحتوي على درجات كل وكيل في كل معيار
        - overall_scores: قاموس يحتوي على الدرجة الإجمالية لكل وكيل
        - best_agent: معرف الوكيل الأفضل أداءً
        - reasoning: شرح سبب اختيار الوكيل الأفضل
        - improvement_suggestions: اقتراحات لتحسين الحوار بشكل عام
        """
        
        try:
            llm_response = get_llm_response(
                prompt,
                temperature=0.2,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            judgment = json.loads(llm_response)
            
            # إضافة معلومات إضافية
            judgment["participating_agents"] = list(participating_agents)
            judgment["message_count"] = len(dialogue)
            judgment["timestamp"] = datetime.now().isoformat()
            
            # تسجيل نتيجة التقييم
            best_agent = judgment.get("best_agent", "غير محدد")
            logger.info(f"تم تقييم الحوار، الوكيل الأفضل: {best_agent}")
            
            return judgment
            
        except Exception as e:
            logger.error(f"خطأ في تقييم الحوار: {str(e)}")
            return {
                "status": "error",
                "message": f"حدث خطأ أثناء التقييم: {str(e)}",
                "best_agent": None,
                "scores": {},
                "reasoning": "حدث خطأ أثناء التقييم"
            }
    
    def _get_evaluation_prompt(self, content: str, content_type: str) -> str:
        """
        إنشاء موجه لتقييم المحتوى
        
        Args:
            content: المحتوى المراد تقييمه
            content_type: نوع المحتوى
            
        Returns:
            موجه التقييم
        """
        prompt_templates = {
            "idea": """
            أنت ناقد أدبي محترف ومتخصص في تقييم الأفكار الأدبية. قم بتقييم الفكرة التالية بموضوعية ودقة.
            
            الفكرة:
            {content}
            
            قم بتقييم الفكرة على مقياس من 0 إلى 100 في المجالات التالية:
            - أصالة الفكرة وإبداعها
            - إمكانية تطويرها إلى عمل أدبي كامل
            - جاذبيتها للقراء
            - قيمتها الأدبية والثقافية
            - وضوح الرؤية والمفهوم
            
            قم أيضاً بتحديد:
            1. نقاط القوة الرئيسية (3 على الأقل)
            2. نقاط الضعف والتحديات (3 على الأقل)
            3. اقتراحات محددة للتحسين (3-5 اقتراحات)
            4. تقييم عام للفكرة في فقرة موجزة
            
            أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
            - scores: قاموس يحتوي على درجات كل مجال
            - strengths: قائمة بنقاط القوة
            - weaknesses: قائمة بنقاط الضعف
            - suggestions: قائمة بالاقتراحات
            - summary: التقييم العام
            """,
            
            "chapter": """
            أنت محرر أدبي محترف ومتخصص في تقييم فصول الروايات. قم بتقييم الفصل التالي بموضوعية ودقة.
            
            الفصل:
            {content}
            
            قم بتقييم الفصل على مقياس من 0 إلى 100 في المجالات التالية:
            - اللغة والأسلوب: جودة الكتابة، الصور البلاغية، تنوع الأسلوب
            - بناء الشخصيات: عمق الشخصيات وتطورها وتفاعلها
            - الحبكة والتشويق: ترابط الأحداث، المنطق، عناصر التشويق
            - الحوار: طبيعية الحوار، تميز أصوات الشخصيات، فعالية الحوار
            - البيئة والوصف: حيوية الوصف، خلق صور ذهنية واضحة
            - التماسك مع القصة: ترابط الفصل مع السياق العام للرواية
            - التأثير العاطفي: قدرة الفصل على إثارة مشاعر القارئ
            
            قم أيضاً بتحديد:
            1. المقاطع الأقوى في الفصل
            2. المقاطع التي تحتاج إلى مراجعة
            3. اقتراحات محددة للتحسين (5-7 اقتراحات)
            4. تقييم عام للفصل في فقرة موجزة
            
            أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
            - scores: قاموس يحتوي على درجات كل مجال
            - best_parts: قائمة بالمقاطع الأقوى
            - parts_to_revise: قائمة بالمقاطع التي تحتاج إلى مراجعة
            - suggestions: قائمة بالاقتراحات
            - summary: التقييم العام
            """,
            
            "blueprint": """
            أنت مستشار أدبي محترف ومتخصص في تقييم مخططات الروايات. قم بتقييم المخطط التالي بموضوعية ودقة.
            
            المخطط:
            {content}
            
            قم بتقييم المخطط على مقياس من 0 إلى 100 في المجالات التالية:
            - بنية القصة: ترابط الأحداث، التسلسل المنطقي، تماسك البنية
            - تطور الشخصيات: خطط نمو الشخصيات وتحولاتها
            - القوس الدرامي: بناء التوتر والتصاعد والذروة والحل
            - الأصالة والإبداع: تميز المخطط وابتكاريته
            - قابلية التنفيذ: إمكانية تحويل المخطط إلى رواية متكاملة
            - التماسك الداخلي: اتساق عناصر المخطط مع بعضها
            - الجاذبية: قدرة المخطط على جذب اهتمام القراء
            
            قم أيضاً بتحديد:
            1. نقاط القوة في المخطط
            2. الثغرات والتحديات المحتملة
            3. اقتراحات محددة للتحسين (5-7 اقتراحات)
            4. تقييم عام للمخطط في فقرة موجزة
            
            أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
            - scores: قاموس يحتوي على درجات كل مجال
            - strengths: قائمة بنقاط القوة
            - gaps: قائمة بالثغرات والتحديات
            - suggestions: قائمة بالاقتراحات
            - summary: التقييم العام
            """,
            
            "character": """
            أنت مستشار أدبي محترف ومتخصص في تقييم تطوير الشخصيات الروائية. قم بتقييم وصف الشخصية التالي بموضوعية ودقة.
            
            وصف الشخصية:
            {content}
            
            قم بتقييم الشخصية على مقياس من 0 إلى 100 في المجالات التالية:
            - العمق النفسي: تعقيد وعمق البناء النفسي للشخصية
            - الاتساق الداخلي: اتساق سمات وأفعال ودوافع الشخصية
            - التميز والفرادة: تميز الشخصية عن غيرها من الشخصيات النمطية
            - الإقناع: قابلية الشخصية للتصديق ضمن سياق القصة
            - إمكانات التطور: قدرة الشخصية على النمو والتغير
            - الأبعاد المتعددة: تعدد جوانب الشخصية وتناقضاتها
            - الجاذبية: قدرة الشخصية على جذب اهتمام القراء
            
            قم أيضاً بتحديد:
            1. السمات الأكثر إقناعاً في الشخصية
            2. الجوانب غير المطورة بشكل كاف
            3. اقتراحات محددة لتعميق الشخصية (5-7 اقتراحات)
            4. تقييم عام للشخصية في فقرة موجزة
            
            أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
            - scores: قاموس يحتوي على درجات كل مجال
            - convincing_traits: قائمة بالسمات الأكثر إقناعاً
            - underdeveloped_aspects: قائمة بالجوانب غير المطورة بشكل كاف
            - suggestions: قائمة بالاقتراحات
            - summary: التقييم العام
            """
        }
        
        # استخدام القالب المناسب أو قالب عام إذا لم يكن النوع موجوداً
        template = prompt_templates.get(content_type, """
        أنت ناقد أدبي محترف ومتخصص في تقييم المحتوى الأدبي. قم بتقييم المحتوى التالي بموضوعية ودقة.
        
        المحتوى:
        {content}
        
        قم بتقييم المحتوى على مقياس من 0 إلى 100 في المجالات التالية:
        - اللغة والأسلوب
        - البنية والتنظيم
        - الإبداع والابتكار
        - التماسك والترابط
        - الصلة بالموضوع
        - جذب اهتمام القارئ
        - الملاءمة الثقافية
        
        قم أيضاً بتحديد:
        1. نقاط القوة الرئيسية (3 على الأقل)
        2. نقاط الضعف (3 على الأقل)
        3. اقتراحات محددة للتحسين (3-5 اقتراحات)
        4. تقييم عام للمحتوى في فقرة موجزة
        
        أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
        - scores: قاموس يحتوي على درجات كل مجال
        - strengths: قائمة بنقاط القوة
        - weaknesses: قائمة بنقاط الضعف
        - suggestions: قائمة بالاقتراحات
        - summary: التقييم العام
        """)
        
        return template.format(content=content)
    
    def _get_correction_prompt(self, content: str, evaluation: Dict, content_type: str) -> str:
        """
        إنشاء موجه لتصحيح المحتوى
        
        Args:
            content: المحتوى المراد تصحيحه
            evaluation: نتائج التقييم
            content_type: نوع المحتوى
            
        Returns:
            موجه التصحيح
        """
        # إعداد ملخص التقييم
        evaluation_summary = json.dumps(evaluation, ensure_ascii=False, indent=2)
        
        prompt = f"""
        أنت محرر أدبي محترف ومتخصص في تحسين وتصحيح المحتوى الأدبي. مهمتك هي تحسين المحتوى بناءً على التقييم المقدم.
        
        المحتوى الأصلي ({content_type}):
        ```
        {content}
        ```
        
        تقييم المحتوى:
        ```
        {evaluation_summary}
        ```
        
        قم بتحسين المحتوى مع مراعاة:
        1. تصحيح أي أخطاء لغوية أو أسلوبية
        2. تحسين نقاط الضعف المذكورة في التقييم
        3. تطبيق الاقتراحات المقدمة في التقييم
        4. الحفاظ على نقاط القوة والهوية الأصلية للمحتوى
        5. الحفاظ على طول المحتوى مماثلاً للأصل ما لم يكن هناك سبب وجيه للتغيير
        
        أعد الإجابة بتنسيق JSON يحتوي على الحقول التالية:
        - corrected_content: المحتوى المصحح كاملاً
        - original_content: المحتوى الأصلي
        - changes_made: قائمة بالتغييرات الرئيسية التي تم إجراؤها
        - correction_notes: ملاحظات توضح سبب التغييرات
        - improvement_focus: المجالات التي تم التركيز عليها في التحسين
        """
        
        return prompt
    
    def _store_evaluation(self, content_id: str, agent_id: str, content_type: str, 
                         evaluation_score: float, evaluation_details: str) -> int:
        """
        تخزين نتائج التقييم في قاعدة البيانات
        
        Args:
            content_id: معرف المحتوى
            agent_id: معرف الوكيل
            content_type: نوع المحتوى
            evaluation_score: درجة التقييم
            evaluation_details: تفاصيل التقييم
            
        Returns:
            معرف التقييم
        """
        cursor = self.db.cursor()
        
        cursor.execute("""
        INSERT INTO content_evaluations 
        (content_id, agent_id, content_type, evaluation_score, evaluation_details)
        VALUES (?, ?, ?, ?, ?)
        """, (content_id, agent_id, content_type, evaluation_score, evaluation_details))
        
        self.db.commit()
        
        return cursor.lastrowid
    
    def _store_feedback(self, source_agent_id: str, target_agent_id: str, 
                       feedback_type: str, feedback_content: str) -> int:
        """
        تخزين التغذية الراجعة في قاعدة البيانات
        
        Args:
            source_agent_id: معرف الوكيل المصدر
            target_agent_id: معرف الوكيل الهدف
            feedback_type: نوع التغذية الراجعة
            feedback_content: محتوى التغذية الراجعة
            
        Returns:
            معرف التغذية الراجعة
        """
        cursor = self.db.cursor()
        
        cursor.execute("""
        INSERT INTO feedback_loops 
        (source_agent_id, target_agent_id, feedback_type, feedback_content)
        VALUES (?, ?, ?, ?)
        """, (source_agent_id, target_agent_id, feedback_type, feedback_content))
        
        self.db.commit()
        
        return cursor.lastrowid


# تهيئة وكيل التحكيم المتقدم عند استيراد الوحدة
arbitrator = AdvancedArbitrator()

def get_arbitrator():
    """
    الحصول على نسخة من وكيل التحكيم المتقدم
    
    Returns:
        وكيل التحكيم المتقدم
    """
    return arbitrator


# وظائف مساعدة للاستخدام المباشر

def evaluate_content(content: str, content_type: str, content_id: str = None, agent_id: str = None) -> Dict:
    """
    تقييم محتوى نصي وإنشاء تقرير تقييم مفصل
    
    Args:
        content: النص المراد تقييمه
        content_type: نوع المحتوى (فكرة، فصل، مخطط، الخ)
        content_id: معرف المحتوى (اختياري)
        agent_id: معرف الوكيل المنتج للمحتوى (اختياري)
        
    Returns:
        قاموس يحتوي على نتائج التقييم
    """
    return arbitrator.evaluate_content(content, content_type, content_id, agent_id)

def correct_content(content: str, evaluation: Dict = None, content_type: str = "chapter", agent_id: str = None) -> Dict:
    """
    تصحيح المحتوى بناءً على التقييم
    
    Args:
        content: المحتوى الأصلي
        evaluation: نتائج التقييم (إذا كانت متوفرة)
        content_type: نوع المحتوى
        agent_id: معرف الوكيل الذي أنتج المحتوى
        
    Returns:
        قاموس يحتوي على المحتوى المصحح ومعلومات التصحيح
    """
    return arbitrator.correct_content(content, evaluation, content_type, agent_id)

def judge_agent_dialogue(dialogue: List[Dict], context: Dict = None) -> Dict:
    """
    تقييم حوار بين الوكلاء وتحديد الوكيل الأفضل أداءً
    
    Args:
        dialogue: قائمة برسائل الحوار
        context: سياق الحوار (اختياري)
        
    Returns:
        قاموس يحتوي على نتائج التقييم
    """
    return arbitrator.judge_agent_dialogue(dialogue, context)


if __name__ == "__main__":
    # اختبار الوكيل
    print("اختبار وكيل التحكيم والتصحيح الذاتي المتقدم")
    
    # اختبار تقييم محتوى
    test_content = """
    كان ياما كان في قديم الزمان، عاش صبي صغير يدعى سلطان في قرية نائية بين الجبال. كان سلطان يحلم دائماً بأن يصبح حكيماً مشهوراً يقصده الناس للاستشارة والعلاج. 
    في يوم من الأيام، سمع سلطان عن حكيم عجوز يسكن في كهف على قمة أعلى جبل في المنطقة. قرر سلطان أن يذهب إليه ليتعلم منه أسرار الحكمة والمعرفة.
    """
    
    evaluation = evaluate_content(test_content, "chapter", "test_chapter_1", "test_agent_1")
    print("نتائج التقييم:", evaluation)
    
    # اختبار تصحيح المحتوى
    correction = correct_content(test_content, evaluation, "chapter", "test_agent_1")
    print("المحتوى المصحح:", correction["corrected_content"])
    
    # اختبار تقييم حوار بين الوكلاء
    test_dialogue = [
        {"agent_id": "agent_1", "content": "أعتقد أن الشخصية الرئيسية يجب أن تواجه تحدياً أكبر في بداية القصة."},
        {"agent_id": "agent_2", "content": "أنا أختلف معك. بداية القصة يجب أن تكون هادئة لتعريف القارئ بالشخصيات والبيئة."},
        {"agent_id": "agent_1", "content": "ولكن القارئ سيفقد الاهتمام إذا لم تبدأ القصة بشكل مثير."},
        {"agent_id": "agent_3", "content": "يمكننا الجمع بين الأمرين بتقديم الشخصية في موقف طبيعي ثم تصعيد التوتر تدريجياً."}
    ]
    
    judgment = judge_agent_dialogue(test_dialogue, {"topic": "بناء بداية القصة", "goal": "تحديد أفضل بداية للقصة"})
    print("نتائج تقييم الحوار:", judgment)