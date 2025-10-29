import datetime as dt
from storage import save_data, load_data
from app import _calc_streaks

def test_streak_calculation():
    """Testaa peräkkäisten päivien laskennan"""
    days = [
        dt.date(2025, 10, 25),
        dt.date(2025, 10, 26),
        dt.date(2025, 10, 28),
        dt.date(2025, 10, 29),
    ]
    current, longest = _calc_streaks(days)
    assert longest == 2
    assert isinstance(current, int)

def test_save_and_load(tmp_path):
    """Testaa JSON-tallennus ja lataus"""
    data = [{"date": "2025-10-29", "habit": "testi", "value": "1"}]
    file_path = tmp_path / "data.json"

    save_data(data)
    loaded = load_data()
    assert isinstance(loaded, list)
    assert all("habit" in e for e in loaded)