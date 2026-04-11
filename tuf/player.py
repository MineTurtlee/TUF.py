import typing
from dataclasses import dataclass
from datetime import datetime
from .clears import Score, TopClear
from .utils import _dt

@dataclass
class User:
    # IDK if this is the user for TUF or the Player, maybe its for TUF user
    id: str # UUID hash for userdata
    username: str
    nickname: str # Display name
    avatar_url: str # Avatar url on TUF or wtv
    is_super_admin: bool
    is_rater: bool
    player_id: int # playerid goes brrr (/player/{id})
    permission_flags: str # flags
    creator: typing.Optional[typing.Any]

    @classmethod
    def from_dict(cls, d: dict) -> "User":
        remap = {
            "avatarUrl": "avatar_url",
            "isSuperAdmin": "is_super_admin",
            "isRater": "is_rater",
            "playerId": "player_id",
            "permissionFlags": "permission_flags",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            id=r["id"],
            username=r["username"],
            nickname=r["nickname"],
            avatar_url=r["avatar_url"],
            is_super_admin=r.get("is_super_admin", False),
            is_rater=r.get("is_rater", False),
            player_id=r["player_id"],
            permission_flags=r.get("permission_flags", ""),
            creator=r.get("creator"),
        )
    
@dataclass
class Player:
    id: int
    name: str
    country: str # 2-digit country code
    is_banned: bool # If user is banned please specify it lol (if hidden please no)
    is_submissions_paused: bool # Idk
    profile_pic: str # Same as avatar URL for ordinary users
    avatar_url: str  # For cardinary users ig this is different
    username: str # Username on TUF
    discord_username: str # Discord user (if OAuth2 linked)
    discord_avatar: str # Discord avatar (may not match TUF avatar)
    discord_avatar_id: str # A hash
    discord_id: str # Discord user ID
    user: User
    ranked_score: float
    general_score: float # Total score, different from ranked
    pure_perfect_score: float
    worlds_first_score: float
    score_12k: float
    average_xacc: float
    universal_passes: int
    worlds_first: int
    top_clear: TopClear
    top_12k_clear: TopClear
    total_passes: int
    created_at: datetime
    updated_at: datetime
    passes: list
    top_scores: list[Score]
    potential_top_scores: list[Score]
    unique_passes: dict # Maybe none, guess?
    stats: dict

    @classmethod
    def from_dict(cls, d: dict) -> "Player":
        remap = {
            "isBanned": "is_banned",
            "isSubmissionsPaused": "is_submissions_paused",
            "pfp": "profile_pic",
            "avatarUrl": "avatar_url",
            "discordUsername": "discord_username",
            "discordAvatar": "discord_avatar",
            "discordAvatarId": "discord_avatar_id",
            "discordId": "discord_id",
            "rankedScore": "ranked_score",
            "generalScore": "general_score",
            "ppScore": "pure_perfect_score",
            "wfScore": "worlds_first_score",
            "score12K": "score_12k",
            "averageXacc": "average_xacc",
            "universalPassCount": "universal_passes",
            "worldsFirstCount": "worlds_first",
            "topDiff": "top_clear",
            "top12kDiff": "top_12k_clear",
            "totalPasses": "total_passes",
            "createdAt": "created_at",
            "updatedAt": "updated_at",
            "topScores": "top_scores",
            "potentialTopScores": "potential_top_scores",
            "uniquePasses": "unique_passes",
        }
        skip = {
            "created_at", "updated_at", "user",
            "top_clear", "top_12k_clear",
            "top_scores", "potential_top_scores",
        }
        r = {remap.get(k, k): v for k, v in d.items()}
        return cls(
            **{k: v for k, v in r.items() if k not in skip},
            created_at=_dt(r["created_at"]),
            updated_at=_dt(r["updated_at"]),
            user=User.from_dict(r["user"]),
            top_clear=TopClear.from_dict(r["top_clear"]),
            top_12k_clear=TopClear.from_dict(r["top_12k_clear"]),
            top_scores=[Score.from_dict(s) for s in r["top_scores"]],
            potential_top_scores=[Score.from_dict(s) for s in r["potential_top_scores"]],
        )