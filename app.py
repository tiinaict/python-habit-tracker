# app.py
# Habit Tracker – lisää, listaa, yhteenveto, streakit, viikon näkymä

import datetime as dt
from collections import defaultdict
from typing import List, Dict, Tuple
from storage import load_data, save_data


def prompt(msg: str) -> str:
    try:
        return input(msg).strip()
    except EOFError:
        return ""


def today_str() -> str:
    return dt.date.today().isoformat()


def add_entry(data: list) -> None:
    """Lisää uusi tapa-merkintä"""
    habit = prompt("Tapa (esim. juoksu, luku): ")
    if not habit:
        print("❌ Tapa on pakollinen.")
        return

    value = prompt("Arvo (esim. 1 kerta, 30 min) [enter jos ei tarvetta]: ")
    date_in = prompt(f"Päivämäärä (YYYY-MM-DD) [enter = {today_str()}]: ")
    date = date_in if date_in else today_str()

    try:
        dt.date.fromisoformat(date)
    except ValueError:
        print("❌ Päivämäärän muoto oltava YYYY-MM-DD.")
        return

    entry = {"date": date, "habit": habit, "value": value or "1"}
    data.append(entry)
    print("✅ Tallennettu.")


def list_entries(data: list) -> None:
    """Näytä kaikki merkinnät aikajärjestyksessä"""
    if not data:
        print("Ei merkintöjä.")
        return
    data_sorted = sorted(data, key=lambda e: e.get("date", ""))
    for i, e in enumerate(data_sorted, start=1):
        print(f"{i:>3}. {e['date']} | {e['habit']:<12} | {e.get('value','')}")


def summarize(data: list) -> None:
    """Laskee montako kertaa kukin tapa on tehty"""
    if not data:
        print("Ei merkintöjä.")
        return
    counts = defaultdict(int)
    for e in data:
        counts[e["habit"]] += 1
    print("\n📊 YHTEENVETO (kertojen määrä)")
    for habit, n in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
        print(f"- {habit:<12} {n} krt")


def _calc_streaks(dates: List[dt.date]) -> Tuple[int, int]:
    """Palauttaa (current_streak, longest_streak) peräkkäisille päiville."""
    if not dates:
        return 0, 0
    dates = sorted(set(dates))
    longest = 1
    current_run = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + dt.timedelta(days=1):
            current_run += 1
        else:
            longest = max(longest, current_run)
            current_run = 1
    longest = max(longest, current_run)
    return current_run, longest  # current_run on viimeisin jakso


def show_streaks(data: list) -> None:
    """Tulostaa nykyisen ja pisimmän streakin jokaiselle tavalle."""
    if not data:
        print("Ei merkintöjä.")
        return
    habit_dates: Dict[str, List[dt.date]] = {}
    for e in data:
        try:
            d = dt.date.fromisoformat(e["date"])
        except Exception:
            continue
        habit = (e.get("habit") or "").strip() or "(nimetön)"
        habit_dates.setdefault(habit, []).append(d)

    print("\n🔥 STREAKIT (peräkkäiset päivät)")
    for habit, dates in sorted(habit_dates.items()):
        current, longest = _calc_streaks(dates)
        latest = max(dates).isoformat() if dates else "-"
        print(f"- {habit:<12}  nykyinen: {current} pv  | pisin: {longest} pv  | viimeisin: {latest}")


def list_last_week(data: list) -> None:
    """Näytä vain viimeisen 7 päivän merkinnät"""
    if not data:
        print("Ei merkintöjä.")
        return
    today = dt.date.today()
    week_ago = today - dt.timedelta(days=7)
    recent = []
    for e in data:
        try:
            d = dt.date.fromisoformat(e["date"])
            if week_ago <= d <= today:
                recent.append(e)
        except Exception:
            continue
    if not recent:
        print("Ei merkintöjä viimeisen viikon ajalta.")
        return
    recent_sorted = sorted(recent, key=lambda e: e.get("date", ""))
    print(f"\n📅 Merkinnät viimeiseltä 7 päivältä ({week_ago}–{today})")
    for i, e in enumerate(recent_sorted, start=1):
        print(f"{i:>3}. {e['date']} | {e['habit']:<12} | {e.get('value','')}")


