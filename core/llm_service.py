# @title 4.1. استيراد وتهيئة النظام بالكامل (النسخة الصحيحة)
import importlib
import sys
import logging

# وظيفة لإعادة تحميل جميع وحدات INES لضمان تطبيق التغييرات
def reload_all_ines_modules():
    # قائمة بجميع الوحدات التي نعرف أنها موجودة في مشروعك
    # (تأكد من أن هذه المسارات تطابق أسماء الملفات التي كتبتها)
    modules_to_reload = [
        'core.base_agent', 'core.llm_service', 'core.core_narrative_memory',
        'core.core_orchestrator', 'core.system_bootstrap',
        # ... أضف مسارات الاستيراد الصحيحة لملفاتك هنا ...
    ]
    for module_name in list(sys.modules.keys()):
        if module_name.startswith('core') or module_name.startswith('agents') or module_name.startswith('engines') or module_name.startswith('orchestrators'):
             try:
                importlib.reload(sys.modules[module_name])
             except Exception:
                pass

print("🔄 Reloading INES modules...")
reload_all_ines_modules()

try:
    # الآن نستورد الحاوية الكاملة من ملف التمهيد
    from core.system_bootstrap import SystemContainer
    
    # نقوم بإنشاء مثيل جديد للنظام بالكامل
    ines_system = SystemContainer()
    
    # نجعل المنسق الأساسي متاحًا بشكل عام
    core_orchestrator = ines_system.core_orchestrator
    
    print('✅ INES System fully imported and initialized via Bootstrap.')
    print(f"Total registered agents in orchestrator: {len(core_orchestrator.agents)}")

except ImportError as e:
    logging.error(f"❌ ImportError: Could not import INES components. Please check the file paths and class names in 'core/system_bootstrap.py'. Error: {e}", exc_info=True)
except Exception as e:
    logging.error(f"❌ An unexpected error occurred during import: {e}", exc_info=True)
