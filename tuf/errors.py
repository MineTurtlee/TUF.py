class ClientError(Exception):
    pass

class AuthenticationError(ClientError):
    def __init__(self, username: str, error: str):
        super().__init__("Authentication failed for {}: {}".format(username, error))

class APIError(ClientError):
    def __init__(self, path: str, error: str):
        super().__init__(f"Error while requesting path {path}: {error}")

class SyntaxError(Exception):
    def __init__(self, *names: str):
        string = ""
        string = ", ".join(names)
        string = string + "were not passed correctly."

        super().__init__()