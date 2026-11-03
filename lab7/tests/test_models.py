import pytest
from app.exceptions import AppError, ValidationError
from app.models import BaseEntity, Currency, Subscription, User

def test_user_created():
    user = User("ivan", "Ivan@Example.com")
    assert user.username == "ivan"
    assert user.email == "ivan@example.com"
    assert user.id == 1

def test_ids_are_sequential():
    first, second = User("anna", "a@ex.ru"), User("boris", "b@ex.ru")
    assert (first.id, second.id) == (1, 2)

def test_invalid_username():
    with pytest.raises(ValidationError):
        User("x", "a@ex.ru")

def test_invalid_email():
    with pytest.raises(ValidationError):
        User("anna", "no-at.ru")

def test_id_is_read_only():
    user = User("anna", "a@ex.ru")
    with pytest.raises(AttributeError):
        user.id = 100

def test_str_and_repr():
    user = User("anna", "a@ex.ru")
    assert str(user) == "anna <a@ex.ru>"
    assert repr(user) == "User(id=1, username='anna')"

def test_subscriptions_equal():
    user, currency = User("anna", "a@ex.ru"), Currency("USD", "Доллар США")
    assert Subscription(user, currency) == Subscription(user, currency)