from google.adk.tools.base_tool import BaseTool

from typing import Optional, Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.models import LlmRequest
#

#db = DBService()
from google.adk.tools import ToolContext
#from google.adk.agents.callback_context import CallbackContext
from ..config.Customer import Customer
from services.session_service import session_service
from services.logger import get_logger
#from services.db_service import DBService
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

# --- Config ---
app_name = os.environ.get("APP_NAME", "Customer Support Agent")
def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    try: 
        if "session_id" not in callback_context.state:
            print("Error: no session_id")
            print(vars(callback_context.state))
            print("\n================================\n")
        else:
            print("%%%%%%%%%%%%%%%%%% Printing context variables")
            print(vars(callback_context.state))
    except Exception as e:
        print(f"Error: Could not check session_id. {e}")
'''
async def before_agent_callback(callback_context: InvocationContext):
    # Grab session details
    print(f"111111111111111111111111111")
    in_context = callback_context._invocation_context
    session_obj = in_context.session_service
    print(f"Variables in session is {vars(session_obj)}")

        
    user_id = callback_context.state.get("user_id")
    session_id = callback_context.state.get("session_id")
    print(f"user_id = {user_id}")
    print(f"session_id = {session_id}")

    #session_id = session_obj
    #print("xxxxxxxxxxxxxxxxxxxxxx:  ", session_id)
    
    #session_deatils = callback_context.session_service.get_session(app_name, user_id, session_id)
    #print(f"22222222222222222222\n\n\n\n\n\n{vars(in_context.session_service)}")




    # Create the Customer object
    customer = Customer(
        user_id=user_id,
        session_id=session_id,
        session_service=session_service,
        app_name=app_name
    )

    # Load session state
    await customer.load_from_session()

    # Log it!
    print(f"User ID: {user_id}, Session ID: {session_id}")
    print(f"Session State: {customer.session_state}")

    # Example forced routing:
    active_subagent = customer.session_state.get("active_subagent")
    if active_subagent:
        print(f" BEFORE_AGENT_CALLBACK - Forcing subagent: {active_subagent}")
        in_context.forced_subagent_name = active_subagent

    # Attach customer to context for use in other callbacks
    in_context.custom_data["customer"] = customer
'''
async def after_agent_callback(callback_context: InvocationContext):
    """
    This is an after agent callback to 
        - reset the flags
        - log the actions
        - save the session
    """
    in_context = callback_context._invocation_context
    customer = in_context.custom_data.get("customer")
    if not customer:
        return

    # Optionally clear the active subagent if user said 'exit'
    if customer.session_state.get("exit_requested"):
        print("AFTER_AGENT_CALLBACK -  Clearing active_subagent")
        customer.session_state["active_subagent"] = None
        customer.session_state["exit_requested"] = None

    # Save session
    await customer.save_to_session()

    # Log
    print(f"AFTER_AGENT_CALLBACK -  Session state saved for User ID: {customer.user_id}")


def before_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: CallbackContext
):
   
    # i make sure all values that the agent is sending to tools are lowercase
    msg = f"MOU: 111111111111111111111 {args}"
    print(msg)
    invocation_context = tool_context._invocation_context
    print("=== Invocation Context ===")
    for attr in dir(invocation_context):
        if not attr.startswith('_') and not callable(getattr(invocation_context, attr)):
            print(f"{attr}: {getattr(invocation_context, attr)}")

    event_actions = tool_context._event_actions
    print("=== Event Actions ===")
    for attr in dir(event_actions):
        if not attr.startswith('_') and not callable(getattr(event_actions, attr)):
            print(f"{attr}: {getattr(event_actions, attr)}")
    

    state = tool_context.state
    print("=== State Variables ===")
    for key in state:
        print(f"{key}: {state[key]}")


    for attr in dir(state):
        if not attr.startswith('_') and not callable(getattr(state, attr)):
            print(f"{attr}: {getattr(state, attr)}")


    




    print(f"MOU:  9999999999999999 Inside double_auth_callback {args} ")
    if tool.name == "create_account":
        
        return None

    username = args.get("username")
    password = args.get("password")
    
    if not username or not password:
        return {
            "status": "AUTH_REQUIRED",
            "message": "Please provide both username and password to continue."
        }

    user_record = db.verify_user(username, password)
    print(user_record)
    if not user_record or user_record['password'] != password:
        print("Inside double_auth_callback: Auth uncesseful")
        return {           
            "error": "Authentication failed. Invalid username or password."
        }
    print("Inside double_auth_callback: Succesgfully authenticated ")

    return None



def double_auth_callback(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext
) -> Optional[Dict]:
    print(f"MOU:  9999999999999999 Inside double_auth_callback {args} ")
    if tool.name == "create_account":
        
        return None

    username = args.get("username")
    password = args.get("password")
    
    if not username or not password:
        return {
            "status": "AUTH_REQUIRED",
            "message": "Please provide both username and password to continue."
        }

    user_record = db.verify_user(username, password)
    print(user_record)
    if not user_record or user_record['password'] != password:
        print("Inside double_auth_callback: Auth uncesseful")
        return {           
            "error": "Authentication failed. Invalid username or password."
        }
    print("Inside double_auth_callback: Succesgfully authenticated ")

    return None
