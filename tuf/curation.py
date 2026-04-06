from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
from aiohttp import ClientSession

def _dt(s: str) -> datetime:
    return datetime.fromisoformat(s)

@dataclass
class CurationType:
    id: int
    name: str
    icon: str
    color: str
    abilities: int
    sort_order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, d: dict) -> "CurationType":
        return cls(**{**d, "created_at": _dt(d["created_at"]), "updated_at": _dt(d["updated_at"])})

@dataclass
class CurationAssignment:
    nickname: str
    username: str
    avatar_url: str

    @classmethod
    def from_dict(cls, d: dict) -> "CurationAssignment":
        return cls(**d)

@dataclass
class Curation:
    id: int
    level_id: int
    type_id: int
    short_desc: Optional[str]
    description: Optional[str]
    preview_link: Optional[str]
    custom_css: Optional[str]
    custom_color: str
    assigned_by: str
    created_at: datetime
    updated_at: datetime
    type: CurationType
    curation_scheds: list
    assigned_by_user: CurationAssignment

    @classmethod
    def from_dict(cls, d: dict) -> "Curation":
        return cls(
            **{k: v for k, v in d.items() if k not in ("created_at", "updated_at", "type", "assigned_by_user")},
            created_at=_dt(d["created_at"]),
            updated_at=_dt(d["updated_at"]),
            type=CurationType.from_dict(d["type"]),
            assigned_by_user=CurationAssignment.from_dict(d["assigned_by_user"])
        )