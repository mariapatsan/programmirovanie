"""Сервисный слой: регистрация пользователей и управление подписками."""
from __future__ import annotations

import json
from pathlib import Path

from app.exceptions import DuplicateError, InactiveUserError, NotFoundError
from app.models import Currency, Rate, Subscription, User
from app.providers import RateProvider


class CurrencyTracker:
    """Хранит пользователей, валюты и подписки в памяти."""

    def __init__(self, provider: RateProvider) -> None:
        self._provider = provider
        self._users: dict[int, User] = {}
        self._currencies: dict[str, Currency] = {}
        self._subscriptions: set[Subscription] = set()

    # ---------- пользователи ----------
    def register_user(self, username: str, email: str, full_name: str | None = None) -> User:
        user = User(username, email, full_name)
        for existing in self._users.values():
            if existing.username.lower() == user.username.lower():
                raise DuplicateError(f"Имя {user.username!r} уже занято")
            if existing.email == user.email:
                raise DuplicateError(f"Email {user.email!r} уже зарегистрирован")
        self._users[user.id] = user
        return user

    def get_user(self, user_id: int) -> User:
        try:
            return self._users[user_id]
        except KeyError:
            raise NotFoundError(f"Пользователь с id={user_id} не найден") from None

    @property
    def users(self) -> list[User]:
        return list(self._users.values())

    # ---------- валюты ----------
    def sync_currencies(self) -> int:
        added = 0
        for code, rate in self._provider.get_rates().items():
            if code in self._currencies:
                self._currencies[code].name = rate.name
                self._currencies[code].num_code = rate.num_code
            else:
                self._currencies[code] = Currency(code, rate.name, rate.num_code)
                added += 1
        return added

    def get_currency(self, code: str) -> Currency:
        code = code.strip().upper()
        if code not in self._currencies:
            raise NotFoundError(f"Валюта {code!r} не найдена")
        return self._currencies[code]

    @property
    def currencies(self) -> list[Currency]:
        return sorted(self._currencies.values(), key=lambda c: c.code)

    # ---------- подписки ----------
    def subscribe(self, user_id: int, code: str) -> Subscription:
        user = self.get_user(user_id)
        if not user.is_active:
            raise InactiveUserError(f"Пользователь {user.username!r} деактивирован")
        subscription = Subscription(user, self.get_currency(code))
        if subscription in self._subscriptions:
            raise DuplicateError("Подписка уже существует")
        self._subscriptions.add(subscription)
        return subscription

    def unsubscribe(self, user_id: int, code: str) -> None:
        subscription = Subscription(self.get_user(user_id), self.get_currency(code))
        if subscription not in self._subscriptions:
            raise NotFoundError("Подписка не найдена")
        self._subscriptions.remove(subscription)

    def get_user_currencies(self, user_id: int) -> list[Currency]:
        user = self.get_user(user_id)
        found = [s.currency for s in self._subscriptions if s.user == user]
        return sorted(found, key=lambda c: c.code)

    def get_subscribers(self, code: str) -> list[User]:
        currency = self.get_currency(code)
        return [s.user for s in self._subscriptions if s.currency == currency]

    def get_user_rates(self, user_id: int) -> list[Rate]:
        rates = self._provider.get_rates()
        return [rates[c.code] for c in self.get_user_currencies(user_id) if c.code in rates]

    # ---------- сохранение в JSON ----------
    def save(self, path: str) -> None:
        """Сохранить состояние трекера в JSON."""
        data = {
            "users": [u.to_dict() for u in self._users.values()],
            "currencies": [c.to_dict() for c in self._currencies.values()],
            "subscriptions": [
                {"user_id": s.user.id, "currency_id": s.currency.id}
                for s in self._subscriptions
            ],
        }
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def load(self, path: str) -> None:
        """Загрузить состояние из JSON (упрощённо)."""
        data = json.loads(Path(path).read_text())
        self._users.clear()
        self._currencies.clear()
        self._subscriptions.clear()

        user_map = {}
        for u in data["users"]:
            user = User(u["username"], u["email"], full_name=u.get("full_name"))
            if not u.get("is_active", True):
                user.deactivate()
            self._users[user.id] = user
            user_map[u["id"]] = user  # <-- сопоставляем старый id с новым объектом

        currency_map = {}
        for c in data["currencies"]:
            currency = Currency(c["code"], c["name"], num_code=c.get("num_code"))
            self._currencies[currency.code] = currency
            currency_map[c["id"]] = currency  # <-- сопоставляем старый id валюты

        for s in data["subscriptions"]:
            user = user_map[s["user_id"]]
            currency = currency_map[s["currency_id"]]
            self._subscriptions.add(Subscription(user, currency))