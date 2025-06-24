# في ملف agents/narrative_constructor_agent.py

class NarrativeConstructorAgent(BaseAgent):
    # ... (في دالة process_task أو دالة الكتابة)
    
    async def construct_play_scene(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        # ...
        
        # [جديد] التحقق من وجود طلب لأسلوب شفوي
        oral_style_fingerprint_id = context.get("oral_style_fingerprint_id")
        
        if oral_style_fingerprint_id:
            # [جديد] جلب البصمة الشفوية من قاعدة البيانات
            # oral_fingerprint = core_db.get_oral_fingerprint(oral_style_fingerprint_id)
            # محاكاة لجلب البصمة
            oral_fingerprint = {
                "performance_style": {
                    "cadence": "storyteller_cadence",
                    "use_of_silence": True
                },
                "oral_formulas": ["قالك يا سيدي بن سيدي...", "وعاشوا في تبات ونبات..."]
            }
            context["oral_fingerprint"] = oral_fingerprint

        # بناء الـ prompt مع التوجيهات الجديدة
        prompt = self._build_prompt_with_oral_style(context)
        
        scene_script = await llm_service.generate_text_response(prompt)
        
        # ...
        
    def _build_prompt_with_oral_style(self, context: Dict) -> str:
        base_prompt = self._build_base_prompt(context) # الـ prompt الأصلي
        
        oral_fingerprint = context.get("oral_fingerprint")
        if not oral_fingerprint:
            return base_prompt

        # [جديد] إضافة توجيهات الأسلوب الشفوي
        oral_instructions = f"""
### تعليمات الأسلوب الشفوي (أسلوب الحكواتي) ###
- **ابدأ القصة** بإحدى هذه العبارات: {oral_fingerprint.get('oral_formulas', [])}
- **الإيقاع:** يجب أن يكون السرد بإيقاع قصصي متمهل (Cadence: {oral_fingerprint['performance_style']['cadence']}).
- **استخدم الصمت:** قم بإضافة وقفات درامية `(وقفة طويلة)` في اللحظات المشوقة.
- **خاطب المستمع:** استخدم عبارات مثل "واسمع يا مستمع..." أو "فهمت يا بني؟".
"""
        
        return base_prompt + "\n\n" + oral_instructions
