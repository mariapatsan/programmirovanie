import pytest
from app.exceptions import InactiveUserError, ValidationError
from app.models import User


@pytest.mark.parametrize("bad_name", [
    "A",                    # слишком коротко
    "A" * 101,              # слишком длинно
    "Anna123",              # цифры не разрешены
    "Anna!",                # спецсимволы
])
def test_invalid_full_name(bad_name):
    with pytest.raises(ValidationError):
        User("anna", "a@ex.ru", full_name=bad_name)


def test_full_name_none_allowed():
    assert User("anna", "a@ex.ru", full_name=None).full_name is None
    assert User("anna", "a@ex.ru", full_name="Иванова Анна").full_name == "Иванова Анна"


def test_is_active_read_only_and_toggle():
    user = User("anna", "a@ex.ru")
    assert user.is_active is True
    with pytest.raises(AttributeError):
        user.is_active = False
    
    user.deactivate()
    assert user.is_active is False
    user.activate()
    assert user.is_active is True


def test_inactive_user_cannot_subscribe(tracker):
    user = tracker.register_user("anna", "a@ex.ru")
    user.deactivate()
    with pytest.raises(InactiveUserError):
        tracker.subscribe(user.id, "USD")