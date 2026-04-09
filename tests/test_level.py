from datetime import datetime

from tuf.level import Level, Levels


def make_sample_level_dict():
    ts = "2023-01-01T00:00:00"
    creator = {
        "id": 1,
        "name": "creator1",
        "created_at": ts,
        "updated_at": ts,
        "is_verified": False,
        "user_id": None,
        "creator_aliases": []
    }

    level_credit = {
        "id": 10,
        "level_id": 100,
        "is_owner": True,
        "creator_id": 1,
        "role": "author",
        "is_verified": False,
        "creator": creator
    }

    difficulty = {
        "id": 5,
        "name": "Hard",
        "type": "standard",
        "icon": "icon.png",
        "emoji": ":fire:",
        "color": "#fff",
        "created_at": ts,
        "updated_at": ts,
        "base_score": 100,
        "sort_order": 1,
        "legacy_diff": "H",
        "legacy_icon": "i",
        "legacy_emoji": "e"
    }

    level = {
        "id": 100,
        "charter": "",
        "charters": [],
        "vfxer": None,
        "vfxers": [],
        "team": None,
        "song_name": "Song",
        "artist": "Artist",
        "diff_id": 5,
        "video_link": "",
        "dl_link": None,
        "legacy_dl_link": None,
        "workshop_link": None,
        "public_comments": None,
        "rate_needed": False,
        "rerate_reason": None,
        "rerate_number": None,
        "previous_diff_id": 0,
        "is_announced": False,
        "is_deleted": False,
        "created_at": ts,
        "updated_at": ts,
        "is_hidden": False,
        "is_verified": False,
        "is_externally_available": False,
        "team_id": None,
        "suffix": None,
        "clears": 0,
        "likes": 0,
        "rating_accuracy": 0,
        "difficulty": difficulty,
        "aliases": [],
        "level_credits": [level_credit],
        "team_object": None,
        "curation": None,
        "tags": []
    }

    return level


def test_level_from_dict_basic():
    d = make_sample_level_dict()
    lvl = Level.from_dict(d)
    assert isinstance(lvl.created_at, datetime)
    assert hasattr(lvl, "difficulty")
    assert len(lvl.level_credits) == 1


def test_levels_from_dict_and_total_pages():
    level_dict = make_sample_level_dict()
    payload = {"results": [level_dict], "page": 1, "offset": 0, "limit": 10, "hasMore": False, "total": 1}
    levels = Levels.from_dict(None, payload)
    assert levels.total_pages == 1
    assert "page=1/1" in repr(levels)
