from dataclasses import dataclass
import typing
from datetime import datetime
from .utils import _dt

@dataclass
class Score:
    id: int
    impact: float

    @classmethod
    def from_dict(cls, d: dict) -> "Score":
        return cls(id=d["id"], impact=d["impact"])

@dataclass
class TopClear:
    id: int # Can be 0 if no stats found
    name: str # Diffname
    type: str # Diff type (pgu/special/etc)
    icon: str 
    emoji: str
    color: str
    created_at: datetime
    updated_at: datetime
    base_score: float
    sort_order: int
    legacy: str
    legacy_icon: typing.Optional[str]
    legacy_emoji: typing.Optional[str]

    @classmethod
    def from_dict(cls, d: dict) -> "TopClear":
        remap = {
            "createdAt": "created_at",
            "updatedAt": "updated_at",
            "baseScore": "base_score",
            "sortOrder": "sort_order",
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
            legacy=r["legacy"],
            legacy_icon=r.get("legacy_icon"),
            legacy_emoji=r.get("legacy_emoji"),
        )