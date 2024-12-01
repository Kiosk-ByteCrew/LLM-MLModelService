

class SessionInactiveError(Exception):
    def __init__(self, session_id: str):
        super().__init__(f"Session '{session_id}' is not active.")
        self.session_id = session_id