import pytest

from tuf.client import TUFClient
from tuf.errors import SyntaxError, ConflictingArgs


@pytest.mark.asyncio
async def test_get_levels_requires_id_or_name():
    client = TUFClient("u", "p")
    with pytest.raises(SyntaxError):
        await client.get_levels()


@pytest.mark.asyncio
async def test_get_levels_conflicting_args():
    client = TUFClient("u", "p")
    with pytest.raises(ConflictingArgs):
        await client.get_levels(id=1, name="something")


@pytest.mark.asyncio
async def test_close_without_session_is_noop():
    client = TUFClient("u", "p")
    # should not raise
    await client.close()
    assert client._session is None
