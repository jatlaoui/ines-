# core/workflow_manager.py (النسخة الكاملة والمحدثة مع خط الإنتاج المسرحي)
import logging
from typing import Dict, Any, List, Callable, Optional, Union
import json
import asyncio

# استيراد المنسق الرئيسي الذي سيقوم بتشغيل المهام الفردية
from core.apollo_orchestrator import apollo
from ingestion.ingestion_engine import InputType, ingestion_engine
from agents.blueprint_architect_agent import StoryBlueprint, ChapterOutline # استيراد نماذج البيانات

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [WorkflowManager] - %(levelname)s - %(message)s')
logger = logging.getLogger("WorkflowManager")

class WorkflowManager:
    """
    يدير خطوط الإنتاج الإبداعية (Pipelines) التي تتكون من عدة مهام متسلسلة،
    مع دعم نقاط التوقف التفاعلية للمستخدم والتعامل مع مدخلات متعددة.
    """
    def __init__(self):
        """
        تهيئة مدير سير العمل.
        """
        self.orchestrator = apollo
        self.ingestion_engine = ingestion_engine
        self.active_pipelines: Dict[str, Dict[str, Any]] = {}

    # --- دالة مساعدة لإدارة التفاعل مع المستخدم ---
    async def _handle_user_feedback(
        self,
        pipeline_id: str,
        step_name: str,
        step_result: Dict[str, Any],
        user_feedback_fn: Optional[Callable],
        user_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """دالة مساعدة لإدارة تفاعل المستخدم."""
        if user_feedback_fn and step_name in user_config.get("user_checkpoints", []):
            logger.info(f"[{pipeline_id}] Awaiting user feedback on '{step_name}'...")
            user_action = await user_feedback_fn(step_name, step_result.get("final_content"))
            
            if isinstance(user_action, dict): # User provided a modified version
                logger.info(f"[{pipeline_id}] User modified the '{step_name}'.")
                step_result["final_content"] = user_action
            elif user_action == "regenerate":
                raise InterruptedError(f"User requested regeneration at step: {step_name}")
        return step_result

    # --- خط الإنتاج الموحد والأساسي ---
    async def transmute_witness(
        self,
        user_id: str, project_id: str, source: Any, input_type: InputType,
        creation_config: Dict[str, Any], user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        خط الإنتاج الموحد الجديد: يستوعب أي شاهد ويحوله إلى إبداع.
        """
        pipeline_id = f"transmute_pipeline_{project_id}"
        logger.info(f"[{pipeline_id}] Starting 'Witness Transmutation' Pipeline")
        self.active_pipelines[pipeline_id] = {"status": "running", "steps": {}}

        try:
            # STEP 0: استيعاب الشاهد
            ingestion_result = await self.ingestion_engine.ingest(source, input_type)
            if not ingestion_result.success:
                raise ValueError(f"فشل في استيعاب المصدر: {ingestion_result.error}")
            self.active_pipelines[pipeline_id]["steps"]["ingestion"] = {"success": True, "metadata": ingestion_result.metadata}
            
            # STEP 1: تحليل الشاهد
            knowledge_base_result = await self.orchestrator.run_refinable_task(
                task_name="analyze_witness", # يفترض وجود هذه المهمة
                initial_context={"text_content": ingestion_result.text_content, "metadata": ingestion_result.metadata},
                user_config=creation_config
            )
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base_result
            knowledge_base = knowledge_base_result["final_content"]

            # STEP 2: التوجيه إلى خط الإنتاج الفرعي المناسب
            creative_form = creation_config.get("creative_form", "novel")
            logger.info(f"[{pipeline_id}] ==> Routing to '{creative_form}' sub-pipeline...")

            sub_pipelines = {
                "novel": self._run_novel_sub_pipeline,
                "poem": self._run_poem_sub_pipeline,
                "play": self._run_play_sub_pipeline # <-- خط الإنتاج الجديد
            }
            
            sub_pipeline_fn = sub_pipelines.get(creative_form)
            if not sub_pipeline_fn:
                raise ValueError(f"Creative form '{creative_form}' is not supported.")
            
            final_product = await sub_pipeline_fn(pipeline_id, knowledge_base, creation_config, user_feedback_fn)

            self.active_pipelines[pipeline_id].update({"status": "completed", "final_product": final_product})
            logger.info(f"[{pipeline_id}] Pipeline completed successfully.")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"[{pipeline_id}] Pipeline failed: {e}")
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    # --- خطوط الإنتاج الفرعية (Sub-Pipelines) ---

    async def _run_novel_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        """خط الإنتاج الفرعي للرواية."""
        logger.info(f"[{pipeline_id}] -> Engaging Novel Production Sub-Pipeline...")
        
        # 1. بناء المخطط
        blueprint_result = await self.orchestrator.run_refinable_task("generate_blueprint", kb, config)
        self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
        blueprint_result = await self._handle_user_feedback(pipeline_id, "blueprint", blueprint_result, feedback_fn, config)

        # 2. كتابة الفصل الأول
        first_chapter_outline = blueprint_result["final_content"].chapters[0]
        chapter_result = await self.orchestrator.run_refinable_task("generate_chapter", {"chapter_outline": first_chapter_outline}, config)
        self.active_pipelines[pipeline_id]["steps"]["chapter_1"] = chapter_result
        
        return chapter_result

    async def _run_poem_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        """خط الإنتاج الفرعي للقصيدة."""
        logger.info(f"[{pipeline_id}] -> Engaging Poem Production Sub-Pipeline...")
        
        emotional_arc = kb.get("emotional_arc", [])
        themes = [entity['name'] for entity in kb.get("entities", []) if entity['type'] == 'concept']
        
        poem_context = {
            "theme_hint": themes[0] if themes else "الحياة",
            "mood_hint": emotional_arc[0]['emotion'] if emotional_arc else "تأملي",
            **config
        }
        
        poem_result = await self.orchestrator.run_refinable_task("generate_poem", poem_context, config)
        self.active_pipelines[pipeline_id]["steps"]["poem"] = poem_result
        await self._handle_user_feedback(pipeline_id, "poem", poem_result, feedback_fn, config)
        
        return poem_result

    # --- خط الإنتاج المسرحي الجديد ---
    async def _run_play_sub_pipeline(
        self,
        pipeline_id: str,
        knowledge_base: Dict[str, Any],
        user_config: Dict[str, Any],
        user_feedback_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        خط الإنتاج الفرعي لكتابة مسرحية كاملة.
        """
        logger.info(f"[{pipeline_id}] -> Engaging Playwriting Sub-Pipeline...")

        # STEP 1: توليد الفكرة الدرامية من قاعدة المعرفة
        idea_context = {
            "genre_hint": "مسرحية",
            "theme_hint": ", ".join([e['name'] for e in knowledge_base.get('entities', []) if e['type'] == 'concept']),
            "initial_characters": [e['name'] for e in knowledge_base.get('entities', []) if e['type'] == 'character']
        }
        idea_result = await self.orchestrator.run_refinable_task("generate_idea", idea_context, user_config)
        self.active_pipelines[pipeline_id]["steps"]["play_idea"] = idea_result
        await self._handle_user_feedback(pipeline_id, "play_idea", idea_result, user_feedback_fn, user_config)

        # STEP 2: بناء المخطط الدرامي
        dramatic_blueprint_result = await self.orchestrator.run_refinable_task(
            task_name="generate_dramatic_blueprint",
            initial_context={"idea": idea_result["final_content"]},
            user_config=user_config
        )
        self.active_pipelines[pipeline_id]["steps"]["dramatic_blueprint"] = dramatic_blueprint_result
        await self._handle_user_feedback(pipeline_id, "dramatic_blueprint", dramatic_blueprint_result, user_feedback_fn, user_config)

        # STEP 3: بناء أقواس تطور الشخصيات
        character_arcs_result = await self.orchestrator.run_refinable_task(
            task_name="develop_character_arcs",
            initial_context={"blueprint": dramatic_blueprint_result["final_content"]},
            user_config=user_config
        )
        self.active_pipelines[pipeline_id]["steps"]["character_arcs"] = character_arcs_result

        # STEP 4: كتابة فصول (مشاهد) المسرحية
        full_play_script = ""
        blueprint_content = dramatic_blueprint_result["final_content"]
        arcs_content = character_arcs_result["final_content"]
        
        for act in blueprint_content.get("acts", []):
            for chapter_outline in act.get("chapters", []): # Assuming chapters are nested in acts
                chapter_script = await self.orchestrator.run_refinable_task(
                    task_name="generate_play_chapter",
                    initial_context={"chapter_outline": chapter_outline, "character_arcs": arcs_content},
                    user_config=user_config
                )
                full_play_script += chapter_script["final_content"]["chapter_content"] + "\n\n---\n\n"
        
        self.active_pipelines[pipeline_id]["steps"]["raw_script"] = {"content": full_play_script}

        # STEP 5: إضافة التوجيهات الإخراجية النهائية
        final_script_result = await self.orchestrator.run_refinable_task(
            task_name="add_staging_directions",
            initial_context={"script": full_play_script},
            user_config=user_config
        )
        self.active_pipelines[pipeline_id]["steps"]["final_script"] = final_script_result

        return final_script_result

# ... (بقية الكود ودالة الاختبار `if __name__ == "__main__":`)

        try:
            # --- الخطوة 0: استيعاب الشاهد ---
            logger.info(f"[{pipeline_id}] ==> STEP 0: Ingesting Witness of type '{input_type.value}'...")
            ingestion_result = await self.ingestion_engine.ingest(source, input_type)
            
            if not ingestion_result.success:
                raise ValueError(f"فشل في استيعاب المصدر: {ingestion_result.error}")
                
            witness_content = ingestion_result.text_content
            witness_metadata = ingestion_result.metadata
            self.active_pipelines[pipeline_id]["steps"]["ingestion"] = {
                "success": True, "metadata": witness_metadata
            }
            
            # --- الخطوة 1: تحليل الشاهد وبناء قاعدة المعرفة ---
            logger.info(f"[{pipeline_id}] ==> STEP 1: Analyzing Witness...")
            # نفترض وجود مهمة `analyze_witness` في أبولو تستخدم `AdvancedContextEngine`
            knowledge_base_result = await self.orchestrator.run_refinable_task(
                task_name="analyze_witness",
                initial_context={"text_content": witness_content, "metadata": witness_metadata},
                user_config=creation_config
            )
            self.active_pipelines[pipeline_id]["steps"]["knowledge_base"] = knowledge_base_result
            knowledge_base = knowledge_base_result["final_content"]

            # --- الخطوة 2: تحديد مسار الإنتاج وتوجيه قاعدة المعرفة ---
            creative_form = creation_config.get("creative_form", "novel")
            logger.info(f"[{pipeline_id}] ==> Routing to '{creative_form}' sub-pipeline...")

            if creative_form == "novel":
                final_product = await self._run_novel_sub_pipeline(pipeline_id, knowledge_base, creation_config, user_feedback_fn)
            elif creative_form == "poem":
                final_product = await self._run_poem_sub_pipeline(pipeline_id, knowledge_base, creation_config, user_feedback_fn)
            elif creative_form == "crime_story":
                final_product = await self._run_crime_story_sub_pipeline(pipeline_id, knowledge_base, creation_config, user_feedback_fn)
            else:
                raise ValueError(f"Creative form '{creative_form}' is not supported.")

            self.active_pipelines[pipeline_id]["status"] = "completed"
            self.active_pipelines[pipeline_id]["final_product"] = final_product
            logger.info(f"[{pipeline_id}] 'Witness Transmutation' Pipeline completed successfully.")
            return self.active_pipelines[pipeline_id]

        except Exception as e:
            logger.error(f"[{pipeline_id}] Pipeline failed: {e}")
            self.active_pipelines[pipeline_id].update({"status": "failed", "error": str(e)})
            raise

    # --- خطوط الإنتاج الفرعية (Sub-Pipelines) ---

    async def _run_novel_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        """خط الإنتاج الفرعي للرواية."""
        logger.info(f"[{pipeline_id}] -> Engaging Novel Production Sub-Pipeline...")
        
        # 1. بناء المخطط من قاعدة المعرفة
        blueprint_result = await self.orchestrator.run_refinable_task(
            task_name="generate_blueprint", initial_context=kb, user_config=config
        )
        self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
        blueprint_result = await self._handle_user_feedback(pipeline_id, "blueprint", blueprint_result, feedback_fn, config)

        # 2. كتابة الفصل الأول
        first_chapter_outline = blueprint_result["final_content"].chapters[0]
        chapter_result = await self.orchestrator.run_refinable_task(
            task_name="generate_chapter", initial_context=first_chapter_outline, user_config=config
        )
        self.active_pipelines[pipeline_id]["steps"]["chapter_1"] = chapter_result
        
        return chapter_result

    async def _run_poem_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        """خط الإنتاج الفرعي للقصيدة."""
        logger.info(f"[{pipeline_id}] -> Engaging Poem Production Sub-Pipeline...")
        
        # 1. استخلاص الموضوع والمشاعر من قاعدة المعرفة
        emotional_arc = kb.get("emotional_arc", [])
        themes = [entity['name'] for entity in kb.get("entities", []) if entity['type'] == 'concept']
        
        poem_context = {
            "theme_hint": themes[0] if themes else "الحياة",
            "mood_hint": emotional_arc[0]['emotion'] if emotional_arc else "تأملي",
            **config
        }
        
        # 2. توليد القصيدة
        poem_result = await self.orchestrator.run_refinable_task(
            task_name="generate_poem", initial_context=poem_context, user_config=config
        )
        self.active_pipelines[pipeline_id]["steps"]["poem"] = poem_result
        await self._handle_user_feedback(pipeline_id, "poem", poem_result, feedback_fn, config)
        
        return poem_result
        
    async def _run_crime_story_sub_pipeline(self, pipeline_id, kb, config, feedback_fn):
        """خط إنتاج فرعي متخصص لقصص الجريمة."""
        logger.info(f"[{pipeline_id}] -> Engaging Crime Story Sub-Pipeline...")
        
        # 1. تحليل منطق الجريمة من قاعدة المعرفة
        # نفترض أن kb.story_text هو النص الكامل
        story_text = kb.get("raw_text", "")
        forensic_analysis = await self.orchestrator.run_refinable_task(
            task_name="analyze_crime_narrative", initial_context={"text_content": story_text}, user_config=config
        )
        self.active_pipelines[pipeline_id]["steps"]["forensic_analysis"] = forensic_analysis

        # 2. بناء المخطط مع الأخذ في الاعتبار التحليل الجنائي
        blueprint_context = {"knowledge_base": kb, "forensic_report": forensic_analysis["final_content"]}
        blueprint_result = await self.orchestrator.run_refinable_task(
            task_name="generate_blueprint", initial_context=blueprint_context, user_config=config
        )
        self.active_pipelines[pipeline_id]["steps"]["blueprint"] = blueprint_result
        
        return blueprint_result

# --- مثال اختبار ---
if __name__ == "__main__":
    # هذا القسم يتطلب وجود جميع ملفات الوكلاء والنواة في المسار الصحيح
    
    # إضافة المسار الحالي للسماح بالاستيرادات
    import sys
    sys.path.append('.')
    
    # استيراد النماذج اللازمة للاختبار
    from agents.blueprint_architect_agent import ChapterOutline
    
    async def cli_feedback_handler(stage: str, content: Optional[Any] = None) -> Union[str, Dict[str, Any]]:
        # ... (نفس دالة cli_feedback_handler من الرد السابق) ...
        pass

    async def test_workflows():
        """اختبار جميع خطوط الإنتاج المتاحة."""
        manager = WorkflowManager()
        
        # --- اختبار خط الإنتاج الموحد (رواية) ---
        print("\n" + "="*80)
        print("🎬🎬🎬  RUNNING UNIFIED STORY WORKFLOW TEST 🎬🎬🎬")
        print("="*80)
        
        sample_witness_text = "في زقاق ضيق من أزقة القاهرة القديمة، كان علي يبحث عن بقايا أمل. الرسالة القديمة التي وجدها في صندوق جده لم تكن مجرد ورق، بل كانت خريطة لكنز مفقود، وربما مفتاحًا لماضيه المجهول."
        
        story_config = {
            "creative_form": "novel",
            "genre_hint": "مغامرة تاريخية",
            "theme_hint": "البحث عن الهوية",
            "quality_threshold": 8.0,
            "user_checkpoints": ["blueprint"]
        }

        try:
            final_story_assets = await manager.transmute_witness(
                user_id="cli_user",
                project_id="project_transmute_001",
                source=sample_witness_text,
                input_type=InputType.RAW_TEXT,
                creation_config=story_config,
                user_feedback_fn=None # تعطيل التفاعل للاختبار السريع
            )
            print("\n--- ✅ النتيجة النهائية لخط إنتاج الرواية الموحد ---")
            # Custom encoder to handle dataclasses
            class DataclassEncoder(json.JSONEncoder):
                def default(self, o):
                    from dataclasses import is_dataclass, asdict
                    if is_dataclass(o):
                        return asdict(o)
                    return super().default(o)
            print(json.dumps(final_story_assets, ensure_ascii=False, indent=2, cls=DataclassEncoder))

        except Exception as e:
            print(f"--- ❌ فشل اختبار خط إنتاج الرواية الموحد --- \n {e}")

    asyncio.run(test_workflows())
        except Exception as e:
            # ... (معالجة الأخطاء) ...
            raise
