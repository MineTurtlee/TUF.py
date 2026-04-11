from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any, TYPE_CHECKING
from aiohttp import ClientSession
from .curation import Curation
from .utils import _dt

if TYPE_CHECKING:
    from .client import TUFClient

@dataclass
class Creator:
    id: int
    name: str
    is_verified: bool
    user_id: Optional[int | str]
    creator_aliases: list[dict[str, Any]]

    @classmethod
    def from_dict(cls, d: dict) -> "Creator":
        remap = {
            "userId": "user_id",
            "isVerified": "is_verified",
            "creatorAliases": "creator_aliases",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            id=r["id"],
            name=r["name"],
            is_verified=r.get("is_verified", False),
            user_id=r.get("user_id"),
            creator_aliases=r.get("creator_aliases", []),
        )

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
        remap = {
            "levelId": "level_id",
            "isOwner": "is_owner",
            "creatorId": "creator_id",
            "isVerified": "is_verified",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            id=r["id"],
            level_id=r["level_id"],
            is_owner=r.get("is_owner", False),
            creator_id=r["creator_id"],
            role=r["role"],
            is_verified=r.get("is_verified", False),
            creator=Creator.from_dict(r["creator"]),
        )

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
        remap = {
            "createdAt": "created_at",
            "updatedAt": "updated_at",
            "baseScore": "base_score",
            "sortOrder": "sort_order",
            "legacy": "legacy_diff",
            "legacyIcon": "legacy_icon",
            "legacyEmoji": "legacy_emoji",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            id=r["id"],
            name=r["name"],
            type=r["type"],
            icon=r["icon"],
            emoji=r["emoji"],
            color=r["color"],
            created_at=_dt(r["created_at"]),
            updated_at=_dt(r["updated_at"]),
            base_score=r["base_score"],
            sort_order=r["sort_order"],
            legacy_diff=r["legacy_diff"],
            legacy_icon=r.get("legacy_icon"),
            legacy_emoji=r.get("legacy_emoji"),
        )

@dataclass
class Level:
    id: int
    charter: Optional[str]
    charters: Optional[list[str]]
    vfxer: Optional[str]
    vfxers: Optional[list[str]]
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
        remap = {
            "song": "song_name",
            "diffId": "diff_id",
            "videoLink": "video_link",
            "dlLink": "dl_link",
            "legacyDllink": "legacy_dl_link",
            "workshopLink": "workshop_link",
            "publicComments": "public_comments",
            "toRate": "rate_needed",
            "rerateReason": "rerate_reason",
            "rerateNum": "rerate_number",
            "previousDiffId": "previous_diff_id",
            "isAnnounced": "is_announced",
            "isDeleted": "is_deleted",
            "createdAt": "created_at",
            "updatedAt": "updated_at",
            "isHidden": "is_hidden",
            "isVerified": "is_verified",
            "isExternallyAvailable": "is_externally_available",
            "teamId": "team_id",
            "ratingAccuracy": "rating_accuracy",
            "levelCredits": "level_credits",
            "teamObject": "team_object",
        }
        skip = {
            "created_at", "updated_at", "difficulty",
            "level_credits", "curation", "tags",
            # drop fields not in dataclass
            "songId", "songObject", "firstPass", "highestAccuracy",
            "ppBaseScore", "previousBaseScore", "baseScore", "totalRatingAccuracyVotes",
            "curations", "curationSchedules",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            id=r["id"],
            charter=r.get("charter"),
            charters=r.get("charters"),
            vfxer=r.get("vfxer"),
            vfxers=r.get("vfxers"),
            team=r.get("team"),
            song_name=r["song_name"],
            artist=r["artist"],
            diff_id=r["diff_id"],
            video_link=r["video_link"],
            dl_link=r.get("dl_link"),
            legacy_dl_link=r.get("legacy_dl_link"),
            workshop_link=r.get("workshop_link"),
            public_comments=r.get("public_comments"),
            rate_needed=r.get("rate_needed", False),
            rerate_reason=r.get("rerate_reason"),
            rerate_number=r.get("rerate_number"),
            previous_diff_id=r.get("previous_diff_id", 0),
            is_announced=r.get("is_announced", False),
            is_deleted=r.get("is_deleted", False),
            created_at=_dt(r["created_at"]),
            updated_at=_dt(r["updated_at"]),
            is_hidden=r.get("is_hidden", False),
            is_verified=r.get("is_verified", False),
            is_externally_available=r.get("is_externally_available", False),
            team_id=r.get("team_id"),
            suffix=r.get("suffix"),
            clears=r.get("clears", 0),
            likes=r.get("likes", 0),
            rating_accuracy=r.get("rating_accuracy", 0),
            difficulty=Difficulty.from_dict(r["difficulty"]),
            aliases=r.get("aliases", []),
            level_credits=[LevelCredits.from_dict(c) for c in r.get("level_credits", [])],
            team_object=r.get("team_object"),
            curation=Curation.from_dict(r["curation"]) if r.get("curation") else None,
            tags=r.get("tags", []),
        )

class Levels:
    def __init__(self,
                 client: "TUFClient",
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
        self._connection = client

    async def next_page(self) -> Optional["Levels"]:
        if not self._more:
            return self
        return await self._connection.get_levels(
            name=self._list[0].song_name,
            page = self._page + 1
        )

    @property
    def total_pages(self) -> int:
        return -(-self._total // self._limit)

    def __repr__(self):
        return f"<Levels page={self._page}/{self.total_pages} offset={self._offset} total={self._total}>"

    @classmethod
    def from_dict(cls, session: ClientSession, d: dict) -> "Levels":
        return cls(
            session,
            [Level.from_dict(l) for l in d["results"]],
            d["page"],
            d["offset"],
            d["limit"],
            d["hasMore"],
            d["total"]
        )