import pytest
from app.exceptions import DuplicateError, NotFoundError

def test_register_user(tracker):
    user = tracker.register_user("anna", "a@ex.ru")
    assert tracker.get_user(user.id) is user

def test_register_duplicate(tracker):
    tracker.register_user("anna", "a@ex.ru")
    with pytest.raises(DuplicateError):
        tracker.register_user("ANNA", "b@ex.ru")

def test_subscribe(tracker):
    user = tracker.register_user("anna", "a@ex.ru")
    tracker.subscribe(user.id, "usd")
    assert [c.code for c in tracker.get_user_currencies(user.id)] == ["USD"]

def test_unsubscribe(tracker):
    user = tracker.register_user("anna", "a@ex.ru")
    tracker.subscribe(user.id, "USD")
    tracker.unsubscribe(user.id, "USD")
    with pytest.raises(NotFoundError):
        tracker.unsubscribe(user.id, "USD")