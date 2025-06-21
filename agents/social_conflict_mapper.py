"""
مخطط الصراعات الاجتماعية
Social Conflict Mapper - Professional tool for realistic social dynamics analysis

أداة متخصصة لبناء صراعات اجتماعية معقدة وواقعية:
- تحليل الطبقات الاجتماعية ونقاط التوتر
- تطوير ديناميكيات الصراع عبر الزمن
- تأثير الصراعات على الشخصيات الفردية
- خرائط بصرية للتوترات الاجتماعية
"""

import asyncio
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import networkx as nx

class SocialClass(Enum):
    """الطبقات الاجتماعية"""
    UPPER_ELITE = "upper_elite"  # النخبة العليا
    UPPER_MIDDLE = "upper_middle"  # الطبقة العليا الوسطى
    MIDDLE = "middle"  # الطبقة الوسطى
    LOWER_MIDDLE = "lower_middle"  # الطبقة الدنيا الوسطى
    WORKING = "working"  # الطبقة العاملة
    POOR = "poor"  # الفقراء
    MARGINALIZED = "marginalized"  # المهمشون

class ConflictType(Enum):
    """أنواع الصراعات الاجتماعية"""
    CLASS_STRUGGLE = "class_struggle"  # صراع طبقي
    ETHNIC_TENSION = "ethnic_tension"  # توتر عرقي
    RELIGIOUS_CONFLICT = "religious_conflict"  # صراع ديني
    GENERATIONAL = "generational"  # صراع الأجيال
    GENDER_ISSUES = "gender_issues"  # قضايا جندرية
    ECONOMIC_DISPARITY = "economic_disparity"  # تفاوت اقتصادي
    POLITICAL_DIVIDE = "political_divide"  # انقسام سياسي
    CULTURAL_CLASH = "cultural_clash"  # صدام ثقافي

class ConflictIntensity(Enum):
    """شدة الصراع"""
    LOW = "low"  # منخفض
    MODERATE = "moderate"  # متوسط
    HIGH = "high"  # عالي
    CRITICAL = "critical"  # حرج

@dataclass
class SocialGroup:
    """مجموعة اجتماعية"""
    id: str
    name: str
    social_class: SocialClass
    size: int
    characteristics: List[str]
    interests: List[str]
    power_level: float
    resources: List[str]
    alliances: List[str]
    enemies: List[str]

@dataclass
class ConflictNode:
    """عقدة صراع"""
    id: str
    conflict_type: ConflictType
    description: str
    involved_groups: List[str]
    intensity: ConflictIntensity
    causes: List[str]
    consequences: List[str]
    timeline: List[Dict[str, Any]]
    resolution_potential: float

@dataclass
class SocialTension:
    """توتر اجتماعي"""
    source_group: str
    target_group: str
    tension_level: float
    causes: List[str]
    manifestations: List[str]
    escalation_triggers: List[str]

