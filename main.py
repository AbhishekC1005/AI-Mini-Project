"""FastAPI server for Hospital Reception Assistant."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import uuid

# -------------------------
# FastAPI Setup
# -------------------------
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize session service and runner
APP_NAME = "hospital_reception"
session_service = InMemorySessionService()

# MUST provide both app_name AND agent
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service
)


class QueryModel(BaseModel):
    user_query: str


@app.post("/ask-reception")
async def ask_reception(data: QueryModel):
    # Use unique session for each request (stateless)
    USER_ID = "api_user"
    SESSION_ID = str(uuid.uuid4())
    
    # Create new session for this request
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # Prepare the user message
    content = types.Content(
        role='user',
        parts=[types.Part(text=data.user_query)]
    )
    
    # Run the agent and collect the final response
    final_response = "No response received."
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            break
    
    return {"response": final_response}


@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Hospital Reception Assistant API")
    print("=" * 60)
    print("\nAPI running at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nEndpoints:")
    print("  POST /ask-reception - Send queries to the assistant")
    print("  GET  /             - Health check")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)