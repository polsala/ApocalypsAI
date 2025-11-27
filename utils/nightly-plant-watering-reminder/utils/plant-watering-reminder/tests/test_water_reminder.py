import datetime as dt

from src.water_reminder import Plant, plants_to_water

# Mock rationale: we construct deterministic Plant instances with fixed dates.

def test_no_plants_need_watering():
    plants = [
        Plant(name="Cactus", interval_days=30, last_watered=dt.date(2025, 11, 20)),
        Plant(name="Fern", interval_days=5, last_watered=dt.date(2025, 11, 24)),
    ]
    today = dt.date(2025, 11, 25)
    assert plants_to_water(plants, today) == []


def test_some_plants_need_watering():
    plants = [
        Plant(name="Basil", interval_days=2, last_watered=dt.date(2025, 11, 22)),
        Plant(name="Mint", interval_days=3, last_watered=dt.date(2025, 11, 23)),
        Plant(name="Rosemary", interval_days=7, last_watered=dt.date(2025, 11, 20)),
    ]
    today = dt.date(2025, 11, 25)
    # Basil: 3 days since last watered >= 2 -> due
    # Mint: 2 days since last watered < 3 -> not due
    # Rosemary: 5 days since last watered < 7 -> not due
    assert plants_to_water(plants, today) == ["Basil"]


def test_all_plants_need_watering():
    plants = [
        Plant(name="Orchid", interval_days=1, last_watered=dt.date(2025, 11, 20)),
        Plant(name="Succulent", interval_days=2, last_watered=dt.date(2025, 11, 22)),
    ]
    today = dt.date(2025, 11, 25)
    assert set(plants_to_water(plants, today)) == {"Orchid", "Succulent"}
