import uuid
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from dotenv import load_dotenv
from utils import call_agent_async
from logger import setup_logger, get_logger

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ADK Agent Setup ---
session_service = InMemorySessionService()
app_name = "state_app"

greeting_agent = LlmAgent(
    name="Greeter",
    model="gemini-2.0-flash",
    instruction=(
        "You are a friendly chatbot assistant. "
        "Always answer user questions or chats clearly"
    ),
    output_key="last_greeting"
)

runner = Runner(
    agent=greeting_agent,
    app_name=app_name,
    session_service=session_service
)

def generate_session_id():
    return str(uuid.uuid4())


# --- Endpoint: Create Session ---
@app.post("/session")
async def create_session_endpoint(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "anonymous")
    session_id = generate_session_id()

    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)

    setup_logger(session_id)
    logger = get_logger()
    logger.info(f"Session created for user: {user_id}")

    return {"session_id": session_id}


# --- Endpoint: Chat ---
@app.post("/chat")
async def chat_with_agent(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "anonymous")
    session_id = data.get("session_id")
    message = data.get("message")

    if not message:
        raise HTTPException(status_code=400, detail="No message provided")

    # Auto-create session if missing
    if not session_id:
        session_id = generate_session_id()
        await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)
        setup_logger(session_id)

    # Ensure logger exists
    setup_logger(session_id)
    logger = get_logger()

    logger.info(f"User ({user_id}): {message}")

    # Ensure session exists
    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id)

    # Call agent
    await call_agent_async(runner, user_id, session_id, message)

    session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    logger.info(f"Session State: {session.state}")

    last_response = session.state.get("last_greeting")
    if not last_response:
        last_response = "Sorry, I didn't understand that."

    logger.info(f"Agent: {last_response}")

    return {"session_id": session_id, "response": last_response}
