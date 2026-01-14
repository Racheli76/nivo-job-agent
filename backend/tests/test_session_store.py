import pytest
import asyncio
from session_store import InMemorySessionStore


def test_inmemory_set_get_delete():
    s = InMemorySessionStore()
    sid = 'test123'
    loop = asyncio.get_event_loop()

    loop.run_until_complete(s.set(sid, {'cv_text': 'hello'}))
    got = loop.run_until_complete(s.get(sid))
    assert got['cv_text'] == 'hello'

    loop.run_until_complete(s.delete(sid))
    assert loop.run_until_complete(s.get(sid)) is None
