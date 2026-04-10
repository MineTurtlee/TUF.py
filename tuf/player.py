import typing
from dataclasses import dataclass
from datetime import datetime

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
    top_clear: 
    top_12k_clear: 
    total_passes: int
    created_at: datetime
    updated_at: datetime
    passes: list
    top_scores: list
    potential_top_scores: list
    unique_passes: dict
    stats: dict