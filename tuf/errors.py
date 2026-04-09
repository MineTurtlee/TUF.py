class ClientError(Exception):
    pass

class AuthenticationError(ClientError):
    def __init__(self, username: str, error: str):
        super().__init__("Authentication failed for {}: {}".format(username, error))

class APIError(ClientError):
    def __init__(self, path: str, error: str):
        super().__init__(f"Error while requesting path {path}: {error}")

class SyntaxError(Exception):
    def __init__(self, *names):
        string = ", ".join(names) + " were not passed correctly."
        super().__init__(string)

class ConflictingArgs(ClientError):
    def __init__(self, *names):
        string = ", ".join(names) + " are conflicting args and one of them should be omitted or None"
        super().__init__(string)