class CustomInMemorySessionStore:
    def __init__(self):
        self.sessions = {}

    def get(self, session_id):
        return self.sessions.get(session_id, {})

    def create(self, session_id):
        self.sessions[session_id] = {}
        return self.sessions[session_id]

    def update(self, session_id, key, value):
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        self.sessions[session_id][key] = value

session_store = CustomInMemorySessionStore()
