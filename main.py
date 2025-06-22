# main.py - The Unified Entry Point for INES
import asyncio
import argparse
import json
from core.core_orchestrator import core_orchestrator
from core.core_auth import get_mock_user_session # لغرض الاختبار

def setup_arg_parser():
    """إعداد محلل وسيطات سطر الأوامر."""
    parser = argparse.ArgumentParser(description="INES: The Super-Intelligent Narrative System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # أمر تشغيل سير العمل
    run_parser = subparsers.add_parser("run-workflow", help="Run a specific workflow template.")
    run_parser.add_argument("--id", type=str, required=True, help="The ID of the workflow template to run.")
    run_parser.add_argument("--input-json", type=str, required=True, help="JSON string containing the initial context for the workflow.")

    # أمر قائمة القوالب
    list_parser = subparsers.add_parser("list-templates", help="List all available workflow templates.")

    return parser

async def main():
    """نقطة الدخول الرئيسية للنظام."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    # محاكاة جلسة مستخدم
    user_session = get_mock_user_session("cli_user_001")

    if args.command == "list-templates":
        # عرض قائمة بالقوالب المتاحة
        from core.workflow_templates import workflow_template_manager
        templates = workflow_template_manager.list_templates()
        print(json.dumps(templates, indent=2, ensure_ascii=False))

    elif args.command == "run-workflow":
        template_id = args.id
        try:
            initial_context = json.loads(args.input_json)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for --input-json.")
            return

        print(f"Starting workflow '{template_id}'...")
        execution_id = await core_orchestrator.start_autonomous_workflow(
            project_goal=initial_context.get("goal", "Complete the requested task."),
            initial_context=initial_context,
            user_session=user_session
        )
        print(f"Workflow started successfully! Execution ID: {execution_id}")
        # يمكن إضافة منطق هنا لمتابعة حالة التنفيذ
        
if __name__ == "__main__":
    asyncio.run(main())
