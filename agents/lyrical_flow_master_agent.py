# agents/lyrical_flow_master_agent.py (V3 - Metaphor-Aware)
# ... (الاستيرادات والتهيئة كما هي)

class LyricalFlowMasterAgent(BaseAgent):
    # ...
    async def engineer_flow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raw_lyrics = context.get("raw_lyrics")
        sectional_fingerprints = context.get("sectional_fingerprints")
        central_metaphor = context.get("central_metaphor") # [جديد]
        
        if not all([raw_lyrics, sectional_fingerprints, central_metaphor]):
            return {"status": "error", "message": "Raw lyrics, fingerprints, and central metaphor are required."}
            
        logger.info(f"Engineering lyrical flow around the metaphor: '{central_metaphor.get('metaphor_object')}'")
        
        prompt = self._build_flow_engineering_prompt(raw_lyrics, sectional_fingerprints, central_metaphor) # [جديد]
        engineered_lyrics = await llm_service.generate_text_response(prompt, temperature=0.7)
        
        return {"status": "success", "content": {"engineered_lyrics": engineered_lyrics}}

    def _build_flow_engineering_prompt(self, raw_text: str, fingerprints: Dict, metaphor: Dict) -> str:
        # [مُحسّن] الـ Prompt الآن لديه مهمة إضافية: نسج الرمز
        return f"""
مهمتك: أنت مهندس كلمات (Lyric Engineer) وشاعر. مهمتك هي تحويل "تيار الوعي" الخام إلى أغنية متكاملة.

**الرمز المركزي للأغنية (يجب أن يكون هو القلب النابض للنص):**
- **الرمز:** {metaphor.get('metaphor_object')}
- **معناه:** {metaphor.get('metaphor_meaning')}

**النص الخام للمراجعة (مستوحى من الرمز):**
---
{raw_text}
---

**التعليمات الهيكلية والأدائية:**
1.  **بنية الأغنية:** [المقطع الأول] -> [اللازمة] -> [المقطع الثاني].
2.  **تطور الرمز:** يجب أن ينسج الرمز ويتطور عبر الأغنية.
    - **المقطع الأول:** قدّم الرمز أو أشر إليه بشكل غامض.
    - **اللازمة:** يجب أن تكون هي التساؤل أو الشعور الأساسي المرتبط بالرمز.
    - **المقطع الثاني:** تعمق في معنى الرمز أو أظهر تأثيره على الشخصية.
3.  **الأسلوب:** اتبع الأسلوب المحدد لكل مقطع بناءً على البصمة الأدائية.
    - **أسلوب المقاطع:** {fingerprints['verse_fingerprint']['flow']}.
    - **أسلوب اللازمة:** {fingerprints['chorus_fingerprint']['flow']}.

**الناتج النهائي يجب أن يكون الكلمات المهندسة فقط، مقسمة بوضوح.**
"""
    # ...
