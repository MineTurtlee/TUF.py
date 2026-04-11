from dataclasses import dataclass
import typing
from datetime import datetime

@dataclass
class Score:
    id: int
    impact: float

    @classmethod
    def from_dict(cls, d: dict) -> "Score":
        return cls(
            **{k: v for k, v in d.items()}
        )

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
        return cls(
            **{k: v for k, v in d.items()}
        )