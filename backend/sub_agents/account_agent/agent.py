from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from .shared_libraries.callbacks import before_tool, before_agent_callback, after_agent_callback
from google.adk.tools import FunctionTool
from .tools.tools import (
    create_account,
    update_contact,
    update_address,
    update_email,
    update_password,
    inspect_session,
)

#my_tools = [
#    FunctionTool(func=inspect_session),
#    FunctionTool(func=update_address),
#]

account_agent = Agent(
    name="account_agent",
    model="gemini-2.5-flash",
    global_instruction="Account Management BOT",
    instruction="""
        You are an Account Manager service agent who helps users with their account-related queries.
        Tasks:
        1. Ask user what functions it  want to do (create account, update_password, update_email, update_contact, or update_address).
        2. Call the appropriate tool and only after executing the tools, then only return to root agent and not before that
    """,
    tools=[
        create_account,
        update_email,
        update_password,
        update_contact,
        update_address,
    ],
    before_agent_callback=before_agent_callback,
    #after_agent_callback=after_agent_callback,
    before_tool_callback=before_tool,


)


