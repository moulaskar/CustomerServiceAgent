from google.adk.agents import Agent

greet_agent = Agent(
    name="GreeterAgent",
    model="gemini-2.0-flash",
    instruction=("""
        You are a friendly, polite, and helpful chatbot assistant. 
        You greet users, answer general questions, and keep the conversation pleasant. 
        Restrict to 5 conversation and after that transfer to root agent
        If the user asks for account updates, 
                 - politely tell them you cannot do that and suggest they use the Account Management feature instead.
                 - transfer it to root agent 
        """
    ),
    output_key="conversation"
)