class SocialConflictMapper:
    """مخطط الصراعات الاجتماعية المتقدم"""
    
    def __init__(self):
        self.social_hierarchy = self._load_social_hierarchy()
        self.conflict_patterns = self._load_conflict_patterns()
        self.historical_conflicts = self._load_historical_conflicts()
        self.resolution_strategies = self._load_resolution_strategies()
        self.network_graph = nx.Graph()
    
    def get_name(self) -> str:
        return "مخطط الصراعات الاجتماعية"
    
    def get_description(self) -> str:
        return "أداة متخصصة لتحليل وتخطيط الديناميكيات والصراعات الاجتماعية المعقدة"
    
    def get_features(self) -> List[str]:
        return [
            "تحليل الطبقات الاجتماعية",
            "تخطيط الصراعات والتوترات",
            "تتبع تطور الصراعات",
            "تحليل شبكة العلاقات",
            "اقتراح حلول واقعية"
        ]
    
    def get_supported_formats(self) -> List[str]:
        return ["text", "network", "timeline", "social_map"]
    
    def get_output_types(self) -> List[str]:
        return ["analysis", "conflict_map", "tension_graph", "recommendations"]
    
    async def analyze(self, content: str, context: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
        """التحليل الشامل للصراعات الاجتماعية"""
        try:
            # تحليل المجموعات الاجتماعية
            social_groups = await self._identify_social_groups(content)
            
            # تحديد الصراعات الموجودة
            conflicts = await self._identify_conflicts(content, social_groups)
            
            # تحليل التوترات الاجتماعية
            tensions = await self._analyze_social_tensions(content, social_groups)
            
            # بناء شبكة العلاقات الاجتماعية
            social_network = await self._build_social_network(social_groups, tensions, conflicts)
            
            # تحليل ديناميكيات القوة
            power_dynamics = await self._analyze_power_dynamics(social_groups, conflicts)
            
            # تطوير سيناريوهات التصعيد
            escalation_scenarios = await self._develop_escalation_scenarios(conflicts, tensions)
            
            # اقتراح استراتيجيات الحل
            resolution_strategies = await self._suggest_resolution_strategies(conflicts, social_groups)
            
            # إنتاج التوصيات
            recommendations = await self._generate_conflict_recommendations(
                social_groups, conflicts, tensions, power_dynamics
            )
            
            # حساب درجة الثقة
            confidence_score = self._calculate_confidence_score(
                social_groups, conflicts, tensions
            )
            
            # إنشاء البيانات المرئية
            visual_data = await self._generate_visual_data(
                social_groups, conflicts, tensions, social_network
            )
            
            return {
                "analysis": {
                    "social_groups_count": len(social_groups),
                    "conflicts_identified": len(conflicts),
                    "tension_points": len(tensions),
                    "network_complexity": len(social_network.get("nodes", [])),
                    "overall_stability": self._assess_social_stability(conflicts, tensions)
                },
                "social_groups": [self._group_to_dict(group) for group in social_groups],
                "conflicts": [self._conflict_to_dict(conflict) for conflict in conflicts],
                "social_tensions": [self._tension_to_dict(tension) for tension in tensions],
                "power_dynamics": power_dynamics,
                "escalation_scenarios": escalation_scenarios,
                "resolution_strategies": resolution_strategies,
                "recommendations": recommendations,
                "confidence_score": confidence_score,
                "visual_data": visual_data,
                "metadata": {
                    "analysis_type": "social_conflict",
                    "processing_time": datetime.now().isoformat(),
                    "network_metrics": self._calculate_network_metrics(social_network)
                }
            }
            
        except Exception as e:
            raise Exception(f"خطأ في تحليل الصراعات الاجتماعية: {str(e)}")
    
    async def _identify_social_groups(self, content: str) -> List[SocialGroup]:
        """تحديد المجموعات الاجتماعية"""
        groups = []
        
        # مؤشرات الطبقات الاجتماعية
        class_indicators = {
            SocialClass.UPPER_ELITE: [
                "الأثرياء", "النخبة", "الأرستقراطية", "الملوك", "الأمراء",
                "رجال الأعمال الكبار", "المليونيرات"
            ],
            SocialClass.UPPER_MIDDLE: [
                "المديرون", "الأطباء", "المهندسون", "المحامون",
                "الأكاديميون", "الطبقة المتعلمة"
            ],
            SocialClass.MIDDLE: [
                "الموظفون", "التجار", "أصحاب المهن",
                "الطبقة الوسطى", "المدرسون"
            ],
            SocialClass.WORKING: [
                "العمال", "الصناع", "السائقون", "البناءون",
                "الفلاحون", "الطبقة العاملة"
            ],
            SocialClass.POOR: [
                "الفقراء", "المحتاجون", "البسطاء", "ذوو الدخل المحدود"
            ],
            SocialClass.MARGINALIZED: [
                "المهمشون", "اللاجئون", "المشردون", "الأقليات"
            ]
        }
        
        group_id = 1
        for social_class, keywords in class_indicators.items():
            for keyword in keywords:
                if keyword in content:
                    group = SocialGroup(
                        id=f"G{group_id:03d}",
                        name=keyword,
                        social_class=social_class,
                        size=100,  # تقدير افتراضي
                        characteristics=self._get_class_characteristics(social_class),
                        interests=self._get_class_interests(social_class),
                        power_level=self._get_class_power_level(social_class),
                        resources=self._get_class_resources(social_class),
                        alliances=[],
                        enemies=[]
                    )
                    groups.append(group)
                    group_id += 1
                    break  # تجنب التكرار لنفس الطبقة
        
        return groups
    
    async def _identify_conflicts(self, content: str, social_groups: List[SocialGroup]) -> List[ConflictNode]:
        """تحديد الصراعات الاجتماعية"""
        conflicts = []
        
        # مؤشرات أنواع الصراعات
        conflict_indicators = {
            ConflictType.CLASS_STRUGGLE: [
                "صراع طبقي", "ثورة", "انتفاضة", "احتجاج",
                "عدالة اجتماعية", "تفاوت في الثروة"
            ],
            ConflictType.ETHNIC_TENSION: [
                "توتر عرقي", "صراع قبلي", "تمييز عنصري",
                "أقلية", "تنوع عرقي"
            ],
            ConflictType.RELIGIOUS_CONFLICT: [
                "صراع ديني", "طائفية", "تعصب", "اضطهاد ديني"
            ],
            ConflictType.GENERATIONAL: [
                "صراع الأجيال", "جيل الآباء", "الشباب والكبار",
                "تقاليد ضد الحداثة"
            ],
            ConflictType.GENDER_ISSUES: [
                "حقوق المرأة", "تمييز جندري", "مساواة",
                "دور المرأة", "العنف ضد المرأة"
            ]
        }
        
        conflict_id = 1
        for conflict_type, keywords in conflict_indicators.items():
            for keyword in keywords:
                if keyword in content:
                    conflict = ConflictNode(
                        id=f"C{conflict_id:03d}",
                        conflict_type=conflict_type,
                        description=keyword,
                        involved_groups=[group.id for group in social_groups[:2]],
                        intensity=ConflictIntensity.MODERATE,
                        causes=self._get_conflict_causes(conflict_type),
                        consequences=self._get_conflict_consequences(conflict_type),
                        timeline=self._generate_conflict_timeline(conflict_type),
                        resolution_potential=0.6
                    )
                    conflicts.append(conflict)
                    conflict_id += 1
                    break
        
        return conflicts
    
    async def _analyze_social_tensions(self, content: str, social_groups: List[SocialGroup]) -> List[SocialTension]:
        """تحليل التوترات الاجتماعية"""
        tensions = []
        
        # إنشاء توترات بين الطبقات المختلفة
        for i, group1 in enumerate(social_groups):
            for group2 in social_groups[i+1:]:
                if self._groups_have_tension(group1, group2):
                    tension = SocialTension(
                        source_group=group1.id,
                        target_group=group2.id,
                        tension_level=self._calculate_tension_level(group1, group2),
                        causes=self._identify_tension_causes(group1, group2),
                        manifestations=self._get_tension_manifestations(group1, group2),
                        escalation_triggers=self._get_escalation_triggers(group1, group2)
                    )
                    tensions.append(tension)
        
        return tensions
    
    async def _build_social_network(self, groups: List[SocialGroup], tensions: List[SocialTension], 
                                   conflicts: List[ConflictNode]) -> Dict[str, Any]:
        """بناء شبكة العلاقات الاجتماعية"""
        self.network_graph.clear()
        
        # إضافة العقد (المجموعات)
        for group in groups:
            self.network_graph.add_node(
                group.id,
                name=group.name,
                social_class=group.social_class.value,
                power_level=group.power_level,
                size=group.size
            )
        
        # إضافة الحواف (التوترات والصراعات)
        for tension in tensions:
            self.network_graph.add_edge(
                tension.source_group,
                tension.target_group,
                weight=tension.tension_level,
                type="tension"
            )
        
        for conflict in conflicts:
            for i, group1 in enumerate(conflict.involved_groups):
                for group2 in conflict.involved_groups[i+1:]:
                    self.network_graph.add_edge(
                        group1,
                        group2,
                        weight=self._intensity_to_weight(conflict.intensity),
                        type="conflict",
                        conflict_type=conflict.conflict_type.value
                    )
        
        # تحويل إلى تنسيق قابل للإرجاع
        return {
            "nodes": [
                {
                    "id": node,
                    **self.network_graph.nodes[node]
                }
                for node in self.network_graph.nodes()
            ],
            "edges": [
                {
                    "source": edge[0],
                    "target": edge[1],
                    **self.network_graph.edges[edge]
                }
                for edge in self.network_graph.edges()
            ]
        }
    
    async def _analyze_power_dynamics(self, groups: List[SocialGroup], conflicts: List[ConflictNode]) -> Dict[str, Any]:
        """تحليل ديناميكيات القوة"""
        power_analysis = {
            "power_distribution": {},
            "power_imbalances": [],
            "coalition_potential": [],
            "power_shifts": []
        }
        
        # توزيع القوة
        total_power = sum(group.power_level for group in groups)
        for group in groups:
            power_analysis["power_distribution"][group.name] = {
                "absolute_power": group.power_level,
                "relative_power": group.power_level / total_power if total_power > 0 else 0,
                "power_sources": group.resources
            }
        
        # عدم التوازن في القوة
        sorted_groups = sorted(groups, key=lambda x: x.power_level, reverse=True)
        if len(sorted_groups) >= 2:
            power_gap = sorted_groups[0].power_level - sorted_groups[-1].power_level
            if power_gap > 0.5:
                power_analysis["power_imbalances"].append({
                    "description": f"فجوة قوة كبيرة بين {sorted_groups[0].name} و {sorted_groups[-1].name}",
                    "gap_size": power_gap
                })
        
        # إمكانية التحالفات
        for i, group1 in enumerate(groups):
            for group2 in groups[i+1:]:
                if self._can_form_coalition(group1, group2):
                    power_analysis["coalition_potential"].append({
                        "groups": [group1.name, group2.name],
                        "combined_power": group1.power_level + group2.power_level,
                        "likelihood": 0.7
                    })
        
        return power_analysis
    
    async def _develop_escalation_scenarios(self, conflicts: List[ConflictNode], tensions: List[SocialTension]) -> List[Dict[str, Any]]:
        """تطوير سيناريوهات التصعيد"""
        scenarios = []
        
        for conflict in conflicts:
            scenario = {
                "conflict_id": conflict.id,
                "escalation_stages": [
                    {
                        "stage": 1,
                        "description": "توتر أولي ومطالب محدودة",
                        "probability": 0.8,
                        "consequences": ["احتجاجات سلمية", "مطالب علنية"]
                    },
                    {
                        "stage": 2,
                        "description": "تصعيد الخطاب وزيادة الضغط",
                        "probability": 0.6,
                        "consequences": ["مظاهرات أكبر", "تدخل إعلامي"]
                    },
                    {
                        "stage": 3,
                        "description": "مواجهات مباشرة وعنف محدود",
                        "probability": 0.3,
                        "consequences": ["اشتباكات", "تدخل الأمن"]
                    }
                ],
                "triggers": [
                    "حدث استفزازي",
                    "قرار حكومي مثير للجدل",
                    "أزمة اقتصادية"
                ]
            }
            scenarios.append(scenario)
        
        return scenarios
    
    async def _suggest_resolution_strategies(self, conflicts: List[ConflictNode], groups: List[SocialGroup]) -> List[Dict[str, Any]]:
        """اقتراح استراتيجيات الحل"""
        strategies = []
        
        for conflict in conflicts:
            strategy = {
                "conflict_id": conflict.id,
                "conflict_type": conflict.conflict_type.value,
                "resolution_approaches": [],
                "success_probability": conflict.resolution_potential,
                "timeline": "6-12 شهر",
                "required_resources": []
            }
            
            if conflict.conflict_type == ConflictType.CLASS_STRUGGLE:
                strategy["resolution_approaches"] = [
                    "إصلاحات اقتصادية",
                    "برامج العدالة الاجتماعية",
                    "الحوار بين الطبقات"
                ]
            elif conflict.conflict_type == ConflictType.ETHNIC_TENSION:
                strategy["resolution_approaches"] = [
                    "تعزيز التنوع الثقافي",
                    "قوانين مكافحة التمييز",
                    "برامج التبادل الثقافي"
                ]
            elif conflict.conflict_type == ConflictType.RELIGIOUS_CONFLICT:
                strategy["resolution_approaches"] = [
                    "الحوار بين الأديان",
                    "تعزيز التسامح",
                    "حماية الحقوق الدينية"
                ]
            
            strategies.append(strategy)
        
        return strategies
    
    async def _generate_conflict_recommendations(self, groups: List[SocialGroup], conflicts: List[ConflictNode],
                                               tensions: List[SocialTension], power_dynamics: Dict[str, Any]) -> List[str]:
        """إنتاج توصيات لتطوير الصراعات"""
        recommendations = []
        
        # توصيات للتطوير الواقعي للصراعات
        if len(conflicts) == 0:
            recommendations.append("إضافة صراعات اجتماعية لزيادة التعقيد والواقعية")
        
        if len(groups) < 3:
            recommendations.append("تطوير المزيد من المجموعات الاجتماعية لإثراء الديناميكيات")
        
        # توصيات للتوازن
        power_imbalances = len(power_dynamics.get("power_imbalances", []))
        if power_imbalances > 2:
            recommendations.append("توازن ديناميكيات القوة لتجنب التطرف في الصراع")
        
        # توصيات للواقعية
        recommendations.extend([
            "ربط الصراعات بالسياق التاريخي والاجتماعي",
            "تطوير شخصيات من خلفيات اجتماعية متنوعة",
            "إظهار تأثير الصراعات على الحياة اليومية للشخصيات"
        ])
        
        return recommendations[:5]
    
    def _groups_have_tension(self, group1: SocialGroup, group2: SocialGroup) -> bool:
        """تحديد ما إذا كان هناك توتر بين مجموعتين"""
        # الطبقات المتباعدة لها توتر أكبر
        class_hierarchy = [
            SocialClass.MARGINALIZED,
            SocialClass.POOR,
            SocialClass.WORKING,
            SocialClass.LOWER_MIDDLE,
            SocialClass.MIDDLE,
            SocialClass.UPPER_MIDDLE,
            SocialClass.UPPER_ELITE
        ]
        
        try:
            index1 = class_hierarchy.index(group1.social_class)
            index2 = class_hierarchy.index(group2.social_class)
            distance = abs(index1 - index2)
            return distance >= 2  # توتر إذا كانت المسافة الطبقية كبيرة
        except ValueError:
            return True  # افتراض وجود توتر إذا لم نتمكن من تحديد المسافة
    
    def _calculate_tension_level(self, group1: SocialGroup, group2: SocialGroup) -> float:
        """حساب مستوى التوتر بين مجموعتين"""
        power_difference = abs(group1.power_level - group2.power_level)
        base_tension = min(power_difference, 0.8)
        
        # زيادة التوتر إذا كانت المصالح متضاربة
        conflicting_interests = len(set(group1.interests).intersection(set(group2.interests)))
        if conflicting_interests == 0:
            base_tension += 0.2
        
        return min(1.0, base_tension)
    
    def _identify_tension_causes(self, group1: SocialGroup, group2: SocialGroup) -> List[str]:
        """تحديد أسباب التوتر بين المجموعات"""
        causes = []
        
        if group1.power_level > group2.power_level + 0.3:
            causes.append("عدم توازن في القوة")
        
        if not set(group1.interests).intersection(set(group2.interests)):
            causes.append("تضارب في المصالح")
        
        causes.extend([
            "تنافس على الموارد المحدودة",
            "اختلاف في القيم والثقافة",
            "تاريخ من الصراعات"
        ])
        
        return causes[:3]
    
    def _get_tension_manifestations(self, group1: SocialGroup, group2: SocialGroup) -> List[str]:
        """مظاهر التوتر بين المجموعات"""
        return [
            "تصريحات عدائية",
            "تجنب التعامل المباشر",
            "التحيز في التعاملات",
            "الشائعات والأقاويل"
        ]
    
    def _get_escalation_triggers(self, group1: SocialGroup, group2: SocialGroup) -> List[str]:
        """محفزات تصعيد التوتر"""
        return [
            "حادثة مثيرة للجدل",
            "قرار يؤثر على إحدى المجموعات",
            "أزمة اقتصادية",
            "تدخل خارجي"
        ]
    
    def _assess_social_stability(self, conflicts: List[ConflictNode], tensions: List[SocialTension]) -> float:
        """تقييم الاستقرار الاجتماعي العام"""
        base_stability = 1.0
        
        # تقليل الاستقرار بناءً على عدد وشدة الصراعات
        for conflict in conflicts:
            if conflict.intensity == ConflictIntensity.CRITICAL:
                base_stability -= 0.3
            elif conflict.intensity == ConflictIntensity.HIGH:
                base_stability -= 0.2
            elif conflict.intensity == ConflictIntensity.MODERATE:
                base_stability -= 0.1
        
        # تقليل الاستقرار بناءً على مستوى التوترات
        high_tension_count = sum(1 for tension in tensions if tension.tension_level > 0.7)
        base_stability -= high_tension_count * 0.1
        
        return max(0.0, min(1.0, base_stability))
    
    def _can_form_coalition(self, group1: SocialGroup, group2: SocialGroup) -> bool:
        """تحديد إمكانية تشكيل تحالف بين مجموعتين"""
        # المجموعات ذات المصالح المشتركة والقوة المتقاربة يمكنها التحالف
        power_difference = abs(group1.power_level - group2.power_level)
        shared_interests = len(set(group1.interests).intersection(set(group2.interests)))
        
        return power_difference < 0.4 and shared_interests > 0
    
    def _intensity_to_weight(self, intensity: ConflictIntensity) -> float:
        """تحويل شدة الصراع إلى وزن في الشبكة"""
        weights = {
            ConflictIntensity.LOW: 0.2,
            ConflictIntensity.MODERATE: 0.5,
            ConflictIntensity.HIGH: 0.8,
            ConflictIntensity.CRITICAL: 1.0
        }
        return weights.get(intensity, 0.5)
    
    def _calculate_network_metrics(self, network: Dict[str, Any]) -> Dict[str, Any]:
        """حساب مقاييس الشبكة"""
        if not network.get("nodes"):
            return {}
        
        try:
            return {
                "node_count": len(network["nodes"]),
                "edge_count": len(network["edges"]),
                "density": len(network["edges"]) / (len(network["nodes"]) * (len(network["nodes"]) - 1) / 2) if len(network["nodes"]) > 1 else 0,
                "connectivity": "متصلة" if len(network["edges"]) > 0 else "منفصلة"
            }
        except:
            return {"error": "خطأ في حساب مقاييس الشبكة"}
    
    def _calculate_confidence_score(self, groups: List[SocialGroup], conflicts: List[ConflictNode], tensions: List[SocialTension]) -> float:
        """حساب درجة الثقة في التحليل"""
        base_score = 0.7
        
        # زيادة الثقة بناءً على عدد المجموعات المحددة
        groups_bonus = min(0.2, len(groups) * 0.05)
        
        # زيادة الثقة بناءً على وجود صراعات وتوترات
        conflicts_bonus = min(0.1, len(conflicts) * 0.03)
        tensions_bonus = min(0.1, len(tensions) * 0.02)
        
        final_score = base_score + groups_bonus + conflicts_bonus + tensions_bonus
        return round(max(0.0, min(1.0, final_score)), 2)
    
    async def _generate_visual_data(self, groups: List[SocialGroup], conflicts: List[ConflictNode],
                                   tensions: List[SocialTension], network: Dict[str, Any]) -> Dict[str, Any]:
        """إنتاج البيانات المرئية للتحليل"""
        return {
            "social_hierarchy": {
                "type": "hierarchy",
                "data": [
                    {
                        "class": group.social_class.value,
                        "name": group.name,
                        "power": group.power_level,
                        "size": group.size
                    }
                    for group in groups
                ]
            },
            "conflict_network": {
                "type": "network",
                "nodes": network.get("nodes", []),
                "edges": network.get("edges", [])
            },
            "tension_heatmap": {
                "type": "heatmap",
                "data": [
                    {
                        "source": tension.source_group,
                        "target": tension.target_group,
                        "intensity": tension.tension_level
                    }
                    for tension in tensions
                ]
            },
            "stability_gauge": {
                "type": "gauge",
                "value": self._assess_social_stability(conflicts, tensions) * 100,
                "max": 100
            }
        }
    
    def _group_to_dict(self, group: SocialGroup) -> Dict[str, Any]:
        """تحويل المجموعة الاجتماعية إلى قاموس"""
        return {
            "id": group.id,
            "name": group.name,
            "social_class": group.social_class.value,
            "size": group.size,
            "characteristics": group.characteristics,
            "interests": group.interests,
            "power_level": group.power_level,
            "resources": group.resources,
            "alliances": group.alliances,
            "enemies": group.enemies
        }
    
    def _conflict_to_dict(self, conflict: ConflictNode) -> Dict[str, Any]:
        """تحويل الصراع إلى قاموس"""
        return {
            "id": conflict.id,
            "conflict_type": conflict.conflict_type.value,
            "description": conflict.description,
            "involved_groups": conflict.involved_groups,
            "intensity": conflict.intensity.value,
            "causes": conflict.causes,
            "consequences": conflict.consequences,
            "timeline": conflict.timeline,
            "resolution_potential": conflict.resolution_potential
        }
    
    def _tension_to_dict(self, tension: SocialTension) -> Dict[str, Any]:
        """تحويل التوتر إلى قاموس"""
        return {
            "source_group": tension.source_group,
            "target_group": tension.target_group,
            "tension_level": tension.tension_level,
            "causes": tension.causes,
            "manifestations": tension.manifestations,
            "escalation_triggers": tension.escalation_triggers
        }
    
    def _get_class_characteristics(self, social_class: SocialClass) -> List[str]:
        """خصائص الطبقة الاجتماعية"""
        characteristics_map = {
            SocialClass.UPPER_ELITE: ["متعلمة", "نافذة", "متصلة عالمياً", "محافظة على المصالح"],
            SocialClass.UPPER_MIDDLE: ["متعلمة", "طموحة", "مهنية", "تقدر الجودة"],
            SocialClass.MIDDLE: ["متوسطة التعليم", "مستقرة نسبياً", "تسعى للتقدم"],
            SocialClass.WORKING: ["عملية", "تكافح اقتصادياً", "متضامنة"],
            SocialClass.POOR: ["محدودة الموارد", "تبحث عن البقاء", "معتمدة على المساعدة"],
            SocialClass.MARGINALIZED: ["مهمشة", "تعاني التمييز", "محرومة من الخدمات"]
        }
        return characteristics_map.get(social_class, [])
    
    def _get_class_interests(self, social_class: SocialClass) -> List[str]:
        """مصالح الطبقة الاجتماعية"""
        interests_map = {
            SocialClass.UPPER_ELITE: ["الحفاظ على الثروة", "النفوذ السياسي", "الاستثمارات"],
            SocialClass.UPPER_MIDDLE: ["التقدم المهني", "التعليم العالي", "الاستقرار الاقتصادي"],
            SocialClass.MIDDLE: ["الأمان الوظيفي", "تحسين المعيشة", "تعليم الأطفال"],
            SocialClass.WORKING: ["الأجور العادلة", "ظروف العمل", "الضمان الاجتماعي"],
            SocialClass.POOR: ["الحاجات الأساسية", "الرعاية الصحية", "السكن"],
            SocialClass.MARGINALIZED: ["الاعتراف", "الحماية", "الخدمات الأساسية"]
        }
        return interests_map.get(social_class, [])
    
    def _get_class_power_level(self, social_class: SocialClass) -> float:
        """مستوى قوة الطبقة الاجتماعية"""
        power_levels = {
            SocialClass.UPPER_ELITE: 0.9,
            SocialClass.UPPER_MIDDLE: 0.7,
            SocialClass.MIDDLE: 0.5,
            SocialClass.LOWER_MIDDLE: 0.4,
            SocialClass.WORKING: 0.3,
            SocialClass.POOR: 0.2,
            SocialClass.MARGINALIZED: 0.1
        }
        return power_levels.get(social_class, 0.5)
    
    def _get_class_resources(self, social_class: SocialClass) -> List[str]:
        """موارد الطبقة الاجتماعية"""
        resources_map = {
            SocialClass.UPPER_ELITE: ["المال", "النفوذ", "الشبكات", "المعلومات"],
            SocialClass.UPPER_MIDDLE: ["التعليم", "المهارات", "الشبكات المهنية"],
            SocialClass.MIDDLE: ["التعليم المتوسط", "المدخرات المحدودة", "الاستقرار"],
            SocialClass.WORKING: ["العمالة", "التضامن", "التنظيم"],
            SocialClass.POOR: ["العمالة غير المهرة", "الشبكات الاجتماعية"],
            SocialClass.MARGINALIZED: ["المعاناة المشتركة", "التضامن الداخلي"]
        }
        return resources_map.get(social_class, [])
    
    def _get_conflict_causes(self, conflict_type: ConflictType) -> List[str]:
        """أسباب الصراع حسب النوع"""
        causes_map = {
            ConflictType.CLASS_STRUGGLE: ["عدم المساواة الاقتصادية", "الظلم الاجتماعي", "الاستغلال"],
            ConflictType.ETHNIC_TENSION: ["التمييز العنصري", "التنافس على الموارد", "الذاكرة التاريخية"],
            ConflictType.RELIGIOUS_CONFLICT: ["التعصب الديني", "التفسيرات المختلفة", "النفوذ الديني"],
            ConflictType.GENERATIONAL: ["تغير القيم", "التكنولوجيا", "فجوة التواصل"],
            ConflictType.GENDER_ISSUES: ["عدم المساواة", "الأدوار التقليدية", "التمييز"]
        }
        return causes_map.get(conflict_type, [])
    
    def _get_conflict_consequences(self, conflict_type: ConflictType) -> List[str]:
        """عواقب الصراع حسب النوع"""
        consequences_map = {
            ConflictType.CLASS_STRUGGLE: ["عدم الاستقرار", "التغيير الاجتماعي", "العنف"],
            ConflictType.ETHNIC_TENSION: ["التقسيم المجتمعي", "الهجرة", "العنف العرقي"],
            ConflictType.RELIGIOUS_CONFLICT: ["التطرف", "الانقسام", "العنف الطائفي"],
            ConflictType.GENERATIONAL: ["تمزق الأسرة", "تغيير الثقافة", "عدم التفاهم"],
            ConflictType.GENDER_ISSUES: ["التوتر الاجتماعي", "تغيير الأدوار", "الحراك النسائي"]
        }
        return consequences_map.get(conflict_type, [])
    
    def _generate_conflict_timeline(self, conflict_type: ConflictType) -> List[Dict[str, Any]]:
        """إنتاج خط زمني للصراع"""
        return [
            {"phase": "البداية", "description": "ظهور أولى علامات التوتر", "duration": "1-3 أشهر"},
            {"phase": "التصعيد", "description": "زيادة حدة المواجهة", "duration": "3-6 أشهر"},
            {"phase": "الذروة", "description": "وصول الصراع لأقصى شدة", "duration": "1-2 أشهر"},
            {"phase": "الحل أو التهدئة", "description": "محاولات الحل أو خفض التوتر", "duration": "6-12 شهر"}
        ]
    
    def _load_social_hierarchy(self) -> Dict[str, Any]:
        """تحميل التسلسل الهرمي الاجتماعي"""
        return {
            "traditional_arab": {
                "top": ["الأمراء", "الوجهاء", "كبار التجار"],
                "middle": ["العلماء", "التجار", "الحرفيون"],
                "bottom": ["الفلاحون", "البدو", "الخدم"]
            },
            "modern_urban": {
                "top": ["رجال الأعمال", "السياسيون", "المثقفون"],
                "middle": ["الموظفون", "المهنيون", "التجار الصغار"],
                "bottom": ["العمال", "الباعة", "العاطلون"]
            }
        }
    
    def _load_conflict_patterns(self) -> Dict[str, List[str]]:
        """تحميل أنماط الصراعات"""
        return {
            "escalation_patterns": [
                "تبادل الاتهامات",
                "حشد الأنصار",
                "المواجهة المباشرة",
                "التدخل الخارجي"
            ],
            "resolution_patterns": [
                "الوساطة",
                "التفاوض",
                "التنازلات المتبادلة",
                "تدخل السلطة"
            ]
        }
    
    def _load_historical_conflicts(self) -> List[Dict[str, str]]:
        """تحميل الصراعات التاريخية كمرجع"""
        return [
            {
                "name": "ثورة الزنج",
                "type": "class_struggle",
                "causes": "الظلم الاجتماعي والعبودية",
                "outcome": "قمع بعد صراع طويل"
            },
            {
                "name": "الفتنة الكبرى",
                "type": "political_religious",
                "causes": "خلافات حول الخلافة",
                "outcome": "انقسام دائم في الأمة"
            }
        ]
    
    def _load_resolution_strategies(self) -> Dict[str, List[str]]:
        """تحميل استراتيجيات الحل"""
        return {
            "dialogue_based": [
                "المجالس التشاورية",
                "لجان الوساطة",
                "الحوار المجتمعي"
            ],
            "institutional": [
                "إصلاح القوانين",
                "إنشاء مؤسسات جديدة",
                "آليات الشكاوى"
            ],
            "economic": [
                "برامج التنمية",
                "إعادة التوزيع",
                "خلق فرص العمل"
            ]
        }
