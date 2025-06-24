# main.py - The Unified Entry Point for INES
import asyncio
import argparse
import json
import logging

# التأكد من أن جميع الوحدات والوكلاء يتم استيرادهم ليتم تسجيلهم
from core.core_orchestrator import core_orchestrator

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')

def setup_arg_parser():
    """إعداد محلل وسيطات سطر الأوامر."""
    parser = argparse.ArgumentParser(description="INES: The Super-Intelligent Narrative System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # أمر تشغيل سير العمل
    run_parser = subparsers.add_parser("run", help="Run an autonomous creative workflow.")
    run_parser.add_argument("--goal", type=str, required=True, help="The high-level goal for the project (e.g., 'Write a short novel about Tunisian resistance').")
    run_parser.add_argument("--context", type=str, default='{}', help="JSON string containing any initial context for the workflow (e.g., '{\"initial_topic\": \"...\"}').")

    # أمر التحقق من الحالة
    status_parser = subparsers.add_parser("status", help="Check the status of a running or completed workflow.")
    status_parser.add_argument("--id", type=str, required=True, help="The execution ID of the workflow to check.")
    
    return parser

async def main():
    """نقطة الدخول الرئيسية للنظام."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    if args.command == "run":
        try:
            initial_context = json.loads(args.context)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for --context.")
            return

        execution_id = await core_orchestrator.start_autonomous_workflow(
            project_goal=args.goal,
            initial_context=initial_context,
        )
        print(f"\n🚀 Workflow started successfully! Execution ID: {execution_id}")
        print("Use 'python main.py status --id <EXECUTION_ID>' to check its progress.")
        
        # الانتظار والمراقبة (في تطبيق حقيقي قد يكون هذا نظام طابور)
        while True:
            status = core_orchestrator.get_workflow_status(execution_id)
            if status['status'] != 'running':
                print("\n--- Workflow Finished ---")
                print(f"Final Status: {status['status']}")
                if status.get('error'):
                    print(f"Error: {status['error']}")
                else:
                    print("Final Output:")
                    # طباعة المخرجات النهائية بشكل جميل
                    print(json.dumps(status.get('final_output'), indent=2, ensure_ascii=False))
                break
            await asyncio.sleep(10) # تحقق كل 10 ثوان

    elif args.command == "status":
        status = core_orchestrator.get_workflow_status(args.id)
        print(json.dumps(status, indent=2, ensure_ascii=False))
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWorkflow execution interrupted by user.")
