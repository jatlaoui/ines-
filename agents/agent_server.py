# api/agent_server.py
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import argparse

# استيراد الوكلاء الذين نريد تشغيلهم كخدمات
from ..agents.playwright_agent import playwright_agent
from ..agents.lore_master_agent import lore_master_agent
from ..agents.base_agent import BaseAgent
# ... يمكن إضافة أي وكيل آخر هنا

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentServer")

# إنشاء تطبيق FastAPI
app = FastAPI(title="INES Agent Microservice")

# قاموس لتسجيل الوكلاء المتاحين في هذه الخدمة
AVAILABLE_AGENTS: Dict[str, BaseAgent] = {
    "playwright": playwright_agent,
    "lore_master": lore_master_agent
}

class TaskRequest(BaseModel):
    """نموذج الطلب لتنفيذ مهمة."""
    agent_id: str
    context: Dict

@app.post("/execute-task", summary="Execute a task on a specific agent")
async def execute_task(request: TaskRequest):
    """
    نقطة نهاية (Endpoint) موحدة لاستدعاء أي وكيل.
    n8n سيقوم بإرسال طلبات POST إلى هنا.
    """
    logger.info(f"Received task for agent: {request.agent_id}")
    
    agent = AVAILABLE_AGENTS.get(request.agent_id)
    if not agent:
        logger.error(f"Agent '{request.agent_id}' not found.")
        raise HTTPException(status_code=404, detail=f"Agent '{request.agent_id}' not found.")

    try:
        # استدعاء دالة process_task الخاصة بالوكيل المحدد
        result = await agent.process_task(request.context)
        return result
    except Exception as e:
        logger.error(f"Error processing task for agent {request.agent_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-agents", summary="List all available agents on this server")
async def list_agents():
    """نقطة نهاية لعرض قائمة بالوكلاء المتاحين."""
    return {"agents": [agent.get_info() for agent in AVAILABLE_AGENTS.values()]}

def start_server(host: str = "127.0.0.1", port: int = 8000):
    """بدء تشغيل خادم الـ API."""
    logger.info(f"Starting INES Agent Server at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    # هذا يسمح بتشغيل الخادم من سطر الأوامر
    # مثال: python -m ines.api.agent_server
    parser = argparse.ArgumentParser(description="INES Agent Microservice Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server to.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to.")
    args = parser.parse_args()
    start_server(host=args.host, port=args.port)
