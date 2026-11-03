from app.services import CurrencyTracker
from app.providers import StaticRateProvider

def test_save_and_load(tmp_path, tracker):
    user = tracker.register_user("anna", "a@ex.ru")
    tracker.subscribe(user.id, "USD")
    
    path = tmp_path / "data.json"
    tracker.save(str(path))
    
    new_tracker = CurrencyTracker(StaticRateProvider.demo())
    new_tracker.load(str(path))
    
    # Ищем пользователя по username, так как id при загрузке изменился
    loaded_user = next(u for u in new_tracker.users if u.username == "anna")
    assert loaded_user.username == "anna"
    assert [c.code for c in new_tracker.get_user_currencies(loaded_user.id)] == ["USD"]