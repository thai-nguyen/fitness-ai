from app.modules.exercise_catalog.domain.fixtures import load_fixture_catalog
from app.modules.exercise_catalog.domain.validation import validate_catalog


def test_fixture_catalog_valid_and_sized():
    catalog = load_fixture_catalog()
    assert catalog.catalog_version == "fixture-v1"
    assert 20 <= len(catalog.exercises) <= 40
    assert validate_catalog(catalog) == []


def test_inactive_exercise_present_but_not_in_active():
    catalog = load_fixture_catalog()
    assert any(not e.active_status for e in catalog.exercises)
    assert all(e.active_status for e in catalog.active())