def main():
    data = load_data()
    while True:
        print("\n=== HABIT TRACKER ===")
        print("1) Lisää merkintä")
        print("2) Listaa kaikki merkinnät")
        print("3) Näytä yhteenveto")
        print("4) Näytä streakit")
        print("5) Näytä viimeisen viikon merkinnät")
        print("6) Tallenna ja lopeta")
        choice = prompt("Valinta: ")

        if choice == "1":
            add_entry(data)
        elif choice == "2":
            list_entries(data)
        elif choice == "3":
            summarize(data)
        elif choice == "4":
            show_streaks(data)
        elif choice == "5":
            list_last_week(data)
        elif choice == "6":
            save_data(data)
            print("💾 Tallennettu. Moikka!")
            break
        else:
            print("Tuntematon komento.")


if __name__ == "__main__":
    main()
    data_sorted = sorted(data, key=lambda e: e.get("date", ""))
    for i, e in enumerate(data_sorted, start=1):
        print(f"{i:>3}. {e['date']} | {e['habit']:<12} | {e.get('value','')}")


def summarize(data: list) -> None:
    """Laskee montako kertaa kukin tapa on tehty"""
    if not data:
        print("Ei merkintöjä.")
        return

    counts = defaultdict(int)
    for e in data:
        counts[e["habit"]] += 1

    print("\n📊 YHTEENVETO (kertojen määrä)")
    for habit, n in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
        print(f"- {habit:<12} {n} krt")


def _calc_streaks(dates: List[dt.date]) -> Tuple[int, int]:
    """
    Palauttaa (current_streak, longest_streak) listalle päiviä (uniikit), nousevassa järjestyksessä.
    current_streak = viimeisimpään päivään päättyvän jakson pituus
    """
    if not dates:
        return 0, 0

    dates = sorted(set(dates))
    longest = 1
    current_run = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + dt.timedelta(days=1):
            current_run += 1
        else:
            longest = max(longest, current_run)
            current_run = 1

    longest = max(longest, current_run)
    current_streak = current_run  # viimeisen jakson pituus
    return current_streak, longest


def show_streaks(data: list) -> None:
    """Tulostaa nykyisen ja pisimmän streakin jokaiselle tavalle."""
    if not data:
        print("Ei merkintöjä.")
        return

    habit_dates: Dict[str, List[dt.date]] = {}
    for e in data:
        try:
            d = dt.date.fromisoformat(e["date"])
        except Exception:
            continue
        habit = (e.get("habit") or "").strip() or "(nimetön)"
        habit_dates.setdefault(habit, []).append(d)

    print("\n🔥 STREAKIT (peräkkäiset päivät)")
    for habit, dates in sorted(habit_dates.items()):
        current, longest = _calc_streaks(dates)
        latest = max(dates).isoformat() if dates else "-"
        print(f"- {habit:<12}  nykyinen: {current} pv  | pisin: {longest} pv  | viimeisin: {latest}")


def main():
    data = load_data()
    while True:
        print("\n=== HABIT TRACKER ===")
        print("1) Lisää merkintä")
        print("2) Listaa merkinnät")
        print("3) Näytä yhteenveto")
        print("4) Näytä streakit")
        print("5) Näytä viimeisen viikon merkinnät")
        print("6) Tallenna ja lopeta")
        choice = prompt("Valinta: ")

        if choice == "1":
            add_entry(data)
        elif choice == "2":
            list_entries(data)
        elif choice == "3":
            summarize(data)
        elif choice == "4":
            show_streaks(data)
        elif choice == "5":
            list_last_week(data)
        elif choice == ("6"):
            save_data(data)
            print("💾 Tallennettu. Moikka!")
            break
        else:
            print("Tuntematon komento.")


if __name__ == "__main__":
    main()