from typing import Optional

from aiohttp import ClientSession
from .errors import APIError, AuthenticationError, SyntaxError, ConflictingArgs
from .level import Levels, Level

class TUFClient:
    """The TUF API client.
    """

    def __init__(self, username: str, password: str, base_url: str = "https://api.tuforums.com/v2/"):
        self.base_url = base_url
        self.username = username
        self.password = password
        self._session: Optional[ClientSession] = None

    @classmethod
    async def create(cls, username: str, password: str) -> "TUFClient":
        """Creates a client with actual auth and stuff

        Args:
            username (str): User's username to use
            password (str): User password to login

        Returns:
            TUFClient
        """
        self = cls(username, password, "https://api.tuforums.com/v2/")
        self._session = ClientSession(base_url=self.base_url)

        josn = {
            "emailOrUsername": username,
            "password": password,
            "captchaToken": "string"
        }

        resp = await self._session.get("auth/login", json=josn)
        resptext = await resp.json()
        if resp.status != 200:
            match resp.status:
                case 400, 401:
                    raise AuthenticationError(self.username, resptext["message"])
                case 500:
                    raise APIError(self._session._base_url + "auth/login", resptext["message"])
        
        self._token = resptext["sessionId"]

        return self

    async def close(self) -> None:
        """Close the underlying aiohttp session."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_levels(self, 
                        id: int = None,
                        name: str = None, 
                        range: str = None, 
                        sort: str = None,
                        page: int = None,
                        offset: int = None,
                        limit: int = None
                        ) -> Levels | Level:
        if not id and not name: raise SyntaxError("id", "name")
        if id and name: raise ConflictingArgs('id', 'name')
        if not id and name:
            query = f"query={name}"
            if range:
                query = query + f"&pguRange={range}"
            if sort:
                query = query + f"&sort={sort}"
            if page:
                query = query + f"&page={page}"
            if offset:
                query = query + f"&offset={offset}"
            if limit:
                query = query + f"&limit={limit}"
            
            req = await self._session.get("database/levels?{}".format(query))
            res = await req.json()

            return Levels.from_dict(self._session, res)
        if id and not name: 
            req = await self._session.head(f"database/levels/{id}")
            req.raise_for_status()
            query = await self._session.get(f"database/levels/{id}")
            resptext = await query.json()

            return Level.from_dict(resptext)