from typing import Optional
from dataclasses import dataclass
from .utils import _dt
from datetime import datetime

@dataclass
class CurationType:
    id: int
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None
    abilities: Optional[int] = None
    sort_order: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, d: dict) -> "CurationType":
        remap = {
            "createdAt": "created_at",
            "updatedAt": "updated_at",
            "sortOrder": "sort_order",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            id=r["id"],
            name=r["name"],
            icon=r.get("icon"),
            color=r.get("color"),
            abilities=r.get("abilities"),
            sort_order=r.get("sort_order"),
            created_at=_dt(r["created_at"]) if r.get("created_at") else None,
            updated_at=_dt(r["updated_at"]) if r.get("updated_at") else None,
        )

@dataclass
class CurationAssignment:
    nickname: str
    username: str
    avatar_url: str

    @classmethod
    def from_dict(cls, d: dict) -> "CurationAssignment":
        return cls(
            nickname=d["nickname"],
            username=d["username"],
            avatar_url=d["avatarUrl"],
        )

@dataclass
class Curation:
    id: int
    level_id: int
    type_id: Optional[int]
    short_desc: Optional[str]
    description: Optional[str]
    preview_link: Optional[str]
    custom_css: Optional[str]
    custom_color: Optional[str]
    assigned_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    type: Optional[CurationType]
    curation_scheds: list
    assigned_by_user: Optional[CurationAssignment]

    @classmethod
    def from_dict(cls, d: dict) -> "Curation":
        remap = {
            "levelId": "level_id",
            "typeId": "type_id",
            "shortDescription": "short_desc",
            "previewLink": "preview_link",
            "customCSS": "custom_css",
            "customColor": "custom_color",
            "assignedBy": "assigned_by",
            "createdAt": "created_at",
            "updatedAt": "updated_at",
            "assignedByUser": "assigned_by_user",
            "curationSchedules": "curation_scheds",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            id=r["id"],
            level_id=r.get("level_id"),
            type_id=r.get("type_id"),
            short_desc=r.get("short_desc"),
            description=r.get("description"),
            preview_link=r.get("preview_link"),
            custom_css=r.get("custom_css"),
            custom_color=r.get("custom_color"),
            assigned_by=r.get("assigned_by"),
            created_at=_dt(r["created_at"]) if r.get("created_at") else None,
            updated_at=_dt(r["updated_at"]) if r.get("updated_at") else None,
            type=CurationType.from_dict(r["type"]) if r.get("type") else None,
            curation_scheds=r.get("curation_scheds", []),
            assigned_by_user=CurationAssignment.from_dict(r["assigned_by_user"]) if r.get("assigned_by_user") else None,
        )