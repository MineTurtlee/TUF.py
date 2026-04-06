from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
from aiohttp import ClientSession
from .curation import Curation

def _dt(s: str) -> datetime:
    return datetime.fromisoformat(s)

@dataclass
class Creator:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    user_id: Optional[int | str]
    creator_aliases: list[dict[str, Any]]

    @classmethod
    def from_dict(cls, d: dict) -> "Creator":
        return cls(**{**d, "created_at": _dt(d["created_at"]), "updated_at": _dt(d["updated_at"])})

@dataclass
class LevelCredits:
    id: int
    level_id: int
    is_owner: bool
    creator_id: int
    role: str
    is_verified: bool
    creator: Creator

    @classmethod
    def from_dict(cls, d: dict) -> "LevelCredits":
        return cls(**{**d, "creator": Creator.from_dict(d["creator"])})

@dataclass
class Difficulty:
    id: int
    name: str
    type: str
    icon: str
    emoji: str
    color: str
    created_at: datetime
    updated_at: datetime
    base_score: int
    sort_order: int
    legacy_diff: str
    legacy_icon: str
    legacy_emoji: str

    @classmethod
    def from_dict(cls, d: dict) -> "Difficulty":
        return cls(**{**d, "created_at": _dt(d["created_at"]), "updated_at": _dt(d["updated_at"])})

@dataclass
class Level:
    id: int
    charter: str
    charters: list[str]
    vfxer: Optional[str]
    vfxers: list[str]
    team: Optional[str]
    song_name: str
    artist: str
    diff_id: int
    video_link: str
    dl_link: Optional[str]
    legacy_dl_link: Optional[str]
    workshop_link: Optional[str]
    public_comments: Optional[str]
    rate_needed: bool
    rerate_reason: Optional[str]
    rerate_number: Optional[str]
    previous_diff_id: int
    is_announced: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    is_hidden: bool
    is_verified: bool
    is_externally_available: bool
    team_id: Optional[int]
    suffix: Optional[str]
    clears: int
    likes: int
    rating_accuracy: int
    difficulty: Difficulty
    aliases: list
    level_credits: list[LevelCredits]
    team_object: Optional[Any]
    curation: Optional[Curation]
    tags: list

    @classmethod
    def from_dict(cls, d: dict) -> "Level":
        return cls(
            **{k: v for k, v in d.items() if k not in ("created_at", "updated_at", "difficulty", "level_credits", "curation")},
            created_at=_dt(d["created_at"]),
            updated_at=_dt(d["updated_at"]),
            difficulty=Difficulty.from_dict(d["difficulty"]),
            level_credits=[LevelCredits.from_dict(c) for c in d["level_credits"]],
            curation=Curation.from_dict(d["curation"]) if d.get("curation") else None
        )

class Levels:
    def __init__(self,
                 session: ClientSession,
                 levels: list[Level],
                 curpage: int,
                 offset: int,
                 limit: int,
                 hasmore: bool,
                 total: int
                 ):
        self._page = curpage
        self._offset = offset
        self._limit = limit
        self._more = hasmore
        self._total = total
        self._list = levels
        self._session = session

    async def next_page(self) -> Optional["Levels"]:
        if not self._more:
            return self
        req = await self._session.get("database/levels")

    @property
    def total_pages(self) -> int:
        return -(-self._total // self._limit)

    def __repr__(self):
        return f"<Levels page={self._page}/{self.total_pages} offset={self._offset} total={self._total}>"

    @classmethod
    def from_dict(cls, session: ClientSession, d: dict) -> "Levels":
        return cls(
            session=session,
            levels=[Level.from_dict(l) for l in d["results"]],
            curpage=d["page"],
            offset=d["offset"],
            limit=d["limit"],
            hasmore=d["hasMore"],
            total=d["total"]
        )