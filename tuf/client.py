from typing import Optional

from aiohttp import ClientSession
from .errors import APIError, AuthenticationError, SyntaxError, ConflictingArgs
from .level import Levels, Level
from .player import Player

class TUFClient:
    """The TUF API client.
    """

    def __init__(self, username: Optional[str] = None,
                password: Optional[str] = None, 
                base_url: Optional[str] = "https://api.tuforums.com/v2/"):
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

        resp = await self._session.post("auth/login", json=josn)
        resptext = await resp.json()
        if resp.status != 200:
            match resp.status:
                case 400 | 401:
                    raise AuthenticationError(self.username, resptext["message"])
                case 500:
                    raise APIError(self._session._base_url + "auth/login", resptext["message"])
                case _: resp.raise_for_status()
        
        self._token = resptext["sessionId"]
        self._headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token}"
        }

        await self._session.close()
        self._session = ClientSession(base_url=self.base_url, headers=self._headers)

        return self

    async def close(self) -> None:
        """Close the underlying aiohttp session."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_levels(self,
                        name: str, 
                        range: str = None, 
                        sort: str = None,
                        page: int = None,
                        offset: int = None,
                        limit: int = None
                        ) -> Levels | Level:
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

            return Levels.from_dict(self, res)
    
    async def get_level(self, id: int):
            req = await self._session.head(f"database/levels/{id}")
            try:
                req.raise_for_status()
            except:
                raise APIError("database/levels/{}".format(id), "Level not accessible")
            query = await self._session.get(f"database/levels/{id}")
            resptext = await query.json()

            return Level.from_dict(resptext["level"])
    
    async def like_level(self, id: int, action: str["like" | "unlike"]):
        match action:
            case "like":
                req = await self._session.put(f"database/levels/{id}/like", json={"action": "like"})
                try:
                    req.raise_for_status()
                except:
                    raise APIError("database/levels/{}/likes".format(id), f"Request failed with status code {req.status}")
                res = await req.json()
                return True if res.get("success", False) else False
            case "unlike":
                req = await self._session.put(f"database/levels/{id}/like", json={"action": "unlike"})
                try:
                    req.raise_for_status()
                except:
                    raise APIError("database/levels/{}/likes".format(id), f"Request failed with status code {req.status}")
                res = await req.json()
                return True if res.get("success", False) else False
            case _: raise SyntaxError("action")
        
    async def get_level_file(self, id: int):
        req = await self._session.get(f"database/levels/{id}/level.adofai")
        return await req.text() # Do whatever with this, its just leveladofai
    
    async def get_likes(self, id: int):
        req = await self._session.get(f"database/levels/{id}/isLiked")
        try: req.raise_for_status()
        except: raise APIError(f"database/levels/{id}/isLiked", "Server error, probably.")
        res = await req.json()
        return res["likes"]

    async def get_player(self, id: int):
        req = await self._session.get(f"database/players/{id}")
        res = await req.json()
        return Player.from_dict(res)
         
    async def get_players(self, name: str):
        req1 = await self._session.get(f"database/players/search/{name}")
        res1 = await req1.json()

        plist = []
        for player in res1:
            id = player["id"]
            req = await self._session.get(f"database/players/{id}")
            res = await req.json()
            plist.append(Player.from_dict(res))
        return plist