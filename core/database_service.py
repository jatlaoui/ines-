# core/database_service.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

logger = logging.getLogger("DatabaseService")
load_dotenv()

class DatabaseService:
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in your .env file.")
        
        try:
            self.client: Client = create_client(url, key)
            logger.info("✅ Successfully connected to Supabase.")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Supabase: {e}")
            self.client = None

    def get_client(self) -> Optional[Client]:
        return self.client
        
    # --- مثال على دالة لإضافة وكيل ---
    def add_agent(self, agent_data: dict):
        if not self.client:
            return {"status": "error", "message": "Database not connected."}
        try:
            # 'agents' هو اسم الجدول في Supabase
            data, count = self.client.table('agents').insert(agent_data).execute()
            return {"status": "success", "data": data[1]}
        except Exception as e:
            logger.error(f"Error adding agent: {e}")
            return {"status": "error", "message": str(e)}

    # --- مثال على دالة لجلب وكيل ---
    def get_agent(self, agent_id: str):
        if not self.client:
            return {"status": "error", "message": "Database not connected."}
        try:
            data, count = self.client.table('agents').select("*").eq('agent_id', agent_id).execute()
            if data and data[1]:
                return {"status": "success", "data": data[1][0]}
            return {"status": "not_found", "message": "Agent not found."}
        except Exception as e:
            logger.error(f"Error getting agent: {e}")
            return {"status": "error", "message": str(e)}

# إنشاء مثيل وحيد يمكن استيراده في أي مكان
db_service = DatabaseService()
